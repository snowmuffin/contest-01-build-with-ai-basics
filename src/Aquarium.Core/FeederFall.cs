using System;

namespace Aquarium.Core;

// Presentation motion only. Falling never submits held-pointer samples or emits food.
public sealed class FeederFall
{
    private const double Gravity = 1800;
    private const double TerminalSpeed = 1100;
    public double Speed { get; private set; }
    public void Reset() => Speed = 0;

    public bool Advance(FeederState state, Rect2 workArea, double width, double height, double dt)
    {
        if (!double.IsFinite(dt) || dt < 0 || dt > .1)
            throw new ArgumentOutOfRangeException(nameof(dt));
        if (state.Mode != FeederMode.Resting || !workArea.Valid)
        { Reset(); return false; }
        if (dt == 0) return false;

        var before = state.Position;
        var p = workArea.ClampOrigin(before, width, height);
        var floor = Math.Max(workArea.Y, workArea.Bottom - height);
        if (p.Y >= floor) Reset();
        else
        {
            var nextSpeed = Math.Min(TerminalSpeed, Speed + Gravity * dt);
            p = new(p.X, Math.Min(floor, p.Y + (Speed + nextSpeed) * .5 * dt));
            Speed = p.Y >= floor ? 0 : nextSpeed;
        }
        state.Relocate(p);
        return p != before;
    }
}
