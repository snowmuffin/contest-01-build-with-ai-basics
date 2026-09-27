---
doc: checklist
status: approved
---

# Desktop Aquarium — Build Checklist

Build mode: fast — explicitly selected by the learner; keep the scheduled hands-on checkpoints.

The technical specification is approved. This checklist translates it into four runnable increments, not a new product or architecture proposal. The learner approved this order and fast mode. Slice completion still requires mechanical evidence and the scheduled hands-on feedback. Markdown only: do not generate an HTML build checklist.

The first increment is the spec's critical Windows integration gate. Core tests are included where behavior becomes usable, not a separate long stage of hidden plumbing. Existing feasibility checks are introduced early and exercised again against the complete feeding experience.

## Current Execution Status

All four build slices G0-G4 and the current source/Release Final Review are complete. The final exploratory feedback led to four fish silhouettes, directional poses, native-size depth perspective and a transparent falling feeder. After the updated app was launched, the owner accepted this implementation level and chose submission preparation on 2026-09-27. This records general PoC acceptance, not unreported individual test actions or wider environment coverage.

This is a Final Review refinement pass, not a reopened product scope. Preserve five fish, existing feeding/fullscreen/hide/instance behavior, three logical depth bands, Windows 11 x64 target and no external runtime service. Do not add rarity, collection, growth, free 3D movement, additional OS targets or multi-monitor scope.

Publication boundaries: PolyForm Noncommercial applies only within the project-owned code scope; assets and third parties retain separate terms. The owner has now authorized final documentation and an update to the existing public GitHub repository. Use the separate noreply copy and preserve the original local history, old uncommitted atlas, `Clean-FishAtlas.py` and unrelated work.

Current task boundary (2026-09-28): record the participant's completed submission, with no product scope or runtime change. The public [Desktop Aquarium entry](https://devpost.com/software/desktop-aquarium) lists Build With AI: Basics under “Submitted to” and includes the repository and YouTube demo links. The participant handled the submission; the agent did not author the public copy or submit the form. The private exit survey and exact submitted commit/tag are not independently established. A new self-contained binary release is optional and needs fresh package/notice checks before it can be offered; historical G4 evidence remains valid only for its recorded bytes.

## Public repository preparation

Optional portable release authorized (2026-09-28): prepare v0.1.0 from the accepted source with complete notices, verify the exact ZIP and Desktop shortcut workflow, then publish it and update download links. This supersedes the earlier preparation-only publishing boundary for this release. Preserve the separate noreply publication history and the existing unfinished atlas/cleaner. No app feature or scope change. Progress: `../docs/release-v0.1.0.md`.

- [x] Owner selected PolyForm Noncommercial 1.0.0 as the source-available/noncommercial strategy, with separate asset and third-party scopes and retained future commercial-edition rights.
- [x] Reviewed official Rules: public access required, open-source license recommended; this choice does not satisfy that recommendation. Separate judging/organizer permissions are documented without editing the license text.
- [x] Final license/notice/link/provenance and source/history publication checks recorded in `../docs/submission-readiness.md`.
- [x] Public GitHub repository created/pushed and its source URL verified without authentication — owner authorized publication after review. A separate public copy uses GitHub noreply author/committer emails; the 22 original commits retain identical trees, names, dates, messages and parent relationships. Original local history and unfinished work are preserved. Anonymous repository, commit and raw-source access passed on 2026-09-27; see `../docs/submission-readiness.md`.
- [ ] Archival follow-up: identify the exact submitted commit and create a fixed `v0.1-contest-submission` tag. Submission is already reported complete; no commit is guessed and no tag is created or moved in this documentation update.
- [ ] Before any public binary release: include all new licensing documents and actual dependency notices; verify the new package. Existing local ZIPs are historical candidates.

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

- [x] **4. G4 — Run the self-contained package offline and record real limits**
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
- [x] Final kick-the-tires exploration and feedback completed after slice 4 ? learner identified fish silhouette diversity, missing toward/away presentation, weak depth perspective, and feeder visual integration as the main submission-readiness gaps.

## Final Review

- [x] Independent sprite extraction — 32 source-sized PNGs and 32 reproducible masks prepared from the supplied preview; mechanical pixel/boundary/identity checks pass. This marks preparation only, not artwork acceptance.
- [x] Participant inspection of all 32 extracted PNGs — participant explicitly confirmed inspection and instructed implementation. `assets/fish/approval.json` pins acceptance to these exact frames; this is artwork approval, not final package acceptance.
- [x] After frame acceptance: built the variable-rectangle runtime atlas/metadata, replaced fixed crop lookup, and passed source/package feeding and lifecycle checks. New binary-release checks are separate from current source acceptance.
- [x] Requested 100% display size accepted as part of the owner's overall current-implementation review. Front 100%, Middle 86%, Rear 72%; existing simulation bounds remain unchanged. `../docs/fish-runtime-verification.md` retains the visual geometry limitations; no unreported pixel-level manual check is inferred.

