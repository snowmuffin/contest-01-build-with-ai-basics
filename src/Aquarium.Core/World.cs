using System;
using System.Collections.Generic;
using System.Linq;

namespace Aquarium.Core;

// UI host is the single writer. State and randomness remain portable, deterministic and bounded.
public sealed class World
{
    private readonly WorldSettings settings;
    private readonly Random random;
    private readonly List<FishState> fish=new();
    private readonly List<FoodState> food=new();
    private readonly Queue<ConsumptionEvent> meals=new();
    private readonly ShakeDetector shake=new();
    private Rect2 previousDisplay;
    private bool enabled;
    private int nextFoodId=1;
    public FeederState Feeder {get;}=new();
    public double Time {get;private set;}
    public long TotalEmitted {get;private set;}
    public long TotalConsumed {get;private set;}
    public long TotalExpired {get;private set;}
    public long ShakeCount {get;private set;}
    public long CuriosityCount {get;private set;}
    public World(WorldSettings? settings=null,int seed=4919)
    {
        this.settings=settings??new WorldSettings();this.settings.Validate();random=new Random(seed);
    }
    public void ResetFeeding() => shake.Reset();
    public void SetEnabled(bool value)
    {
        enabled=value;
        if(!value){Feeder.Release();ResetFeeding();}
    }
    public void SubmitHeldMotion(Point2 pointer,double timestamp,EnvironmentSnapshot environment)
    {
        if(!enabled || Feeder.Mode!=FeederMode.Held || !environment.Valid || environment.Suppression!=Suppression.None)
        {ResetFeeding();return;}
        if(!shake.Sample(pointer,timestamp))return;
        ShakeCount++;
        // The feeder nozzle is just BELOW the interactive object, so visible food never sits behind its body.
        var origin=new Point2(Feeder.Position.X+34,Feeder.Position.Y+116);
        if(!Occlusion.VisibleAt(origin,DepthBand.Front,environment))return;
        for(var i=0;i<3 && food.Count<settings.MaxPellets;i++)
        {
            var p=new Point2(origin.X+(random.NextDouble()-.5)*14,origin.Y+i*3);
            if(!Occlusion.VisibleAt(p,DepthBand.Front,environment))continue;
            food.Add(new FoodState{Id=nextFoodId++,Position=p,SpeedX=(random.NextDouble()-.5)*38,SpeedY=20+random.NextDouble()*10});TotalEmitted++;
        }
    }
    public void Advance(double dt,EnvironmentSnapshot s)
    {
        if(!double.IsFinite(dt)||dt<0)throw new ArgumentOutOfRangeException(nameof(dt));
        if(dt==0 || !enabled || !s.Valid || s.Suppression!=Suppression.None)return;
        if(dt>0.1)throw new ArgumentOutOfRangeException(nameof(dt),"Host must use bounded fixed steps, not advance hidden time.");
        if(fish.Count==0)Initialize(s);
        if(previousDisplay!=s.Display)
        {
            foreach(var f in fish){f.Position=ClampCenter(f.Position,s.WorkArea);f.Phase=DepthPhase.None;f.NextWander=0;}
            previousDisplay=s.Display;Feeder.Release();ResetFeeding();
        }
        Time+=dt;
        for(var i=food.Count-1;i>=0;i--)
        {
            var p=food[i];p.Age+=dt;
            if(p.Age>=settings.PelletLifetime){food.RemoveAt(i);TotalExpired++;continue;}
            p.SpeedY=Math.Min(62,p.SpeedY+20*dt);p.SpeedX*=Math.Exp(-1.1*dt);
            p.Position=new(Math.Clamp(p.Position.X+p.SpeedX*dt,s.WorkArea.X+3,s.WorkArea.Right-3),Math.Min(s.WorkArea.Bottom-5,p.Position.Y+p.SpeedY*dt));
        }
        var claimed=new HashSet<int>();
        foreach(var f in fish)StepFish(f,s,dt,claimed);
        while(meals.Count>0 && Time-meals.Peek().Time>0.55)meals.Dequeue();
    }
    private void Initialize(EnvironmentSnapshot s)
    {
        var area=s.WorkArea;
        for(var i=0;i<settings.FishCount;i++)
        {
            var p=ClampCenter(new Point2(area.X+area.Width*(.18+.15*(i%5)),area.Y+area.Height*(.24+.105*(i%5))),area);
            fish.Add(new FishState{Id=i+1,Position=p,WanderTarget=p,Band=i==0?DepthBand.Front:i%2==0?DepthBand.Rear:DepthBand.Middle,
                HomeBand=i%2==0?DepthBand.Rear:DepthBand.Middle,TargetBand=DepthBand.Front,
                ForegroundUntil=i==0?10:0,NextCuriosity=3+random.NextDouble()*10,NextWander=0});
        }
        previousDisplay=s.Display;
    }
    private void StepFish(FishState f,EnvironmentSnapshot s,double dt,HashSet<int> claimed)
    {
        FoodState? target=null;var best=double.MaxValue;
        foreach(var p in food)
        {
            if(claimed.Contains(p.Id)||!Occlusion.VisibleAt(p.Position,DepthBand.Front,s))continue;
            var foodDistance=FishGeometry.Distance(f.Position,p.Position);
            if(foodDistance<best){target=p;best=foodDistance;}
        }
        if(target is not null)claimed.Add(target.Id);
        if(target is null && Time>=f.NextCuriosity)
        {
            f.NextCuriosity=Time+9+random.NextDouble()*12;
            if(Feeder.Mode!=FeederMode.Held && FishGeometry.Distance(f.Position,s.Cursor)<settings.CuriosityRadius &&
                Occlusion.VisibleAt(s.Cursor,DepthBand.Front,s))
            {f.CuriousUntil=Time+2+random.NextDouble()*2;CuriosityCount++;}
        }
        var curious=target is null && Time<f.CuriousUntil;
        var desired=target is not null||curious||Time<f.ForegroundUntil||Time<f.EatingUntil?DepthBand.Front:f.HomeBand;
        if(DepthTransitions.Advance(f,desired,s,settings,dt))return;
        if(Time<f.EatingUntil)
        {f.Activity=FishActivity.Eat;f.Velocity=new(f.Velocity.X*.9,f.Velocity.Y*.9);return;}
        Point2 goal;double speed;
        if(target is not null)
        {
            // Aim the mouth, rather than the sprite's centre, at the pellet.
            var sign=target.Position.X>=f.Position.X?1:-1;
            if(Math.Abs(target.Position.X-f.Position.X)>settings.FishWidth*.45)f.FacingRight=sign>0;
            sign=f.FacingRight?1:-1;
            goal=new Point2(target.Position.X-sign*settings.FishWidth*.30,target.Position.Y);
            f.Activity=FishActivity.SeekFood;speed=settings.SeekSpeed;f.ForegroundUntil=Time+3;
        }
        else if(curious)
        {
            goal=ClampCenter(new Point2(s.Cursor.X+(f.Id%2==0?58:-58),s.Cursor.Y+16),s.WorkArea);
            speed=90;f.Activity=FishActivity.Curious;
        }
        else
        {
            if(Time>=f.NextWander||FishGeometry.Distance(f.Position,f.WanderTarget)<16)
            {
                // Neighbourhood wandering avoids repeated straight-line cross-screen travel.
                f.WanderTarget=ClampCenter(new Point2(f.Position.X+(random.NextDouble()-.5)*430,f.Position.Y+(random.NextDouble()-.5)*180),s.WorkArea);
                f.NextWander=Time+4+random.NextDouble()*5;
            }
            goal=f.WanderTarget;speed=32+f.Id*3;f.Activity=FishActivity.Wander;
        }
        var before=f.Position;
        var distance=FishGeometry.Distance(before,goal);
        var desiredSpeed=Math.Min(speed,distance*3.5);
        // Seek approaches are fast enough to reach sinking food, without instantaneous relocation.
        f.Position=FishGeometry.MoveTowards(before,goal,desiredSpeed*dt);
        // Only destinations are clamped: after feeding near an edge, swim back instead of snapping the centre.
        f.Velocity=new((f.Position.X-before.X)/dt,(f.Position.Y-before.Y)/dt);
        if(target is null && Math.Abs(f.Velocity.X)>3)f.FacingRight=f.Velocity.X>0;
        if(target is not null && f.Band==DepthBand.Front)
        {
            var mouth=new Point2(f.Position.X+(f.FacingRight?1:-1)*settings.FishWidth*.30,f.Position.Y);
            if(FishGeometry.Distance(mouth,target.Position)<=10 && Occlusion.VisibleAt(mouth,DepthBand.Front,s) &&
                Occlusion.VisibleAt(target.Position,DepthBand.Front,s) && food.Remove(target))
            {
                TotalConsumed++;f.EatingUntil=Time+.22;f.Activity=FishActivity.Eat;
                meals.Enqueue(new(f.Id,target.Id,f.Position,target.Position,Time,true,f.Band));
                while(meals.Count>32)meals.Dequeue();
            }
        }
    }
    private Point2 ClampCenter(Point2 p,Rect2 area)
    {
        var mx=settings.FishWidth/2+3;var my=settings.FishHeight/2+3;
        return new(Math.Clamp(p.X,area.X+mx,Math.Max(area.X+mx,area.Right-mx)),
            Math.Clamp(p.Y,area.Y+my,Math.Max(area.Y+my,area.Bottom-my)));
    }
    public SceneFrame Snapshot() => new(Time,
        Array.AsReadOnly(fish.Select(f=>new FishPose(f.Id,f.Position,f.Velocity,f.Band,f.Activity,f.FacingRight,settings.FishWidth,settings.FishHeight,f.Phase)).ToArray()),
        Array.AsReadOnly(food.Select(p=>new FoodPose(p.Id,p.Position,p.Age)).ToArray()),Array.AsReadOnly(meals.ToArray()));
}
