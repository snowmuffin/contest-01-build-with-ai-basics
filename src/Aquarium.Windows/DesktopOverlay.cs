using System;
using System.Globalization;
using System.Linq;
using System.Windows;
using System.Windows.Interop;
using System.Windows.Media;
using Aquarium.Core;
using Aquarium.Windows.Platform;
using Aquarium.Windows.Rendering;

namespace Aquarium.Windows;

// G0 probe only: three labelled, temporary pixel markers. No final fish behavior.
internal sealed class DesktopOverlay : Window
{
    private readonly ProbeCanvas canvas=new();
    private readonly SpriteRenderer aquarium=new();
    private readonly bool probe;
    public nint Handle {get;private set;}
    public long FrameCount=>probe?canvas.FrameCount:aquarium.FrameCount;
    public Rect2[] MarkerRects=>canvas.Markers;
    public DesktopOverlay(bool probe=false)
    {
        this.probe=probe;
        Title=probe?"Aquarium G0 passive habitat":"Aquarium habitat";WindowStyle=WindowStyle.None;ResizeMode=ResizeMode.NoResize;
        AllowsTransparency=true;Background=Brushes.Transparent;ShowInTaskbar=false;ShowActivated=false;
        Topmost=true;Focusable=false;IsHitTestVisible=false;Content=probe?canvas:aquarium;
        SourceInitialized+=(_,_)=>
        {
            Handle=new WindowInteropHelper(this).Handle;
            var ex=(long)NativeMethods.GetWindowLongPtr(Handle,NativeMethods.GwlExStyle);
            NativeMethods.SetWindowLongPtr(Handle,NativeMethods.GwlExStyle,new nint(ex|NativeMethods.ExTransparent|NativeMethods.ExNoActivate|NativeMethods.ExToolWindow));
            HwndSource.FromHwnd(Handle)?.AddHook(Hook);
        };
    }
    private nint Hook(nint h,int msg,nint wp,nint lp,ref bool handled)
    {
        if(msg==NativeMethods.WmMouseActivate){handled=true;return new nint(3);}
        return 0;
    }
    public void Position(Rect2 physical,DisplayTransform transform)
    {
        Left=physical.X/transform.Scale;Top=physical.Y/transform.Scale;Width=physical.Width/transform.Scale;Height=physical.Height/transform.Scale;
        if(Handle!=0)NativeMethods.SetWindowPos(Handle,0,(int)physical.X,(int)physical.Y,(int)physical.Width,(int)physical.Height,NativeMethods.NoActivate|NativeMethods.NoZOrder);
    }
    public void UpdateFrame(EnvironmentSnapshot snapshot,double phase) => canvas.Update(snapshot,phase);
    public void UpdateWorld(EnvironmentSnapshot snapshot,SceneFrame frame) => aquarium.Update(snapshot,frame);
    private sealed class ProbeCanvas : FrameworkElement
    {
        private EnvironmentSnapshot? snapshot;
        private long version=-1;
        private readonly Geometry[] clips=new Geometry[3];
        public Rect2[] Markers {get;private set;}=Array.Empty<Rect2>();
        public long FrameCount {get;private set;}
        private double phase;
        private static readonly Brush[] Colors={Freeze("#EEB560"),Freeze("#52C6AF"),Freeze("#DF81A6")};
        private static Brush Freeze(string color){var b=(SolidColorBrush)new BrushConverter().ConvertFromString(color)!;b.Freeze();return b;}
        public void Update(EnvironmentSnapshot value,double elapsed)
        {
            snapshot=value;phase=elapsed;
            if(version!=value.Version)
            {
                version=value.Version;
                for(var i=0;i<3;i++)
                {
                    Geometry g=new RectangleGeometry(ToRect(value.Display));
                    var count=i==2?0:i==1?Math.Min(1,value.WorkWindows.Count):value.WorkWindows.Count;
                    foreach(var r in value.ProtectedRegions.Concat(value.WorkWindows.Take(count)))
                        g=new CombinedGeometry(GeometryCombineMode.Exclude,g,new RectangleGeometry(ToRect(r)));
                    g.Freeze();clips[i]=g;
                }
            }
            var x=Math.Max(30,value.Display.Width*0.10);
            var y=Math.Max(100,value.Display.Height*0.33);
            Markers=new[]{new Rect2(x,y,138,46),new Rect2(x+35,y+70,138,46),new Rect2(x+70,y+140,138,46)};
            InvalidateVisual();
        }
        protected override void OnRender(DrawingContext dc)
        {
            if(snapshot is null)return;
            FrameCount++;
            for(var i=0;i<3;i++)
            {
                dc.PushClip(clips[i]);var r=Markers[i];
                dc.DrawRectangle(Brushes.Black,null,new Rect(r.X-2,r.Y-2,r.Width+4,r.Height+4));
                dc.DrawRectangle(Colors[i],null,ToRect(r));
                var text=new FormattedText("G0 "+((DepthBand)i).ToString().ToUpperInvariant(),CultureInfo.InvariantCulture,FlowDirection.LeftToRight,new Typeface("Consolas"),14,Brushes.Black,VisualTreeHelper.GetDpi(this).PixelsPerDip);
                dc.DrawText(text,new Point(r.X+12,r.Y+12));
                // Visible pulse verifies the surface is live; it is not autonomous fish movement.
                dc.DrawRectangle(Brushes.White,null,new Rect(r.Right-12,r.Y+8+(int)(phase*2)%2*4,5,5));
                dc.Pop();
            }
        }
        private static Rect ToRect(Rect2 r)=>new(r.X,r.Y,r.Width,r.Height);
    }
}
