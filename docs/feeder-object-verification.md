# Feeder object and falling refinement

Owner-requested optional interaction refinement, 2026-09-27. Source implementation changes the previous stationary release into a vertical drop onto the primary work-area floor above the taskbar. After relaunching the updated app, the owner accepted the current implementation and requested submission preparation; current source/Release Final Review is complete.

The existing opaque canister sprite is rendered in a transparent WPF tool window with a small close button. The panel, border and permanent instruction text are gone. Existing asset pixels are unchanged. Nozzle placement preserves the existing food origin; fish movement, feeding calculations, depth and occlusion code are unchanged.

The feeder can be picked up while falling or at rest. Only physical held motion enters shake detection. Gravity uses the host fixed steps, pauses while suppressed, resets on cancellation/pickup and clamps to changed work areas. It adds no bounce, throwing, arbitrary-window collision or dependency.

## Mechanical verification

- Release build: passed with zero warnings/errors.
- Existing Core suite plus seven feeder-fall cases: 73 passed. Cases cover landing, catching/releasing, closed state, work-area changes, undersized work areas, suppression timing and no automatic food from falling.
- Native feeding / per-pixel transparency: 23 passed, including actual falling/landing, no automatic food/capture, transparent-corner pixel and click-through checks, opaque-body pixel/hit checks, pickup/lifting/shaking, visible food consumption, close and real shortcut reuse.
- Native lifecycle: 27 passed, including physical pickup during a fall, no movement/food while held still, Hide/Show and fullscreen pause, capture cancellation, simulated display/tray notifications, repeated activation and normal Exit.

Native fixture adjustments wait for landing and use reported hit points/dimensions; feeding fixtures deliberately lift the canister before shaking. Existing defaults are retained for older package reports. Runs target only test-owned windows and the aquarium, preserve the cursor and use bounded normal exit. Artifacts stay in ignored `artifacts/feeder-object/`, with final reports in `feeding/report.json` and `lifecycle-catch/report.json`. The checked `feeding/feeder-object.png` crop shows the real canister over a test-owned background, not a design mockup. The RDP session was tested at 100% scaling; no real resolution/session change or Explorer restart was performed.

Changed Python fixtures passed syntax checks. G0 and measurement-helper hit points were adapted, but their full runs were not repeated; no new resource/performance claim is made. Source comparison confirms that existing fish movement, feeding, depth, visibility rules, renderer, asset bytes and licensing documents are unchanged. Relative Markdown paths and the configured credential-pattern checks pass. The pre-existing dirty legacy atlas and untracked cleaner remain untouched.

## Remaining review and distribution

Participant acceptance is recorded on 2026-09-27 after relaunching the updated app. This is overall acceptance of the current PoC, not a claim that every listed native test was repeated manually or that other display environments were checked.

The implementation commit did not itself publish a ZIP or update GitHub. The owner subsequently authorized publication of that source and the final technical documentation. Current publication/submission state is tracked in [submission readiness](submission-readiness.md). Archived ZIPs retain the earlier feeder behavior; no old clean-room/performance result transfers to changed bytes. Other DPI/display configurations remain unverified.

Implementation basis: [WPF AllowsTransparency](https://learn.microsoft.com/dotnet/api/system.windows.window.allowstransparency) and [Win32 layered-window hit testing](https://learn.microsoft.com/en-us/windows/win32/winmsg/window-features). The native checks, rather than documentation alone, establish behavior in the tested session.
