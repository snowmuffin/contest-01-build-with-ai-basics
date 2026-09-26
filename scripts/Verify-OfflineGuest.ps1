# G4-only runner for the disposable, network-disabled Windows Sandbox.

# Run by the prepared WSB LogonCommand; never use this on the host.

# Does not install an SDK, change networking/policies, or write manual acceptance answers.

$ErrorActionPreference = 'Stop'

$ProgressPreference = 'SilentlyContinue'

$inputRoot = 'C:\AquariumInput'

$outputRoot = 'C:\AquariumResults'

$work = 'C:\AquariumTest'

$receipt = Join-Path $outputRoot 'acceptance.json'

$record = [ordered]@{kind='G4 offline guest native verification';status='started';checks=@();environment=$null;phase='preflight';manual_acceptance='not-run';app_changed=$false;error=$null;started_utc=[DateTime]::UtcNow.ToString('o')}

function Save-Record {

    [IO.File]::WriteAllText($receipt,($record|ConvertTo-Json -Depth 14),[Text.UTF8Encoding]::new($false))

}

function Check([string]$name,[bool]$passed,$details=$null) {

    $record.checks += [ordered]@{name=$name;passed=$passed;details=$details}

    Save-Record

    if(-not $passed){throw ('Check failed: '+$name)}

}

function Snapshot-Environment {

    $sdkRoots=@((Join-Path $env:ProgramFiles 'dotnet\sdk'),(Join-Path ${env:ProgramFiles(x86)} 'dotnet\sdk'),(Join-Path $env:USERPROFILE '.dotnet\sdk'))

    $routes=@(Get-NetRoute -ErrorAction Stop|Where-Object {$_.DestinationPrefix -in @('0.0.0.0/0','::/0')}|Select-Object DestinationPrefix,InterfaceIndex)

    $addresses=@(Get-NetIPAddress -ErrorAction Stop|Where-Object {$_.IPAddress -notin @('127.0.0.1','::1')}|Select-Object IPAddress,InterfaceIndex)

    $nics=@(Get-CimInstance Win32_NetworkAdapter -Filter 'NetEnabled=true' -ErrorAction Stop)

    $os=Get-CimInstance Win32_OperatingSystem

    return [ordered]@{computer=$env:COMPUTERNAME;user=$env:USERNAME;os=$os.Caption;version=$os.Version;is64bit=[Environment]::Is64BitOperatingSystem;dotnet_on_path=[bool](Get-Command dotnet -ErrorAction SilentlyContinue);sdk_directories=@($sdkRoots|Where-Object {Test-Path $_});default_routes=$routes;non_loopback_addresses=$addresses;enabled_network_adapters=$nics.Count;python_on_path_before_test_driver=[bool](Get-Command python -ErrorAction SilentlyContinue);execution_policy=[string](Get-ExecutionPolicy)}

}

function Read-State([string]$path) {

    for($i=0;$i -lt 20;$i++){

        try{return (Get-Content -LiteralPath $path -Raw -Encoding UTF8|ConvertFrom-Json)}catch{Start-Sleep -Milliseconds 100}

    }

    throw ('No readable app diagnostic: '+$path)

}

