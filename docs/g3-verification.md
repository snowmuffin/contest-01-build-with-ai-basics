# G3 desktop coexistence and lifecycle verification

## Status and limits

The implemented G3 behavior has passed the tests listed below. Fast-mode final hands-on review remains pending; this is not release approval or broad Windows compatibility certification. G2 was committed as `d2f35a4` after the learner's positive review, Desktop launcher verification and instruction to continue.

Observed native environment: Windows 11 x64, build 26200, RDP session 2, primary 2160 x 3840 display at 150% scaling. The real Edge test used a separate workspace-local profile and an offline local HTML fixture; no existing user browser tab/profile was controlled. No global resolution, DPI, session lock/disconnect, Explorer restart, security policy or startup setting was changed.

## Build and regression

- Locked restore and Release build passed; no reported errors or warnings. The existing narrowly documented WFO0003 exception remains; no new warning suppression was added.
- 64 core tests passed (`artifacts/g3/test-results/G3-final.trx`): the prior 54 plus ten lifecycle/clock tests.
- 25 G0 native regression checks passed again on the new build.
- 18 live feeding native checks passed again on the new build, including normal/maximized work windows and the actual controlled `.lnk`.
- G3 adds 25 lifecycle checks, 7 actual-browser checks and 3 malformed-client protocol checks, detailed below. These categories are not 35 different applications or environments.

## Repairs and implementation refinements

1. A queued render could still draw after Hide. Both rendering surfaces now reject rendering while not visible. The unchanged native freeze assertion then passed with identical before/after simulation time and frame count; it was not relaxed.
2. `SimulationClock` discards hidden time and permits only three fixed-step updates after a visible stall. The first restored tick rebases instead of advancing a hidden-time backlog.
3. Lock and disconnect are independent flags. Reconnection does not clear a lock, and unlocking does not falsely reconnect a session. These flag sequences were unit-tested; real disconnect/lock tests remain unrun.
4. WM_CANCELMODE, deactivation and display-change notifications cancel a held feeder and clear shake history. Native display/DPI hooks invalidate geometry before recovery. The native test sends a display-change notification to this app only; it does not change the actual screen configuration.
5. The tray's own menu temporarily suspends the habitat; closing it respects manual Hide and other guards. Disposal stops the timer, tray, native hooks and capture before reporting Exit.
6. Local activation now waits for a bounded acknowledgement after dispatcher handling, retries startup races, and acquires the actual mutex ownership rather than relying on object creation. Unknown 8-byte input is rejected; a truncated client times out; valid launch works afterward. No new network listener or command category was added.

## Executed checks

### Controlled Windows lifecycle

Receipt: `artifacts/g3/native/report.json` (local and Git-ignored).

| Check | Result |
| --- | --- |
| actual feeding host is running | Pass |
| controlled real work window created | Pass |
| work fixture foreground established | Pass |
| actual tray Hide removes both surfaces | Pass |
| manual Hide freezes drawing and simulation | Pass |
| feeder launch cannot override manual Hide | Pass |
| fullscreen protection coexists with manual Hide | Pass |
| fullscreen exit does not undo manual Hide | Pass |
| tray Show restores only a resting feeder | Pass |
| WM_CANCELMODE releases captured feeder | Pass |
| external work window gains focus for interruption test | Pass |
| deactivation cancels held input | Pass |
| fullscreen during holding clears capture and tool | Pass |
| fullscreen stops simulation, redraw and emission | Pass |
| fullscreen recovery cannot resume old hold | Pass |
| simulated display-change notification cancels drag | Pass |
| display-change recovery leaves feeder inside primary display | Pass |
| ten rapid launches all receive handled-command acknowledgements | Pass |
| rapid launches preserve resident, feeder and no automatic pickup | Pass |
| simulated TaskbarCreated keeps tray menu usable | Pass |
| restoration after tray recovery keeps ordinary input | Pass |
| ordinary maximize remains distinct from fullscreen | Pass |
| actual tray Exit terminates the resident normally | Pass |
| exit stops timer, tray, hooks and capture | Pass |
| exit destroys both native windows | Pass |

### Actual isolated-profile Edge F11

Receipt: `artifacts/g3/browser/report.json` (local and Git-ignored).

| Check | Result |
| --- | --- |
| isolated-profile Edge window identified | Pass |
| only test-owned browser gets F11 input | Pass |
| normal maximized Edge keeps habitat visible | Pass |
| actual Edge F11 hides fish and feeder | Pass |
| Edge fullscreen freezes world and rendering | Pass |
| leaving Edge F11 restores resting feeder | Pass |
| no unsolicited food after fullscreen cycle | Pass |

### Local instance protocol

Receipt: `artifacts/g3/protocol/report.json` (local and Git-ignored).

| Check | Result |
| --- | --- |
| unknown command rejected | Pass |
| truncated client timed out | Pass |
| valid launcher works after both malformed clients | Pass |

## Test mechanics and unsuccessful attempts

The lifecycle harness opens the application's actual NotifyIcon menu through its native callback in the controlled test, then clicks the real menu items. It does not add a production debug command endpoint or click unrelated applications. The callback/message mechanism is test-only and may need adjustment if the framework changes. Process and geometry ownership are checked before synthesized input.

The first Hide freeze check failed before the hidden-render repair and is not counted as passed. The first isolated Edge startup did not identify a usable window in time; no F11 input was sent to an unidentified window. A later run identified the separate-profile window and passed all seven checks. These are actual test outcomes, not inferred compatibility. The protocol script's checks and clean timed exit passed; an outer PowerShell runner initially misread a stale `$LASTEXITCODE`, which was a harness status issue, not a failed protocol assertion.

## Explicitly unrun

- Local-console execution and other Windows/device configurations.
- Real resolution/DPI changes, session locking/disconnection/reconnection and Explorer restart. Simulated messages and unit tests do not certify these integrations.
- Actual fullscreen games, exclusive-D3D applications, media-element fullscreen and presentation software. Actual Edge F11 and native borderless-fullscreen fixture behavior are covered, not all of these.
- Unusual translucent/rounded/topmost windows and every shell surface. Rectangle masking remains an approximation.
- Sustained CPU/GPU/memory measurements, no-SDK/offline clean environment and self-contained release package (G4).

## Technical references

Production and harness choices were checked against official documentation/source, not third-party snippets:
- https://learn.microsoft.com/en-us/windows/win32/hidpi/setting-the-default-dpi-awareness-for-a-process
- https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getdpiforwindow
- https://raw.githubusercontent.com/dotnet/winforms/main/src/System.Windows.Forms/System/Windows/Forms/NotifyIcon.cs

The application still uses the approved C#/.NET 10 WPF/Win32 host and portable core. No cloud/API dependency or gameplay feature was added.
