namespace Aquarium.Core;

public enum FeederMode { Closed, Resting, Held }
public sealed class FeederState
{
    public FeederMode Mode { get; private set; }
    public Point2 Position { get; private set; }
    public int HoldCount { get; private set; }
    public void Open(Point2 position)
    {
        if(Mode!=FeederMode.Closed) return;
        Position=position; Mode=FeederMode.Resting;
    }
    public bool BeginHold()
    {
        if(Mode!=FeederMode.Resting) return false;
        Mode=FeederMode.Held; HoldCount++; return true;
    }
    public void Move(Point2 p) { if(Mode==FeederMode.Held) Position=p; }
    public void Relocate(Point2 p) => Position=p;
    public void Release() { if(Mode==FeederMode.Held) Mode=FeederMode.Resting; }
    public void Close() => Mode=FeederMode.Closed;
}
