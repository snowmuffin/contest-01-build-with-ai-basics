using System;

namespace Aquarium.Core;

[Flags]
public enum Suppression { None=0, Fullscreen=1, SystemUi=2, Session=4, DisplayChange=8, InvalidSnapshot=16 }
public sealed class VisibilityPolicy
{
    public bool ManualHidden { get; private set; }
    public Suppression Reasons { get; private set; }
    public bool Visible => !ManualHidden && Reasons==Suppression.None;
    public void Hide() => ManualHidden=true;
    public void Show() => ManualHidden=false;
    public void Observe(Suppression reasons) => Reasons=reasons;
}

public static class FullscreenRules
{
    // Actual client-area coverage distinguishes F11/borderless fullscreen from a captioned maximized work window.
    public static bool CoversDisplay(Rect2 client, Rect2 display, bool captionedMaximized, double tolerance=2)
    {
        if(!client.Valid || !display.Valid || captionedMaximized) return false;
        return client.X<=display.X+tolerance && client.Y<=display.Y+tolerance && client.Right>=display.Right-tolerance && client.Bottom>=display.Bottom-tolerance;
    }
}
