# Release-candidate verification after RDP reconnection

## Current result

The user elected to keep RDP connected rather than transfer to the dummy-display console. Input-desktop access and foreground lookup succeeded. No console-transfer command, elevation, display-setting change, security-policy change or public publishing was performed in this pass. The prior development aquarium was closed through its own tray before testing the actual extracted package.

The candidate remains `artifacts/packages/pre-submit-01/DesktopAquarium-win-x64.zip`, runtime 10.0.12, application source `12baa4d`. Its 489 inventory hashes were checked again. No application source, sprite, product behavior or package bytes were changed by this verification pass. Test fixture placement/activation was corrected for the reconnected desktop.

## Executed checks

| Check | Result and evidence |
| --- | --- |
| Current source locked restore / Release build | Passed; build reported zero warnings/errors with the existing documented project exception unchanged |
| Core tests | 64 passed; `artifacts/pre-submit/rdp-recheck/tests/rdp-resume.trx` |
| Actual extracted-candidate feeding | 18 passed; `rdp-recheck/feeding/report.json` |
| Lifecycle / tray / cancellation | 25 passed again with the final fixture changes; `rdp-recheck/lifecycle-final/report.json` |
| Real Edge F11 / maximize distinction | 7 passed; `rdp-recheck/browser/report.json`, using a separate test profile and local page |
| Bundled runtime loading | Passed for 10.0.12; `rdp-recheck/startup.json`. Child PATH/DOTNET_ROOT tests do not make the host SDK-free or network-isolated |
| Recorded live feeding rehearsal | 18 checks passed during recording; `artifacts/pre-submit/demo/native/report.json` |
| Short ordinary / feeding / hidden measurement | All three approximately five-second phases and normal exit passed; `rdp-recheck/performance-short-final/report.json` |

Receipt paths abbreviated above are under `artifacts/pre-submit/`. All native observations are RDP, not local-console certification. The initial reconnected display was 1512 x 949 at 100%; it later changed to 1008 x 623 at 100% without the agent changing display settings. The successful movie used the smaller display. Tests using simulated display/TaskbarCreated messages remain labelled as simulations, not physical monitor changes or an Explorer restart.

## Real recording, not final submission footage

Original: `artifacts/pre-submit/demo/feeding-rehearsal-1790399209158235000.mp4`.
Duration: 7.95 seconds; dimensions: 888 x 422; bytes: 102986.
The clip records the actual packaged candidate over an opaque test-owned work window. Physical held pointer input drives the real food generation and consumption. It has no authored narration and does not show the actual Desktop shortcut icon. It is a local rehearsal, not an uploaded or owner-approved final demo.

A reduced preview (`feeding-small-preview.mp4`, 480 x 228, 8 fps) was transferred for chat review and matched SHA-256 `9346bd8ea5388f6f6f821da508786ff5884f3ecabe797b7da5a7f7917265eb89`. The local preview decoded without errors. One-second sampled frames showed only the test-owned background and application objects; final original-video privacy/content review remains for the owner.

## Resource samples and limits

The earlier three-phase 60-second attempt did not complete: ordinary and held-shaking phases each ran for approximately 60 seconds, but the test's later tray-menu lookup timed out. A second attempt stopped on a foreign-foreground safety check. These are retained as unsuccessful full-run attempts, not labelled as passes. After fixture activation corrections, all three short five-second phases passed. The app was not rewritten to make the tests pass.

The completed portions of the long attempt measured about 0.4351% / 0.2171% app CPU (all 32 logical processors), 138.08 / 143.27 MiB working set at phase end, and 20.73 / 20.79 render callbacks per second for ordinary/feeding respectively. Feeding reached the configured 64-pellet cap. These measurements come from the incomplete run and must not be presented as a completed sustained benchmark.

Final short-run measurements:

| Phase | Seconds | App CPU (32 logical processors) | End working set (MiB) | Render callbacks/s |
| --- | ---: | ---: | ---: | ---: |
| ordinary habitat | 5.04 | 0.4072% | 138.66 | 18.66 |
| held shaking / feeding | 5.05 | 0.3774% | 143.96 | 20.41 |
| manual hidden | 5.05 | 0.1258% | 146.88 | 0.00 |

Hidden drawing/emission stopped in the short sample. Diagnostic output was enabled and other host workloads were present; the environment was not performance-isolated. Callback interval/CPU elapsed metrics are bounded local WPF samples, not compositor/GPU frame latency. GPU utilization was not measured. No long-duration leak-free, battery, performance or broad display-compatibility claim follows.

## Test setup repairs

Sparse fixed-coordinate targets were covered after RDP reconnected at a different size. The fixtures now locate their own exposed area. If none is exposed, only the temporary test fixture is briefly staged topmost and then returned to ordinary non-topmost placement before aquarium verification; no user window is resized or minimized. The browser activation point is below its toolbar rather than on window chrome. Native target/focus ownership checks remain.

The feeding tool now opens through `--feed` after moving the pointer over the owned work fixture. This avoids having the tool start beneath a protected shell surface left under the original pointer. A native inspection identified that shell hit target; it was not clicked, disabled, or bypassed by changing aquarium z-order. The shell-overlap case is not certified as a supported interactive region.

A scripted helper edit initially removed the feeding harness's setup globals and caused a NameError. They were restored and the full recorded feeding run subsequently passed. Longer sampling also exposed foreground/tray setup limitations; the corrected shorter measurement completed. Product assertions were retained; unsuccessful setup attempts are not application passes.

## Remaining gates

G4 remains open for genuinely separate SDK-free/offline execution, full-duration measurement as planned, and final owner package review. There is no accessible Windows Sandbox installation on this host; the prepared guest-network-disabled kit has not executed. Local-console, actual other DPI/session cases, games/presentations and final video quality remain unverified where not explicitly recorded.

Final project name, project-source license, public GitHub/video links, participant-authored submission fields and exit survey remain owner tasks. No final review, learning activity, public release or Devpost submission is inferred from these tests. HTML and learner-profile documents remain Git-ignored.
