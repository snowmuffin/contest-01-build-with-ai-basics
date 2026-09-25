@echo off
cd /d "%~dp0.."
dotnet run --project src\Aquarium.Windows\Aquarium.Windows.csproj -c Release -- --feed
if errorlevel 1 pause
