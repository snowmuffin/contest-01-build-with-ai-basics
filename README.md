# Desktop Aquarium — G0 integration probe

**Not the finished aquarium.** This first runnable slice draws three labelled temporary pixel markers (REAR / MIDDLE / FRONT) and a draggable feeder. It does not dispense food or simulate fish yet.

## Run on Windows 11 x64

From the repository root with the approved .NET 10 SDK:

```powershell
dotnet restore Aquarium.slnx
dotnet build Aquarium.slnx -c Release
dotnet test tests/Aquarium.Core.Tests/Aquarium.Core.Tests.csproj -c Release
dotnet run --project src/Aquarium.Windows/Aquarium.Windows.csproj -c Release -- --feed
```

Drag the feeder body, release to put it down, and use its X to close only the tool. The notification-area icon offers Open feeder, Hide, Show again and Exit. Fullscreen work is intended to suppress the probe automatically. No application startup registration or system cursor scheme is changed. All three markers are placeholders, not fish artwork.

The habitat targets the primary display. Move two normal opaque windows across the labelled markers to inspect clipping; click/scroll through them to check ordinary input. The FRONT marker stays over ordinary windows; MIDDLE is masked by the foremost work window; REAR is masked by all work windows. Maximize is distinct from fullscreen. Transparency/rounded boundaries are an approximation.

## Optional local diagnostics

```powershell
dotnet run --project src/Aquarium.Windows/Aquarium.Windows.csproj -c Release -- --feed --diagnostics artifacts/g0/state.json
```

The opt-in report is overwritten, not appended. It records only the probe's own window handles/state, counts, display geometry and flags; it contains no foreign window titles, document text or keystrokes. It is not telemetry and is excluded from Git. `--probe-seconds 10` closes a controlled test run automatically.

See `docs/verification.md` for actual results versus pending manual checks. Canonical plans are under `devpost/`; generated HTML and the personal learner profile are local-only. No public release or broad compatibility claim exists yet.
