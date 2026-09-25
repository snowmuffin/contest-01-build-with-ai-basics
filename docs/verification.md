# G0 verification record

For the newer live feeding implementation and its pending checkpoint, see `feeding-verification.md`. The G0-specific results below are retained as the first-slice record.

## Status

G0 native probe is implemented and accepted for continuation after the learner reported that it appears to work. This is general hands-on feedback, not certification of each application or environment. **This is not a finished aquarium and no fish feeding exists yet.** No public release has been made.

## Executed environment

Windows 11 x64 (host previously reports build 26200), primary display 2160×3840, 150% scaling, session 2. `GetSystemMetrics(SM_REMOTESESSION)` returned 1: **these native checks ran in RDP**, not a verified local-console session. SDK 10.0.202; installed Windows Desktop runtime 10.0.6. Version observations are not a latest-servicing claim.

## Build and pure-core checks

- `dotnet restore Aquarium.slnx --locked-mode`: passed.
- `dotnet build Aquarium.slnx -c Release --no-restore`: passed, zero reported warnings/errors.
- `dotnet test tests/Aquarium.Core.Tests/Aquarium.Core.Tests.csproj -c Release --no-build`: 26 passed, 0 failed, 0 skipped.
- Core has no project or package reference to Windows/WPF/WinForms and no native imports. Its tests use synthetic geometry only; native evidence is separate below.
- One explicitly documented Windows-project WFO0003 suppression is intentional: WPF owns process DPI through the manifest, with WinForms used only for the tray. Other warnings remain errors. No global warning suppression or machine DPI change was made.

References for that narrow DPI decision:
https://learn.microsoft.com/en-us/dotnet/desktop/winforms/compiler-messages/wfo0003
https://learn.microsoft.com/en-us/windows/win32/hidpi/setting-the-default-dpi-awareness-for-a-process

## Real native fixture checks

`python scripts/Verify-G0Native.py` creates two temporary native Win32 windows in a separate process from the WPF aquarium. It verifies hit-test ownership before sending bounded test input, observes actual screen pixels only over its own fixture, and restores the pointer/cleans up its windows. It does not send input to the user's existing apps. Fixture geometry is real, not a browser mock; that still does not establish compatibility with every normal application.

Latest final rerun: all 25 checks passed; the timed application exit returned 0. Raw local evidence is `artifacts/g0/native/report.json`, `state.json` and `fixture-composition.png`. Unit test evidence is `artifacts/g0/test-results/g0-final.trx`. These generated details remain Git-ignored.

| Check | Result |
| --- | --- |
| process entered interactive session | Pass |
| passive overlay is layered, noactivate and transparent | Pass |
| two native fixture windows created | Pass |
| fixture B is actually foremost after controlled click | Pass |
| passive habitat did not activate its own process | Pass |
| middle clipped where foremost window covers it | Pass |
| middle drawn above rear window | Pass |
| front drawn above ordinary windows | Pass |
| rear clipped by work window | Pass |
| opaque marker routes hit test to fixture | Pass |
| transparent area routes hit test to fixture | Pass |
| real injected click delivered through opaque overlay | Pass |
| wheel delivered through transparent overlay | Pass |
| fixture receives drag through passive overlay | Pass |
| middle returns when B raised | Pass |
| middle occlusion follows changed order | Pass |
| feeder owns native capture after deliberate pickup | Pass |
| captured feeder actually moved | Pass |
| release clears capture and rests feeder | Pass |
| ordinary maximize does not suppress habitat | Pass |
| foreign borderless fullscreen suppresses both surfaces | Pass |
| hidden render count stops | Pass |
| fullscreen exit restores feeder resting | Pass |
| X closes feeder but not habitat | Pass |
| second launch reuses original process | Pass |

## Repairs and limits discovered

The first native attempt found over-broad suppression for a visible but inactive `XamlExplorerHostIslandWindow`. Its known region is now masked, while an active system interaction can still suppress the overlay. Fullscreen tests were repeated after this repair.

The fixture could not assume background `SetForegroundWindow` succeeded. Tests initially observed a different application's foreground and then an incorrect assumed foremost test window. The final harness checks its own target, activates via a controlled fixture-only click and confirms order before asserting pixel colors. The earlier attempts are not counted as passed tests.

G0 markers were placed toward the left side of the primary display to keep the controlled fixture away from an unrelated work window. No existing user window was closed, resized or repositioned. The markers are temporary rectangles labelled G0 REAR / MIDDLE / FRONT, not final fish artwork.

## Explicitly pending — do not mark these as passed

- Detailed named-application/local-console coverage remains to be recorded. The learner completed the general hands-on checkpoint and reported no issue, without identifying which specific cases were exercised.
- Actual browser F11, fullscreen video, a presentation and an available fullscreen game. The automated positive case was a controlled native borderless-fullscreen fixture, not those apps.
- Local-console execution, other DPI/display configurations, lock/disconnect/reconnect and display changes. The tested RDP geometry is not broad supported-environment evidence.
- Start/Task View/system menus, unusual transparent/rounded/topmost windows, Explorer restart and sustained performance. The rectangle mask remains an approximation.
- Full fish behavior, shake-to-feed and consumption (slice 2); extended lifecycle matrix (slice 3); self-contained offline package and clean-environment run (slice 4).

The scheduled G0 hands-on checkpoint is accepted. Proceed to slice 2 while retaining the unrun compatibility matrix above for later verification; do not represent the RDP result as local-console evidence.

## Try the probe

From the repository root:

```powershell
dotnet run --project src/Aquarium.Windows/Aquarium.Windows.csproj -c Release -- --feed
```

Or double-click `scripts/Start-G0.cmd`. The notification-area icon offers Open feeder / Hide / Show again / Exit. Feeder X closes only the feeder. Use the tray Exit to stop the whole probe.
