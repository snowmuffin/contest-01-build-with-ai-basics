using System;
using Aquarium.Core;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace Aquarium.Core.Tests;

[TestClass]
public sealed class LifecycleTests
{
    [TestMethod]
    public void ResumeDoesNotAdvanceHiddenTime()
    {
        var clock = new SimulationClock();
        Assert.AreEqual(0, clock.Advance(0, true));
        Assert.AreEqual(2, clock.Advance(1.0 / 30, true));
        Assert.AreEqual(0, clock.Advance(1, false));
        Assert.AreEqual(0, clock.Advance(100, false));
        Assert.AreEqual(0, clock.Advance(150, true));
        Assert.AreEqual(2, clock.Advance(150 + 1.0 / 30, true));
    }
    [TestMethod]
    public void LongVisibleStallHasBoundedCatchUp()
    {
        var clock = new SimulationClock();
        clock.Advance(0, true);
        Assert.AreEqual(3, clock.Advance(10, true));
        Assert.AreEqual(0, clock.Advance(10, true));
    }
    [TestMethod]
    public void BackwardsClockRebasesWithoutSteps()
    {
        var clock = new SimulationClock();
        clock.Advance(10, true);
        Assert.AreEqual(0, clock.Advance(1, true));
        Assert.AreEqual(1, clock.Advance(1 + 1.0 / 60, true));
    }
    [TestMethod]
    public void FractionalFramesAccumulate()
    {
        var clock = new SimulationClock();
        clock.Advance(0, true);
        Assert.AreEqual(0, clock.Advance(1.0 / 120, true));
        Assert.AreEqual(1, clock.Advance(1.0 / 60, true));
    }
    [TestMethod]
    public void ReconnectDoesNotUnlockSession()
    {
        var state = new SessionAvailability();
        state.Apply(SessionSignal.Lock);
        state.Apply(SessionSignal.Disconnect);
        state.Apply(SessionSignal.Connect);
        Assert.IsTrue(state.Unavailable);
        state.Apply(SessionSignal.Unlock);
        Assert.IsFalse(state.Unavailable);
    }
    [TestMethod]
    public void UnlockDoesNotReconnectSession()
    {
        var state = new SessionAvailability();
        state.Apply(SessionSignal.Disconnect);
        state.Apply(SessionSignal.Lock);
        state.Apply(SessionSignal.Unlock);
        Assert.IsTrue(state.Unavailable);
        state.Apply(SessionSignal.Connect);
        Assert.IsFalse(state.Unavailable);
    }
    [TestMethod]
    public void SessionEventsAreIdempotent()
    {
        var state = new SessionAvailability();
        state.Apply(SessionSignal.Lock);
        state.Apply(SessionSignal.Lock);
        state.Apply(SessionSignal.Unlock);
        Assert.IsFalse(state.Unavailable);
    }
    [TestMethod]
    public void ManualHideSurvivesEveryAutomaticGuardCombination()
    {
        var policy = new VisibilityPolicy();
        policy.Hide();
        for (var flags = 0; flags < 64; flags++)
        {
            policy.Observe((Suppression)flags);
            Assert.IsFalse(policy.Visible);
        }
        policy.Observe(Suppression.None);
        Assert.IsFalse(policy.Visible);
        policy.Show();
        Assert.IsTrue(policy.Visible);
    }
    [TestMethod]
    public void ShowDoesNotBypassGuard()
    {
        var policy = new VisibilityPolicy();
        policy.Hide();
        policy.Observe(Suppression.Fullscreen | Suppression.Session);
        policy.Show();
        Assert.IsFalse(policy.Visible);
        policy.Observe(Suppression.Session);
        Assert.IsFalse(policy.Visible);
        policy.Observe(Suppression.None);
        Assert.IsTrue(policy.Visible);
    }
    [TestMethod]
    public void ClosedFeederStaysClosedOnRepeatedCancellation()
    {
        var feeder = new FeederState();
        feeder.Open(new Point2(10, 10));
        feeder.BeginHold();
        feeder.Close();
        feeder.Release();
        feeder.Release();
        Assert.AreEqual(FeederMode.Closed, feeder.Mode);
    }
}
