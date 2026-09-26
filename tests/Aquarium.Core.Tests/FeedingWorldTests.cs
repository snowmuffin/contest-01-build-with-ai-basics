using System;
using System.Linq;
using Aquarium.Core;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace Aquarium.Core.Tests;

[TestClass]
public sealed class FeedingWorldTests
{
    private static EnvironmentSnapshot Env(bool covered=false,Suppression reason=Suppression.None) => new(1,new(0,0,900,700),new(0,0,900,670),
        covered?new[]{new Rect2(0,0,900,700)}:Array.Empty<Rect2>(),Array.Empty<Rect2>(),new(450,350),reason,true);
    private static World Make(int count=5,int cap=64,double lifetime=12)
    {
        var w=new World(new WorldSettings{FishCount=count,MaxPellets=cap,PelletLifetime=lifetime},123);w.SetEnabled(true);w.Advance(1.0/60,Env());return w;
    }
    private static void Shake(World w,EnvironmentSnapshot e,double start=1)
    {
        var points=new[]{new Point2(0,0),new(50,0),new(0,0),new(50,0),new(0,0),new(50,0)};
        for(var i=0;i<points.Length;i++)w.SubmitHeldMotion(points[i],start+i*.07,e);
    }
    private static void Feed(World w,EnvironmentSnapshot e)
    {
        w.Feeder.Open(new(420,290));w.Feeder.BeginHold();w.ResetFeeding();Shake(w,e);
    }
    private static void Run(World w,EnvironmentSnapshot e,double seconds)
    {for(var i=0;i<seconds*60;i++)w.Advance(1.0/60,e);}

