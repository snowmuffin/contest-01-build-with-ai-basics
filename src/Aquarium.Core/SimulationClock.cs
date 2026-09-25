using System;

namespace Aquarium.Core;

// Fixed steps never consume hidden time. The caller provides monotonic seconds.
public sealed class SimulationClock
{
    private readonly double step;
    private readonly int maximumSteps;
    private double previous, remainder;
    private bool initialized, wasVisible;
    public SimulationClock(double step = 1.0 / 60, int maximumSteps = 3)
    {
        if (!double.IsFinite(step) || step <= 0 || maximumSteps < 1)
            throw new ArgumentOutOfRangeException(nameof(step));
        this.step = step;
        this.maximumSteps = maximumSteps;
    }
    public int Advance(double now, bool visible)
    {
        if (!double.IsFinite(now)) throw new ArgumentOutOfRangeException(nameof(now));
        var elapsed = now - previous;
        if (!initialized || now < previous || !visible || !wasVisible)
        {
            previous = now;
            initialized = true;
            wasVisible = visible;
            remainder = 0;
            return 0;
        }
        previous = now;
        remainder += Math.Min(elapsed, step * maximumSteps);
        var count = Math.Min(maximumSteps, (int)((remainder + 1e-10) / step));
        remainder = Math.Clamp(remainder - count * step, 0, step);
        return count;
    }
}

public enum SessionSignal { Lock, Unlock, Disconnect, Connect }

// Reconnection must not clear a still-locked session, or vice versa.
public sealed class SessionAvailability
{
    private bool locked, disconnected;
    public bool Unavailable => locked || disconnected;
    public void Apply(SessionSignal signal)
    {
        switch (signal)
        {
            case SessionSignal.Lock: locked = true; break;
            case SessionSignal.Unlock: locked = false; break;
            case SessionSignal.Disconnect: disconnected = true; break;
            case SessionSignal.Connect: disconnected = false; break;
            default: throw new ArgumentOutOfRangeException(nameof(signal));
        }
    }
}
