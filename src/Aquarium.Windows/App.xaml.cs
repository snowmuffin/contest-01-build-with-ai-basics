using System;
using System.Linq;
using System.Windows;
using System.Windows.Threading;
using Aquarium.Windows.Platform;

namespace Aquarium.Windows;

public partial class App : Application
{
    private HostController? host;
    private InstanceBroker? broker;
    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);
        try
        {
            broker=new InstanceBroker();
            if(!broker.IsOwner){var ok=!e.Args.Contains("--feed")||broker.SendFeed();Shutdown(ok?0:2);return;}
            string? diagnostics=null;int? duration=null;
            for(var i=0;i<e.Args.Length;i++)
            {
                if(e.Args[i]=="--diagnostics" && i+1<e.Args.Length)diagnostics=e.Args[++i];
                else if(e.Args[i]=="--probe-seconds" && i+1<e.Args.Length && int.TryParse(e.Args[++i],out var seconds))duration=Math.Clamp(seconds,1,600);
            }
            host=new HostController(diagnostics);broker.Listen(()=>Dispatcher.BeginInvoke(new Action(()=>host?.OpenFeeder())));
            if(e.Args.Contains("--feed"))host.OpenFeeder();
            if(duration is int timeout){var clock=new DispatcherTimer{Interval=TimeSpan.FromSeconds(timeout)};clock.Tick+=(_,_)=>{clock.Stop();Shutdown();};clock.Start();}
        }
        catch(Exception ex){MessageBox.Show("Aquarium could not start: "+ex.Message,"Aquarium G0",MessageBoxButton.OK,MessageBoxImage.Error);Shutdown(1);}
    }
    protected override void OnExit(ExitEventArgs e){host?.Dispose();broker?.Dispose();base.OnExit(e);}
}
