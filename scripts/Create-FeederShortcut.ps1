[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ExePath,
    [string]$DestinationDirectory = [Environment]::GetFolderPath([Environment+SpecialFolder]::DesktopDirectory)
)
$ErrorActionPreference = 'Stop'
$exe = (Resolve-Path -LiteralPath $ExePath -ErrorAction Stop).Path
if ([IO.Path]::GetExtension($exe) -ine '.exe') { throw 'ExePath must name an existing executable.' }
$directory = (Resolve-Path -LiteralPath $DestinationDirectory -ErrorAction Stop).Path
if (-not [IO.Directory]::Exists($directory)) { throw 'DestinationDirectory must be an existing folder.' }
$destination = Join-Path $directory 'Feed Fish.lnk'
$shell = New-Object -ComObject WScript.Shell
$shortcut = $null
try {
    $shortcut = $shell.CreateShortcut($destination)
    if (Test-Path -LiteralPath $destination) {
        if ($shortcut.TargetPath -ine $exe -or $shortcut.Arguments -ne '--feed') {
            throw "Refusing to overwrite an unrelated shortcut: $destination"
        }
        Write-Output "Reusing existing app-owned shortcut: $destination"
    } else {
        $shortcut.TargetPath = $exe
        $shortcut.Arguments = '--feed'
        $shortcut.WorkingDirectory = [IO.Path]::GetDirectoryName($exe)
        $icon = Join-Path $shortcut.WorkingDirectory 'Assets\feeder.ico'
        if (-not (Test-Path -LiteralPath $icon)) { throw 'Bundled feeder.ico is missing. Build the complete app first.' }
        $shortcut.IconLocation = "$icon,0"
        $shortcut.Description = 'Open the local Desktop Aquarium feeder. Prototype build.'
        $shortcut.Save()
        Write-Output "Created app-owned shortcut: $destination"
    }
} finally {
    if ($null -ne $shortcut) { [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($shortcut) }
    if ($null -ne $shell) { [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($shell) }
}
