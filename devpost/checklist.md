---
doc: checklist
status: approved
---

# Desktop Aquarium — Build Checklist

Build mode: fast — explicitly selected by the learner; keep the scheduled hands-on checkpoints.

The technical specification is approved. This checklist translates it into four runnable increments, not a new product or architecture proposal. The learner approved this order and fast mode. Slice completion still requires mechanical evidence and the scheduled hands-on feedback. Markdown only: do not generate an HTML build checklist.

The first increment is the spec's critical Windows integration gate. Core tests are included where behavior becomes usable, not a separate long stage of hidden plumbing. Existing feasibility checks are introduced early and exercised again against the complete feeding experience.

## Current Execution Status

Current instruction: work through G4 only. Remain on RDP; do not retry console transfer or proceed to final user review, learning wrap-up, submission recording, public repository work or actual submission.

G0/G2/G3 remain accepted. The runtime-10.0.12 candidate has the previously recorded native feeding/lifecycle/browser and package-local runtime checks. In this G4 pass, locked restore/Release build/64 core tests and 489 package hashes were rechecked. One finite measurement run now completed ordinary, feeding and hidden phases for 60 seconds each, with stable fish identity/food accounting, hidden freeze, safe recovery and normal exit: all eight assertions passed. The earlier incomplete benchmark is historical, not the latest outcome.

CPU/memory/callback results are recorded in `docs/g4-verification.md`. The GPU counter provider returned no process engine instances in 80 observations, so GPU utilization is unavailable rather than zero. These are finite RDP measurements, not long-duration or local-console certification. Product source and artwork were unchanged.

The remaining G4 mechanical blocker is genuine separate SDK-free/offline Windows execution. Windows Sandbox and Hyper-V features are disabled, no Sandbox executable is available, and Docker is Linux. The prepared WSB kit has not run. Enabling a Windows feature/reboot is not silently authorized; no system/security/network changes were made. Keep G4 unchecked pending real evidence. Final review, app-map wrap-up, licensing/naming/public links/form answers and submission remain unchanged and outside this pass.

## Slices

- [x] **1. G0 — Try a passive desktop object and a draggable feeder against real windows**
  Becomes usable: A runnable Windows host displays a clearly labelled temporary pixel marker and a small feeder body/X. Ordinary desktop clicks and scrolling pass through the habitat; the tool can be deliberately dragged and released. Basic Hide/Show/Exit and fullscreen suppression provide a safe way to test it.
  Why now: This is the single critical-integration exception to a full product slice. It proves native transparency, input, depth masking and safe exit before investing in fish artwork or broader behavior. Bootstrap lives inside this runnable gate.
  PRD ref: `prd.md > Window depth — accepted direction, MVP value`; `prd.md > Feeder handling — accepted, MVP value`; `prd.md > Aquarium controls and feeder activation — accepted, MVP value`; `prd.md > Fullscreen work takes priority — accepted, MVP value`.
  Spec ref: `spec.md > Aquarium.Windows / DesktopSnapshotService`; `spec.md > Aquarium.Windows / Occlusion and SpriteRenderer`; `spec.md > Aquarium.Windows / FeederWindow and InputAdapter`; `spec.md > Aquarium.Windows / VisibilityPolicy and FullscreenGuard`; `spec.md > Aquarium.Windows / Host, Tray and InstanceBroker`; `spec.md > Where It Runs and How Someone Tries It`.
  Build: Create the solution, Core/Windows/test projects and build configuration while delivering the minimal live native probe. Preserve HTML/profile ignore rules; ignore generated build outputs. Add immutable geometry contracts, OS observation/coordinate normalization, the passive surface, separate feeder input and cancellation, minimal resident controls and guard behavior. Keep temporary assets explicitly labelled. Do not add final fish behavior yet or replace real desktop interaction with a browser mock.
  Verify (mechanical): Run `dotnet restore Aquarium.slnx`, `dotnet build Aquarium.slnx -c Release`, and `dotnet test tests/Aquarium.Core.Tests/Aquarium.Core.Tests.csproj -c Release`; check that Core has no Windows/UI reference. Launch `dotnet run --project src/Aquarium.Windows/Aquarium.Windows.csproj -- --feed` in an authorized interactive session. Record native hit-test/capture/focus and actual rendered observations for opaque marker pixels versus transparent space, two overlapping ordinary windows, deliberate feeder drag, release/X, tray exit and fullscreen versus ordinary maximize in `docs/verification.md`. Build success or synthetic geometry alone is not a passed Windows gate. When interactive evidence cannot be obtained, leave the gate incomplete and state what still needs testing.
  Learner check: Start the same command on the Windows desktop. Try clicking/scrolling the work app through the marker, move the feeder across another app and release it, overlap/reorder two windows, and try fullscreen plus Hide/Show/Exit. Report anything blocked, visually wrong, or unexpectedly focused. This is a native integration probe, not the finished aquarium.
  Commit: `Prove Windows overlay input and depth integration`

