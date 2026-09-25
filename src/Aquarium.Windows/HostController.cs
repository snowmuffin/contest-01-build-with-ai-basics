using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Windows;
using System.Windows.Threading;
using Aquarium.Core;
using Aquarium.Windows.Platform;
using Microsoft.Win32;
using Forms=System.Windows.Forms;

namespace Aquarium.Windows;

internal sealed class HostController : IDisposable
{
    private readonly DesktopSnapshotService observer=new();
    private readonly DesktopOverlay overlay=new();
    private readonly FeederState feederState=new();
    private readonly FeederWindow feeder;
    private readonly VisibilityPolicy visibility=new();
    private readonly Forms.NotifyIcon tray;
    private readonly DispatcherTimer timer;
    private readonly Stopwatch time=Stopwatch.StartNew();
    private readonly string? diagnostics;
    private EnvironmentSnapshot? snapshot;
    private double nextObserve,nextReport,clearSince=-1;
    private Rect2 lastPhysical;
    private DisplayTransform lastTransform;
    private bool disposed;
    private string lastEvent="startup";
    private long reportCount;
    private int closeCount;
    public HostController(string? diagnostics)
    {
        this.diagnostics=diagnostics;
        feeder=new(feederState);
        feeder.Changed+=ev=>{lastEvent=ev;WriteReport();};feeder.ClosedByUser+=()=>closeCount++;
        var menu=new Forms.ContextMenuStrip();
        menu.Items.Add("G0 integration probe (not final fish)").Enabled=false;
        menu.Items.Add("Open feeder",null,(_,_)=>OpenFeeder());
        menu.Items.Add("Hide",null,(_,_)=>SetManualHidden(true));
        menu.Items.Add("Show again",null,(_,_)=>SetManualHidden(false));
        menu.Items.Add(new Forms.ToolStripSeparator());menu.Items.Add("Exit",null,(_,_)=>System.Windows.Application.Current.Shutdown());
        tray=new Forms.NotifyIcon{Icon=System.Drawing.SystemIcons.Application,Text="Aquarium G0 - input/depth probe",ContextMenuStrip=menu,Visible=true};
        tray.DoubleClick+=(_,_)=>OpenFeeder();
        SystemEvents.SessionSwitch+=OnSession;
        timer=new DispatcherTimer(DispatcherPriority.Background){Interval=TimeSpan.FromMilliseconds(33)};timer.Tick+=Tick;
        Observe();ApplyVisibility();timer.Start();WriteReport();
    }
    private void OnSession(object sender,SessionSwitchEventArgs e)
    {
        System.Windows.Application.Current.Dispatcher.BeginInvoke(new Action(()=>
        {observer.SessionLocked=e.Reason is SessionSwitchReason.SessionLock or SessionSwitchReason.ConsoleDisconnect or SessionSwitchReason.RemoteDisconnect;nextObserve=0;Tick(null,EventArgs.Empty);}));
    }
    public void OpenFeeder()
    {
        if(snapshot is null)return;
        feederState.Open(snapshot.WorkArea.ClampOrigin(new(snapshot.Cursor.X+20,snapshot.Cursor.Y+20),feeder.Width,feeder.Height));
        feeder.UpdateEnvironment(snapshot,observer.Transform);feeder.Place();ApplyVisibility();lastEvent="open-feeder";WriteReport();
    }
    public void SetManualHidden(bool hidden)
    {
        if(hidden)visibility.Hide();else visibility.Show();ApplyVisibility();lastEvent=hidden?"manual-hide":"manual-show";WriteReport();
    }
    private void Observe()
    {
        try
        {
            var old=snapshot;snapshot=observer.Read();
            if(lastPhysical!=observer.PhysicalDisplay || lastTransform!=observer.Transform)
            {
                feeder.CancelHold();overlay.Position(observer.PhysicalDisplay,observer.Transform);
                lastPhysical=observer.PhysicalDisplay;lastTransform=observer.Transform;
            }
            feeder.UpdateEnvironment(snapshot,observer.Transform);feeder.Place();
            if(snapshot.Suppression!=Suppression.None){clearSince=-1;visibility.Observe(snapshot.Suppression);}
            else if(visibility.Reasons!=Suppression.None)
            { if(clearSince<0)clearSince=time.Elapsed.TotalSeconds;if(time.Elapsed.TotalSeconds-clearSince>=0.25)visibility.Observe(Suppression.None); }
            else visibility.Observe(Suppression.None);
            if(old is null || old.Suppression!=snapshot.Suppression)lastEvent="guard:"+snapshot.Suppression;
        }
        catch(Exception e) when(e is InvalidOperationException or System.ComponentModel.Win32Exception)
        {visibility.Observe(Suppression.InvalidSnapshot);lastEvent="observer-failed:"+e.GetType().Name;}
    }
    private void Tick(object? sender,EventArgs e)
    {
        if(disposed)return;var t=time.Elapsed.TotalSeconds;
        if(t>=nextObserve || observer.Dirty){Observe();nextObserve=t+(visibility.Visible?0.10:0.5);ApplyVisibility();}
        if(feederState.Mode==FeederMode.Held && (NativeMethods.GetAsyncKeyState(1)&0x8000)==0)feeder.CancelHold();
        if(visibility.Visible && snapshot is not null)overlay.UpdateFrame(snapshot,t);
        if(t>=nextReport){WriteReport();nextReport=t+0.25;}
    }
    private void ApplyVisibility()
    {
        timer.Interval=TimeSpan.FromMilliseconds(visibility.Visible?33:500);
        if(visibility.Visible && snapshot is not null)
        {
            overlay.UpdateFrame(snapshot,time.Elapsed.TotalSeconds);
            if(!overlay.IsVisible){overlay.Show();overlay.Position(observer.PhysicalDisplay,observer.Transform);}
            if(feederState.Mode!=FeederMode.Closed && !feeder.IsVisible){feeder.Place();feeder.Show();feeder.Place();}
        }
        else
        {feeder.CancelHold();if(feeder.IsVisible)feeder.Hide();if(overlay.IsVisible)overlay.Hide();}
    }
    private void WriteReport()
    {
        if(diagnostics is null)return;
        try
        {
            var capture=NativeMethods.GetCapture();
            var report=new{
                stage="G0 native integration probe",pid=Environment.ProcessId,session=Process.GetCurrentProcess().SessionId,
                utc=DateTimeOffset.UtcNow,report=++reportCount,alive=!disposed,lastEvent,
                overlayVisible=overlay.IsVisible,feederVisible=feeder.IsVisible,feederMode=feederState.Mode.ToString(),
                manualHidden=visibility.ManualHidden,suppression=visibility.Reasons.ToString(),
                feederCapture=feeder.BodyCaptured,nativeCaptureOwned=capture!=0 && NativeMethods.IsOwn(capture),
                holdCount=feederState.HoldCount,moveCount=feeder.MoveCount,closeCount,
                overlayHandle=(long)overlay.Handle,feederHandle=(long)feeder.Handle,
                overlayExtendedStyle=overlay.Handle==0?0:(long)NativeMethods.GetWindowLongPtr(overlay.Handle,NativeMethods.GwlExStyle),
                foregroundIsAquarium=NativeMethods.IsOwn(NativeMethods.GetForegroundWindow()),
                display=observer.PhysicalDisplay,transform=observer.Transform,
                feederPosition=feederState.Position,markers=overlay.MarkerRects,frames=overlay.FrameCount,
                workWindowCount=snapshot?.WorkWindows.Count,protectedRegionCount=snapshot?.ProtectedRegions.Count,
                shellState=observer.ShellState,eventHooks=observer.HookCount,
                foodImplemented=false,finalArtwork=false
            };
            var path=Path.GetFullPath(diagnostics);Directory.CreateDirectory(Path.GetDirectoryName(path)!);
            File.WriteAllText(path+".tmp",JsonSerializer.Serialize(report,new JsonSerializerOptions{WriteIndented=true}));File.Move(path+".tmp",path,true);
        }
        catch(IOException){ } // Diagnostics must never take down the desktop host.
        catch(UnauthorizedAccessException){ }
    }
    public void Dispose()
    {
        if(disposed)return;disposed=true;timer.Stop();feeder.CancelHold();SystemEvents.SessionSwitch-=OnSession;
        feeder.Hide();overlay.Hide();lastEvent="exit";WriteReport();tray.Visible=false;tray.ContextMenuStrip?.Dispose();tray.Dispose();observer.Dispose();feeder.Close();overlay.Close();
    }
}
