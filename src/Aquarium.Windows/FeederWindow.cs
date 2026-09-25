using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Interop;
using System.Windows.Media;
using Aquarium.Core;
using Aquarium.Windows.Platform;

namespace Aquarium.Windows;

internal sealed class FeederWindow : Window
{
    private readonly Border body;
    private readonly TextBlock stateText;
    private readonly FeederState state;
    private EnvironmentSnapshot? snapshot;
    private DisplayTransform transform;
    private Point2 dragStart,origin;
    public nint Handle {get;private set;}
    public long MoveCount {get;private set;}
    public bool BodyCaptured=>body.IsMouseCaptured;
    public event Action? ClosedByUser;
    public event Action<string>? Changed;
    public FeederWindow(FeederState state)
    {
        this.state=state;
        Title="Aquarium G0 feeder";Width=164;Height=112;WindowStyle=WindowStyle.None;ResizeMode=ResizeMode.NoResize;
        AllowsTransparency=true;Background=Brushes.Transparent;ShowInTaskbar=false;ShowActivated=false;Topmost=true;
        var grid=new Grid{Background=Brushes.Transparent};
        body=new Border{Background=new SolidColorBrush(Color.FromRgb(36,61,65)),BorderBrush=new SolidColorBrush(Color.FromRgb(109,205,175)),BorderThickness=new Thickness(2),Padding=new Thickness(12,22,12,8),Cursor=Cursors.Hand};
        var stack=new StackPanel();
        stack.Children.Add(new TextBlock{Text="G0 FEEDER",Foreground=Brushes.White,FontSize=15,FontWeight=FontWeights.Bold});
        stateText=new TextBlock{Text="Resting | drag to hold",Foreground=Brushes.White,FontSize=11,Margin=new Thickness(0,8,0,0)};
        stack.Children.Add(stateText);stack.Children.Add(new TextBlock{Text="Input probe - no food yet",Foreground=Brushes.LightGray,FontSize=10,Margin=new Thickness(0,6,0,0)});body.Child=stack;grid.Children.Add(body);
        var close=new Button{Content="\u00d7",Width=25,Height=23,HorizontalAlignment=HorizontalAlignment.Right,VerticalAlignment=VerticalAlignment.Top,Margin=new Thickness(3),ToolTip="Close feeder only"};
        close.Click+=(_,e)=>{e.Handled=true;CancelHold();state.Close();Hide();ClosedByUser?.Invoke();Changed?.Invoke("close");};grid.Children.Add(close);Content=grid;
        body.MouseLeftButtonDown+=Begin;
        body.MouseMove+=Move;
        body.MouseLeftButtonUp+=(_,e)=>{e.Handled=true;CancelHold();};
        body.LostMouseCapture+=(_,_)=>CancelHold();
        Deactivated+=(_,_)=>CancelHold();
        SourceInitialized+=(_,_)=>{Handle=new WindowInteropHelper(this).Handle;var ex=(long)NativeMethods.GetWindowLongPtr(Handle,NativeMethods.GwlExStyle);NativeMethods.SetWindowLongPtr(Handle,NativeMethods.GwlExStyle,new nint(ex|NativeMethods.ExToolWindow));};
    }
    public void UpdateEnvironment(EnvironmentSnapshot value,DisplayTransform tx){snapshot=value;transform=tx;}
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
        NativeMethods.GetCursorPos(out var p);dragStart=transform.ToLocal(p.ToPoint());origin=state.Position;
        stateText.Text="Held | release to put down";body.Cursor=Cursors.SizeAll;Changed?.Invoke("begin-hold");
    }
    private void Move(object sender,MouseEventArgs e)
    {
        if(state.Mode!=FeederMode.Held || snapshot is null)return;
        if(e.LeftButton!=MouseButtonState.Pressed){CancelHold();return;}
        NativeMethods.GetCursorPos(out var p);var current=transform.ToLocal(p.ToPoint());
        state.Move(snapshot.WorkArea.ClampOrigin(new(origin.X+current.X-dragStart.X,origin.Y+current.Y-dragStart.Y),Width,Height));
        Place();MoveCount++;e.Handled=true;
    }
    public void CancelHold()
    {
        var wasHeld=state.Mode==FeederMode.Held;state.Release();
        if(body.IsMouseCaptured)body.ReleaseMouseCapture();
        stateText.Text="Resting | drag to hold";body.Cursor=Cursors.Hand;
        if(wasHeld)Changed?.Invoke("end-hold");
    }
}
