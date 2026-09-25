[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$out = Join-Path $root 'artifacts\g3\protocol'
[IO.Directory]::CreateDirectory($out) | Out-Null
$exe = Join-Path $root 'src\Aquarium.Windows\bin\Release\net10.0-windows\Aquarium.Windows.exe'
$existing = @(Get-Process Aquarium.Windows -ErrorAction SilentlyContinue | Where-Object { $_.Path -ieq $exe })
if ($existing.Count) { throw 'Close the current aquarium with its tray Exit before this isolated instance test.' }
$state = Join-Path $out 'state.json'
if (Test-Path $state) { Remove-Item -LiteralPath $state }
$app = Start-Process $exe -ArgumentList @('--feed','--diagnostics',$state,'--probe-seconds','18') -WorkingDirectory $root -PassThru
$checks = @()
try {
    $deadline = [DateTime]::UtcNow.AddSeconds(6)
    do { Start-Sleep -Milliseconds 100 } while (-not (Test-Path $state) -and [DateTime]::UtcNow -lt $deadline)
    if (-not (Test-Path $state)) { throw 'No isolated application receipt.' }
    $sid = [Security.Principal.WindowsIdentity]::GetCurrent().User.Value
    $sha = [Security.Cryptography.SHA256]::Create()
    try { $hash = -join ($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($sid)) | ForEach-Object { $_.ToString('X2') }) }
    finally { $sha.Dispose() }
    $session = (Get-Process -Id $app.Id).SessionId
    $pipeName = "AquariumG0-$($hash.Substring(0,16))-$session"
    foreach ($payload in @("junk-v1`n",'fee')) {
        $pipe = [IO.Pipes.NamedPipeClientStream]::new('.', $pipeName, [IO.Pipes.PipeDirection]::InOut, [IO.Pipes.PipeOptions]::Asynchronous)
        try {
            $pipe.Connect(3000)
            $bytes = [Text.Encoding]::ASCII.GetBytes($payload)
            $pipe.Write($bytes,0,$bytes.Length)
            $response = New-Object byte[] 1
            $read = $pipe.ReadAsync($response,0,1)
            if (-not $read.Wait(3500)) { throw 'Malformed-client deadline was not bounded.' }
            if ($read.Result -ne 0) { throw 'Unexpected acknowledgement for malformed command.' }
            $checks += [ordered]@{name=($(if ($payload.Length -eq 8) {'unknown command rejected'} else {'truncated client timed out'}));passed=$true}
        } finally { $pipe.Dispose() }
        $forwarder = Start-Process $exe -ArgumentList '--feed' -PassThru -WorkingDirectory $root
        if (-not $forwarder.WaitForExit(6000) -or $forwarder.ExitCode -ne 0) { throw 'Valid launcher failed after malformed client.' }
    }
    $receipt = Get-Content $state -Raw -Encoding UTF8 | ConvertFrom-Json
    $checks += [ordered]@{name='valid launcher works after both malformed clients';passed=($receipt.pid -eq $app.Id -and $receipt.alive)}
    if (@($checks | Where-Object {-not $_.passed}).Count) { throw 'Protocol check failed.' }
    [ordered]@{passed=$true;checks=$checks;server_pid=$app.Id;raw_sid_logged=$false} | ConvertTo-Json -Depth 6 | Set-Content (Join-Path $out 'report.json') -Encoding UTF8
    Get-Content (Join-Path $out 'report.json') -Raw -Encoding UTF8
} finally {
    if (-not $app.WaitForExit(22000)) { throw 'Isolated application did not honor its timed exit.' }
}