    [TestMethod] public void TwoDirectionReversalsGenerateShake()
    {var d=new ShakeDetector();Assert.IsFalse(d.Sample(new(0,0),0));Assert.IsFalse(d.Sample(new(50,0),.07));Assert.IsFalse(d.Sample(new(0,0),.14));Assert.IsTrue(d.Sample(new(50,0),.21));}
    [TestMethod] public void OneFastSweepNeverCounts()
    {var d=new ShakeDetector();for(var i=0;i<20;i++)Assert.IsFalse(d.Sample(new(i*25,0),i*.02));}
    [TestMethod] public void StationaryJitterNeverCounts()
    {var d=new ShakeDetector();for(var i=0;i<200;i++)Assert.IsFalse(d.Sample(new(i%2==0?2:-2,0),i*.02));}
    [TestMethod] public void SlowMovementNeverCounts()
    {var d=new ShakeDetector();for(var i=0;i<20;i++)Assert.IsFalse(d.Sample(new(i%2==0?10:-10,0),i*.4));}
    [TestMethod] public void LongPauseDiscardsPreviousReversals()
    {var d=new ShakeDetector();d.Sample(new(0,0),0);d.Sample(new(50,0),.07);d.Sample(new(0,0),.14);Assert.IsFalse(d.Sample(new(50,0),2));}
    [TestMethod] public void ResetDiscardsPreviousReversals()
    {var d=new ShakeDetector();d.Sample(new(0,0),0);d.Sample(new(50,0),.07);d.Sample(new(0,0),.14);d.Reset();Assert.IsFalse(d.Sample(new(50,0),.21));}
    [TestMethod] public void NonFinitePointerResetsWithoutEmission()
    {var d=new ShakeDetector();Assert.IsFalse(d.Sample(new(double.NaN,0),1));Assert.IsFalse(d.Sample(new(50,0),2));}
    [TestMethod] public void NoFoodWhileClosed()
    {var w=Make();Shake(w,Env());Assert.AreEqual(0L,w.TotalEmitted);}
    [TestMethod] public void NoFoodWhileResting()
    {var w=Make();w.Feeder.Open(new(300,200));Shake(w,Env());Assert.AreEqual(0L,w.TotalEmitted);}
    [TestMethod] public void HeldShakeActuallyEmits()
    {var w=Make();Feed(w,Env());Assert.IsGreaterThan(0L,w.TotalEmitted);Assert.IsNotEmpty(w.Snapshot().Food);}
    [TestMethod] public void ReleasePreservesExistingPelletsButStopsEmission()
    {var w=Make();Feed(w,Env());var n=w.TotalEmitted;w.Feeder.Release();w.ResetFeeding();Shake(w,Env(),2);Assert.AreEqual(n,w.TotalEmitted);Assert.HasCount((int)n,w.Snapshot().Food);}
    [TestMethod] public void ClosingFeederDoesNotDeleteWorld()
    {var w=Make();Feed(w,Env());w.Feeder.Close();w.ResetFeeding();Assert.HasCount(5,w.Snapshot().Fish);Assert.IsNotEmpty(w.Snapshot().Food);}
    [TestMethod] public void PelletCountIsCapped()
    {var w=Make(cap:4);Feed(w,Env());for(var i=2;i<10;i++)Shake(w,Env(),i);Assert.HasCount(4,w.Snapshot().Food);}
    [TestMethod] public void ExpiryIsBoundedAndAccountedFor()
    {var w=Make(lifetime:.03);Feed(w,Env());Run(w,Env(),.05);Assert.IsEmpty(w.Snapshot().Food);Assert.AreEqual(w.TotalEmitted,w.TotalConsumed+w.TotalExpired);}
    [TestMethod] public void DisabledSimulationFreezesAndReleasesHold()
    {var w=Make();Feed(w,Env());var t=w.Time;var n=w.TotalEmitted;w.SetEnabled(false);Run(w,Env(),2);Shake(w,Env(),3);Assert.AreEqual(t,w.Time);Assert.AreEqual(n,w.TotalEmitted);Assert.AreEqual(FeederMode.Resting,w.Feeder.Mode);}
    [TestMethod] public void FullscreenSnapshotCannotEmitOrConsume()
    {var w=Make();Feed(w,Env());var t=w.Time;var n=w.TotalEmitted;Run(w,Env(reason:Suppression.Fullscreen),2);Shake(w,Env(reason:Suppression.Fullscreen),3);Assert.AreEqual(t,w.Time);Assert.AreEqual(n,w.TotalEmitted);Assert.AreEqual(0L,w.TotalConsumed);}
    [TestMethod] public void ActualFoodIsConsumedVisiblyOnce()
    {var w=Make();Feed(w,Env());var total=w.TotalEmitted;Run(w,Env(),8);Assert.IsGreaterThan(0L,w.TotalConsumed,"Real steering must reach food.");Assert.IsLessThanOrEqualTo(total,w.TotalConsumed);Assert.AreEqual(total,w.TotalConsumed+w.TotalExpired+w.Snapshot().Food.Count);}
    [TestMethod] public void MealsAlwaysComeFromVisibleForegroundFish()
    {
        var w=Make();Feed(w,Env());var seen=0;
        for(var i=0;i<600;i++){w.Advance(1.0/60,Env());foreach(var meal in w.Snapshot().RecentMeals){seen++;Assert.IsTrue(meal.Visible);Assert.AreEqual(DepthBand.Front,meal.Band);}}
        Assert.IsGreaterThan(0,seen);
    }
    [TestMethod] public void MaximizedWindowDoesNotPreventFeeding()
    {var w=Make();Feed(w,Env(true));Run(w,Env(true),11);Assert.IsGreaterThan(0L,w.TotalConsumed);Assert.HasCount(5,w.Snapshot().Fish);}
    [TestMethod] public void EdgeTransitionsKeepIdsAndBoundTravel()
    {
        var w=Make();var ids=w.Snapshot().Fish.Select(f=>f.Id).ToArray();Feed(w,Env(true));var transitioned=false;
        for(var i=0;i<600;i++)
        {
            var old=w.Snapshot();w.Advance(1.0/60,Env(true));var now=w.Snapshot();
            CollectionAssert.AreEqual(ids,now.Fish.Select(f=>f.Id).ToArray());
            for(var j=0;j<now.Fish.Count;j++)
            {Assert.IsLessThanOrEqualTo(4.01,FishGeometry.Distance(old.Fish[j].Position,now.Fish[j].Position),"No teleporting fish.");if(now.Fish[j].Transition!=DepthPhase.None)transitioned=true;}
        }
        Assert.IsTrue(transitioned);
    }
    [TestMethod] public void DepthCannotSwitchThroughCoveredSprite()
    {Assert.IsFalse(FishGeometry.CanSwitchWithoutPop(new(300,200),68,40,DepthBand.Rear,DepthBand.Front,Env(true)));}
    [TestMethod] public void OffscreenDepthSwitchIsAllowed()
    {Assert.IsTrue(FishGeometry.CanSwitchWithoutPop(new(-50,200),68,40,DepthBand.Rear,DepthBand.Front,Env(true)));}
    [TestMethod] public void SameInputSeedProducesSameWorld()
    {var a=Make();var b=Make();Feed(a,Env());Feed(b,Env());Run(a,Env(),6);Run(b,Env(),6);CollectionAssert.AreEqual(a.Snapshot().Fish.ToArray(),b.Snapshot().Fish.ToArray());Assert.AreEqual(a.TotalConsumed,b.TotalConsumed);}
    [TestMethod] public void FiveFishKeepAtLeastFourStableSpecies()
    {
        var w=Make();var before=w.Snapshot().Fish.Select(f=>f.Species).ToArray();
        Assert.IsGreaterThanOrEqualTo(4,before.Distinct().Count());
        Run(w,Env(),12);
        CollectionAssert.AreEqual(before,w.Snapshot().Fish.Select(f=>f.Species).ToArray());
    }
    [TestMethod] public void DepthPresentationShowsTowardAndAwayWithoutChangingIds()
    {
        var w=Make();var ids=w.Snapshot().Fish.Select(f=>f.Id).ToArray();var toward=false;var away=false;
        Feed(w,Env());
        for(var i=0;i<180;i++)
        {
            w.Advance(1.0/60,Env());var frame=w.Snapshot();
            toward|=frame.Fish.Any(f=>f.Facing==FishFacing.TowardViewer);
            Assert.IsTrue(frame.Fish.All(f=>f.VisualDepth>=0&&f.VisualDepth<=2));
        }
        w.Feeder.Release();w.ResetFeeding();
        for(var i=0;i<900;i++)
        {
            w.Advance(1.0/60,Env());var frame=w.Snapshot();
            away|=frame.Fish.Any(f=>f.Facing==FishFacing.AwayFromViewer);
        }
        Assert.IsTrue(toward,"At least one fish should visually approach the viewer.");
        Assert.IsTrue(away,"At least one fish should visually recede from the viewer.");
        CollectionAssert.AreEqual(ids,w.Snapshot().Fish.Select(f=>f.Id).ToArray());
    }
    [TestMethod] public void FishMoveWithoutFeeding()
    {var w=Make();var before=w.Snapshot();Run(w,Env(),2);Assert.AreNotEqual(before.Fish[0].Position,w.Snapshot().Fish[0].Position);Assert.AreEqual(0L,w.TotalEmitted);}
    [TestMethod] public void CursorCuriosityIsOccasional()
    {
        var w=Make(count:1);var active=0;
        for(var i=0;i<40*60;i++){var p=w.Snapshot().Fish[0].Position;var e=Env() with{Cursor=new Point2(p.X+70,p.Y+10)};w.Advance(1.0/60,e);if(w.Snapshot().Fish[0].Activity==FishActivity.Curious)active++;}
        Assert.IsGreaterThan(0L,w.CuriosityCount);Assert.IsGreaterThan(0,active);Assert.IsLessThan(40*60/2,active);
    }
    [TestMethod] public void ResizeCancelsHoldingWithoutCreatingFish()
    {var w=Make();Feed(w,Env());w.Advance(1.0/60,Env() with{Display=new(0,0,1000,800),WorkArea=new(0,0,1000,770)});Assert.AreEqual(FeederMode.Resting,w.Feeder.Mode);Assert.HasCount(5,w.Snapshot().Fish);}
    [TestMethod] public void ExtremeElapsedTimeIsRejectedInsteadOfCatchup()
    {var w=Make();Assert.ThrowsExactly<ArgumentOutOfRangeException>(()=>w.Advance(5,Env()));}
    [TestMethod] public void NewWorldDoesNotPersistFood()
    {var a=Make();Feed(a,Env());var b=Make();Assert.IsEmpty(b.Snapshot().Food);Assert.AreEqual(0L,b.TotalEmitted);}
}
