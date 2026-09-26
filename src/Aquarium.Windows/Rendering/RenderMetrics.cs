using System;
using System.Diagnostics;
using System.Linq;

namespace Aquarium.Windows.Rendering;

// Bounded and opt-in; elapsed callback time is NOT compositor/GPU display latency.
internal sealed class RenderMetrics
{
    private readonly double[] intervals = new double[512], durations = new double[512];
    private int count, cursor;
    private long previousStart;
    public bool Enabled { get; set; }
    public void ResetInterval() => previousStart = 0;
    public long Begin() => Enabled ? Stopwatch.GetTimestamp() : 0;
    public void End(long started)
    {
        if (!Enabled || started == 0) return;
        var ended = Stopwatch.GetTimestamp();
        var interval = previousStart == 0 ? 0 : (started - previousStart) * 1000.0 / Stopwatch.Frequency;
        previousStart = started;
        intervals[cursor] = interval;
        durations[cursor] = (ended - started) * 1000.0 / Stopwatch.Frequency;
        cursor = (cursor + 1) % durations.Length;
        count = Math.Min(count + 1, durations.Length);
    }
    public object? Snapshot()
    {
        if (!Enabled || count == 0) return null;
        var gaps = intervals.Take(count).Where(x => x > 0).OrderBy(x => x).ToArray();
        var costs = durations.Take(count).OrderBy(x => x).ToArray();
        static double Percentile(double[] values, double fraction) => values.Length == 0 ? 0 : values[(int)Math.Floor((values.Length - 1) * fraction)];
        return new { samples = count, callbackIntervalP50Ms = Percentile(gaps, .50),
            callbackIntervalP95Ms = Percentile(gaps, .95), callbackCpuP50Ms = Percentile(costs, .50),
            callbackCpuP95Ms = Percentile(costs, .95), scope = "WPF OnRender callback, not compositor/GPU latency" };
    }
}
