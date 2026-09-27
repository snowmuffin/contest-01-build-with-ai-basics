# Desktop Aquarium - feeding prototype

The real Windows prototype renders five original pixel fish and accepts held mouse shaking to release food. Fish approach and visibly consume food. G0 markers are available only via the explicit `--g0` test flag.

## Download and try

[Windows x64 portable release — v0.1.0](https://github.com/snowmuffin/contest-01-build-with-ai-basics/releases/tag/v0.1.0)

1. Download `DesktopAquarium-v0.1.0-win-x64.zip` from the release's **Assets** section.
2. Extract the whole ZIP, for example onto your Desktop, and open `DesktopAquarium`.
3. Double-click `Start-Aquarium.cmd`. The fish and feeder appear; no separate .NET installation is needed.
4. Optionally run `Setup-FeederShortcut.cmd` once to create **Feed Fish** on your Desktop. Double-click that icon to open the aquarium and feeder again. Existing shortcuts pointing to another app copy are preserved.

Keep the entire extracted folder together. Hold the feeder and shake left/right to feed; release to drop it above the taskbar. X closes only the feeder; use the notification-area icon's **Exit** to stop the aquarium. Exit before deleting the folder to remove the portable app; remove any shortcut you created separately.

Windows 11 x64, primary display. This prototype is unsigned; Windows may show a reputation warning. Do not disable antivirus or SmartScreen. Source-build instructions remain below. See the release notes and [release verification](docs/release-v0.1.0.md) for the exact checks and known limits.

## Licensing

Original project source code is made publicly available under the [PolyForm Noncommercial License 1.0.0](LICENSE), within the scope defined in [LICENSING.md](LICENSING.md). This is a **source-available / noncommercial** project, not OSI-approved open source. Third-party commercial use outside the license's permitted purposes requires separate permission from the project owner.

Project assets and third-party components have separate terms: see [ASSET_NOTICE.md](ASSET_NOTICE.md) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). The project owner may distribute the public contest version and a future commercial edition under different terms for rights the owner holds. Contest testing/organizer permissions and the unmet open-source recommendation are explained in [LICENSING.md](LICENSING.md#contest-access-and-rights).

## Project status

Current status (2026-09-28): the participant submitted [Desktop Aquarium on Devpost](https://devpost.com/software/desktop-aquarium). The anonymously accessible project page lists Build With AI: Basics under “Submitted to” and links this repository and a [YouTube demo](https://www.youtube.com/watch?v=KZNpCvBXBvw). G0–G4 and the current source/Release Final Review are complete. The final submission commit/tag has not been pinned. See the [submission record](docs/submission-readiness.md) for verification limits and archival follow-up.

The participant inspected and approved the 32 independently extracted fish PNGs. The app uses their variable-rectangle atlas/metadata and preserves sprite aspect ratios, replacing fixed 80x48 cropping. Source regions/masks remain available in `assets/fish/`; [fish verification](docs/fish-runtime-verification.md) records integration evidence. Movement, feeding, depth and occlusion logic are unchanged by these visual refinements.

The current source/Release build also implements the requested 100% display size: Front uses one source pixel per DIP, with Middle 86% and Rear 72% retained. Windows display scaling applies. Logical feeding/depth geometry is unchanged. The historical ZIPs listed below predate this size adjustment; v0.1.0 packages the current source.

The latest source refinement removes the rectangular feeder panel. The canister can be picked up, shaken, and dropped; it falls to the primary work-area floor above the taskbar and can be picked up again, including while falling. Transparent pixels pass clicks through, and falling never dispenses food. Historical ZIPs predate this refinement; v0.1.0 packages it. See [feeder verification](docs/feeder-object-verification.md) for mechanical results and participant acceptance.

## Run

```powershell
dotnet restore Aquarium.slnx --locked-mode
dotnet build Aquarium.slnx -c Release
dotnet test tests/Aquarium.Core.Tests/Aquarium.Core.Tests.csproj -c Release
dotnet run --project src/Aquarium.Windows/Aquarium.Windows.csproj -c Release -- --feed
```

Or double-click `scripts/Start-Aquarium.cmd`. Source builds require a .NET 10 SDK compatible with `global.json`; initial restore needs package-server access. No separate asset-generation step is needed: the runtime sprites and metadata are committed. The target is Windows 11 x64 on the primary display; native test evidence covers the recorded RDP/Sandbox environments, not general compatibility certification. The portable release above bundles .NET. Historical ZIP paths below are ignored local archives, not files included in a clone.

Pick up the feeder body, shake left/right while holding, and release to drop it to the work-area floor. Ordinary cursor movement never dispenses food. X closes only the feeder. The tray provides Open feeder / Hide / Show again / Exit. Fullscreen protection and manual Hide are distinct. No registration at login, background service, account, model download or external runtime API is added.

## App-owned launcher

On a new local setup, double-click `scripts/Setup-FeederShortcut.cmd`, or run `scripts/Create-FeederShortcut.ps1 -ExePath <absolute-path-to-Aquarium.Windows.exe>`. The installer creates only `Feed Fish.lnk`, refuses unrelated shortcut collisions and does not change security policy or login startup settings.

The current development machine's Desktop grant is now active and its real `Feed Fish.lnk` has been installed. Two launches through that actual Desktop shortcut reused the same resident and visible resting feeder. The link targets the current Release build folder; this is development installation evidence, not a self-contained release. See `docs/feeding-verification.md` for the receipt and remaining coverage.

## Test evidence

The accepted source passed a Release build with zero warnings/errors, 73 Core tests, 23 native feeding/transparency checks and 27 lifecycle checks. The unchanged native-size renderer separately passed 73 WPF checks. See [feeder verification](docs/feeder-object-verification.md) and [fish verification](docs/fish-runtime-verification.md) for the exact checkpoints and environment limits.

`docs/g3-verification.md` records lifecycle/guard verification, actual isolated-profile Edge F11, repeated activation and bounded malformed-client handling. Other sessions/displays/games remain untested.

`docs/feeding-verification.md` separates tests executed from unrun work. The G0 fixture runner uses `--g0`; the feeding fixture runner uses the actual world and targets only its own native windows and the feeder. Both require an idle interactive test desktop. Native fixture success does not replace user feedback.

Optional local diagnostic state can be enabled using `--diagnostics artifacts/feeding/state.json`; it is an overwritten local report, never telemetry. `--probe-seconds 45` is a bounded test-run exit, not a feeding animation.

Canonical plans are in `devpost/`; generated HTML and the learner profile are local-only. Source licensing is recorded above. A public source repository is separate from a verified binary release, final contest submission and broad performance claims.

## Historical packages and optional binary release

Build with `scripts/Publish-Windows.ps1 -RuntimeVersion 10.0.12`; output must be a new folder under `artifacts/`. This wrapper keeps platform-specific publish restore separate from the normal source lockfiles. Verify normal `dotnet restore Aquarium.slnx --locked-mode` after packaging.

Archived artwork integration candidate: `artifacts/fish-runtime/package-01/DesktopAquarium-win-x64.zip`. This includes the approved sprites and replaces fixed-cell lookup, but retains the earlier smaller display size and panel feeder. Use the source instructions above for the accepted current version. Refreshing and verifying a ZIP is separate optional distribution work. The earlier G4 ZIP at `artifacts/g4-only-20260926/package-02/DesktopAquarium-win-x64.zip` remains an archived, separately verified checkpoint.
Extract the **whole** folder and run its `Start-Aquarium.cmd` or `app/Aquarium.Windows.exe`.
Close an already-running development aquarium using its tray Exit first, otherwise single-instance forwarding intentionally reuses that existing process. The current Desktop shortcut still targets the development Release folder, not this package. No automatic migration of that shortcut is performed.

`docs/g4-verification.md` records hashes, packaged tests, loaded runtime paths and resource samples. This G4 checkpoint passed separate SDK-free/offline Sandbox verification and its actual-package learner check; it predates the new fish artwork. The current source acceptance does not certify a future package. Existing ZIPs also predate the current licensing documents. Before any public binary release, complete the [notice-packaging plan](THIRD_PARTY_NOTICES.md#binary-distribution-plan--separate-from-public-source), refresh package tests and obtain acceptance of that package.

Test-only environment overrides `AQUARIUM_TEST_EXE`, `AQUARIUM_TEST_OUTPUT` and (feeding harness) `AQUARIUM_TEST_SHORTCUT` select a project-local candidate for `Verify-FeedingNative.py`/`Verify-G3Native.py`. They do not alter the product's runtime behavior. `Verify-PackagedStartup.ps1 -PackageDirectory <extracted-folder>` performs a bounded own-process runtime-module check. Native scripts require an idle authorized interactive desktop.

Current preparation and participant-owned items: [submission readiness](docs/submission-readiness.md). Native/browser/startup checks and a local rehearsal are recorded in `docs/rdp-candidate-verification.md`. The rehearsal is not a final uploaded demo.

## Historical G4 validation

A full finite ordinary/feeding/hidden measurement (60 seconds each) now passed, with safe restoration and normal exit. See `docs/g4-verification.md` for CPU/memory/callback results and the absence of usable per-process GPU counter values. Reproduce the optional GPU observation with `scripts/Measure-GpuProcess.ps1` against the measurement run directory; this remains a test-only tool.

G4's separate SDK-free/offline run and learner check completed; earlier unavailable-Sandbox notes describe historical checkpoints. The current source/Release implementation is accepted. The old clean-room pass is not transferred to later builds or packages, and Devpost submission remains pending.
