using System;
using System.Collections.Generic;

namespace Aquarium.Core;

public sealed record WorldSettings
{
    public int FishCount { get; init; } = 5;
    public int MaxPellets { get; init; } = 64;
    public double PelletLifetime { get; init; } = 12;
    public double FishWidth { get; init; } = 68;
    public double FishHeight { get; init; } = 40;
    public double SeekSpeed { get; init; } = 240;
    public double CuriosityRadius { get; init; } = 280;
    public void Validate()
    {
        if (FishCount < 1 || FishCount > 32 || MaxPellets < 1 || MaxPellets > 256 ||
            !double.IsFinite(PelletLifetime) || PelletLifetime <= 0 ||
            !double.IsFinite(FishWidth) || FishWidth <= 0 || !double.IsFinite(FishHeight) || FishHeight <= 0 ||
            !double.IsFinite(SeekSpeed) || SeekSpeed <= 0 || !double.IsFinite(CuriosityRadius) || CuriosityRadius < 0)
            throw new ArgumentOutOfRangeException(nameof(WorldSettings));
    }
}

// Timestamped samples come only from an explicit held drag. No wall clock or OS input here.
public sealed class ShakeDetector
{
    private readonly Queue<double> reversals = new();
    private bool initialized;
    private Point2 previous;
    private double previousTime, extreme, lastAccepted = double.NegativeInfinity;
    private int direction;
    public void Reset()
    {
        reversals.Clear(); initialized = false; direction = 0; lastAccepted = double.NegativeInfinity;
    }
    public bool Sample(Point2 point, double timestamp)
    {
        if (!double.IsFinite(point.X) || !double.IsFinite(point.Y) || !double.IsFinite(timestamp)) { Reset(); return false; }
        if (!initialized || timestamp - previousTime > 0.65 || timestamp <= previousTime)
        {
            Reset(); initialized = true; previous = point; previousTime = timestamp; extreme = point.X; return false;
        }
        var dt = timestamp - previousTime;
        var dx = point.X - previous.X;
        previous = point; previousTime = timestamp;
        while (reversals.Count > 0 && timestamp - reversals.Peek() > 0.55) reversals.Dequeue();
        if (Math.Abs(dx) < 1) return false;
        if (direction == 0)
        {
            if (Math.Abs(point.X - extreme) >= 14) { direction = Math.Sign(point.X - extreme); extreme = point.X; }
            return false;
        }
        if ((point.X - extreme) * direction >= 0) { extreme = point.X; return false; }
        // Require meaningful motion in the opposite direction, not mouse sensor jitter.
        if (Math.Abs(point.X - extreme) < 14 || Math.Abs(dx) / dt < 65) return false;
        direction = -direction; extreme = point.X; reversals.Enqueue(timestamp);
        if (reversals.Count < 2 || timestamp - lastAccepted < 0.18) return false;
        lastAccepted = timestamp; reversals.Clear(); return true;
    }
}

public enum FishActivity { Wander, Curious, SeekFood, Eat, ChangingDepth }
public enum DepthPhase { None, Leaving, Entering }
public enum FishSpecies { Goldfish, Tetra, Angelfish, Guppy }
public enum FishFacing { Left, Right, TowardViewer, AwayFromViewer }
public readonly record struct FishPose(int Id, Point2 Position, Point2 Velocity, DepthBand Band,
    FishActivity Activity, bool FacingRight, double Width, double Height, DepthPhase Transition,
    FishSpecies Species, FishFacing Facing, double VisualDepth);
public readonly record struct FoodPose(int Id, Point2 Position, double Age);
public readonly record struct ConsumptionEvent(int FishId, int FoodId, Point2 FishPosition,
    Point2 FoodPosition, double Time, bool Visible, DepthBand Band);
public sealed record SceneFrame(double Time, IReadOnlyList<FishPose> Fish, IReadOnlyList<FoodPose> Food,
    IReadOnlyList<ConsumptionEvent> RecentMeals);

internal sealed class FishState
{
    public int Id;
    public Point2 Position, Velocity, WanderTarget, EdgeTarget;
    public DepthBand Band, HomeBand, TargetBand;
    public DepthPhase Phase;
    public FishActivity Activity;
    public FishSpecies Species;
    public FishFacing Facing = FishFacing.Right;
    public bool FacingRight = true;
    public double VisualDepth;
    public double NextWander, NextCuriosity, CuriousUntil, ForegroundUntil, EatingUntil;
}
internal sealed class FoodState
{
    public int Id;
    public Point2 Position;
    public double Age, SpeedX, SpeedY;
}