- [x] **2. G1/G2 — Feed a fish through the real desktop feeder loop**
  Becomes usable: Original pixel-art fish swim on the display and occasionally notice the cursor. A real feeder launcher opens one resting tool; holding and shaking releases food; a fish visibly approaches and eats; releasing/X returns the user to ordinary work.
  Why now: This delivers the unique kernel immediately after the native risk gate. Deterministic rules, unit tests and their visible Windows connections are built together, rather than completing a core library with nothing usable on screen.
  PRD ref: `prd.md > The Core Journey`; `prd.md > Desktop presence and cursor curiosity — MVP value`; `prd.md > Window depth — accepted direction, MVP value`; `prd.md > Feeder handling — accepted, MVP value`; `prd.md > Look and Feel`.
  Spec ref: `spec.md > Aquarium.Core / World and Commands`; `spec.md > Aquarium.Core / Shake and Food`; `spec.md > Aquarium.Core / DepthTransitionPlanner`; `spec.md > Aquarium.Windows / Host, Tray and InstanceBroker`; `spec.md > Look and Feel`.
  Build: Implement autonomous movement, intermittent curiosity, held-only shake detection, bounded food and single consumption, stable fish identities and foreground approach/edge re-entry. Connect these rules to live input and cached original sprites. Add the current-user/session instance broker and explicit app-owned shortcut script; preserve unrelated desktop items. Opening, holding, resting and closing remain distinct. Do not add rarity, visiting fish, persistent raising, or a settings suite.
  Verify (mechanical): Repeat Release build and core tests. Test no-held/no-food, stationary jitter, a single sweep versus reversals, release/cancel clearing samples, capped food/lifetime, one consumption per pellet, consistent bands and identity-preserving edge re-entry. Exercise the real launcher twice and verify one resident/feeder. Record actual held-shake → emitted food → visible approach/consumption → release/X behavior against normal and maximized windows. Do not count timed sample animation as feeding.
  Learner check: Use the app-owned desktop shortcut, pick up and shake the feeder, release it and continue working, then pick it up again and close it. Describe whether the interaction feels understandable and whether the fish feel autonomous. This is the early complete-core-journey feedback checkpoint.
  Commit: `Implement the live shake-to-feed aquarium loop`

- [x] **3. G3 — Keep the aquarium safe across fullscreen, hiding and interrupted input**
  Becomes usable: The complete feeding app reliably yields to fullscreen/system tasks, recovers resting rather than held, preserves manual Hide, and avoids stuck input or duplicate tools during repeated use.
  Why now: Basic protection already existed in G0. This expands the actual acceptance matrix with the complete behavior, when lifecycle regressions and hidden food emission can be observed rather than guessed.
  PRD ref: `prd.md > Fullscreen work takes priority — accepted, MVP value`; `prd.md > Aquarium controls and feeder activation — accepted, MVP value`; `prd.md > States and Boundaries`.
  Spec ref: `spec.md > Aquarium.Windows / VisibilityPolicy and FullscreenGuard`; `spec.md > Aquarium.Windows / FeederWindow and InputAdapter`; `spec.md > Aquarium.Windows / DesktopSnapshotService`; `spec.md > Data Model and Lifetime`; `spec.md > Verification Order and Important Failure Modes`.
  Build: Complete guard independence, capture/deactivation cancellation, hidden simulation pause and clock reset, repeated activation/race handling, safe DPI/display reconfiguration, and cleanup/tray recovery. Fail safely on invalid observations. Preserve the accepted primary-monitor test envelope; do not silently expand OS support or change rendering architecture.
  Verify (mechanical): Repeat Release build/tests and visibility truth-table tests. Record expected/actual results for fullscreen entry while held, return without feeding, manual Hide across fullscreen exit, ordinary maximize, menu/window switching, rapid feeder launches and normal Exit cleanup. Test session/display changes only in a controlled authorized session; do not restart Explorer, lock the desktop, change DPI or disrupt unrelated work without agreement. Record untested environments explicitly rather than marking them passed.
  Learner check: Try the completed app alongside actual work, including fullscreen video and interrupted dragging. Verify the cursor is never stuck, ordinary movement cannot feed, and manual Hide is respected. Report any conflict with the primary task.
  Commit: `Harden desktop coexistence and lifecycle recovery`

