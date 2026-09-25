@echo off
setlocal
rem Run locally by the user. Creates only this application's Feed Fish.lnk.
rem Does not change PowerShell execution policy or register an automatic startup task.
set "AQUARIUM_EXE=%~dp0..\src\Aquarium.Windows\bin\Release\net10.0-windows\Aquarium.Windows.exe"
if not exist "%AQUARIUM_EXE%" (
  echo The Release build was not found. Run Start-Aquarium.cmd first.
  pause
  exit /b 1
)
powershell.exe -NoLogo -NoProfile -File "%~dp0Create-FeederShortcut.ps1" -ExePath "%AQUARIUM_EXE%"
if errorlevel 1 (
  echo.
  echo Shortcut setup did not finish. No security policy was changed.
  echo Keep the error above for diagnosis; do not disable system protection.
  pause
  exit /b 1
)
echo.
echo Feed Fish is ready on your Desktop.
echo Double-click it, hold and shake the feeder, then release to put it down.
pause
exit /b 0
