[CmdletBinding()]
param(
    # Pinned candidate version, rechecked against live official metadata on 2026-09-26.
    # Recheck servicing before public distribution; this does not update the machine's SDK/runtime.
    [ValidatePattern('^10\.0\.\d+$')][string]$RuntimeVersion = '10.0.12',
    [string]$OutputDirectory
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$artifactRoot = [IO.Path]::GetFullPath((Join-Path $root 'artifacts'))
if (-not $OutputDirectory) {
    $OutputDirectory = Join-Path $artifactRoot ('packages\candidate-' + [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss'))
}
$output = [IO.Path]::GetFullPath($OutputDirectory)
if (-not $output.StartsWith($artifactRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'OutputDirectory must be a new directory under this repository artifacts folder.'
}
if (Test-Path -LiteralPath $output) { throw 'Refusing to overwrite an existing package directory.' }
$package = Join-Path $output 'DesktopAquarium'
$app = Join-Path $package 'app'
[IO.Directory]::CreateDirectory($app) | Out-Null
Push-Location $root
try {
    $revision = (& git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Cannot identify source checkpoint.' }
    # RID-specific publish must not rewrite the normal source restore lockfiles.
    $sourceLockFiles = @('src/Aquarium.Core/packages.lock.json','src/Aquarium.Windows/packages.lock.json')
    $lockHashes = @{}
    foreach ($path in $sourceLockFiles) { $lockHashes[$path] = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash }
    $publishLockPath = Join-Path $output 'unused-publish.lock.json'
    & dotnet publish src/Aquarium.Windows/Aquarium.Windows.csproj -c Release -r win-x64 --self-contained true `
        -p:PublishSingleFile=false -p:PublishTrimmed=false "-p:RuntimeFrameworkVersion=$RuntimeVersion" `
        -p:RestorePackagesWithLockFile=false -p:RestoreLockedMode=false "-p:NuGetLockFilePath=$publishLockPath" -o $app
    if ($LASTEXITCODE -ne 0) { throw 'Self-contained publish failed; partial output remains for inspection.' }
    foreach ($path in $sourceLockFiles) {
        if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash -ne $lockHashes[$path]) {
            throw "Publish unexpectedly changed a source lockfile: $path. Inspect before proceeding."
        }
    }

    foreach ($name in @('Aquarium.Windows.exe','Aquarium.Windows.runtimeconfig.json','hostfxr.dll','hostpolicy.dll','coreclr.dll','PresentationFramework.dll','Assets\feeder.ico')) {
        if (-not (Test-Path -LiteralPath (Join-Path $app $name))) { throw "Missing required packaged file: $name" }
    }
    $runtime = Get-Content (Join-Path $app 'Aquarium.Windows.runtimeconfig.json') -Raw | ConvertFrom-Json
    if (-not $runtime.runtimeOptions.includedFrameworks -or $runtime.runtimeOptions.frameworks) { throw 'Publish is not a verified self-contained runtime layout.' }
    [IO.Directory]::CreateDirectory((Join-Path $package 'scripts')) | Out-Null
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'Create-FeederShortcut.ps1') -Destination (Join-Path $package 'scripts')
    Copy-Item -LiteralPath (Join-Path $root 'THIRD_PARTY_NOTICES.md') -Destination $package
    $noticeSource = Join-Path $root ("notices\dotnet-" + $RuntimeVersion)
    if (-not (Test-Path (Join-Path $noticeSource 'provenance.json'))) { throw 'Matching runtime notices are missing. Run Collect-RuntimeNotices.py before packaging.' }
    $provenance = Get-Content (Join-Path $noticeSource 'provenance.json') -Raw | ConvertFrom-Json
    if ($provenance.runtime_version -ne $RuntimeVersion) { throw 'Notice version does not match package runtime.' }
    [IO.Directory]::CreateDirectory((Join-Path $package 'notices')) | Out-Null
    Copy-Item -LiteralPath $noticeSource -Destination (Join-Path $package 'notices') -Recurse
    foreach($record in $provenance.archives) {
        foreach($notice in $record.notices) {
            $sourceNotice = Join-Path $root $notice.path
            if((Get-FileHash $sourceNotice -Algorithm SHA256).Hash -ine $notice.sha256) { throw 'Notice content differs from the verified distribution.' }
        }
    }

    $start = '@echo off' + "`r`n" + 'start "" "%~dp0app\Aquarium.Windows.exe" --feed' + "`r`n"
    [IO.File]::WriteAllText((Join-Path $package 'Start-Aquarium.cmd'), $start, [Text.Encoding]::ASCII)
    $setup = @'
@echo off
powershell.exe -NoLogo -NoProfile -File "%~dp0scripts\Create-FeederShortcut.ps1" -ExePath "%~dp0app\Aquarium.Windows.exe"
if errorlevel 1 (
  echo Setup did not finish. Existing unrelated shortcuts and security settings were not changed.
  pause
  exit /b 1
)
echo Feed Fish is ready. Existing development shortcuts are never silently overwritten.
pause
'@
    [IO.File]::WriteAllText((Join-Path $package 'Setup-FeederShortcut.cmd'), ($setup -replace "`r?`n", "`r`n"), [Text.Encoding]::ASCII)
    $readme = @'
Desktop Aquarium - local validation candidate, not a public release

Extract the entire ZIP into a stable folder, then run Start-Aquarium.cmd or
app\Aquarium.Windows.exe. Keep all bundled DLLs and Assets together.

Open the feeder, hold its body and shake left/right, then release to put it down.
X closes only the feeder. The notification-area icon provides Hide, Show again,
Open feeder and Exit. The intended first target is Windows 11 x64, primary monitor.

Setup-FeederShortcut.cmd optionally creates Feed Fish on the current user's Desktop.
An existing shortcut pointing to a different executable is NOT overwritten. In
particular, a development shortcut must be deliberately replaced by its owner
before setting up this packaged copy. The package does not change startup, security
policy, or system cursor settings. Do not disable SmartScreen or antivirus to run it.

The runtime is bundled. No account, model download or external service is required
by the application. A real no-SDK/offline clean-machine run and final user review
remain required before release claims. RDP tests do not certify other configurations.
See BUILD.json for the source checkpoint/runtime and notices/ for bundled dependency notices. Source license and final public
submission materials are still being reviewed; no public publishing is performed.
'@
    [IO.File]::WriteAllText((Join-Path $package 'README.txt'), $readme, [Text.UTF8Encoding]::new($false))
    $metadata = [ordered]@{
        stage='G4 local candidate; clean environment and final review pending'
        source_commit=$revision
        runtime_version=$RuntimeVersion
        included_frameworks=$runtime.runtimeOptions.includedFrameworks
        runtime_metadata_source='https://builds.dotnet.microsoft.com/dotnet/release-metadata/10.0/releases.json'
        metadata_release_date_observed=$provenance.release_date
        source_worktree_dirty=[bool](& git status --porcelain --untracked-files=no)
        source_inputs=@(Get-ChildItem src -Recurse -File | Where-Object { $_.FullName -notmatch '\\(bin|obj)\\' } | Sort-Object FullName | ForEach-Object { [ordered]@{path=$_.FullName.Substring($root.Length+1).Replace('\','/');sha256=(Get-FileHash $_.FullName -Algorithm SHA256).Hash} })
        architecture='win-x64'
        self_contained=$true
        trimmed=$false
        public_release=$false
    }
    $metadata | ConvertTo-Json -Depth 8 | Set-Content (Join-Path $package 'BUILD.json') -Encoding UTF8
    $inventory = @(Get-ChildItem -LiteralPath $package -Recurse -File | Sort-Object FullName | ForEach-Object {
        [ordered]@{path=$_.FullName.Substring($package.Length+1).Replace('\','/');bytes=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash}
    })
    $inventory | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $package 'FILES.json') -Encoding UTF8
    $zip = Join-Path $output 'DesktopAquarium-win-x64.zip'
    Compress-Archive -Path $package -DestinationPath $zip -CompressionLevel Optimal
    $receipt = [ordered]@{package_directory=$package;zip=$zip;zip_bytes=(Get-Item $zip).Length;sha256=(Get-FileHash $zip -Algorithm SHA256).Hash;runtime=$RuntimeVersion;source_commit=$revision;clean_machine_tested=$false;offline_tested=$false}
    $receipt | ConvertTo-Json | Set-Content (Join-Path $output 'package-receipt.json') -Encoding UTF8
    $receipt | ConvertTo-Json
} finally { Pop-Location }