- [ ] **4. G4 — Run the self-contained package offline and record real limits**
  Becomes usable: Another person can extract the complete Windows x64 publish folder and run the actual aquarium without an SDK, account or runtime service. Run/test instructions and measured support limits accompany it.
  Why now: Package and resource verification must exercise the finished kernel and recovery behavior, not certify an empty scaffold. It precedes the final user review and later submission work.
  PRD ref: `prd.md > Platform and Documentation Decisions`; `prd.md > What We're Building`; `prd.md > Non-Goals`.
  Spec ref: `spec.md > Where It Runs and How Someone Tries It`; `spec.md > External Services and Dependencies`; `spec.md > Verification Order and Important Failure Modes`; `spec.md > Decisions and Open Issues`.
  Build: Add the planned self-contained publish/ZIP script and reproducible instructions. Record exact dependencies/runtime and asset provenance. Measure Release behavior in ordinary, feeding and hidden states. Keep HTML learning/review files outside Git. Do not publish publicly, select a license on the learner's behalf, or draft their final competition submission in this slice.
  Verify (mechanical): Run Release build/core tests and `scripts/Publish-Windows.ps1` (self-contained win-x64 with publish-only restore isolation), followed by `dotnet restore Aquarium.slnx --locked-mode` to verify that packaging preserved normal source restore. Inspect the complete ZIP and record hashes. Run the extracted app on a controlled Windows 11 x64 local session without an SDK and with runtime networking unavailable; do not disconnect the user's host or alter security policy. Repeat real feeding and clean Exit. Compare baseline/ordinary/feeding/hidden CPU, memory, available GPU and frame timings with environment/counts recorded. Check that generated HTML/private profile/secrets are not staged. Missing clean-environment evidence remains unrun, not a pass.
  Learner check: Extract and start the package, open the feeder, complete the feeding loop and explore awkward inputs. Give final feedback on the actual app, not a documentation page.
  Commit: `Package and verify the offline Windows prototype`

## Hands-on Checkpoints

- [x] Early native integration checked after slice 1 - learner reported the running probe appears to work; specific application/session coverage is not inferred.
- [x] Complete core journey checkpoint accepted after positive review of the live test, verified Desktop installation, and explicit instruction to continue; no unreported detailed manual sequence or environment coverage inferred.
- [ ] Final kick-the-tires exploration and feedback completed after slice 4.

## Final Review

- [ ] Final review complete — feedback resolved, agreed fixes verified/committed/retried, and learner confirms ready to ship.

## Code Tour and App Map

- [ ] Learning activity complete — use one real desktop overlay/input/OS-integration investigation; count equivalent practice already completed rather than repeat it.
- [ ] Optional edit and transfer reflection addressed — offered/declined/already covered/not applicable as appropriate.
- [ ] `devpost/app-map.html` generated from finished code, checked, and shown locally; remains Git-ignored.

Activity and evidence: no learner wrap-up activity is claimed. A local static app-map preview has been generated with five checked path/symbol anchors and a headless-browser DOM check; this is reference material pending final review, not proof of completed learning.
Route and stops: select actual source paths and symbols after they exist.
Edit outcome: not performed.
Reflection: not yet offered; personal answer belongs only in the ignored profile.
Activity mode: not selected; tie the wrap-up to actual implementation evidence.

