using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using Aquarium.Core;

namespace Aquarium.Windows.Platform;

internal sealed class DesktopSnapshotService : IDisposable
{
    private readonly NativeMethods.WinEventCallback callback;
    private readonly List<nint> hooks=new();
    private long version;
    private EnvironmentSnapshot? previous;
    public bool Dirty {get;private set;}=true;
    public Rect2 PhysicalDisplay {get;private set;}
    public DisplayTransform Transform {get;private set;}
    public bool SessionLocked {get;set;}
    public bool LastForeignForeground {get;private set;}
    public int ShellState {get;private set;}
    public int HookCount=>hooks.Count;
    public DesktopSnapshotService()
    {
        callback=(_,_,_,_,_,_,_)=>Dirty=true;
        foreach(var range in new[]{(3u,3u),(0x8000u,0x8017u),(4u,7u)})
        {var h=NativeMethods.SetWinEventHook(range.Item1,range.Item2,0,callback,0,0,2);if(h!=0)hooks.Add(h);}
    }
    public EnvironmentSnapshot Read()
    {
        Dirty=false;
        var monitor=NativeMethods.MonitorFromPoint(new NativeMethods.Point(),1);
        var mi=new NativeMethods.MonitorInfo{Size=Marshal.SizeOf<NativeMethods.MonitorInfo>()};
        if(!NativeMethods.GetMonitorInfo(monitor,ref mi))throw new InvalidOperationException("Cannot read primary display.");
        var scale=NativeMethods.GetDpiForMonitor(monitor,0,out var dx,out _)==0?dx/96d:1d;
        PhysicalDisplay=mi.Monitor.ToRect(); Transform=new(PhysicalDisplay.X,PhysicalDisplay.Y,scale);
        var display=Transform.ToLocal(PhysicalDisplay);var work=Transform.ToLocal(mi.Work.ToRect());
        NativeMethods.GetCursorPos(out var pointer);
        var candidates=new HashSet<nint>(); NativeMethods.EnumCallback enumerate=(h,_)=>{candidates.Add(h);return true;};
        if(!NativeMethods.EnumWindows(enumerate,0))throw new InvalidOperationException("Cannot enumerate windows.");
        var windows=new List<Rect2>();var protectedRegions=new List<Rect2>();
        var visited=new HashSet<nint>(); var valid=true;var reason=Suppression.None;
        var h=NativeMethods.GetTopWindow(0); var count=0;
        while(h!=0)
        {
            if(++count>4096 || !visited.Add(h)){valid=false;break;}
            var next=NativeMethods.GetWindow(h,2);
            if(candidates.Contains(h) && NativeMethods.IsWindowVisible(h) && !NativeMethods.IsIconic(h) && !NativeMethods.IsOwn(h))
            {
                var cls=NativeMethods.ClassName(h);
                var cloaked=NativeMethods.DwmInt(h,14,out var cloak,4)==0 && cloak!=0;
                if(!cloaked && cls!="Progman" && cls!="WorkerW" && NativeMethods.TryBounds(h,out var bounds) && bounds.Intersects(PhysicalDisplay))
                {
                    var r=Transform.ToLocal(bounds);
                    if(cls is "Shell_TrayWnd" or "Shell_SecondaryTrayWnd" or "tooltips_class32" or "XamlExplorerHostIslandWindow")protectedRegions.Add(r);
                    else if(cls is "#32768" or "MultitaskingViewFrame")reason|=Suppression.SystemUi;
                    else windows.Add(r);
                }
            }
            h=next;
        }
        var fg=NativeMethods.GetForegroundWindow();LastForeignForeground=fg!=0 && !NativeMethods.IsOwn(fg);
        if(LastForeignForeground)
        {
            var cls=NativeMethods.ClassName(fg);
            if(cls is "Windows.UI.Core.CoreWindow" or "XamlExplorerHostIslandWindow" or "MultitaskingViewFrame")reason|=Suppression.SystemUi;
            if(cls!="Progman" && cls!="WorkerW" && cls!="Shell_TrayWnd" && NativeMethods.TryClient(fg,out var client))
            {
                var caption=((long)NativeMethods.GetWindowLongPtr(fg,NativeMethods.GwlStyle)&0x00c00000)!=0;
                if(FullscreenRules.CoversDisplay(client,PhysicalDisplay,NativeMethods.IsZoomed(fg)&&caption))reason|=Suppression.Fullscreen;
            }
        }
        ShellState=NativeMethods.SHQueryUserNotificationState(out var state)==0?state:0;
        // Generic busy/quiet-time flags alone are not fullscreen; our own overlay can cause them.
        if(ShellState is 3 or 4)reason|=Suppression.Fullscreen;
        if(SessionLocked || !NativeMethods.InputDesktopAvailable())reason|=Suppression.Session;
        if(!valid)reason|=Suppression.InvalidSnapshot;
        if(previous is null || previous.Display!=display || previous.WorkArea!=work || !previous.WorkWindows.SequenceEqual(windows) || !previous.ProtectedRegions.SequenceEqual(protectedRegions))version++;
        previous=new(version,display,work,Array.AsReadOnly(windows.ToArray()),Array.AsReadOnly(protectedRegions.ToArray()),Transform.ToLocal(pointer.ToPoint()),reason,valid);
        return previous;
    }
    public void Dispose(){foreach(var h in hooks)NativeMethods.UnhookWinEvent(h); hooks.Clear();GC.KeepAlive(callback);}
}
