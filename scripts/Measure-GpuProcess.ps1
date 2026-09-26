[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$RunDirectory,
    [ValidateRange(30,600)][int]$MaximumSeconds=300
)
# Optional, read-only sampler for the one process started by Measure-Prototype.py.
# No adapter changes, network changes, counters reset, or unrelated process data.
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$run=[IO.Path]::GetFullPath($RunDirectory)
$allowed=[IO.Path]::GetFullPath((Join-Path $root 'artifacts'))+'\'
if(-not $run.StartsWith($allowed,[StringComparison]::OrdinalIgnoreCase)){throw 'Results must remain under project artifacts.'}
[IO.Directory]::CreateDirectory($run)|Out-Null
$progressPath=Join-Path $run 'phase.json'
$output=Join-Path $run 'gpu-samples.json'
if(Test-Path $output){throw 'Use a new run directory; existing measurements are never overwritten.'}
$rows=[Collections.Generic.List[object]]::new()
$errors=[Collections.Generic.List[string]]::new()
$observedProcess=$null
$deadline=[DateTime]::UtcNow.AddSeconds($MaximumSeconds)
try {
    while([DateTime]::UtcNow -lt $deadline){
        if(Test-Path (Join-Path $run 'report.json')){break}
        if(Test-Path $progressPath){
            try {$phase=Get-Content -LiteralPath $progressPath -Raw -Encoding UTF8|ConvertFrom-Json}
            catch {Start-Sleep -Milliseconds 250;continue}
            if($phase.pid -and $phase.phase -in @('ordinary habitat','held shaking / feeding','manual hidden')){
                $appId=[int]$phase.pid
                if($null -eq $observedProcess){
                    $process=Get-CimInstance Win32_Process -Filter "ProcessId=$appId"
                    $path=$process.ExecutablePath
                    if(-not $path -or -not $path.StartsWith($allowed,[StringComparison]::OrdinalIgnoreCase) -or [IO.Path]::GetFileName($path) -ne 'Aquarium.Windows.exe'){
                        throw 'Measurement PID is not the expected project artifact.'
                    }
                    $observedProcess=$appId
                }
                if($appId -ne $observedProcess){throw 'Measurement process changed during GPU sampling.'}
                try {
                    $items=@(Get-CimInstance -ClassName Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine -Filter "Name LIKE 'pid_${appId}_%'" -OperationTimeoutSec 5 -ErrorAction Stop | ForEach-Object {
                        [ordered]@{instance=$_.Name;utilization_percent=[double]$_.UtilizationPercentage}
                    })
                    $rows.Add([ordered]@{utc=[DateTime]::UtcNow.ToString('o');phase=$phase.phase;pid=$appId;engines=$items})
                } catch {
                    if($errors.Count -lt 10){$errors.Add($_.Exception.Message)}
                }
            }
        }
        Start-Sleep -Seconds 2
    }
} catch { $errors.Add($_.Exception.Message) }
finally {
    $result=[ordered]@{
        kind='Read-only Windows GPU engine counters for measured aquarium PID'
        pid=$observedProcess
        interval_seconds=2
        samples=@($rows.ToArray())
        errors=@($errors.ToArray())
        scope='Per-process engine counters; not whole-system GPU load, compositor latency, or an offline test. Empty counter sets are unavailable, not zero utilization.'
    }
    $result|ConvertTo-Json -Depth 8|Set-Content -LiteralPath $output -Encoding UTF8
    [ordered]@{gpu_receipt=$output;observations=$rows.Count;errors=$errors.Count}|ConvertTo-Json
}
