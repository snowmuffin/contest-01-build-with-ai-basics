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
    private readonly CancellationTokenSource stop = new();
    private Task? worker;
    private bool disposed;
    public bool IsOwner { get; }

    public InstanceBroker()
    {
        var sid = WindowsIdentity.GetCurrent().User?.Value
            ?? throw new InvalidOperationException("No current user identity.");
        var token = Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(sid)))[..16];
        pipeName = $"AquariumG0-{token}-{Process.GetCurrentProcess().SessionId}";
        mutex = new Mutex(false, "Local\\" + pipeName);
        try { IsOwner = mutex.WaitOne(0); }
        catch (AbandonedMutexException) { IsOwner = true; }
    }

    public void Listen(Func<Task> open)
    {
        if (!IsOwner || worker is not null) throw new InvalidOperationException("Only the resident listens once.");
        var token = stop.Token;
        worker = Task.Run(async () =>
        {
            while (!token.IsCancellationRequested)
            {
                try
                {
                    using var pipe = new NamedPipeServerStream(pipeName, PipeDirection.InOut, 1,
                        PipeTransmissionMode.Byte, PipeOptions.Asynchronous | PipeOptions.CurrentUserOnly);
                    await pipe.WaitForConnectionAsync(token).ConfigureAwait(false);
                    using var deadline = CancellationTokenSource.CreateLinkedTokenSource(token);
                    deadline.CancelAfter(1800);
                    var data = new byte[8];
                    await pipe.ReadExactlyAsync(data, deadline.Token).ConfigureAwait(false);
                    if (Encoding.ASCII.GetString(data) != "feed-v1\n") continue;
                    // Acknowledgement means the dispatcher has handled the command, not merely queued it.
                    await open().WaitAsync(deadline.Token).ConfigureAwait(false);
                    await pipe.WriteAsync(new byte[] { 1 }, deadline.Token).ConfigureAwait(false);
                }
                catch (OperationCanceledException) { if (token.IsCancellationRequested) break; }
                catch (IOException) { /* A disconnected/malformed client cannot kill the resident. */ }
            }
        });
    }

    public bool SendFeed() => SendFeedAsync().GetAwaiter().GetResult();
    private async Task<bool> SendFeedAsync()
    {
        using var deadline = new CancellationTokenSource(TimeSpan.FromSeconds(4));
        while (!deadline.IsCancellationRequested)
        {
            try
            {
                using var pipe = new NamedPipeClientStream(".", pipeName, PipeDirection.InOut,
                    PipeOptions.Asynchronous | PipeOptions.CurrentUserOnly);
                await pipe.ConnectAsync(300, deadline.Token).ConfigureAwait(false);
                await pipe.WriteAsync(Encoding.ASCII.GetBytes("feed-v1\n"), deadline.Token).ConfigureAwait(false);
                var response = new byte[1];
                await pipe.ReadExactlyAsync(response, deadline.Token).ConfigureAwait(false);
                return response[0] == 1;
            }
            catch (Exception error) when (error is IOException or TimeoutException or OperationCanceledException)
            {
                if (deadline.IsCancellationRequested) return false;
                try { await Task.Delay(40, deadline.Token).ConfigureAwait(false); }
                catch (OperationCanceledException) { return false; }
            }
        }
        return false;
    }
    public void Dispose()
    {
        if (disposed) return;
        disposed = true;
        stop.Cancel();
        if (IsOwner) mutex.ReleaseMutex();
        mutex.Dispose();
        // Do not block the dispatcher on a worker that may be waiting for that dispatcher.
        if (worker is null) stop.Dispose();
        else _ = worker.ContinueWith(_ => stop.Dispose(), TaskScheduler.Default);
    }
}
