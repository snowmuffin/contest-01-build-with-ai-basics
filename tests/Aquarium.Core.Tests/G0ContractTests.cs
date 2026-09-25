using System;
using Aquarium.Core;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace Aquarium.Core.Tests;

[TestClass]
public sealed class G0ContractTests
{
    private static EnvironmentSnapshot Sample() => new(1,new(0,0,1000,800),new(0,0,1000,760),
        Array.AsReadOnly(new[]{new Rect2(100,100,200,200),new Rect2(200,200,400,400)}),
        Array.AsReadOnly(new[]{new Rect2(0,760,1000,40)}),new(10,10),Suppression.None,true);

    [TestMethod] public void MiddleHiddenBehindForemost() => Assert.IsFalse(Occlusion.VisibleAt(new(150,150),DepthBand.Middle,Sample()));
    [TestMethod] public void MiddleVisibleOverRearWindow() => Assert.IsTrue(Occlusion.VisibleAt(new(400,400),DepthBand.Middle,Sample()));
    [TestMethod] public void RearHiddenBehindEitherWindow() => Assert.IsFalse(Occlusion.VisibleAt(new(400,400),DepthBand.Rear,Sample()));
    [TestMethod] public void FrontVisibleOverWork() => Assert.IsTrue(Occlusion.VisibleAt(new(150,150),DepthBand.Front,Sample()));
    [TestMethod] public void ProtectedAreaWinsOverFront() => Assert.IsFalse(Occlusion.VisibleAt(new(20,780),DepthBand.Front,Sample()));
    [TestMethod] public void OutsideDisplayNeverVisible() => Assert.IsFalse(Occlusion.VisibleAt(new(-1,20),DepthBand.Front,Sample()));
    [TestMethod] public void InvalidSnapshotNeverVisible() => Assert.IsFalse(Occlusion.VisibleAt(new(20,20),DepthBand.Front,Sample() with {Valid=false}));
    [TestMethod] public void EmptyWindowsHaveNoWorkMask() => Assert.IsTrue(Occlusion.VisibleAt(new(150,150),DepthBand.Rear,Sample() with {WorkWindows=Array.Empty<Rect2>()}));
    [TestMethod] public void DpiRoundtripNegativeOrigin()
    {var t=new DisplayTransform(-1920,100,1.5);var p=new Point2(-1770,250);Assert.AreEqual(new Point2(100,100),t.ToLocal(p));Assert.AreEqual(p,t.ToPhysical(t.ToLocal(p)));}
    [TestMethod] public void DpiRectangleNormalizesOnce() => Assert.AreEqual(new Rect2(20,40,100,80),new DisplayTransform(10,20,2).ToLocal(new Rect2(50,100,200,160)));
    [TestMethod] public void ZeroDpiRejected() => Assert.ThrowsExactly<ArgumentOutOfRangeException>(()=>new DisplayTransform(0,0,0).ToLocal(new Point2(1,1)));
    [TestMethod] public void ClampFeederAtDisplayEdge() => Assert.AreEqual(new Point2(836,648),new Rect2(0,0,1000,760).ClampOrigin(new(1000,800),164,112));
    [TestMethod] public void OversizeObjectClampDoesNotThrow() => Assert.AreEqual(new Point2(0,0),new Rect2(0,0,50,50).ClampOrigin(new(100,100),164,112));
    [TestMethod] public void HideSurvivesFullscreenExit()
    {var v=new VisibilityPolicy();v.Hide();v.Observe(Suppression.Fullscreen);v.Observe(Suppression.None);Assert.IsFalse(v.Visible);v.Show();Assert.IsTrue(v.Visible);}
    [TestMethod] public void ShowCannotOverrideFullscreen()
    {var v=new VisibilityPolicy();v.Observe(Suppression.Fullscreen);v.Hide();v.Show();Assert.IsFalse(v.Visible);}
    [TestMethod] public void MultipleGuardsRemainIndependent()
    {var v=new VisibilityPolicy();v.Observe(Suppression.Fullscreen|Suppression.Session);v.Observe(Suppression.Session);Assert.IsFalse(v.Visible);v.Observe(Suppression.None);Assert.IsTrue(v.Visible);}
    [TestMethod] public void OrdinaryCaptionedMaximizeIsNotFullscreen() => Assert.IsFalse(FullscreenRules.CoversDisplay(new(0,0,1920,1080),new(0,0,1920,1080),true));
    [TestMethod] public void BorderlessClientCoverIsFullscreen() => Assert.IsTrue(FullscreenRules.CoversDisplay(new(0,0,1920,1080),new(0,0,1920,1080),false));
    [TestMethod] public void WorkAreaClientIsNotFullscreen() => Assert.IsFalse(FullscreenRules.CoversDisplay(new(0,30,1920,1000),new(0,0,1920,1080),false));
    [TestMethod] public void InvalidClientNotFullscreen() => Assert.IsFalse(FullscreenRules.CoversDisplay(default,new(0,0,1920,1080),false));
    [TestMethod] public void OpenDoesNotHold()
    {var f=new FeederState();f.Open(new(2,3));Assert.AreEqual(FeederMode.Resting,f.Mode);Assert.AreEqual(0,f.HoldCount);}
    [TestMethod] public void RepeatedOpenPreservesPosition()
    {var f=new FeederState();f.Open(new(2,3));f.Open(new(500,500));Assert.AreEqual(new Point2(2,3),f.Position);}
    [TestMethod] public void ReleaseAndCloseAreDifferent()
    {var f=new FeederState();f.Open(new(2,3));Assert.IsTrue(f.BeginHold());f.Move(new(20,30));f.Release();Assert.AreEqual(FeederMode.Resting,f.Mode);Assert.AreEqual(new Point2(20,30),f.Position);f.Close();Assert.AreEqual(FeederMode.Closed,f.Mode);}
    [TestMethod] public void OrdinaryMotionDoesNotMoveFeeder()
    {var f=new FeederState();f.Open(new(2,3));f.Move(new(100,100));Assert.AreEqual(new Point2(2,3),f.Position);}
    [TestMethod] public void CannotHoldClosedFeeder() => Assert.IsFalse(new FeederState().BeginHold());
    [TestMethod] public void CancellationRequiresFreshPickup()
    {var f=new FeederState();f.Open(new(1,1));f.BeginHold();f.Release();f.Move(new(10,10));Assert.AreEqual(new Point2(1,1),f.Position);Assert.IsTrue(f.BeginHold());Assert.AreEqual(2,f.HoldCount);}
}
