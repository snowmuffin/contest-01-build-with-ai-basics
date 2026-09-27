# Desktop Aquarium - feeding prototype

Working project label, not final competition submission copy. The real Windows prototype now renders five original pixel fish and accepts held mouse shaking to release food. Fish approach and visibly consume food. G0 markers are available only via the explicit `--g0` test flag.

Current status (2026-09-27): G0–G4 and the initial package learner check are complete; Final Review is open. The participant inspected and approved the 32 independently extracted fish PNGs. The app now uses their variable-rectangle atlas/metadata and preserves sprite aspect ratios, replacing fixed 80x48 cropping. Source regions/masks remain available in `assets/fish/`; `docs/fish-runtime-verification.md` records integration evidence. Movement, feeding, depth and occlusion logic are unchanged.

## Run

```powershell
dotnet restore Aquarium.slnx --locked-mode
dotnet build Aquarium.slnx -c Release
dotnet test tests/Aquarium.Core.Tests/Aquarium.Core.Tests.csproj -c Release
dotnet run --project src/Aquarium.Windows/Aquarium.Windows.csproj -c Release -- --feed
```

Or double-click `scripts/Start-Aquarium.cmd`. The source launcher requires a development .NET 10 SDK. A separate self-contained candidate is now available for verification as described below. The target is Windows 11 x64 on the primary display; current native test evidence is specifically an RDP session, not general compatibility certification.

Pick up the feeder body, shake left/right while holding, and release to put it down. Ordinary cursor movement never dispenses food. X closes only the feeder. The tray provides Open feeder / Hide / Show again / Exit. Fullscreen protection and manual Hide are distinct. No registration at login, background service, account, model download or external runtime API is added.

## App-owned launcher

On a new local setup, double-click `scripts/Setup-FeederShortcut.cmd`, or run `scripts/Create-FeederShortcut.ps1 -ExePath <absolute-path-to-Aquarium.Windows.exe>`. The installer creates only `Feed Fish.lnk`, refuses unrelated shortcut collisions and does not change security policy or login startup settings.

The current development machine's Desktop grant is now active and its real `Feed Fish.lnk` has been installed. Two launches through that actual Desktop shortcut reused the same resident and visible resting feeder. The link targets the current Release build folder; this is development installation evidence, not a self-contained release. See `docs/feeding-verification.md` for the receipt and remaining coverage.

## Test evidence

`docs/g3-verification.md` records lifecycle/guard verification, actual isolated-profile Edge F11, repeated activation and bounded malformed-client handling. Other sessions/displays/games remain untested.

`docs/feeding-verification.md` separates tests executed from unrun work. The G0 fixture runner uses `--g0`; the feeding fixture runner uses the actual world and targets only its own native windows and the feeder. Both require an idle interactive test desktop. Native fixture success does not replace user feedback.

Optional local diagnostic state can be enabled using `--diagnostics artifacts/feeding/state.json`; it is an overwritten local report, never telemetry. `--probe-seconds 45` is a bounded test-run exit, not a feeding animation.

Canonical plans are in `devpost/`; generated HTML and the learner profile are local-only. No public release, final license selection or broad performance claim has been made.

## Verified G4 package checkpoint (Final Review still open)

Build with `scripts/Publish-Windows.ps1 -RuntimeVersion 10.0.12`; output must be a new folder under `artifacts/`. This wrapper keeps platform-specific publish restore separate from the normal source lockfiles. Verify normal `dotnet restore Aquarium.slnx --locked-mode` after packaging.

Latest artwork candidate: `artifacts/fish-runtime/package-01/DesktopAquarium-win-x64.zip`. This includes the approved sprites and replaces fixed-cell lookup. Its current evidence and remaining clean-room/final user review are in `docs/fish-runtime-verification.md`. The earlier G4 ZIP at `artifacts/g4-only-20260926/package-02/DesktopAquarium-win-x64.zip` remains an archived, separately verified checkpoint.
Extract the **whole** folder and run its `Start-Aquarium.cmd` or `app/Aquarium.Windows.exe`.
Close an already-running development aquarium using its tray Exit first, otherwise single-instance forwarding intentionally reuses that existing process. The current Desktop shortcut still targets the development Release folder, not this package. No automatic migration of that shortcut is performed.

`docs/g4-verification.md` records hashes, packaged tests, loaded runtime paths and resource samples. This G4 checkpoint passed separate SDK-free/offline Sandbox verification and its actual-package learner check. Final Review and subsequent artwork acceptance are separate and remain open; the package does not contain the new extraction candidates. Matching upstream runtime/WPF/WinForms notice files are bundled with provenance; the project owner's source/publication license decision remains pending.

Test-only environment overrides `AQUARIUM_TEST_EXE`, `AQUARIUM_TEST_OUTPUT` and (feeding harness) `AQUARIUM_TEST_SHORTCUT` select a project-local candidate for `Verify-FeedingNative.py`/`Verify-G3Native.py`. They do not alter the product's runtime behavior. `Verify-PackagedStartup.ps1 -PackageDirectory <extracted-folder>` performs a bounded own-process runtime-module check. Native scripts require an idle authorized interactive desktop.

Current preparation and owner-only items: `docs/submission-readiness.md`. Native/browser/startup checks and a local rehearsal are recorded in `docs/rdp-candidate-verification.md`. The rehearsal is not a final uploaded demo. Current final artwork/package review remains distinct from completed G4 evidence.

## Latest G4 validation

A full finite ordinary/feeding/hidden measurement (60 seconds each) now passed, with safe restoration and normal exit. See `docs/g4-verification.md` for CPU/memory/callback results and the absence of usable per-process GPU counter values. Reproduce the optional GPU observation with `scripts/Measure-GpuProcess.ps1` against the measurement run directory; this remains a test-only tool.

G4's separate SDK-free/offline run and learner check completed; earlier unavailable-Sandbox notes describe historical checkpoints. The approved sprites are now integrated into source and a fresh package candidate. The old clean-room pass is not transferred to the new package, and final user review/submission remain pending.
