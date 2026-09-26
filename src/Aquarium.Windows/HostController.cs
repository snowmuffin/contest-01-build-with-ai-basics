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
    private readonly DesktopOverlay overlay;
    private readonly bool probe;
    private readonly World world=new();
    private SceneFrame? scene;
    private readonly SimulationClock simulationClock=new();
    private readonly SessionAvailability sessionAvailability=new();
    private bool trayMenuOpen;
    private bool Allowed=>visibility.Visible&&!trayMenuOpen;
    private FeederState feederState=>world.Feeder;
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
    public HostController(string? diagnostics,bool probe=false)
    {
        this.diagnostics=diagnostics;this.probe=probe;overlay=new DesktopOverlay(probe);overlay.EnableMetrics(diagnostics is not null);
        feeder=new(feederState,probe);
        feeder.Changed+=ev=>{world.ResetFeeding();lastEvent=ev;WriteReport();};
        feeder.HeldMoved+=point=>{if(!probe && snapshot is not null)world.SubmitHeldMotion(point,time.Elapsed.TotalSeconds,snapshot);};feeder.ClosedByUser+=()=>closeCount++;
        var menu=new Forms.ContextMenuStrip();
        menu.Items.Add(probe?"G0 integration probe":"Desktop Aquarium · prototype").Enabled=false;
        menu.Items.Add("Open feeder",null,(_,_)=>OpenFeeder());
        menu.Items.Add("Hide",null,(_,_)=>SetManualHidden(true));
        menu.Items.Add("Show again",null,(_,_)=>SetManualHidden(false));
        menu.Opening+=(_,_)=>{trayMenuOpen=true;ApplyVisibility();};
        menu.Closed+=(_,_)=>{trayMenuOpen=false;if(!disposed)ApplyVisibility();};
        menu.Items.Add(new Forms.ToolStripSeparator());menu.Items.Add("Exit",null,(_,_)=>System.Windows.Application.Current.Shutdown());
        tray=new Forms.NotifyIcon{Icon=new System.Drawing.Icon(Path.Combine(AppContext.BaseDirectory,"Assets","feeder.ico")),Text=probe?"Aquarium G0 probe":"Desktop Aquarium",ContextMenuStrip=menu,Visible=true};
        tray.DoubleClick+=(_,_)=>OpenFeeder();
        SystemEvents.SessionSwitch+=OnSession;
        overlay.EnvironmentChanged+=OnEnvironmentChanged;feeder.EnvironmentChanged+=OnEnvironmentChanged;
        timer=new DispatcherTimer(DispatcherPriority.Background){Interval=TimeSpan.FromMilliseconds(33)};timer.Tick+=Tick;
        Observe();ApplyVisibility();timer.Start();WriteReport();
    }
    private void OnSession(object sender,SessionSwitchEventArgs e)
    {
        System.Windows.Application.Current.Dispatcher.BeginInvoke(new Action(()=>
        {
            if(disposed)return;
            switch(e.Reason)
            {
                case SessionSwitchReason.SessionLock: sessionAvailability.Apply(SessionSignal.Lock);break;
                case SessionSwitchReason.SessionUnlock: sessionAvailability.Apply(SessionSignal.Unlock);break;
                case SessionSwitchReason.ConsoleDisconnect:
                case SessionSwitchReason.RemoteDisconnect: sessionAvailability.Apply(SessionSignal.Disconnect);break;
                case SessionSwitchReason.ConsoleConnect:
                case SessionSwitchReason.RemoteConnect: sessionAvailability.Apply(SessionSignal.Connect);break;
                default:return;
            }
            observer.SessionLocked=sessionAvailability.Unavailable;
            feeder.CancelHold();world.ResetFeeding();nextObserve=0;Tick(null,EventArgs.Empty);
        }));
    }
    private void OnEnvironmentChanged()
    {
        if(disposed)return;
        // Native callbacks only invalidate/cancel; reading fresh geometry is deferred to the dispatcher.
        feeder.CancelHold();world.ResetFeeding();visibility.Observe(Suppression.DisplayChange);
        ApplyVisibility();nextObserve=0;
        System.Windows.Application.Current.Dispatcher.BeginInvoke(new Action(()=>{if(!disposed)Tick(null,EventArgs.Empty);}));
    }
    public void OpenFeeder()
    {
        if(disposed || snapshot is null)return;
        feederState.Open(snapshot.WorkArea.ClampOrigin(new(snapshot.Cursor.X+20,snapshot.Cursor.Y+20),feeder.Width,feeder.Height));
        feeder.UpdateEnvironment(snapshot,observer.Transform);feeder.Place();ApplyVisibility();lastEvent="open-feeder";WriteReport();
    }
    public void SetManualHidden(bool hidden)
    {
        if(disposed)return;
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
        if(t>=nextObserve || observer.Dirty){Observe();nextObserve=t+(Allowed?0.10:0.5);ApplyVisibility();}
        if(feederState.Mode==FeederMode.Held && (NativeMethods.GetAsyncKeyState(1)&0x8000)==0)feeder.CancelHold();
        var steps=simulationClock.Advance(t,Allowed);
        if(Allowed && snapshot is not null)
        {
            if(probe)overlay.UpdateFrame(snapshot,t);
            else
            {
                world.SetEnabled(true);
                for(var i=0;i<steps;i++)world.Advance(1.0/60,snapshot);
                scene=world.Snapshot();overlay.UpdateWorld(snapshot,scene);
            }
        }
        else world.SetEnabled(false);
        if(t>=nextReport){WriteReport();nextReport=t+0.25;}
    }
    private void ApplyVisibility()
    {
        timer.Interval=TimeSpan.FromMilliseconds(Allowed?33:500);
        world.SetEnabled(Allowed);
        if(Allowed && snapshot is not null)
        {
            if(probe)overlay.UpdateFrame(snapshot,time.Elapsed.TotalSeconds);
            else overlay.UpdateWorld(snapshot,scene??world.Snapshot());
            if(!overlay.IsVisible){overlay.Show();overlay.Position(observer.PhysicalDisplay,observer.Transform);}
            if(feederState.Mode!=FeederMode.Closed && !feeder.IsVisible){feeder.Place();feeder.Show();feeder.Place();}
        }
        else
        {feeder.CancelHold();world.ResetFeeding();simulationClock.Advance(time.Elapsed.TotalSeconds,false);if(feeder.IsVisible)feeder.Hide();if(overlay.IsVisible)overlay.Hide();}
    }
    private void WriteReport()
    {
        if(diagnostics is null)return;
        try
        {
            var capture=NativeMethods.GetCapture();
            var report=new{
                stage=probe?"G0 native integration probe":"G1/G2 live feeding prototype",pid=Environment.ProcessId,session=Process.GetCurrentProcess().SessionId,
                utc=DateTimeOffset.UtcNow,report=++reportCount,alive=!disposed,lastEvent,
                overlayVisible=overlay.IsVisible,feederVisible=feeder.IsVisible,feederMode=feederState.Mode.ToString(),
                manualHidden=visibility.ManualHidden,suppression=(visibility.Reasons|(trayMenuOpen?Suppression.SystemUi:Suppression.None)).ToString(),
                timerRunning=timer.IsEnabled,trayVisible=!disposed&&tray.Visible,
                trayMenu=MenuReport(),
                feederCapture=feeder.BodyCaptured,nativeCaptureOwned=capture!=0 && NativeMethods.IsOwn(capture),
                holdCount=feederState.HoldCount,moveCount=feeder.MoveCount,closeCount,
                overlayHandle=(long)overlay.Handle,feederHandle=(long)feeder.Handle,
                overlayExtendedStyle=overlay.Handle==0?0:(long)NativeMethods.GetWindowLongPtr(overlay.Handle,NativeMethods.GwlExStyle),
                foregroundIsAquarium=NativeMethods.IsOwn(NativeMethods.GetForegroundWindow()),
                display=observer.PhysicalDisplay,transform=observer.Transform,
                feederPosition=feederState.Position,markers=overlay.MarkerRects,frames=overlay.FrameCount,
                workWindowCount=snapshot?.WorkWindows.Count,protectedRegionCount=snapshot?.ProtectedRegions.Count,
                shellState=observer.ShellState,eventHooks=observer.HookCount,
                foodImplemented=!probe,finalArtwork=false,renderMetrics=overlay.RenderMetricSnapshot,
                fish=scene?.Fish.Select(f=>new{id=f.Id,species=f.Species.ToString(),position=f.Position,velocity=f.Velocity,band=f.Band.ToString(),visualDepth=f.VisualDepth,activity=f.Activity.ToString(),transition=f.Transition.ToString(),facing=f.Facing.ToString(),facingRight=f.FacingRight,width=f.Width,height=f.Height,visible=snapshot is not null&&Occlusion.VisibleAt(f.Position,f.Band,snapshot)}),
                food=scene?.Food,meals=scene?.RecentMeals,simulationTime=world.Time,
                emitted=world.TotalEmitted,consumed=world.TotalConsumed,expired=world.TotalExpired,shakes=world.ShakeCount,curiosity=world.CuriosityCount
            };
            var path=Path.GetFullPath(diagnostics);Directory.CreateDirectory(Path.GetDirectoryName(path)!);
            File.WriteAllText(path+".tmp",JsonSerializer.Serialize(report,new JsonSerializerOptions{WriteIndented=true}));File.Move(path+".tmp",path,true);
        }
        catch(IOException){ } // Diagnostics must never take down the desktop host.
        catch(UnauthorizedAccessException){ }
    }
    private object? MenuReport()
    {
        if(disposed || tray.ContextMenuStrip is not { Visible:true } menu)return null;
        return new {handle=(long)menu.Handle,items=menu.Items.Cast<Forms.ToolStripItem>()
            .Where(item=>item.Enabled).Select(item=>new {text=item.Text,
                bounds=menu.RectangleToScreen(item.Bounds)}).ToArray()};
    }
    public void Dispose()
    {
        if(disposed)return;disposed=true;timer.Stop();feeder.CancelHold();SystemEvents.SessionSwitch-=OnSession;
        world.SetEnabled(false);feeder.Hide();overlay.Hide();lastEvent="exit";tray.Visible=false;tray.ContextMenuStrip?.Dispose();tray.Icon?.Dispose();tray.Dispose();observer.Dispose();feeder.Close();overlay.Close();WriteReport();
    }
}
