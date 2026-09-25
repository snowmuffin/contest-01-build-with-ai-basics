using System;
using System.Collections.Generic;

namespace Aquarium.Core;

public readonly record struct Point2(double X, double Y);
public readonly record struct Rect2(double X, double Y, double Width, double Height)
{
    public double Right => X + Width;
    public double Bottom => Y + Height;
    public bool Valid => double.IsFinite(X) && double.IsFinite(Y) && double.IsFinite(Width) && double.IsFinite(Height) && Width > 0 && Height > 0;
    public bool Contains(Point2 p) => Valid && p.X >= X && p.Y >= Y && p.X < Right && p.Y < Bottom;
    public bool Intersects(Rect2 r) => Valid && r.Valid && X < r.Right && Right > r.X && Y < r.Bottom && Bottom > r.Y;
    public Point2 ClampOrigin(Point2 p, double width, double height) => new(
        Math.Clamp(p.X, X, Math.Max(X, Right - width)), Math.Clamp(p.Y, Y, Math.Max(Y, Bottom - height)));
}

// All core coordinates are display-local DIPs; all OS handles remain in the host.
public readonly record struct DisplayTransform(double OriginX, double OriginY, double Scale)
{
    public Point2 ToLocal(Point2 p)
    {
        Validate(); return new((p.X - OriginX) / Scale, (p.Y - OriginY) / Scale);
    }
    public Point2 ToPhysical(Point2 p)
    {
        Validate(); return new(OriginX + p.X * Scale, OriginY + p.Y * Scale);
    }
    public Rect2 ToLocal(Rect2 r)
    {
        var p = ToLocal(new Point2(r.X,r.Y)); return new(p.X,p.Y,r.Width / Scale,r.Height / Scale);
    }
    private void Validate() { if (!double.IsFinite(Scale) || Scale <= 0) throw new ArgumentOutOfRangeException(nameof(Scale)); }
}

public enum DepthBand { Rear, Middle, Front }
public sealed record EnvironmentSnapshot(long Version, Rect2 Display, Rect2 WorkArea,
    IReadOnlyList<Rect2> WorkWindows, IReadOnlyList<Rect2> ProtectedRegions, Point2 Cursor,
    Suppression Suppression, bool Valid);

public static class Occlusion
{
    public static bool VisibleAt(Point2 p, DepthBand band, EnvironmentSnapshot s)
    {
        if (!s.Valid || !s.Display.Contains(p)) return false;
        foreach (var r in s.ProtectedRegions) if (r.Contains(p)) return false;
        var count=band==DepthBand.Front ? 0 : band==DepthBand.Middle ? Math.Min(1,s.WorkWindows.Count) : s.WorkWindows.Count;
        for(var i=0;i<count;i++) if(s.WorkWindows[i].Contains(p)) return false;
        return true;
    }
}
