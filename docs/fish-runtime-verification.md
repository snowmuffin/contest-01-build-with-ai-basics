# Approved fish runtime integration — 2026-09-27

Status: approved artwork integrated; final running-package learner review remains separate.
Classification: optional visual refinement within the accepted Final Review; no product scope expansion.

## Approval and implementation

The participant confirmed inspecting the 32 independent PNGs and instructed implementation. `assets/fish/approval.json` pins the original source and frame-set SHA-256. The exact approved frame-set fingerprint is `fc2147469d6a51dd0799af76edf110d79023d62090e811d355df8afca92a7555`. Earlier extraction receipts deliberately retain their preparation-time state.

`scripts/Pack-FishAtlas.py --build` packs those individual RGBA PNGs, unscaled and unrotated, into `src/Aquarium.Windows/Assets/fish-sprites.png` (1024x821). It writes variable source rectangles, Species/Facing/Frame mappings, per-species canvas dimensions and frame offsets to `fish-sprites.json`. Every approved pixel and four-pixel transparent margin is preserved; adjacent rectangles have an additional two-pixel gutter. `--verify` reproduces the packing and checks all 32 RGBA round trips, approval identity, transparent gutters and non-overlap. `Generate-Assets.py` now calls that verifier before regenerating the original feeder/icon.

`Rendering/FishSpriteAtlas.cs` loads and validates the embedded PNG/JSON once and freezes all cached frames. `SpriteRenderer.cs` uses these explicit mappings and fits the common per-species canvas proportionally into the existing fish display bounds. This preserves sprite proportions and stable scale between frames/directions. The old `(facing*2+frame)*80, species*48` grid lookup is removed. The legacy dirty `fish-atlas.png` is neither loaded nor embedded; it is preserved without overwriting the participant's intermediate work.

No changes were made to `Aquarium.Core`, movement, feeding/contact geometry, depth transitions, occlusion masks, fullscreen/visibility logic, feeder controls, instance handling or animation cadence. The logical 68x40 fish bounds and Rear/Middle/Front scale remain unchanged. Proportional sprites can occupy less of that box than the previous stretched image; the logical box is intentionally unchanged. Runtime dependencies remain the existing .NET desktop framework only.

## Executed verification

| Check | Actual result |
| --- | --- |
| Approved PNGs → packed atlas → extracted rectangles | All 32 RGBA round trips exact; no overlapping rectangles or gutter contamination |
| Asset generator | Fish PNG/JSON and legacy atlas unchanged; feeder PNG/ICO reproduced with identical hashes |
| Locked restore / Release build | Pass; zero warnings and errors |
| Core suite | 66 passed; also passed after publishing |
| WPF resource and renderer probe | 69 checks passed: 32 decoded crops match approved PNGs, all 32 render, Front/Middle/Rear/protected masking works, existing depth scaling increases monotonically |
| Source native feeding | Existing 18 checks passed, including held emission, visible consumption, release/X, repeated shortcut activation and ordinary maximize |
| Source native lifecycle | Existing 25 checks passed, including Hide/Show, fullscreen/capture recovery, activation reuse and normal tray exit |
| New package inventory and ZIP | 489 inventory files verified; ZIP entries match the publish directory |
| Bundled runtime startup | Pass; five fish initialize, hostfxr/hostpolicy/coreclr load from package .NET 10.0.12, normal exit 0 |
| Packaged native feeding/lifecycle | Existing 18 feeding and 25 lifecycle checks passed again on the new package executable; normal exits |
| Post-publish source restore/build/tests | Locked restore/build and all 66 core tests pass; source lockfiles preserved |

Source native evidence: `artifacts/fish-runtime/feeding/report.json` and `lifecycle/report.json`. Tests target their own native fixtures and the aquarium's controls. Native environment is the current RDP session, with some lifecycle notifications explicitly simulated; no DPI setting, actual session disconnect, Explorer restart or host networking change was performed.

Packaged native evidence: `artifacts/fish-runtime/package-feeding/report.json` and `package-lifecycle/report.json`, with a separate project-local test shortcut pointing at the new packaged executable. The user's Desktop shortcut was not migrated; it continues to target the updated normal Release build path.

WPF evidence: `artifacts/fish-runtime/renderer-report.json`, `rendered-32.png` and the local `renderer-probe/` harness. That probe renders synthetic scenes through the actual WPF class on a test-owned offscreen window; it is additional resource/rendering evidence, not a substitute for native feeding. Screenshot `feeding/feeding-live.png` contains only the test fixture. Core evidence is in `artifacts/fish-runtime/tests/`.

The existing package-startup helper gained an optional `-OutputDirectory` confined to a fresh repository `artifacts/` folder. This preserves earlier G4 test evidence; default callers retain their existing behavior. No new testing framework was introduced.

## New package candidate

- ZIP: `artifacts/fish-runtime/package-01/DesktopAquarium-win-x64.zip`.
- Size: 74,831,474 bytes.
- SHA-256: `8b47e65640dfaefe7b7b42177d9a7033dcee2b26949a6ead092b344737cf5804`.
- Runtime: self-contained Windows x64, .NET 10.0.12; no shared runtime change.
- Build provenance: base commit `4c858c2` plus the in-progress integration source inputs recorded by hash in `BUILD.json`. Do not describe it as a clean build of that base commit; the package was built before the integration commit.
- Inventory/startup evidence: `artifacts/fish-runtime/package-integrity.json` and `package-startup/report.json`.

The package smoke test runs on an SDK-equipped host with intentionally unavailable child DOTNET_ROOT/PATH entries. It does not establish a new SDK-free/offline clean-room pass. Earlier G4 clean-room evidence belongs to its earlier package and is not transferred to these changed bytes. New clean-room verification and final package learner review remain open; source artwork approval is not final submission approval. No publishing, licensing choice or submission action occurred.

## Reproduce

```powershell
python scripts/Pack-FishAtlas.py --verify
dotnet restore Aquarium.slnx --locked-mode
dotnet build Aquarium.slnx -c Release --no-restore
dotnet test tests/Aquarium.Core.Tests/Aquarium.Core.Tests.csproj -c Release --no-build
```

Use the existing `Verify-FeedingNative.py` and `Verify-G3Native.py` only on an idle interactive test desktop with no resident aquarium, setting `AQUARIUM_TEST_OUTPUT`, `AQUARIUM_TEST_EXE` and the feeding harness's `AQUARIUM_TEST_SHORTCUT` to the intended project-local paths. Packaged startup accepts `-PackageDirectory` and a fresh `-OutputDirectory`. Keep tests sequential because the application deliberately permits only one instance per user/session.
