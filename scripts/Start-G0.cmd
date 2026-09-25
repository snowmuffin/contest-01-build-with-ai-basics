@echo off
cd /d "%~dp0.."
dotnet run --project src\Aquarium.Windows\Aquarium.Windows.csproj -c Release -- --g0 --feed
if errorlevel 1 pause