- [x] Feeder object/drop refinement accepted in the owner's overall review after the updated app was launched. Opaque sprite and small X, transparent surroundings, work-area-floor landing and pickup while falling/resting are implemented; mechanical results are in `../docs/feeder-object-verification.md`.
- [x] Fish visual diversity — five stable fish use four distinct visual families; artwork approval, renderer checks and overall source acceptance recorded. No collection/rarity mechanics added.
- [x] Four-direction presentation and depth perspective — Left/Right/TowardViewer/AwayFromViewer with Rear/Middle/Front scale differences; implemented, mechanically checked and included in overall source acceptance.
- [x] Proportional source regression — current Release build, 73 Core tests, 23 native feeding/transparency checks and 27 lifecycle checks passed. The unchanged native-size renderer passed 73 WPF checks at its recorded checkpoint. No new performance or clean-package pass is inferred.
- [x] Final source/Release review complete — agreed refinements implemented, verified and committed; owner accepted the implementation and requested submission preparation. Optional fresh-ZIP verification remains under Public repository preparation, not silently marked complete.

## Code Tour and App Map

- [x] Evidence-based wrap-up recap — connect the owner's observed rectangular feeder problem to the transparent-object change and the native transparency/input checks. This is a recap of the actual refinement and acceptance, not a new hands-on code tour or a claim of learning mastery.
- [x] Extra code edit not applicable to this documentation/publication task; no personal reflection or survey answer inferred. An optional reflection is not a completion prerequisite.
- [x] `devpost/app-map.html` refreshed against the accepted source, statically checked and linked locally as a reference route; remains Git-ignored. No interactive browser review by the participant is claimed.

Activity and evidence: the owner identified the visible feeder window as unnatural, requested a falling/pickable object, retried the launched build and accepted the implementation. The recap connects that concrete requirement to transparent-corner click-through, opaque-body hit testing and held-only feeding checks in `../docs/feeder-object-verification.md`. It distinguishes observed appearance from automatically tested input behavior.
Reference route (not an interactive tour): `FeederWindow.Move/HeldMoved` -> `World.SubmitHeldMotion` -> `SpriteRenderer.Update/OnRender`; gravity uses `HostController.Tick` -> `FeederWindow.Advance` -> `FeederFall.Advance`.
Edit outcome: no additional code edit; no product scope change.
Reflection: no response requested or invented; any later personal response belongs only in the ignored profile.
Activity mode: focused evidence recap and local map. Reusable practice: turn an appearance request into separate visible-pixel, input and state-transition checks; broad test-environment claims require separate evidence.

## Submission status — 2026-09-28