## Revisions
- G0 checkpoint accepted after general positive learner feedback; commit `b9d361a` preserves the verified probe. Specific local-console/browser/game checks remain unrun, not inferred from that feedback.
- Default application now runs the feeding world. `--g0` preserves the labelled native-regression probe and does not substitute for the real fish loop.
- Core/Windows boundaries are unchanged. Core motion/feeding uses `World.cs`, `Feeding.cs`, and `DepthTransitions.cs`; UI mouse callbacks enter the one UI-owned core synchronously, with the instance broker still marshalled onto the dispatcher. Renderer lives in `Rendering/SpriteRenderer.cs`.
- A movement-invariant test found a boundary snap after edge feeding. Clamping destinations instead of the fish's current position fixes the discontinuity without weakening the test.
- The native feeding harness aborts if the test-owned input point is occluded by another application; it now selects a verified visible point on its own fixture. This is test safety, not a new product behavior.
- Desktop shortcut placement was delayed by failed grant requests. The learner subsequently approved access; the successful grant was verified before installing the real Desktop shortcut. Two actual Desktop launches and idempotent setup passed without bypassing access controls.

- G0 uses code-only `DesktopOverlay.cs` and `FeederWindow.cs` rather than empty XAML wrappers; the approved two-project WPF/Win32 architecture is unchanged. A stdlib Python native fixture script provides reproducible controlled integration evidence without introducing a runtime dependency.
- An inactive, visible XAML shell island initially suppressed the entire habitat. The adapter now masks its known bounds and reserves blanket suppression for active/protected interactions. Native fixture checks were rerun after the fix.
- The background fixture could not assume `SetForegroundWindow` succeeded. The test now verifies its own target and uses a bounded click on that fixture to establish ordering before reading pixels. No input is sent to unrelated windows; fixture failures are not application passes.

- The learner positively reviewed the running feeding test. Record this as observed-test feedback, not an independent manual-use claim. A user-run shortcut helper addresses the failed MCP directory-grant path without bypassing it; the actual Desktop launch/feed check remains open.

- Desktop access resolution: actual `Feed Fish.lnk` installation and two settled same-instance launches are verified. The first immediate composite assertion is retained as an unsuccessful verification attempt; later checks wait for process settlement. No new application code or G3 test pass is claimed.

- The learner accepted the current live feeding experience and requested continuation after launcher access was resolved. Prior repeated pending-review text is superseded; no redesign or new gate is required. Final user review and untested environment claims remain separate.

- G3: guard independent lock/disconnect flags, bound local activation acknowledgements/retries, and use a fixed-step clock that discards hidden time. A real Hide-frame assertion found a queued invisible render; adding visibility guards fixed it without changing the assertion. Actual Edge F11 and native fixtures passed; simulated notifications and unrun environments remain labelled.

- G4 partial: packaged and extracted the real app, checked bundle-local runtime loading and reran feeding/lifecycle tests on the package. A bare RID publish changed canonical lockfiles and broke NU1004 locked restore; the publishing wrapper now isolates restore state and verifies source lock hashes. R2 publish followed by locked restore/build/64 tests passed. Clean no-SDK/offline and sustained performance remain unrun, so G4 stays unchecked.

- Pre-submission pass requested: prepare technical deliverables before optional refinements, without publishing/submitting. A live metadata fetch showed runtime 10.0.12 while cached research still showed 10.0.10; new notices and candidate use the live value. Input-desktop denial and missing Sandbox prevent claiming fresh interactive/offline passes.

- RDP resume: input access recovered without console transfer. Real candidate feeding/lifecycle/browser/loader checks and an 8-second local rehearsal now exist; partial 60-second measurements and a completed short run are explicitly separated. Test-only fixture positioning/activation changed for the smaller desktop; no product behavior or user windows were changed.

- G4-only continuation: completed all three 60-second resource phases and eight assertions, rechecked the 489-file candidate and 64 core tests, and observed no PID GPU counter instances. Only measurement tooling changed. A separate no-SDK/offline Windows environment is unavailable; the outer G4 box stays unchecked, and no later stage was started.
