[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$PackageDirectory)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$package=(Resolve-Path -LiteralPath $PackageDirectory).Path
$exe=Join-Path $package 'app\Aquarium.Windows.exe'
if (-not (Test-Path $exe)) { throw 'Expected package/app/Aquarium.Windows.exe.' }
if (@(Get-Process Aquarium.Windows -ErrorAction SilentlyContinue).Count) { throw 'Close the running aquarium using tray Exit before the isolated package smoke test.' }
$out=Join-Path $root 'artifacts\g4\startup'
[IO.Directory]::CreateDirectory($out)|Out-Null
$state=Join-Path $out 'state.json'
if (Test-Path $state) { Remove-Item -LiteralPath $state }
$info=[Diagnostics.ProcessStartInfo]::new()
$info.FileName=$exe
$info.Arguments="--feed --diagnostics `"$state`" --probe-seconds 10"
$info.WorkingDirectory=Join-Path $package 'app'
$info.UseShellExecute=$false
$missing=Join-Path $out 'no-dotnet-here'
$info.EnvironmentVariables['DOTNET_ROOT']=$missing
$info.EnvironmentVariables['DOTNET_ROOT_X64']=$missing
$info.EnvironmentVariables['PATH']=Join-Path $env:WINDIR 'System32'
$info.EnvironmentVariables['DOTNET_HOST_TRACE']='1'
$info.EnvironmentVariables['DOTNET_HOST_TRACEFILE']=Join-Path $out 'host-trace.log'
$app=[Diagnostics.Process]::Start($info)
try {
    $deadline=[DateTime]::UtcNow.AddSeconds(6)
    do { Start-Sleep -Milliseconds 150 } while (-not (Test-Path $state) -and [DateTime]::UtcNow -lt $deadline)
    if (-not (Test-Path $state)) { throw 'No package startup state.' }
    Start-Sleep -Milliseconds 600
    $s=Get-Content $state -Raw -Encoding UTF8|ConvertFrom-Json
    $app.Refresh()
    $modules=@($app.Modules|Where-Object {$_.ModuleName -in @('hostfxr.dll','hostpolicy.dll','coreclr.dll')}|ForEach-Object {[ordered]@{name=$_.ModuleName;path=$_.FileName;version=$_.FileVersionInfo.ProductVersion}})
    if ($modules.Count -ne 3) { throw 'Required host/runtime modules were not observed.' }
    $runtimeDirectory=Join-Path $package 'app'
    foreach($module in $modules) { if(-not $module.path.StartsWith($runtimeDirectory+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'The process used a runtime module outside its package.'} }
    if(-not $s.alive -or -not $s.foodImplemented -or $s.fish.Count -ne 5){throw 'Packaged world did not initialize.'}
    $result=[ordered]@{passed=$true;package=$package;bundled_runtime_modules=$modules;package_process=$app.Id;dotnet_roots_intentionally_missing=$true;path_excludes_sdk=$true;host_still_has_sdk_installed=$true;real_clean_machine_tested=$false;offline_network_tested=$false;machine_environment_changed=$false}
} finally {
    if(-not $app.WaitForExit(15000)){throw 'Packaged process did not exit within the bounded smoke test.'}
}
if($app.ExitCode -ne 0){throw 'Packaged smoke test exit was nonzero.'}
$result['exit_code']=$app.ExitCode
$result|ConvertTo-Json -Depth 8|Set-Content (Join-Path $out 'report.json') -Encoding UTF8
$result|ConvertTo-Json -Depth 8