function Run-Native([string]$label,[string]$script,[int]$expected) {

    $record.phase=$label;Save-Record

    $out=Join-Path $work ('artifacts\'+$label)

    [IO.Directory]::CreateDirectory($out)|Out-Null

    $env:AQUARIUM_TEST_OUTPUT=$out

    $env:AQUARIUM_TEST_EXE=$exe

    $env:AQUARIUM_TEST_SHORTCUT=$shortcut

    $env:PYTHONIOENCODING='utf-8'

    Start-Sleep -Seconds 4

    $stdout=Join-Path $out 'stdout.log'

    $stderr=Join-Path $out 'stderr.log'

    $exitPath=Join-Path $out 'exit-code.txt'

    $nativeScript=Join-Path $work ('scripts\'+$script)

    $runner=Join-Path $out 'run-native.cmd'

    $runnerText='@echo off'+[Environment]::NewLine+'"'+$python+'" -I "'+$nativeScript+'" 1>"'+$stdout+'" 2>"'+$stderr+'"'+[Environment]::NewLine+'echo %ERRORLEVEL%>"'+$exitPath+'"'+[Environment]::NewLine

    [IO.File]::WriteAllText($runner,$runnerText,[Text.Encoding]::ASCII)

    $proc=Start-Process -FilePath $env:ComSpec -ArgumentList @('/d','/c',$runner) -WorkingDirectory $work -PassThru

    if(-not $proc.WaitForExit(170000)){throw ('Bounded guest test did not complete: '+$label)}
    $proc.WaitForExit()
    Copy-Item -LiteralPath $out -Destination $outputRoot -Recurse
    $report=Get-Content (Join-Path $out 'report.json') -Raw -Encoding UTF8|ConvertFrom-Json
    $reportedExit=$null
    if($null -ne $report.auto_exit_code){$reportedExit=[int]$report.auto_exit_code}
    elseif($null -ne $report.exit_code){$reportedExit=[int]$report.exit_code}
    Check ($label+' reports a zero test exit code') ($reportedExit -eq 0) @{reported_exit_code=$reportedExit;report=($label+'/report.json')}
    Check ($label+' passes all '+$expected+' original native assertions') ($report.all_automated_checks_passed -and $report.checks.Count -eq $expected -and @($report.checks|Where-Object {-not $_.passed}).Count -eq 0) @{count=$report.checks.Count;report=($label+'/report.json');error=$report.error}

    $s=Read-State (Join-Path $out 'state.json')

    Check ($label+' leaves no resident process or captured input') (-not $s.alive -and -not $s.nativeCaptureOwned -and @(Get-Process Aquarium.Windows -ErrorAction SilentlyContinue).Count -eq 0) @{pid=$s.pid;final_event=$s.lastEvent;display=$s.display;transform=$s.transform}

}

if(-not (Test-Path (Join-Path $inputRoot 'kit.json')) -or -not (Test-Path $outputRoot)){throw 'Required disposable-guest mappings missing; no work performed.'}

if(Test-Path $receipt){throw 'Previous receipt exists; do not overwrite evidence.'}

$manifest=Get-Content (Join-Path $inputRoot 'kit.json') -Raw -Encoding UTF8|ConvertFrom-Json

if($env:COMPUTERNAME -eq $manifest.host_name -or $env:USERNAME -ne 'WDAGUtilityAccount'){throw 'This runner may only execute as the disposable Windows Sandbox user, never on the host.'}

Save-Record

try {

    $record['nonce']=$manifest.nonce

    $record.environment=Snapshot-Environment;Save-Record

    Check 'guest is Windows 11 x64' ($record.environment.is64bit -and $record.environment.os -like '*Windows 11*') $record.environment.version

    Check 'no .NET SDK or global dotnet available before execution' (-not $record.environment.dotnet_on_path -and $record.environment.sdk_directories.Count -eq 0)

    Check 'guest has no default routes, non-loopback addresses or enabled network adapter' ($record.environment.default_routes.Count -eq 0 -and $record.environment.non_loopback_addresses.Count -eq 0 -and $record.environment.enabled_network_adapters -eq 0)

    Check 'clean working directory and no prior aquarium' (-not (Test-Path $work) -and @(Get-Process Aquarium.Windows -ErrorAction SilentlyContinue).Count -eq 0)

    foreach($entry in $manifest.files.PSObject.Properties){

        $path=[IO.Path]::GetFullPath((Join-Path $inputRoot $entry.Name))

        if(-not $path.StartsWith($inputRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Unsafe input manifest path'}

        if((Get-Item $path).Length -ne $entry.Value.bytes -or (Get-FileHash $path -Algorithm SHA256).Hash -ine $entry.Value.sha256){throw ('Input hash mismatch: '+$entry.Name)}

    }

    Check 'read-only input files match host manifest hashes' $true $manifest.files.PSObject.Properties.Name

    [IO.Directory]::CreateDirectory($work)|Out-Null

    [IO.Directory]::CreateDirectory((Join-Path $work 'scripts'))|Out-Null

    Add-Type -AssemblyName System.IO.Compression.FileSystem

    [IO.Compression.ZipFile]::ExtractToDirectory((Join-Path $inputRoot 'DesktopAquarium-win-x64.zip'),(Join-Path $work 'package'))

    $package=Join-Path $work 'package\DesktopAquarium'

    $exe=Join-Path $package 'app\Aquarium.Windows.exe'

    $inventory=Get-Content (Join-Path $package 'FILES.json') -Raw -Encoding UTF8|ConvertFrom-Json

    foreach($item in $inventory){

        $path=[IO.Path]::GetFullPath((Join-Path $package $item.path))

        if(-not $path.StartsWith($package+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Unsafe package path'}

        if((Get-Item $path).Length -ne $item.bytes -or (Get-FileHash $path -Algorithm SHA256).Hash -ine $item.sha256){throw ('Package payload mismatch: '+$item.path)}

    }

    $record['package_build']=Get-Content (Join-Path $package 'BUILD.json') -Raw -Encoding UTF8|ConvertFrom-Json

    Check 'all extracted application payload hashes match' ($inventory.Count -eq 489) $inventory.Count

    $record.phase='startup-before-python-extraction';Save-Record

    $state=Join-Path $work 'startup-state.json'

    $startup=Start-Process -FilePath $exe -ArgumentList ('--feed --diagnostics "'+$state+'" --probe-seconds 25') -WorkingDirectory (Split-Path $exe -Parent) -PassThru

    $deadline=[DateTime]::UtcNow.AddSeconds(18)

    $s=$null

    do{

        Start-Sleep -Milliseconds 200

        $startup.Refresh()

        if(Test-Path $state){

            try{

                $candidate=Get-Content $state -Raw -Encoding UTF8|ConvertFrom-Json

                if($candidate.pid -eq $startup.Id -and $candidate.alive -and @($candidate.fish).Count -eq 5 -and $candidate.foodImplemented){

                    $s=$candidate

                    break

                }

            } catch {}

        }

    }while(-not $startup.HasExited -and [DateTime]::UtcNow -lt $deadline)

    Check 'unmodified package initializes five fish without SDK or Python' ($null -ne $s) @{start_pid=$startup.Id;state_pid=if($s){$s.pid}else{$null};alive=if($s){$s.alive}else{$null};fish_count=if($s){@($s.fish).Count}else{$null};food_implemented=if($s){$s.foodImplemented}else{$null};display=if($s){$s.display}else{$null};transform=if($s){$s.transform}else{$null}}

    $startup.Refresh()

    $modules=@($startup.Modules|Where-Object {$_.ModuleName -in @('hostfxr.dll','hostpolicy.dll','coreclr.dll')}|ForEach-Object {@{name=$_.ModuleName;path=$_.FileName;version=$_.FileVersionInfo.ProductVersion}})

    Check 'all three .NET loader/runtime modules are package-local' ($modules.Count -eq 3 -and @($modules|Where-Object {-not $_.path.StartsWith((Join-Path $package 'app')+'\',[StringComparison]::OrdinalIgnoreCase)}).Count -eq 0) $modules

    if(-not $startup.WaitForExit(30000)){throw 'Bounded startup probe did not exit'}

    $startup.Refresh();Check 'bounded startup probe exits normally' ($startup.ExitCode -eq 0)

    Copy-Item -LiteralPath $state -Destination (Join-Path $outputRoot 'startup-state.json')

    # Only now add a local test driver; the product already started without it.

    [IO.Compression.ZipFile]::ExtractToDirectory((Join-Path $inputRoot 'python-embed.zip'),(Join-Path $work 'python'))

    $python=Join-Path $work 'python\python.exe'

    foreach($name in @('Verify-FeedingNative.py','Verify-G3Native.py','Create-FeederShortcut.ps1')){Copy-Item -LiteralPath (Join-Path $inputRoot $name) -Destination (Join-Path $work 'scripts')}

    $record['python_test_driver']=$manifest.python_test_driver

    $shortcuts=Join-Path $work 'shortcuts';[IO.Directory]::CreateDirectory($shortcuts)|Out-Null

    & (Join-Path $work 'scripts\Create-FeederShortcut.ps1') -ExePath $exe -DestinationDirectory $shortcuts

    $shortcut=Join-Path $shortcuts 'Feed Fish.lnk'

    Run-Native 'feeding' 'Verify-FeedingNative.py' 18

    Run-Native 'lifecycle' 'Verify-G3Native.py' 25

    $after=Snapshot-Environment;$record['environment_after']=$after

    Check 'guest remains SDK-free and offline after native tests' (-not $after.dotnet_on_path -and $after.sdk_directories.Count -eq 0 -and $after.default_routes.Count -eq 0 -and $after.non_loopback_addresses.Count -eq 0 -and $after.enabled_network_adapters -eq 0)

    foreach($item in $inventory){

        $path=Join-Path $package $item.path

        if((Get-Item $path).Length -ne $item.bytes -or (Get-FileHash $path -Algorithm SHA256).Hash -ine $item.sha256){throw ('App payload changed during tests: '+$item.path)}

    }

    Check 'application payload remains unchanged after all tests' $true

    $record.status='passed';$record.phase='complete'

} catch {

    $record.status='failed-or-blocked';$record.error=$_.Exception.Message;$record['error_position']=$_.InvocationInfo.PositionMessage

} finally {

    $record['finished_utc']=[DateTime]::UtcNow.ToString('o');Save-Record

    if(Test-Path (Join-Path $work 'artifacts')){Copy-Item -LiteralPath (Join-Path $work 'artifacts') -Destination (Join-Path $outputRoot 'guest-artifacts') -Recurse -ErrorAction Continue}

    Write-Output ($record|ConvertTo-Json -Depth 14)

}

if($record.status -eq 'passed'){exit 0}else{exit 1}
