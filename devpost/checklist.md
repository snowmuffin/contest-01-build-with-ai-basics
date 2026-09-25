---
doc: checklist
status: approved
---

# Desktop Aquarium — Build Checklist

Build mode: fast — explicitly selected by the learner; keep the scheduled hands-on checkpoints.

The technical specification is approved. This checklist translates it into four runnable increments, not a new product or architecture proposal. The learner approved this order and fast mode. Slice completion still requires mechanical evidence and the scheduled hands-on feedback. Markdown only: do not generate an HTML build checklist.

The first increment is the spec's critical Windows integration gate. Core tests are included where behavior becomes usable, not a separate long stage of hidden plumbing. Existing feasibility checks are introduced early and exercised again against the complete feeding experience.

## Current Execution Status

G0 is accepted for continuation: the learner reported that the running probe appears to work. This records hands-on feedback without inferring specific apps, local-console use, or broad compatibility. The 26 core tests and 25 controlled native fixture checks passed in the previously documented RDP session. Expanded ordinary-app/local-console and lifecycle coverage remains explicitly pending in slices 3 and 4; no unrun test is marked passed.

Slice 2 is next: the real feeding loop. Fast mode and the complete-core-journey checkpoint are unchanged.

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

- [ ] **2. G1/G2 — Feed a fish through the real desktop feeder loop**
  Becomes usable: Original pixel-art fish swim on the display and occasionally notice the cursor. A real feeder launcher opens one resting tool; holding and shaking releases food; a fish visibly approaches and eats; releasing/X returns the user to ordinary work.
  Why now: This delivers the unique kernel immediately after the native risk gate. Deterministic rules, unit tests and their visible Windows connections are built together, rather than completing a core library with nothing usable on screen.
  PRD ref: `prd.md > The Core Journey`; `prd.md > Desktop presence and cursor curiosity — MVP value`; `prd.md > Window depth — accepted direction, MVP value`; `prd.md > Feeder handling — accepted, MVP value`; `prd.md > Look and Feel`.
  Spec ref: `spec.md > Aquarium.Core / World and Commands`; `spec.md > Aquarium.Core / Shake and Food`; `spec.md > Aquarium.Core / DepthTransitionPlanner`; `spec.md > Aquarium.Windows / Host, Tray and InstanceBroker`; `spec.md > Look and Feel`.
  Build: Implement autonomous movement, intermittent curiosity, held-only shake detection, bounded food and single consumption, stable fish identities and foreground approach/edge re-entry. Connect these rules to live input and cached original sprites. Add the current-user/session instance broker and explicit app-owned shortcut script; preserve unrelated desktop items. Opening, holding, resting and closing remain distinct. Do not add rarity, visiting fish, persistent raising, or a settings suite.
  Verify (mechanical): Repeat Release build and core tests. Test no-held/no-food, stationary jitter, a single sweep versus reversals, release/cancel clearing samples, capped food/lifetime, one consumption per pellet, consistent bands and identity-preserving edge re-entry. Exercise the real launcher twice and verify one resident/feeder. Record actual held-shake → emitted food → visible approach/consumption → release/X behavior against normal and maximized windows. Do not count timed sample animation as feeding.
  Learner check: Use the app-owned desktop shortcut, pick up and shake the feeder, release it and continue working, then pick it up again and close it. Describe whether the interaction feels understandable and whether the fish feel autonomous. This is the early complete-core-journey feedback checkpoint.
  Commit: `Implement the live shake-to-feed aquarium loop`

- [ ] **3. G3 — Keep the aquarium safe across fullscreen, hiding and interrupted input**
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
  Verify (mechanical): Run Release build/core tests and `dotnet publish src/Aquarium.Windows/Aquarium.Windows.csproj -c Release -r win-x64 --self-contained true -p:PublishSingleFile=false -p:PublishTrimmed=false -o artifacts/win-x64`. Inspect the complete ZIP and record hashes. Run the extracted app on a controlled Windows 11 x64 local session without an SDK and with runtime networking unavailable; do not disconnect the user's host or alter security policy. Repeat real feeding and clean Exit. Compare baseline/ordinary/feeding/hidden CPU, memory, available GPU and frame timings with environment/counts recorded. Check that generated HTML/private profile/secrets are not staged. Missing clean-environment evidence remains unrun, not a pass.
  Learner check: Extract and start the package, open the feeder, complete the feeding loop and explore awkward inputs. Give final feedback on the actual app, not a documentation page.
  Commit: `Package and verify the offline Windows prototype`

## Hands-on Checkpoints

- [ ] Early native integration checked after slice 1 — learner tries click-through, layering, dragging and recovery before fish behavior is expanded.
- [ ] Complete core journey checked after slice 2 — learner uses the real feeder and reports feel/clarity, with fixes verified before continuation.
- [ ] Final kick-the-tires exploration and feedback completed after slice 4.

## Final Review

- [ ] Final review complete — feedback resolved, agreed fixes verified/committed/retried, and learner confirms ready to ship.

## Code Tour and App Map

- [ ] Learning activity complete — use one real desktop overlay/input/OS-integration investigation; count equivalent practice already completed rather than repeat it.
- [ ] Optional edit and transfer reflection addressed — offered/declined/already covered/not applicable as appropriate.
- [ ] `devpost/app-map.html` generated from finished code, checked, and shown locally; remains Git-ignored.

Activity and evidence: not performed yet; no learning or runtime evidence claimed.
Route and stops: select actual source paths and symbols after they exist.
Edit outcome: not performed.
Reflection: not yet offered; personal answer belongs only in the ignored profile.
Activity mode: not selected; tie the wrap-up to actual implementation evidence.

## Revisions

- G0 uses code-only `DesktopOverlay.cs` and `FeederWindow.cs` rather than empty XAML wrappers; the approved two-project WPF/Win32 architecture is unchanged. A stdlib Python native fixture script provides reproducible controlled integration evidence without introducing a runtime dependency.
- An inactive, visible XAML shell island initially suppressed the entire habitat. The adapter now masks its known bounds and reserves blanket suppression for active/protected interactions. Native fixture checks were rerun after the fix.
- The background fixture could not assume `SetForegroundWindow` succeeded. The test now verifies its own target and uses a bounded click on that fixture to establish ordering before reading pixels. No input is sent to unrelated windows; fixture failures are not application passes.
