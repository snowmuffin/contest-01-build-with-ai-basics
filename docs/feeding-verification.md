# Feeding prototype verification

## Current stage

G0 is accepted by the learner and committed as `b9d361a`. Slice 2 (real feeding) is implemented and mechanically tested. The learner watched the running test and gave positive feedback; the actual Desktop shortcut has now been installed under an explicit grant and launched successfully. A detailed user-reported launcher/feed sequence has not been inferred from that feedback. This is not a release or a claim that all lifecycle/compatibility scenarios pass.

## Executed evidence

- Release build: passed, zero reported warnings or errors. The existing project-scoped WFO0003 exception remains documented; no new analyzer suppression was introduced.
- Core tests: 54 passed, 0 failed, 0 skipped. Test receipts: `artifacts/feeding/test-results/feeding.trx`.
- G0 native regression: 25 passed after adding `--g0` to select the original probe.
- Native feeding harness: 18 passed in `artifacts/feeding/native/report.json`. The harness creates actual Win32 work windows and uses physical pointer/button events targeted only to those fixtures and the app's feeder. It does not call an internal food-spawn API.
- First native feeding cycle: 4 detected shakes emitted 12 pellets; a fish visibly consumed food. A second real input cycle also produced consumption with the native work window maximized.
- An actual `.lnk` in the controlled workspace opened/reused the existing resident and feeder; repeated direct executable activation also passed.
- Native screenshot: `artifacts/feeding/native/feeding-live.png`, captured only over the opaque, test-owned background. It shows rendered fish and food, not a conceptual mock-up or the user's private desktop contents.

Native execution environment remains Windows 11 x64 / build 26200, RDP session, primary 2160 x 3840 display at 150% scaling. These results do not certify a local console, another monitor configuration, browser F11, presentations, or games.

## Native feeding checks

| Check | Result |
| --- | --- |
| actual world has five fish, no G0 markers substituted | Pass |
| feeder opens resting without food | Pass |
| native test background created | Pass |
| actual native fixture is foreground | Pass |
| one-way relocation does not dispense | Pass |
| physical held drag emits actual pellets | Pass |
| release leaves emitted pellets available | Pass |
| fish visibly approaches and consumes live input food | Pass |
| feeding does not create replacement fish | Pass |
| normal cursor never emits after release | Pass |
| recorded meals are visible foreground contact | Pass |
| pellet accounting is consistent | Pass |
| X closes only the tool while fish continue | Pass |
| repeat executable activation reuses resident and feeder | Pass |
| maximized ordinary window still permits live aquarium | Pass |
| visible consumption also works over maximized window | Pass |
| same five identities after maximized-window feeding | Pass |
| actual feeder shortcut reuses the same resident | Pass |

## Core coverage and repair

Tests cover no-food while closed/resting, held shaking, jitter/single sweep/slow motion, sample reset and long gaps, cap and expiry accounting, visible single consumption, same fish IDs through window-depth transitions, speed-bounded edge travel, deterministic seed/input, intermittent cursor curiosity, suppression freeze/cancel, resize cancellation and new-session reset.

A test exposed an actual post-feeding boundary jump. Only destinations are now clamped; fish move back into the work area without snapping. The speed-invariant test was retained and passes. Initial C# name resolution and MSTest assertion-style findings were fixed rather than suppressing their diagnostics.

## Desktop launcher status — resolved

After the learner reported approving access, `request_path_access` returned a successful Desktop grant. Only then was `Create-FeederShortcut.ps1` executed against the actual current-user Desktop. It created `Feed Fish.lnk` with the expected executable, `--feed` argument, working directory and bundled feeder icon. Re-running setup reused the same file without changing its SHA-256.

Two verified launches through the real Desktop shortcut produced `open-feeder` events and settled on one existing resident, one existing feeder window, and a visible resting tool. Raw evidence: `artifacts/feeding/desktop-shortcut-verification.json` (local-only). No other desktop item or security setting was changed, and no application source was changed for this resolution.

The first immediate launch assertion failed after the open event; it combined process-count, resting-state and visibility checks before waiting for settlement. It is not counted as a passed attempt or diagnosed as an application defect. The subsequent checks wait for the short-lived forwarding process to settle and record the actual feeder state. Both passed. No synthetic mouse input was sent in this task.

Live-session diagnostics also showed hold/release activity and food generation/consumption outside the native fixture runs (three holds, 24 emitted pellets and 11 consumed at the recorded observation). These are observed application counters, not a claim that the learner personally performed every prescribed test or clicked the Desktop icon.

Previous directory-grant failures are historical, not a current blocker. `Setup-FeederShortcut.cmd` remains a convenience for future local setup; it no longer needs to be run to install this machine's existing shortcut.

## Pending evidence

- User-operated Desktop launcher/feed check. Positive feedback after watching the live feeding test has been received; do not infer which mouse actions the learner performed.
- Extended fullscreen/media/game/system-menu, lock/reconnect, local-console and DPI/display matrix (slice 3).
- Self-contained ZIP, controlled no-SDK/offline run, sustained resource measurements and source/publication audit (slice 4 / ship).
- No performance guarantee follows from using small pixel images. Runtime performance has not been benchmarked for this feeding version.

Generated test reports/images stay under ignored `artifacts/`. The personal learner profile and `devpost/*.html` remain excluded from commits.

## Feedback follow-up

The learner positively reviewed the running feeding test and requested no change. Locked restore and Release build were repeated successfully, with all 54 core tests passing again (`artifacts/feeding/test-results/feedback-review.trx`). Existing native receipts were inspected, not rerun. No new browser/game/local-console or lifecycle coverage is claimed.

Earlier access requests failed at the tool level. The later successful grant and actual installation supersede that blocker; see Desktop launcher status above. The helper remains policy-preserving and no elevation was requested.

The feeding source remains uncommitted until the remaining practical checkpoint is resolved; G3 has not been advanced or marked passed.

## Feeding milestone accepted for continuation

After positive feedback on the running test and confirmed real Desktop launcher setup, the learner explicitly requested continuation. The milestone is accepted; it does not certify an unreported detailed manual sequence, local-console use, every fullscreen application, or final release readiness. Live-session holding/emission/consumption counters and agent-performed shortcut launches remain separate evidence. The existing 54 core tests passed again in `G2-accepted.trx`. No new native test pass is inferred from this documentation/commit task. G3 and the final hands-on review retain the remaining checks.
