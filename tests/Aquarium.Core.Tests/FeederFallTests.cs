using Aquarium.Core;

namespace Aquarium.Core.Tests;

[TestClass]
public sealed class FeederFallTests
{
    private static readonly Rect2 Area=new(0,0,1000,760);
    private static FeederState Open(double y=100) {var state=new FeederState();state.Open(new(200,y));return state;}
    [TestMethod] public void FallsAndStopsOnWorkAreaFloor()
    {
        var state=Open();var fall=new FeederFall();
        for(var i=0;i<180;i++)fall.Advance(state,Area,80,112,1.0/60);
        Assert.AreEqual(new Point2(200,648),state.Position);Assert.AreEqual(0,fall.Speed);
        Assert.AreEqual(FeederMode.Resting,state.Mode);Assert.AreEqual(0,state.HoldCount);
        Assert.IsFalse(fall.Advance(state,Area,80,112,1.0/60));
    }
    [TestMethod] public void CanCatchFallingFeederAndDropAgain()
    {
        var state=Open();var fall=new FeederFall();fall.Advance(state,Area,80,112,.1);
        Assert.IsGreaterThan(100d,state.Position.Y);Assert.IsTrue(state.BeginHold());var caught=state.Position;
        Assert.IsFalse(fall.Advance(state,Area,80,112,.1));Assert.AreEqual(caught,state.Position);Assert.AreEqual(0,fall.Speed);
        state.Move(new(300,200));state.Release();fall.Advance(state,Area,80,112,.1);
        Assert.AreEqual(300,state.Position.X);Assert.IsGreaterThan(200d,state.Position.Y);
    }
    [TestMethod] public void ClosedFeederDoesNotFall()
    {var state=Open();state.Close();Assert.IsFalse(new FeederFall().Advance(state,Area,80,112,.1));Assert.AreEqual(100,state.Position.Y);}
    [TestMethod] public void FloorChangesKeepObjectReachable()
    {
        var state=Open(648);var fall=new FeederFall();
        fall.Advance(state,new(0,0,250,600),80,112,.1);Assert.AreEqual(new Point2(170,488),state.Position);
        fall.Advance(state,Area,80,112,.1);Assert.IsGreaterThan(488d,state.Position.Y);
    }
    [TestMethod] public void TinyWorkAreaDoesNotThrowOrContinueFalling()
    {var state=Open();var fall=new FeederFall();fall.Advance(state,new(10,20,30,40),80,112,.1);Assert.AreEqual(new Point2(10,20),state.Position);Assert.AreEqual(0,fall.Speed);}
    [TestMethod] public void SuppressionClockCannotAdvanceHiddenFallTime()
    {
        var state=Open();var fall=new FeederFall();var clock=new SimulationClock();clock.Advance(0,true);
        var steps=clock.Advance(.05,true);for(var i=0;i<steps;i++)fall.Advance(state,Area,80,112,1.0/60);
        var before=state.Position;fall.Reset();Assert.AreEqual(0,clock.Advance(10,false));Assert.AreEqual(0,clock.Advance(20,true));
        Assert.AreEqual(before,state.Position);Assert.AreEqual(0,fall.Speed);
    }
    [TestMethod] public void FallingCannotDispenseFood()
    {
        var world=new World();var fall=new FeederFall();
        var env=new EnvironmentSnapshot(1,Area,Area,Array.Empty<Rect2>(),Array.Empty<Rect2>(),new(0,0),Suppression.None,true);
        world.SetEnabled(true);world.Feeder.Open(new(200,100));
        for(var i=0;i<120;i++){fall.Advance(world.Feeder,Area,80,112,1.0/60);world.SubmitHeldMotion(new(i%2*100,0),i/60.0,env);world.Advance(1.0/60,env);}
        Assert.AreEqual(0,world.TotalEmitted);Assert.AreEqual(0,world.ShakeCount);
    }
}
