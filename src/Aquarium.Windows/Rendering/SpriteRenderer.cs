using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Media;
using Aquarium.Core;

namespace Aquarium.Windows.Rendering;

// A single drawing surface, cached bitmap frames and cached clips; not one UI control per fish/pellet.
internal sealed class SpriteRenderer : FrameworkElement
{
    private readonly FishSpriteAtlas sprites=new();
    private readonly Geometry[] clips=new Geometry[3];
    private long clipVersion=long.MinValue;
    private EnvironmentSnapshot? environment;
    private SceneFrame? scene;
    public long FrameCount {get;private set;}
    public RenderMetrics Metrics { get; } = new();
    private static readonly Brush Pellet=Frozen(249,215,137),PelletShadow=Frozen(81,60,34),Spark=Frozen(253,240,189);
    public SpriteRenderer()
    {
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
                var x=Snap(f.Position.X);var y=Snap(f.Position.Y);
                var speed=Math.Sqrt(f.Velocity.X*f.Velocity.X+f.Velocity.Y*f.Velocity.Y);
                var frame=((int)(scene.Time*(speed>100?8:4)+f.Id))&1;
                var sprite=sprites[f.Species,f.Facing,frame];
                // Front is 100%: one source pixel per DIP. Preserve the existing depth perspective.
                var pixelsToWorld=scale;
                var bounds=new Rect(
                    Snap(x+(sprite.OffsetX-sprite.CanvasWidth/2.0)*pixelsToWorld),
                    Snap(y+(sprite.OffsetY-sprite.CanvasHeight/2.0)*pixelsToWorld),
                    sprite.Bitmap.PixelWidth*pixelsToWorld,sprite.Bitmap.PixelHeight*pixelsToWorld);
                if(!Rect(environment.Display).IntersectsWith(bounds))continue;
                drawing.DrawImage(sprite.Bitmap,bounds);
                if(f.Activity==FishActivity.Eat)
                {
                    var width=f.Width*scale;
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
