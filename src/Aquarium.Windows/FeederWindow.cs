using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Interop;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using Aquarium.Core;
using Aquarium.Windows.Platform;

namespace Aquarium.Windows;

internal sealed class FeederWindow : Window
{
    private readonly Image body;
    private readonly FeederFall fall=new();
    private readonly FeederState state;
    private EnvironmentSnapshot? snapshot;
    private DisplayTransform transform;
    private Point2 dragStart,origin;
    public nint Handle {get;private set;}
    public event Action? EnvironmentChanged;
    public long MoveCount {get;private set;}
    public bool BodyCaptured=>body.IsMouseCaptured;
    public Point2 BodyPoint=>new(34,76);
    public Point2 ClosePoint=>new(67,39);
    public bool Falling=>state.Mode==FeederMode.Resting && snapshot is not null && state.Position.Y<Math.Max(snapshot.WorkArea.Y,snapshot.WorkArea.Bottom-Height)-.01;
    public event Action? ClosedByUser;
    public event Action<string>? Changed;
    public event Action<Point2>? HeldMoved;
    public FeederWindow(FeederState state,bool probe=false)
    {
        this.state=state;
        Title=probe?"Aquarium G0 feeder":"Aquarium feeder";Width=80;Height=112;WindowStyle=WindowStyle.None;ResizeMode=ResizeMode.NoResize;
        AllowsTransparency=true;Background=Brushes.Transparent;ShowInTaskbar=false;ShowActivated=false;Topmost=true;
        // Alpha-zero pixels pass native input through; do not set WS_EX_TRANSPARENT on this interactive tool.
        var canvas=new Canvas();
        var bitmap=new BitmapImage(new Uri("pack://application:,,,/Assets/feeder.png"));bitmap.Freeze();
        body=new Image{Source=bitmap,Width=60,Height=72,Cursor=Cursors.Hand,ToolTip="Pick up, then shake to feed. Release to drop."};
        RenderOptions.SetBitmapScalingMode(body,BitmapScalingMode.NearestNeighbor);
        // Keep the nozzle at (34,112), four DIPs above the existing food emission origin.
        Canvas.SetLeft(body,4);Canvas.SetTop(body,40);canvas.Children.Add(body);
        var close=new Button{Content="×",Width=22,Height=22,FontSize=15,Padding=new Thickness(0),
            Background=new SolidColorBrush(Color.FromRgb(31,52,59)),Foreground=Brushes.White,
            BorderThickness=new Thickness(0),Cursor=Cursors.Hand,ToolTip="Close feeder only"};
        Canvas.SetLeft(close,56);Canvas.SetTop(close,28);
        close.Click+=(_,e)=>{e.Handled=true;CancelHold();state.Close();Hide();ClosedByUser?.Invoke();Changed?.Invoke("close");};canvas.Children.Add(close);Content=canvas;
        body.MouseLeftButtonDown+=Begin;
        body.MouseMove+=Move;
        body.MouseLeftButtonUp+=(_,e)=>{e.Handled=true;CancelHold();};
        body.LostMouseCapture+=(_,_)=>CancelHold();
        Deactivated+=(_,_)=>CancelHold();
        SourceInitialized+=(_,_)=>{Handle=new WindowInteropHelper(this).Handle;var ex=(long)NativeMethods.GetWindowLongPtr(Handle,NativeMethods.GwlExStyle);NativeMethods.SetWindowLongPtr(Handle,NativeMethods.GwlExStyle,new nint(ex|NativeMethods.ExToolWindow));HwndSource.FromHwnd(Handle)?.AddHook(Hook);};
    }
    private nint Hook(nint h,int msg,nint wp,nint lp,ref bool handled)
    {
        if(msg==NativeMethods.WmDpiChanged || msg==NativeMethods.WmDisplayChange)EnvironmentChanged?.Invoke();
        if(msg==0x001f)CancelHold(); // WM_CANCELMODE; do not leave a captured drag active.
        return 0;
    }
    public void UpdateEnvironment(EnvironmentSnapshot value,DisplayTransform tx){snapshot=value;transform=tx;}
    public void Advance(double dt)
    {
        if(snapshot is not null && fall.Advance(state,snapshot.WorkArea,Width,Height,dt))Place();
    }
    public void Place()
    {
        if(snapshot is null)return;
        var p=snapshot.WorkArea.ClampOrigin(state.Position,Width,Height);state.Relocate(p);
        var physical=transform.ToPhysical(p);
        if(Handle==0){Left=physical.X/transform.Scale;Top=physical.Y/transform.Scale;}
        else NativeMethods.SetWindowPos(Handle,0,(int)Math.Round(physical.X),(int)Math.Round(physical.Y),(int)Math.Round(Width*transform.Scale),(int)Math.Round(Height*transform.Scale),NativeMethods.NoActivate|NativeMethods.NoZOrder);
    }
    private void Begin(object sender,MouseButtonEventArgs e)
    {
        e.Handled=true;if(snapshot is null || state.Mode!=FeederMode.Resting)return;
        // Only a deliberate body press activates the feeder; showing/restoring never activates it.
        Activate();if(!body.CaptureMouse())return;
        if(!state.BeginHold()){body.ReleaseMouseCapture();return;}
        fall.Reset();
        NativeMethods.GetCursorPos(out var p);dragStart=transform.ToLocal(p.ToPoint());origin=state.Position;
        body.Cursor=Cursors.SizeAll;Changed?.Invoke("begin-hold");
    }
    private void Move(object sender,MouseEventArgs e)
    {
        if(state.Mode!=FeederMode.Held || snapshot is null)return;
        if(e.LeftButton!=MouseButtonState.Pressed){CancelHold();return;}
        NativeMethods.GetCursorPos(out var p);var current=transform.ToLocal(p.ToPoint());
        state.Move(snapshot.WorkArea.ClampOrigin(new(origin.X+current.X-dragStart.X,origin.Y+current.Y-dragStart.Y),Width,Height));
        Place();MoveCount++;HeldMoved?.Invoke(current);e.Handled=true;
    }
    public void CancelHold()
    {
        var wasHeld=state.Mode==FeederMode.Held;state.Release();fall.Reset();
        if(body.IsMouseCaptured)body.ReleaseMouseCapture();
        body.Cursor=Cursors.Hand;
        if(wasHeld)Changed?.Invoke("end-hold");
    }
}
