[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$PackageDirectory,[Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$package=(Resolve-Path -LiteralPath $PackageDirectory).Path
$artifacts=[IO.Path]::GetFullPath((Join-Path $root 'artifacts'))
$output=[IO.Path]::GetFullPath($OutputDirectory)
if(-not $output.StartsWith($artifacts+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Kit must be a new directory under project artifacts.'}
if(Test-Path -LiteralPath $output){throw 'Refusing to overwrite an existing clean-room kit.'}
if(-not(Test-Path (Join-Path $package 'app\Aquarium.Windows.exe'))){throw 'Expected an extracted candidate package.'}
[IO.Directory]::CreateDirectory($output)|Out-Null
$kit=Join-Path $output 'kit';$results=Join-Path $output 'results'
[IO.Directory]::CreateDirectory($kit)|Out-Null;[IO.Directory]::CreateDirectory($results)|Out-Null
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'Run-OfflineAcceptance.ps1') -Destination $kit
# Only package+kit are exposed read-only. The new empty results folder is the only writable host mapping.
$xml=[xml]'<Configuration><Networking>Disable</Networking><vGPU>Disable</vGPU><AudioInput>Disable</AudioInput><VideoInput>Disable</VideoInput><PrinterRedirection>Disable</PrinterRedirection><ClipboardRedirection>Disable</ClipboardRedirection><MemoryInMB>4096</MemoryInMB><MappedFolders/><LogonCommand><Command>powershell.exe -NoLogo -NoProfile -NoExit -File C:\AquariumKit\Run-OfflineAcceptance.ps1 -PackageDirectory C:\AquariumPackage -ResultsDirectory C:\AquariumResults</Command></LogonCommand></Configuration>'
foreach($mapping in @(@($package,'C:\AquariumPackage','true'),@($kit,'C:\AquariumKit','true'),@($results,'C:\AquariumResults','false'))){
    $node=$xml.CreateElement('MappedFolder')
    foreach($pair in @(@('HostFolder',$mapping[0]),@('SandboxFolder',$mapping[1]),@('ReadOnly',$mapping[2]))){$entry=$xml.CreateElement($pair[0]);$entry.InnerText=$pair[1];[void]$node.AppendChild($entry)}
    [void]$xml.SelectSingleNode('/Configuration/MappedFolders').AppendChild($node)
}
$config=Join-Path $output 'Offline-Aquarium.wsb';$xml.Save($config)
$available=Test-Path (Join-Path $env:WINDIR 'System32\WindowsSandbox.exe')
$record=[ordered]@{configuration=$config;networking='Disable';vGPU='Disable';package_read_only=$true;kit_read_only=$true;results_directory=$results;sandbox_executable_found=$available;executed=$false;note='Disabled vGPU is for a conservative functional check, not representative performance. No Windows feature or host network setting is changed.'}
$record|ConvertTo-Json -Depth 4|Set-Content (Join-Path $output 'kit.json') -Encoding UTF8
[IO.File]::WriteAllText((Join-Path $output 'README.txt'),@'
This kit has NOT run merely because this file exists.
On a Windows machine with Windows Sandbox already available, regenerate this kit for
that machine's absolute paths and open Offline-Aquarium.wsb. It disables the guest
network, audio/video/printer/clipboard redirection and virtual GPU. It does not change
your host network or security policy. Only the dedicated results folder is writable.
The script checks package hashes, SDK/default-route state, initialization and records
YOUR actual use results. Blank/skipped checks remain not-run. A separate local-console
check is still needed; software-rendered Sandbox performance is not a physical GPU test.
Do not weaken system protections to run the kit. Feature enablement/reboot needs separate
owner approval and is deliberately not automated here.
'@,[Text.UTF8Encoding]::new($false))
$record|ConvertTo-Json -Depth 4
