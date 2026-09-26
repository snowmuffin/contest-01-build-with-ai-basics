using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using Aquarium.Core;

namespace Aquarium.Windows.Rendering;

// A single drawing surface, cached bitmap frames and cached clips; not one UI control per fish/pellet.
internal sealed class SpriteRenderer : FrameworkElement
{
    private readonly BitmapSource[,,] sprites=new BitmapSource[4,4,2];
    private readonly Geometry[] clips=new Geometry[3];
    private long clipVersion=long.MinValue;
    private EnvironmentSnapshot? environment;
    private SceneFrame? scene;
    public long FrameCount {get;private set;}
    public RenderMetrics Metrics { get; } = new();
    private static readonly Brush Pellet=Frozen(249,215,137),PelletShadow=Frozen(81,60,34),Spark=Frozen(253,240,189);
    public SpriteRenderer()
    {
        var atlas=new BitmapImage();atlas.BeginInit();atlas.CacheOption=BitmapCacheOption.OnLoad;
        atlas.UriSource=new Uri("pack://application:,,,/Assets/fish-atlas.png");atlas.EndInit();atlas.Freeze();
        for(var species=0;species<4;species++)for(var facing=0;facing<4;facing++)for(var frame=0;frame<2;frame++)
        {
            var bitmap=new CroppedBitmap(atlas,new Int32Rect((facing*2+frame)*40,species*24,40,24));
            bitmap.Freeze();sprites[species,facing,frame]=bitmap;
        }
        RenderOptions.SetBitmapScalingMode(this,BitmapScalingMode.NearestNeighbor);
        SnapsToDevicePixels=true;IsHitTestVisible=false;
        IsVisibleChanged += (_, _) => Metrics.ResetInterval();
    }
    private static Brush Frozen(byte r,byte g,byte b){var brush=new SolidColorBrush(Color.FromRgb(r,g,b));brush.Freeze();return brush;}
    public void Update(EnvironmentSnapshot value,SceneFrame frame)
    {
        environment=value;scene=frame;
        if(value.Version!=clipVersion)
        {
            clipVersion=value.Version;
            for(var band=0;band<3;band++)
            {
                Geometry clip=new RectangleGeometry(Rect(value.Display));
                var n=band==2?0:band==1?Math.Min(1,value.WorkWindows.Count):value.WorkWindows.Count;
                foreach(var r in value.ProtectedRegions.Concat(value.WorkWindows.Take(n)))
                    clip=new CombinedGeometry(GeometryCombineMode.Exclude,clip,new RectangleGeometry(Rect(r)));
                clip.Freeze();clips[band]=clip;
            }
        }
        InvalidateVisual();
    }
    protected override void OnRender(DrawingContext drawing)
    {
        if(!IsVisible || scene is null || environment is null)return;
        var started = Metrics.Begin();
        FrameCount++;
        var dpi=VisualTreeHelper.GetDpi(this).DpiScaleX;
        double Snap(double v)=>Math.Round(v*dpi)/dpi;
        for(var band=0;band<3;band++)
        {
            drawing.PushClip(clips[band]);
            foreach(var f in scene.Fish)
            {
                if((int)f.Band!=band)continue;
                var scale=DepthScale(f.VisualDepth);
                var width=f.Width*scale;var height=f.Height*scale;
                var bounds=FishGeometry.Bounds(f.Position,width,height);
                if(!environment.Display.Intersects(bounds))continue;
                var x=Snap(f.Position.X);var y=Snap(f.Position.Y);
                var speed=Math.Sqrt(f.Velocity.X*f.Velocity.X+f.Velocity.Y*f.Velocity.Y);
                var frame=((int)(scene.Time*(speed>100?8:4)+f.Id))&1;
                drawing.DrawImage(sprites[(int)f.Species,(int)f.Facing,frame],new Rect(x-width/2,y-height/2,width,height));
                if(f.Activity==FishActivity.Eat)
                {
                    var sparkX=f.Facing==FishFacing.Right?x+width*.34:f.Facing==FishFacing.Left?x-width*.34:x;
                    drawing.DrawRectangle(Spark,null,new Rect(Snap(sparkX)-1.5,Snap(y)-1.5,3,3));
                }
            }
            drawing.Pop();
        }
        drawing.PushClip(clips[2]);
        foreach(var p in scene.Food)
        {
            var x=Snap(p.Position.X);var y=Snap(p.Position.Y);
            drawing.DrawRectangle(PelletShadow,null,new Rect(x-2,y-2,5,5));
            drawing.DrawRectangle(Pellet,null,new Rect(x-1,y-1,3,3));
        }
        foreach(var meal in scene.RecentMeals)
        {
            var age=scene.Time-meal.Time;if(age<0||age>.38)continue;
            var radius=3+age*18;
            drawing.PushOpacity(Math.Clamp(1-age/.38,0,1));
            for(var i=0;i<3;i++)
            {
                var angle=i*Math.PI*2/3;
                drawing.DrawRectangle(Spark,null,new Rect(Snap(meal.FoodPosition.X+Math.Cos(angle)*radius),Snap(meal.FoodPosition.Y+Math.Sin(angle)*radius),2,2));
            }
            drawing.Pop();
        }
        drawing.Pop();
        Metrics.End(started);
    }
    private static double DepthScale(double visualDepth) => .72+.14*Math.Clamp(visualDepth,0,2);
    private static Rect Rect(Rect2 r)=>new(r.X,r.Y,r.Width,r.Height);
}
