[CmdletBinding()]
param(
    [string]$PackageDirectory = 'C:\AquariumPackage',
    [string]$ResultsDirectory = 'C:\AquariumResults',
    [switch]$AutoOnly
)
# Intended for a disposable, network-disabled Windows Sandbox or a user-provided test VM.
# It does not disable networking, uninstall software, or alter PowerShell/security settings.
$ErrorActionPreference='Stop'
$package=(Resolve-Path -LiteralPath $PackageDirectory).Path
if(-not (Test-Path (Join-Path $package 'app\Aquarium.Windows.exe'))){throw 'Package layout is missing app\Aquarium.Windows.exe.'}
if(@(Get-Process Aquarium.Windows -ErrorAction SilentlyContinue).Count){throw 'Exit any existing aquarium before the isolated acceptance test.'}
[IO.Directory]::CreateDirectory($ResultsDirectory)|Out-Null
$resultPath=Join-Path $ResultsDirectory ('acceptance-'+[DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss')+'.json')
$state=Join-Path $ResultsDirectory 'state.json'
if(Test-Path $state){throw 'Previous state.json exists; use a new results directory.'}
$sdkRoots=@((Join-Path $env:ProgramFiles 'dotnet\sdk'),(Join-Path ${env:ProgramFiles(x86)} 'dotnet\sdk'))
$installedSdk=@($sdkRoots|Where-Object {Test-Path -LiteralPath $_})
$dotnetOnPath=[bool](Get-Command dotnet -ErrorAction SilentlyContinue)
$routes=@();$networkProbeError=$null
try {$routes=@(Get-NetRoute -ErrorAction Stop|Where-Object {$_.DestinationPrefix -in @('0.0.0.0/0','::/0')}|Select-Object DestinationPrefix,InterfaceIndex)} catch {$networkProbeError=$_.Exception.Message}
$inventory=Get-Content (Join-Path $package 'FILES.json') -Raw|ConvertFrom-Json
$hashPass=$true
foreach($entry in $inventory){
    $path=[IO.Path]::GetFullPath((Join-Path $package $entry.path))
    if(-not $path.StartsWith($package+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Unsafe inventory path.'}
    if(-not (Test-Path -LiteralPath $path) -or (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash -ine $entry.sha256){$hashPass=$false;break}
}
if(-not $hashPass){throw 'Package inventory does not match.'}
$record=[ordered]@{kind='clean-room acceptance';host_os=[Environment]::OSVersion.VersionString;inventory_files=$inventory.Count;inventory_pass=$hashPass;dotnet_on_path=$dotnetOnPath;sdk_directory_count=$installedSdk.Count;default_route_count=$routes.Count;network_probe_error=$networkProbeError;network_unavailable_observed=($null -eq $networkProbeError -and $routes.Count -eq 0);package_initialization='not-run';manual_feeding='not-run';manual_depth='not-run';manual_hide_restore='not-run';manual_fullscreen='not-run';manual_exit='not-run';overall='pending'}
$record|ConvertTo-Json -Depth 8|Set-Content -LiteralPath $resultPath -Encoding UTF8
$exe=Join-Path $package 'app\Aquarium.Windows.exe'
$arguments="--feed --diagnostics `"$state`""
if($AutoOnly){$arguments+=' --probe-seconds 15'}
$app=Start-Process -FilePath $exe -ArgumentList $arguments -WorkingDirectory (Split-Path $exe -Parent) -PassThru
$deadline=[DateTime]::UtcNow.AddSeconds(10)
do {Start-Sleep -Milliseconds 200} while(-not(Test-Path $state) -and [DateTime]::UtcNow -lt $deadline -and -not $app.HasExited)
if(Test-Path $state){$s=Get-Content $state -Raw|ConvertFrom-Json;if($s.pid -eq $app.Id -and $s.alive -and $s.fish.Count -eq 5){$record.package_initialization='pass'}}
$record|ConvertTo-Json -Depth 8|Set-Content -LiteralPath $resultPath -Encoding UTF8
if(-not $AutoOnly){
    Write-Host 'Use the actual application. Pick up and shake the feeder; release and close it.'
    Write-Host 'Then try work-window layering, tray Hide/Show and an available fullscreen application.'
    Write-Host 'Answer pass, fail, or not-run for each observation. No answer is pre-filled.'
    foreach($name in @('manual_feeding','manual_depth','manual_hide_restore','manual_fullscreen')){
        $answer=(Read-Host $name).Trim().ToLowerInvariant()
        $record[$name]=if($answer -in @('pass','fail')){$answer}else{'not-run'}
    }
    Write-Host 'Exit the aquarium using its tray Exit, then press Enter.'
    [void](Read-Host)
    $app.Refresh();$record.manual_exit=if($app.HasExited -and $app.ExitCode -eq 0){'pass'}else{'not-run'}
}else{
    if($app.WaitForExit(20000)){$record.manual_exit='not-run';$record['timed_exit_code']=$app.ExitCode}
}
$allManual=@('manual_feeding','manual_depth','manual_hide_restore','manual_fullscreen','manual_exit')|Where-Object {$record[$_] -ne 'pass'}
$record.overall=if($record.package_initialization -eq 'pass' -and -not $dotnetOnPath -and $installedSdk.Count -eq 0 -and $record.network_unavailable_observed -and @($allManual).Count -eq 0){'pass'}else{'pending-or-failed'}
$record|ConvertTo-Json -Depth 8|Set-Content -LiteralPath $resultPath -Encoding UTF8
Write-Host "Evidence saved: $resultPath"
$record|ConvertTo-Json -Depth 8