- [x] Local Sandbox demo candidate reviewed after take-01 feedback: take-05 is 47.50 seconds, 1192×718 at 30 fps, with two actual Edge windows, real desktop shortcut/pickup/two-second shake/food response/drop/close and ordinary page interaction. Full decode, chronological whole-timeline frame review and denser feeding/consumption inspection passed; same Release payload and wallpaper. Earlier takes are preserved with rejection reasons. See `../docs/demo-recording.md` for each PASS and its limits. The hosted video's exact equivalence to this local candidate has not been independently checked.
- [x] Participant completed the submission themselves and provided its URL. The public project name is Desktop Aquarium; the agent did not write or rewrite the submission answers.
- [x] Public project page anonymously retrieved with its GitHub repository link and embedded [YouTube demo](https://www.youtube.com/watch?v=KZNpCvBXBvw); anonymous YouTube oEmbed metadata also returned successfully. Full hosted playback was not re-reviewed.
- [x] Devpost submission reported by the participant and supported by the public page's “Submitted to: Build With AI: Basics” association on 2026-09-28.
- [ ] Archival follow-up: pin the exact submission commit/tag; see Public repository preparation above.

Private exit-survey answers and completion are not visible in the public page and are not independently certified by this record. No additional survey or learning activity is requested.

The public source requirement and optional binary distribution are separate. No extra feature work is required by this checklist.

## Revisions
- 2026-09-28 submission confirmation: participant supplied the published project URL and reported submission. Anonymous HTML retrieval confirmed the project title, contest association, repository link and YouTube embed; anonymous oEmbed confirmed video metadata. Recorded completion without claiming full hosted playback, private survey visibility, exact local-video equivalence or a selected submission commit/tag. Documentation only; product scope, code, assets and licensing are unchanged.
- 2026-09-27 demo refinement: owner requested a 45–60-second silent demonstration with clearer real feeder input and no product changes. Prepared and reviewed take-05 after rejecting takes with remote input interference, snap UI or obscured emission. Same 499-file Release payload; protected code/assets/licensing and unfinished work unchanged. Updated only filming evidence and submission status; no scope expansion, upload, GitHub push or submission.
- 2026-09-27 Sandbox recording: owner requested filming in a disposable desktop with work windows and a suitable wallpaper. Created an 88.73-second local silent draft from public source `88ed4f6`; no application, existing asset, dependency or scope change. Calculator was absent, so the guest used Explorer with two Edge windows. Filming evidence and the new backdrop's provenance are recorded in `../docs/demo-recording.md`; owner review/upload remain open.
- 2026-09-27 final source acceptance/publication: the owner accepted the current implementation after relaunch and requested final documents plus GitHub synchronization. Closed the source review using that acceptance and existing proportional regressions; separated optional future ZIP/clean-room/notice work without claiming it ran. Refreshed the local map and recorded an evidence recap, not a new hands-on tour. Submission prose/video/survey/tag remain open; no product or license scope changed.
- 2026-09-27 feeder object/drop request: the owner asked for the canister to behave as a desktop object rather than a visible panel. Updated the stationary-release plan to gravity toward the primary work-area floor; retained held-only shake feeding and all fish behavior. Existing assets and dependency/licensing boundaries are unchanged. Source verification and final participant acceptance are distinguished in `../docs/feeder-object-verification.md`.
- 2026-09-27 rights/publication preparation: owner explicitly requested a public repository while retaining a future proprietary Steam option. Added unmodified PolyForm Noncommercial source terms with bounded scope, separate project-asset permissions/provenance, and exact third-party notice records. Official Rules distinguish mandatory public access from recommended open-source licensing; no OSI-open-source or guaranteed-eligibility claim is made. Final Review, binary-release work and final submission remain separate. No app code or product scope changes.
- 2026-09-27 native display size: the participant explicitly requested 100%. Removed only renderer fit-to-logical-bounds reduction, retained `.72 + .14 * visualDepth`, and based display culling on the actual sprite rectangle. Source PNGs/atlas and all Core behavior remain unchanged. Classification: optional visual refinement, no scope expansion. Verification and current-source versus historical-package status are recorded in `../docs/fish-runtime-verification.md`.
- 2026-09-27 approved-frame integration: participant explicitly accepted the 32 PNGs. Packed unchanged RGBA pixels into fish-sprites.png/JSON, replaced fixed crop lookup with validated metadata, and fitted a common per-species canvas proportionally inside existing logical bounds. Core/movement/feeding/depth/occlusion are unchanged. Release build, 66 core tests, 69 WPF rendering checks, source and packaged 18 feeding/25 lifecycle checks, 489 package hashes and bundled-runtime startup passed. Current package clean-room and final running-package learner review remain open. Evidence: `../docs/fish-runtime-verification.md`.
- 2026-09-27 sprite extraction: classified as optional visual polish inside accepted Final Review, with no product scope change. The earlier runtime atlas and cell-based cleaner cannot establish correct separation from the original preview. Added a source-pinned, per-sprite extraction and review path; 32 PNGs/masks, 225,983 retained RGB pixels unchanged, four-pixel transparent padding, unique frame hashes and independent mask reproduction pass. Headless review-page checks pass. Existing runtime source/assets are untouched by this pass; original alpha was flattened and cannot be recovered exactly. Details: `../docs/fish-sprite-verification.md`.
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

- G4 clean-room: offline-native-05 passed no-SDK/no-network startup, package-local .NET 10.0.12 loading, 489 payload hashes, 18 feeding checks, 25 lifecycle checks, clean exits and post-test payload integrity. Earlier guest attempts are retained as verifier-race failures. Product source was unchanged. The actual-package learner check remains before the outer G4 box is ticked.

- G4 learner check: the owner used the actual package-02 build after the clean-room pass and reported that it worked well. Diagnostics showed five fish, feeder resting, 9 emitted / 9 consumed, and the app remained alive. This completes G4 only; Final kick-the-tires and Final Review remain separate and unchecked.

- Final kick-the-tires feedback: learner requested four presentation refinements before ship readiness ? visibly different fish species/silhouettes, toward/away poses, depth perspective tied to existing bands, and a solid feeder that does not reveal the work window behind its body. These are accepted as bounded Final Review refinements; collection/rarity/free-3D scope remains excluded.
