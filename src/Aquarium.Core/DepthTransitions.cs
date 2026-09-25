using System;

namespace Aquarium.Core;

public static class FishGeometry
{
    public static double Distance(Point2 a, Point2 b) => Math.Sqrt((a.X-b.X)*(a.X-b.X)+(a.Y-b.Y)*(a.Y-b.Y));
    public static Point2 MoveTowards(Point2 from, Point2 target, double distance)
    {
        var length=Distance(from,target);
        if(length<=distance || length<0.0001) return target;
        return new(from.X+(target.X-from.X)*distance/length,from.Y+(target.Y-from.Y)*distance/length);
    }
    public static Rect2 Bounds(Point2 center, double width, double height) => new(center.X-width/2,center.Y-height/2,width,height);
    public static bool CanSwitchWithoutPop(Point2 p, double w, double h, DepthBand from, DepthBand to, EnvironmentSnapshot s)
    {
        if(from==to || !FishGeometry.Bounds(p,w,h).Intersects(s.Display)) return true;
        var a=Count(from,s); var b=Count(to,s); var bounds=Bounds(p,w,h);
        for(var i=Math.Min(a,b);i<Math.Max(a,b);i++) if(bounds.Intersects(s.WorkWindows[i]))return false;
        return true;
    }
    private static int Count(DepthBand band,EnvironmentSnapshot s) => band==DepthBand.Front?0:band==DepthBand.Middle?Math.Min(1,s.WorkWindows.Count):s.WorkWindows.Count;
}

internal static class DepthTransitions
{
    // Move the SAME fish out past the screen edge before changing a currently occluded band.
    public static bool Advance(FishState f, DepthBand requested, EnvironmentSnapshot s, WorldSettings settings, double dt)
    {
        var margin=settings.FishWidth/2+10;
        if(f.Phase==DepthPhase.None)
        {
            if(f.Band==requested)return false;
            if(FishGeometry.CanSwitchWithoutPop(f.Position,settings.FishWidth,settings.FishHeight,f.Band,requested,s))
            {f.Band=requested;return false;}
            f.TargetBand=requested;f.Phase=DepthPhase.Leaving;
            var left=f.Position.X-s.Display.X < s.Display.Right-f.Position.X;
            f.EdgeTarget=new(left?s.Display.X-margin:s.Display.Right+margin,
                Math.Clamp(f.Position.Y,s.WorkArea.Y+margin,Math.Max(s.WorkArea.Y+margin,s.WorkArea.Bottom-margin)));
        }
        var before=f.Position;
        f.Position=FishGeometry.MoveTowards(f.Position,f.EdgeTarget,settings.SeekSpeed*dt);
        f.Velocity=new((f.Position.X-before.X)/dt,(f.Position.Y-before.Y)/dt);
        if(Math.Abs(f.Velocity.X)>1)f.FacingRight=f.Velocity.X>0;
        f.Activity=FishActivity.ChangingDepth;
        if(FishGeometry.Distance(f.Position,f.EdgeTarget)<0.01)
        {
            if(f.Phase==DepthPhase.Leaving)
            {
                f.Band=f.TargetBand;f.Phase=DepthPhase.Entering;
                var left=f.Position.X<s.Display.X;
                f.EdgeTarget=new(left?s.WorkArea.X+margin:s.WorkArea.Right-margin,f.Position.Y);
            }
            else f.Phase=DepthPhase.None;
        }
        return true;
    }
}
