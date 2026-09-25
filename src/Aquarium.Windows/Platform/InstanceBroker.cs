using System;
using System.Diagnostics;
using System.IO;
using System.IO.Pipes;
using System.Security.Cryptography;
using System.Security.Principal;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Aquarium.Windows.Platform;

internal sealed class InstanceBroker : IDisposable
{
    private readonly Mutex mutex;
    private readonly string pipeName;
    private readonly CancellationTokenSource stop=new();
    public bool IsOwner {get;}
    public InstanceBroker()
    {
        var sid=WindowsIdentity.GetCurrent().User?.Value??throw new InvalidOperationException("No current user identity.");
        var token=Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(sid)))[..16];
        pipeName=$"AquariumG0-{token}-{Process.GetCurrentProcess().SessionId}";
        mutex=new Mutex(true,"Local\\"+pipeName,out var created);IsOwner=created;
    }
    public void Listen(Action open)
    {
        var token=stop.Token;
        _=Task.Run(async()=>
        {
            while(!token.IsCancellationRequested)
            {
                try
                {
                    using var pipe=new NamedPipeServerStream(pipeName,PipeDirection.InOut,1,PipeTransmissionMode.Byte,PipeOptions.Asynchronous|PipeOptions.CurrentUserOnly);
                    await pipe.WaitForConnectionAsync(token);
                    using var deadline=CancellationTokenSource.CreateLinkedTokenSource(token);deadline.CancelAfter(2000);
                    var buf=new byte[8];await pipe.ReadExactlyAsync(buf,deadline.Token);
                    if(Encoding.ASCII.GetString(buf)=="feed-v1\n") {open();await pipe.WriteAsync(new byte[]{1},deadline.Token);}
                }
                catch(OperationCanceledException) {if(token.IsCancellationRequested)break;}
                catch(IOException) { }
            }
        });
    }
    public bool SendFeed()
    {
        try{using var pipe=new NamedPipeClientStream(".",pipeName,PipeDirection.InOut,PipeOptions.CurrentUserOnly);pipe.Connect(2000);pipe.Write(Encoding.ASCII.GetBytes("feed-v1\n"));return true;}
        catch(Exception e) when(e is IOException or TimeoutException){return false;}
    }
    public void Dispose(){stop.Cancel();if(IsOwner)mutex.ReleaseMutex();mutex.Dispose();stop.Dispose();}
}
