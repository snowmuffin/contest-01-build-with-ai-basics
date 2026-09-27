---
doc: spec
status: approved
---

# Desktop Aquarium — Technical Spec (working label)

## Public-source licensing preparation — 2026-09-27

The owner authorized public-repository preparation with PolyForm Noncommercial 1.0.0 for project-owned source, tests and build scripts/configuration. `../LICENSE` preserves the official text unchanged; `../LICENSING.md` defines scope and separate contest permissions. `../ASSET_NOTICE.md` governs project-created assets with AI-output rights limitations. Dependencies and curriculum retain their own terms in `../THIRD_PARTY_NOTICES.md`; runtime-pack notices are now distinguished from the earlier runtime ZIP notices. This is source-available/noncommercial, not OSI-approved open source. It does not satisfy the Rules' open-source recommendation; no automatic eligibility approval is claimed.

Publication target: `https://github.com/snowmuffin/contest-01-build-with-ai-basics`; actual public access is recorded in `../docs/submission-readiness.md`. Keep source publication separate from binary distribution. Existing ZIPs predate the new licensing documents; before a public binary release, carry the new root licensing documents and matching dependency notices into the package and verify its inventory. The current publish script has not been changed in this task. No application behavior, dependencies or build output are changed.

After the owner selects the final submitted version, record its exact commit and create a fixed tag such as `v0.1-contest-submission`; never move that tag to later commercial work. No such tag is created now. Subsequent Steam development may use another branch or private commercial repository, respecting existing grants and third-party rights. This is a handoff plan, not implementation of a Steam edition.

## Current feeder object refinement - 2026-09-27

The owner requested removal of the feeder panel and gravity after release. `FeederWindow.cs` now uses an alpha-transparent 80x112 DIP WPF tool window: the existing 60x72 canister is positioned at (4,40), keeping its nozzle at (34,112), just above the unchanged food origin (34,116). Only sprite pixels and a small X are visible; there is no surrounding panel or permanent label. Transparent pixels pass through native input.

`FeederFall.cs` adds bounded vertical presentation motion to the existing Closed/Resting/Held state: Resting means unheld, which may be falling or landed. It clamps to the current work area, accelerates downward, stops on its floor, resets velocity on pickup/cancellation, and never submits held-motion samples. The existing host fixed-step clock advances it only while allowed/visible, so hidden time cannot accumulate into a jump. Fish movement, feeding calculations, depth and occlusion are unchanged. No external dependency or general physics engine is added. Existing native fixtures use reported object dimensions/hit points and deliberately lift the canister before shaking. Verification and current source acceptance: `../docs/feeder-object-verification.md`.

## Current Implementation and Asset Review — 2026-09-27

G0–G4, the initial package learner check and the current source/Release Final Review are complete. After the updated app was launched, the owner accepted the present implementation and authorized final documentation/GitHub synchronization. Latest source evidence: Release build with zero warnings/errors, 73 Core tests, 23 native feeding/transparency checks and 27 lifecycle checks. The unchanged native-size renderer has 73 WPF checks. No new binary release, video, submitted entry or contest tag is implied. The canonical current state is `checklist.md > Current Execution Status`.

The approved blueprint and dated evidence below preserve earlier decisions and test checkpoints. Past statements such as "G4 remains incomplete" or "pause until restart" describe those checkpoints, not current instructions. Current source behavior is described here and in the feeder section above; optional binary release requires refreshed package verification and notices.

Local demo preparation: an 88.73-second silent Windows Sandbox recording now demonstrates public source `88ed4f6` with two Edge windows, Explorer and a separately generated recording wallpaper. Application code and existing assets are unchanged. The recording is local-only and awaits participant review/upload; see `../docs/demo-recording.md`. This does not create a product wallpaper feature or certify a public binary release.

The participant inspected and approved all 32 independently extracted PNGs for runtime integration on 2026-09-27. `assets/fish/approval.json` pins that approval to the source and exact frame-set hashes. `scripts/Extract-FishFrames.py` preserves the SHA-256-pinned 1448x1086 preview, individual source regions and masks under `assets/fish/`; each sprite retains original RGB/resolution and four transparent padding pixels. Historical extraction receipts remain the record of preparation before approval.

The source has alpha 255 everywhere. Transparency is a reproducible binary mask (maximum RGB channel above 30, plus enclosed dark holes of at most 64 pixels), not recovered original alpha. Detached foreground fin fragments are retained. The extraction receipt records source coordinates, output/mask hashes and mechanical checks; it is audit data, **not runtime atlas metadata**. Pillow 11.0.0 is a development-only tool dependency already available in the environment; no runtime dependency was added.

`scripts/Pack-FishAtlas.py` verifies that approval and deterministically packs the approved PNGs unchanged into `Assets/fish-sprites.png` (1024x821) and `Assets/fish-sprites.json`. Rectangles have variable sizes, preserve each PNG's RGBA bytes and transparent padding, and add two-pixel gutters. Metadata maps the complete Species/Facing/Frame matrix to rectangles plus a shared centered canvas per species. No preview-sheet grid arithmetic, resampling or rotation occurs during packing. `--verify` checks approval, all round trips, non-overlap and gutters. `Generate-Assets.py` validates these resources and regenerates only the original feeder/icon.

`Rendering/FishSpriteAtlas.cs` loads the embedded PNG/JSON once, validates dimensions and the 32 unique mappings, and freezes cached crops. Following the participant's 100% display-size request, `SpriteRenderer.cs` maps one source pixel to one DIP at Front, retaining the existing interpolated Middle 0.86 / Rear 0.72 depth scale and nearest-neighbour sampling. It no longer fits images inside the logical 68x40 fish bounds. Centered metadata offsets preserve aspect ratio and alignment across frames/directions; display culling uses the actual drawn rectangle so a partially visible large sprite is retained. Windows DPI scaling still applies: source pixels map 1:1 to physical pixels at 100% OS scaling. Existing simulation geometry, animation cadence, depth scale, clipping masks, food and spark logic are unchanged. The old dirty `fish-atlas.png` is preserved locally but is excluded from embedded resources and no longer consumed. No Core, movement, feeding, depth, occlusion or feeder logic changes are made.

The logical feeding/contact and depth-transition bounds remain 68x40. Native-size artwork is larger than those bounds. The participant accepted the current presentation for the PoC; this is not a claim of pixel-perfect mouth alignment or exhaustive depth-transition coverage. The existing `artifacts/fish-runtime/package-01/` archive predates 100% rendering and the falling feeder; the updated source/Release build is the accepted current version.

`devpost/fish-sprite-review.html` remains the local, ignored original/PNG/mask review. Artwork approval permits integration; final running-package acceptance remains separate. See `../docs/fish-sprite-verification.md` for extraction evidence and `../docs/fish-runtime-verification.md` for current integration tests.

## How This Works, In Plain Language

The aquarium has two application projects. **Aquarium.Core** decides where fish swim, whether they are curious, whether the feeder is held, and when a food particle is eaten. It knows coordinates and commands, but nothing about Windows handles, WPF, or the screen's contents. **Aquarium.Windows** observes window geometry and pointer activity, translates them into simple inputs, and draws the core's result over the real desktop.

The fish surface is display-only and passes clicks to the user's applications. The feeder is a separate small interactive window. This separation avoids making the entire display interactive just to drag one object. For apparent depth, the renderer leaves out the parts of a fish that should be covered by a nearer work window. It never changes another application's window order. This is the selected geometric-masking approach, not a screenshot of the desktop or a replacement compositor.

This document develops the **approved** `scope.md` and `prd.md`. Windows-first, separate core/OS responsibilities, feeding-only scope, and local-only HTML reviews are learner decisions. **The learner explicitly approved the technical recommendation: C#/.NET 10 with WPF/Win32, the Windows 11 x64 primary-monitor validation envelope, geometric masking with an early feasibility gate, and self-contained ZIP distribution.** This approval completes technical planning; it is not evidence of implementation, compatibility or measured performance. The G0 integration probe and initial live feeding implementation now exist. Current implementation/evidence is recorded below and in `docs/feeding-verification.md`; unfinished components and validation remain part of the target blueprint, not completed capabilities.

Source snapshots checked on 2026-09-25:
- `scope.md`: SHA-256 `6ceb3e16d86a387bb16a0b981ddf04d17e2c755ca1b9459afc58c98902e207d1`.
- `prd.md`: SHA-256 `2ef7f76d47787aff3f202922e23cbc13582cb694dffa4c07826003da1d8ea61c`.

## The Core Journey Through the System

Implements `prd.md > The Core Journey` and `Features and Behavior`.

1. **Start:** the Windows host establishes one per-user, per-session instance, creates a tray control and a display-only habitat, and initializes a small fish population. No feeder is held at startup.
2. **Observe:** the Windows adapter supplies a versioned snapshot of relevant window bounds/order, display geometry, pointer position, and suppression conditions. The core advances autonomous movement and occasional curiosity.
3. **Open feeder:** a real desktop shortcut runs the same executable with `--feed`. An existing instance receives an allowlisted local message and reuses the feeder. Otherwise, that executable starts the aquarium and opens one resting feeder. Initial appearance is near the pointer, clamped inside the target display.
4. **Pick up:** a deliberate press on the feeder body activates that small window as needed and starts a captured drag. The body displays a held pose. Simply opening the feeder does not pick it up.
5. **Shake:** timestamped movement while held enters the core's shake detector. Qualifying back-and-forth movement releases bounded foreground food particles. A stationary hold or ordinary movement after release does not feed.
6. **Eat:** responding fish reach the foreground and approach the food; a visible contact consumes a particle once. They subsequently return to autonomous swimming. Existing fish can re-enter from a display edge when a maximized work window hides their route.
7. **Return to work:** release clears holding and new emission; the unheld feeder falls to the work-area floor. Its X closes the feeder only. Tray Hide/Show/Exit controls the aquarium. Fullscreen protection cancels holding and suppresses the habitat without stealing focus; restore never resumes a drag or overrides a manual Hide.

## Stack — Approved Approach

| Part | Approved choice | Rationale / tradeoff |
| --- | --- | --- |
| Core | C# class library targeting `net10.0` | Keep behavior and geometry independent of UI and OS; unit-test without a desktop. |
| Windows application | .NET 10 WPF, `net10.0-windows` | Direct access to desktop windows and .NET; first target is Windows. WPF is Windows-specific, not a cross-platform UI promise. [D1] |
| Fish rendering | A small retained drawing surface using WPF DrawingVisual/DrawingContext and cached PNG sprites | Avoid one framework control per particle; WPF documents lighter-weight drawing primitives. Full-display transparency still needs measurement. [D2, D3] |
| Native adapter | Small documented Win32 interop surface in the Windows project | Window geometry, display conversion, pointer sampling, event invalidation, suppression and lifecycle. No shell injection or undocumented wallpaper parenting. |
| Resident control | `System.Windows.Forms.NotifyIcon`, fully qualified, inside the WPF host | Reuse the .NET desktop tray implementation for Hide/Show/Exit; no separate dashboard. [D4] |
| Local instance messaging | .NET named mutex + named pipe, restricted to the current user/session | Deliver a fixed `ShowFeeder` command; not a network service. [D5] |
| Tests | MSTest, development-only, referencing the core | Geometry, shake recognition, state transitions and consumption. Lock resolved package versions during build setup. [D6] |
| Distribution | Self-contained `win-x64` publish directory in a ZIP | Include runtime and assets; no installed SDK or network account needed to run. Larger than framework-dependent output. [D7] |

The current workspace has .NET SDK **10.0.202** and **9.0.313** on PATH; Rust tooling was not on PATH. This is an environment observation, not a benchmark or proof of compatibility. Proposed `global.json` starts from installed SDK 10.0.202 with patch roll-forward and no prerelease selection; recheck servicing before public release. No SDK installation or update has been performed in this design step.

No application NuGet dependency is proposed beyond the .NET desktop framework. Test packages remain development-only; their exact versions are to be recorded when restored, not invented here. Use neither Native AOT nor trimming in the first WPF publish. WPF manages its layered rendering; do not independently mix its transparency pipeline with `UpdateLayeredWindow`/`SetLayeredWindowAttributes` on the same HWND.

**Alternative considered:** a cross-platform UI host would still need native window observation and platform-specific overlay checks. The recommendation deliberately prioritizes Windows integration now. Portability means reusing the pure core later; a future macOS/Linux host and renderer would still need implementation. This is not an automatic port.

## Where It Runs and How Someone Tries It

Implements `prd.md > Platform and Documentation Decisions`.

**Approved first validation envelope:** Windows 11 x64, a local interactive desktop session, and one primary-monitor habitat. Basic geometry/DPI changes must recover safely; cross-monitor ecosystems and identical RDP behavior are not promised. Windows 10, ARM64, multiple simultaneous habitats, macOS and Linux are outside this agreed first validation envelope. Target selection does not establish that any environment has passed the planned checks.

The inspected host reports Windows NT build **26200**, x64. UI evidence now exists for the documented RDP environment; see `docs/g3-verification.md` for the precise tested cases. Validation should record the actual display resolution, scaling and local-vs-remote session; also test a stable supported Windows installation before claiming broad Windows 11 compatibility. Proposed scenarios include 100/125/150/200% scaling where available. Tests in unavailable environments remain explicitly unrun.

Source build/test/run commands for the current implementation; the publish command is the G4 delivery target:

```powershell
dotnet restore Aquarium.slnx
dotnet test tests/Aquarium.Core.Tests/Aquarium.Core.Tests.csproj -c Release
dotnet run --project src/Aquarium.Windows/Aquarium.Windows.csproj -- --feed

# Preserves normal source lockfiles while producing self-contained win-x64 artifacts:
./scripts/Publish-Windows.ps1 -RuntimeVersion 10.0.12
```

Planned packaged use: extract the **whole** published directory, run `Aquarium.Windows.exe`, then run the documented `scripts/Create-FeederShortcut.ps1 -ExePath <absolute-exe-path>` once to create the app-owned desktop shortcut. That script must refuse to overwrite an unrelated shortcut; use the OS's current-user Desktop known-folder location rather than a hardcoded path. The shortcut targets the absolute executable path plus `--feed` and its own bundled icon. No startup registration, background service, administrator elevation or security-policy modification is required by the design.

Build/restore can use package servers; the packaged core interaction must work after networking is disconnected. Documentation URLs are research references, not runtime requests. Do not disable antivirus/SmartScreen or ask users to weaken security to run an unsigned test build. If distribution warnings occur, document them honestly and offer source-build instructions.

A real desktop feeding recording and a public repository remain submission work. A browser diagram or local HTML review cannot replace that recording. Final project naming and submission prose remain the learner's decisions.

## Look and Feel

Implements `prd.md > Look and Feel`.

Preserve the user's desktop and applications: no tank border, glass, water tint, replacement wallpaper or decorative underwater scene. Use original pixel-art fish and a compact, visually distinct feeder with a separate X target. Cache/decode sprites once and use nearest-neighbor sampling; quantize drawing coordinates to physical pixels where appropriate without quantizing the simulation itself. Fine sprite dimensions and frame counts are tunable, not promises.

Use a small number of poses for swimming, turning, curiosity and eating; do not introduce species collection or elaborate mood systems. Final-review polish fixes five stable fish identities to four original silhouettes, with directional poses for Left, Right, TowardViewer and AwayFromViewer. Direction is presentation state derived from movement/depth intent; it does not create a second simulation or free 3D coordinate. Use ordinary readable native menu text. No audio or extra notifications are added by this proposal. Temporary test sprites must be labelled placeholders and replaced or explicitly identified before a final demo.

## Components

### Aquarium.Core / World and Commands

Implements `prd.md > Desktop presence and cursor curiosity — MVP value`, `Feeder handling — accepted, MVP value`.

Core accepts immutable `EnvironmentSnapshot` values and an ordered queue of `OpenFeeder`, `BeginHold`, `MoveHeld`, `EndHold`, `CloseFeeder`, `Hide`, `Show`, and `Exit` intents. The host calls a deterministic `Advance(dt, environment, commands)` and receives a render snapshot. Core references neither WPF/WinForms types nor P/Invoke, files, real-time clocks or OS handles. Randomness and elapsed time are injected for reproducible tests.

Use one state owner on the UI dispatcher; background pipe messages are queued, not allowed to mutate fish collections. Begin with simple wander/steering, not a full physics/boids engine. Priority is suppression/interrupt handling, food seeking, temporary cursor interest, then wandering. Curiosity has per-fish cooldown and duration; it is not continuous pursuit.

### Aquarium.Core / Shake and Food

Implements `prd.md > Feeder handling — accepted, MVP value`.

Track a bounded time window of held-pointer samples. Detect directional reversals with minimum travel and speed, not raw distance alone. Debounce reversals, rate-limit pellet emission, and reset history on pickup/release/cancel so old movements cannot trigger new food. Button-down by itself is insufficient. All tuning is in one plain configuration object, not a settings UI.

Each pellet has a stable ID, position, velocity, age and a consumed flag. Enforce a population cap and a finite lifetime; expire uneaten food without a hunger penalty. A release stops emission but does not clear existing food. Only a fish in the front interaction band with visible contact may consume foreground food, and a pellet is removed once even when two fish arrive together.

Proposed tuning seed, **not measured guarantees:** five fish, at most 64 pellets, roughly 12 seconds maximum pellet lifetime, 30 rendered frames per second, and a 60 Hz fixed simulation step with bounded catch-up. Validate shaking with slow movement, one fast sweep, stationary jitter, intentional reversals and release; tune thresholds using actual mouse and trackpad use rather than assuming one sensor DPI.

### Aquarium.Windows / DesktopSnapshotService

Implements `prd.md > Window depth — accepted direction, MVP value`.

Use `EnumWindows` for top-level candidates. Filter our own windows, hidden/minimized/cloaked windows and desktop shell surfaces; keep ordinary application windows/dialogs relevant to the primary display. Collect visible bounds via `DwmGetWindowAttribute(DWMWA_EXTENDED_FRAME_BOUNDS)` with an explicit, coordinate-correct fallback when unavailable. [D8, D9, D10]

Keep all HWNDs and OS classifications inside the adapter. Core receives only normalized rectangles/roles/order. Do not read window titles, document contents, desktop file contents, screenshots or keystrokes. Window IDs are short-lived opaque identifiers and are not written into telemetry.

Obtain/validate front-to-back order using documented z-order traversal with a visited set, bounded iteration and consistency checks against enumerated candidates; reject a changing/inconsistent snapshot rather than use an unbounded `GetWindow` loop. Microsoft's enumeration guidance explicitly warns about destroyed handles and infinite loops. [D8, D11] Use out-of-context WinEvents to invalidate cached geometry/order, and coalesce updates; callbacks do minimal work and are retained for their registered lifetime. [D12]

Coordinate contract: native data is normalized to physical screen pixels, including negative origins, then converted once to primary-display-local logical units. WPF drawing gets the reverse conversion at the boundary. `GetWindowRect` is DPI-virtualized while DWM frame bounds are not, so never mix the two raw coordinate sets. Handle `WM_DPICHANGED` and display changes by cancelling a hold and rebuilding the transform; do not change system scaling to test it without user agreement. [D10]

Proposed polling safety net: geometry/suppression checks at 10 Hz while visible, rate-limited immediate invalidation on important window events, slower checks while suppressed. Rates are provisional and must not imply instantaneous compositor synchronization.

### Aquarium.Windows / Occlusion and SpriteRenderer

Implements `prd.md > Window depth — accepted direction, MVP value` and `Look and Feel`.

One nonactivating, fully click-through, transparent habitat window covers the target display. WPF requires `AllowsTransparency=true` with `WindowStyle=None`; use an OS-level layered-window click-through policy, not just WPF `IsHitTestVisible=false`. `HTTRANSPARENT` alone has a same-thread routing limitation and is not the complete cross-application solution. Validate opaque fish pixels as well as transparent background pixels. [D2, D11, D13]

For display domain `D`, frontmost ordinary window rectangle `W0`, all ordinary rectangles `Wi`, and protected system-UI region `P`:

```text
front visible region  = D minus P
middle visible region = D minus (P union W0)
rear visible region   = D minus (P union all Wi)
```

If no ordinary window exists, its mask is empty. Clip to these regions and draw fish rear-to-front; draw food in the foreground region. Cache masks until geometry/order changes. The small feeder window is separate and does not participate in ordinary-window ranking. Moving our own overlay never changes another app's relative order; do not repeatedly call a bring-to-front operation to fight the user.

**Important approximation:** bounding-rectangle masks reproduce front/behind relationships for ordinary opaque windows, not exact DWM composition. Rounded corners, shadows, translucent windows and rapid transitions can differ. Do not capture/repaint other apps to disguise this limitation. Establish whether this approximation meets the PRD in the first integration gate; if it does not, review a native interleaving/rendering alternative before further build. No silent fallback to all-fish-always-on-top is acceptable.

Protected surfaces, including visible taskbar/menu/popup regions, must take priority even over foreground fish. Where a protected transient cannot be located reliably, suppress the habitat/feeder temporarily rather than compete above it. Test Start, menus and window switching. Classification is a capability to verify, not a claim to identify every shell surface.

### Aquarium.Core / DepthTransitionPlanner

Implements `prd.md > Window depth — accepted direction, MVP value`.

Maintain `currentBand`, `targetBand` and a transition phase. Do not randomly change the band while a visible overlap would pop. Move the same fish to an uncovered edge/waypoint, change depth where the visibility remains coherent, then approach food. These waypoints express a rendering transition, not window collision or general pathfinding.

For a maximized ordinary window with no route, advance that existing fish toward an offscreen edge buffer, change its band while hidden, then let it swim into the display toward food. Preserve its identity/population count. Do not teleport all fish, spawn a visitor, or allow an invisible fish to eat. If window geometry changes during the transition, recompute its waypoint without changing the user's window order.

### Aquarium.Windows / FeederWindow and InputAdapter

Implements `prd.md > Feeder handling — accepted, MVP value` and `Aquarium controls and feeder activation — accepted, MVP value`.

Use a second small borderless, per-pixel transparent window; only its visible canister/X pixels accept interaction. Resting/unheld objects fall to the primary work-area floor and can be picked up in flight or after landing. Show it without automatic foreground activation. A **deliberate user press** on its body may activate this tool and obtain normal mouse capture. A permanently nonactivating feeder plus `SetCapture` cannot be assumed to deliver reliable cross-window dragging: the API documents foreground restrictions. [D14] Do not fake unrestricted capture with global input hooks.

Convert captured movement into core commands and update the feeder's native position without starting an OS title-bar move loop; distinguish its X hit target before any drag. Release/capture loss/deactivation/session interruption must clear holding and pending shake samples. Visible unheld objects then fall; suppressed objects pause, with gravity velocity reset and no hidden-time catch-up. Do not change the system-wide cursor scheme, warp the pointer, or simulate clicks in other apps. Held appearance is local to the feeder/tool interaction.

Clamp feeder placement and drag within the active habitat's usable area. Proposed one-monitor behavior: launch near the pointer if it is on the primary display; otherwise use the nearest safe position on the primary display. Reusing an open feeder does not create another or force an unrelated foreground change. Verify capture across other processes in the first gate; failure means revise the input approach, not claim success.

### Aquarium.Windows / VisibilityPolicy and FullscreenGuard

Implements `prd.md > Fullscreen work takes priority — accepted, MVP value` and `States and Boundaries`.

Keep **manual visibility** separate from automatic suppression reasons. Compute visibility from both; exiting fullscreen must never undo manual Hide. Guard reasons include fullscreen/presentation, locked/inactive desktop, protected system interaction, display reconfiguration, and invalid integration state. Entering a guard cancels holding and emission before hiding both surfaces. An open feeder remains logically open but returns resting, never held.

Combine foreign-foreground window geometry/client bounds/style and monitor/work-area comparisons with `SHQueryUserNotificationState` hints. Its result is about notification appropriateness, not an authoritative per-window fullscreen contract; it does not emit notifications for fullscreen start/end. [D15, D16] Exclude our own full-display overlay from geometry detection and check for self-induced `QUNS_BUSY` loops. Correlate generic busy hints with foreign-window evidence; presentation, exclusive-D3D and locked-session states need their own tests. Do not equate every maximized window, every quiet-time flag, or every Store app with fullscreen.

Use prompt suppression on a positive signal and a brief clear-state debounce before restoring. Poll while hidden so fullscreen exit can be detected; no focus or window reordering is used as a test. Proposed hidden-state default: freeze fish/food simulation and stop drawing; keep only a slow guard watcher. Reset elapsed-time accumulation on restoration so hidden time causes no catch-up jump or pellet burst.

Auto-hide taskbars, borderless windows, system UI and remote sessions can be ambiguous. Record actual tested cases and use tray Hide as a user escape, not as a substitute for passing automatic fullscreen tests. If detection fails on an intended supported case, the integration gate fails.

### Aquarium.Windows / Host, Tray and InstanceBroker

Implements `prd.md > Aquarium controls and feeder activation — accepted, MVP value`.

A WPF application with explicit shutdown owns the world, windows, event subscriptions, timer and `NotifyIcon`. Closing a tool window cannot terminate the host. Tray Hide/Show/Exit maps to core visibility/exit commands. Exit cancels input, stops timers, hides/disposes both windows and tray, closes the pipe and unregisters hooks. Explorer restart should restore the tray control; test rather than assume.

Use one named mutex and pipe scoped to the current user and desktop session, with `PipeOptions.CurrentUserOnly`, bounded input and a small fixed message schema: version 1, command `ShowFeeder`, no arbitrary path, shell command or code. [D5] A second launch retries briefly until the first broker is ready; failure reports an ordinary error and exits instead of creating duplicate habitats. No TCP listener or external service is involved.

Only the explicit shortcut-creation step writes an app-owned launcher into Desktop. It does not enumerate or alter other desktop icons. Logs, if needed for validation, are opt-in/local, bounded and exclude window titles, typed text and file contents.

### Final-review visual-state contract

- Add FishSpecies with four stable visual families. Assign species deterministically from fish identity; never replace a fish merely to change appearance.
- Add FishFacing with Left, Right, TowardViewer, and AwayFromViewer. Preserve a separate horizontal mouth-side orientation for feeding geometry so front/back presentation cannot break consumption.
- Keep DepthBand as the authoritative occlusion band. Add a bounded visual-depth value only for perspective interpolation. Nominal render scale is Rear 0.72, Middle 0.86, Front 1.00.
- When a band change is safe in place, change the logical band using the existing occlusion rule and ease visual depth toward the new band, displaying TowardViewer/AwayFromViewer during the transition. When a covered sprite cannot switch safely, retain the existing edge-leave/switch/re-enter fallback.
- The sprite atlas contains four distinct silhouettes, four facing directions and two animation frames per direction. Decode/crop once, render nearest-neighbor, and do not add per-fish UI controls.
- Keep the feeder drag/capture/shake contract unchanged. Keep the canister body opaque and the surrounding pixels transparent; a small X is the only separate visible control. Release drops the unheld object to the primary work-area floor. The earlier opaque-panel proposal is superseded by the owner-requested object refinement.

## Data Model and Lifetime

| Data | Owner / update | Lifetime and restart behavior |
| --- | --- | --- |
| Fish ID, pose, velocity, band, intent/cooldown | Core fixed-step update | In memory; initial population restarts on app relaunch. No persistent collection promised. |
| Food ID, position, age, consumed | Core while visible | In memory, capped and expiring; button release preserves particles, suppression freezes them, Exit removes them. |
| Feeder open/resting/held, position, shake history | Core commands + input adapter | One per session; cancellation clears held/history, not the aquarium. |
| Manual visibility and guard reasons | Core policy, platform observations | Manual Hide persists across automatic guard changes within the session; no autostart or cross-session preferences implied. |
| Window bounds/order/protected regions | Windows adapter | Ephemeral versioned snapshot; no screenshot or document text stored. |
| Sprite assets | Renderer reads bundled files once | Distributed files with provenance/license; no downloads at runtime. |

Native handles never enter persisted data or the portable core. Keep state mutation on one thread; use monotonic time, bounded arrays and a bounded command queue. Proposed `60 Hz` simulation can be rendered at `30 Hz`; cap catch-up work after stalls and skip hidden-time advancement. Tune using real measurements.

## File Structure — Target Blueprint

```text
contest-01-build-with-ai-basics/
├─ Aquarium.slnx                       # two source projects + tests
├─ global.json                         # SDK pin established at build setup
├─ Directory.Build.props               # nullable, warnings and common defaults
├─ .gitignore                          # preserve /devpost/*.html and private profile rules
├─ README.md                           # run/demo/limits; not invented final submission copy
├─ LICENSE                             # unmodified PolyForm Noncommercial 1.0.0 text
├─ LICENSING.md                        # scope, source-available status and contest permissions
├─ ASSET_NOTICE.md                     # separate project-asset terms and provenance
├─ THIRD_PARTY_NOTICES.md               # upstream terms; never covered by the project code license
├─ src/
│  ├─ Aquarium.Core/                   # net10.0; no Windows or UI references
│  │  ├─ Aquarium.Core.csproj
│  │  ├─ World.cs                      # sole behavior-state owner
│  │  ├─ FeederFall.cs                 # bounded unheld drop and work-area floor
│  │  ├─ Contracts.cs                  # snapshots, commands, draw records, coordinate units
│  │  ├─ FishBehavior.cs               # wander, curiosity, seek and eat
│  │  ├─ Feeding.cs                    # held-only shake recognition and bounded pellets
│  │  ├─ DepthTransitions.cs           # stable bands and edge re-entry
│  │  └─ VisibilityPolicy.cs           # manual versus automatic suppression
│  └─ Aquarium.Windows/                # references Core, never the reverse
│     ├─ Aquarium.Windows.csproj       # WPF + WinForms tray framework support
│     ├─ App.xaml / App.xaml.cs        # explicit shutdown, composition root
│     ├─ app.manifest                  # normal-user execution, DPI awareness
│     ├─ HostController.cs             # timer, snapshot/command orchestration
│     ├─ DesktopOverlay.cs     # nonactivating, native click-through surface
│     ├─ FeederWindow.cs       # small interactive tool and X
│     ├─ Rendering/SpriteRenderer.cs   # cached sprites and band clipping
│     ├─ Platform/NativeMethods.cs     # small documented interop surface
│     ├─ Platform/DesktopSnapshot.cs  # geometry, ordering, DPI transforms, events
│     ├─ Platform/FullscreenGuard.cs   # foreign-window checks and guard observations
│     ├─ Platform/InputAdapter.cs      # held drag, cancellation, pointer sampling
│     ├─ Platform/InstanceBroker.cs    # current-user/session mutex and pipe
│     ├─ Platform/TrayController.cs    # Hide/Show/Exit, dispose/restart behavior
│     └─ Assets/                      # original fish sprites + feeder/app icons
├─ tests/Aquarium.Core.Tests/          # deterministic automated tests
│  ├─ Aquarium.Core.Tests.csproj
│  ├─ FeedingTests.cs
│  ├─ DepthAndOcclusionTests.cs
│  ├─ VisibilityTests.cs
│  └─ WorldInvariantsTests.cs
├─ scripts/
│  ├─ Create-FeederShortcut.ps1        # explicit current-user launcher creation
│  └─ Publish-Windows.ps1             # self-contained folder/ZIP + hashes
├─ docs/verification.md               # actual environment, checks and results
├─ devpost/
│  ├─ scope.md / prd.md               # approved source requirements
│  ├─ spec.md                         # approved technical blueprint
│  ├─ checklist.md                    # created in 5-build after spec approval
│  ├─ learner-profile.md              # local-only, ignored
│  └─ *.html                          # visual reviews/app map; local-only, ignored
└─ artifacts/                         # later build/test outputs; ignore at build setup
```

No generic plugin system, dependency-injection framework, renderer selection UI or multiple backend services. All Windows API calls stay under the Windows host. Core tests must build without its reference.

## External Services and Dependencies

**Runtime external services: none.** No API keys, model downloads, login, telemetry endpoint, online asset service, browser engine service or local HTTP server is required. .NET/Windows libraries are local software dependencies, not external services.

Build inputs are the installed SDK, documented .NET desktop runtime, development test packages and the official Skill Pack already installed. Record exact resolved package/runtime versions and their licenses at build time. Bundle required runtime/assets in the release. Do not copy old project implementations or a desktop pet's character assets; keep a provenance record for anything incorporated. The official Skill Pack material is development curriculum, not aquarium feature code.

## Verification Order and Important Failure Modes

**The first build slice is an integration gate, not polished fish artwork.** No app code is created by this document. `5-build` converts these gates into its official Markdown checklist after approval.

| Gate | Evidence required | Failure response |
| --- | --- | --- |
| 1. Real overlay/input/depth | Temporary labelled sprite over Explorer, Notepad and a browser; ordinary click/drag/wheel pass at opaque and transparent pixels; feeder drag across another process; two real overlapping windows demonstrate middle masking; no unexpected focus theft | Stop expanding features. Fix/review native overlay, activation/capture or masking approach. Do not replace the kernel with a browser animation. |
| 2. Coexistence and recovery | Maximize versus F11/fullscreen media/presentation; interrupt a held feeder; manual Hide during fullscreen then exit; Start/menu/window switching; no stuck cursor/hold | Suppress safely and log local diagnostics; intended supported behavior must pass before acceptance. |
| 3. Actual feeding | Real launcher reuses one instance; held shake creates pellets; a visible fish approaches and consumes; release/X work; cap/expiry and no invisible/double consumption | Fix deterministic core tests and end-to-end input connections; no timed mock feeding. |
| 4. Stable packaged run | Correct DPI masks, hide/show/exit, display reconfiguration, repeated use and local-session test; published ZIP on a machine/session without SDK and with networking off | Narrow the supported envelope explicitly or improve code. Untested environments stay marked untested. |

Unit tests cover no-held/no-food, single sweep versus reversals, release clearing shake history, one-consumer-per-pellet, band mask intersection, identity-preserving edge transitions and the visibility truth table. Add a static dependency check that Core has no Windows/UI reference. Synthetic snapshots are unit-test fixtures only; final demonstration uses real desktop windows.

Performance verification: record CPU, memory, GPU usage where available, update/render frame timings, fish/pellet counts and display/session details for baseline desktop, ordinary aquarium, feeding and hidden/fullscreen states. Compare to baseline; check that hidden drawing stops and memory remains bounded across repeated feed cycles. Initial targets are tunable, not claims of a CPU percentage or battery saving. If transparent full-display rendering dominates cost, revisit rendering rather than claim that pixel art made it cheap.

Other failure handling: stop emission on capture loss; cancel hold on display/DPI change and clamp the feeder; keep manual Hide across automatic recovery; refuse unknown pipe commands; skip invalid handles and reject inconsistent snapshots; dispose hooks/capture/windows on normal Exit. Do not seek administrator rights or alter user security settings as a workaround.

## What Was Simplified and Why

- **Agreed:** feeding only; no rare visitors, keeping/raising systems or hunger penalties.
- **Agreed:** three depth bands, not arbitrary placement between every window or physical window collision.
- **Agreed:** pixel-art objects on the existing desktop, not a 3D aquarium/water renderer.
- **Agreed:** Windows first, local-only HTML documentation, portable behavior separated from OS integration.
- **Accepted in the technical review:** two source projects, a single primary-display validation target, geometric occlusion, WPF drawing, in-memory world state and self-contained folder distribution. Implementation and performance still require real verification.

## Decisions and Open Issues

**Already selected by the learner:** first OS Windows; no runtime external services; core/OS separation; the approved feeding/depth/fullscreen/controls product behavior; HTML reviews outside Git. Do not reopen the approved PRD.

**Technical recommendation approved:** the learner explicitly accepted C#/.NET 10 plus WPF/Win32, Windows 11 x64 primary-display-first validation, geometric masking subject to the early capability gate, and self-contained ZIP delivery. Do not request a second technical sign-off. The build checklist and Fast mode have also been approved; `checklist.md` records current execution.

**Genuine uncertainty being addressed:** the learner asked how a fish can be between ordinary windows without breaking their order. The proposed answer is logical bands plus masks, while keeping a small feeder interactive and the fish layer passive. Evidence must come from the real-window depth/input gate; this remains unverified until build.

**Remaining build-time investigations:** exact compositor behavior and costs of transparent WPF, rounded/translucent-window treatment, fullscreen classification without reacting to our own overlay, DPI correctness, capture loss and system-menu suppression. A failed capability gate requires explicit design revision; it is not permission to remove an approved feature silently.

**Before public release:** choose the final project name, confirm license/provenance, pin and service dependencies, verify clean source/build instructions, check secrets and Git history, and record actual support/test evidence. The user-visible demo must be real and the submitted work must match the documentation. No commit, push, installation or app launch has been performed in this design step.

## Implementation Evidence - G0 and live feeding

G0 is accepted for continuation after positive learner feedback and committed as `b9d361a`. Its controlled RDP-native evidence remains narrower than local-console or broad application compatibility.

The live feeding subset now exists: `World.cs`, `Feeding.cs`, and `DepthTransitions.cs` implement autonomous movement, intermittent curiosity, held-only shake detection, capped expiring food and visible single consumption. `FeederState.cs` remains the core tool state. `Rendering/SpriteRenderer.cs` draws cached original pixel atlas frames on the passive surface. `FeederWindow.cs` raises held-motion/boundary events to the one UI-owned core; it does not add a parallel state owner or native dependency to the core. The instance broker still posts onto the dispatcher. G0 remains selectable only for regression through `--g0`.

Release build, 54 core tests, 25 G0 native regression checks and 18 live feeding native checks pass. The native feeding script used actual pointer/button events and real work windows in normal/maximized states; its controlled `.lnk` launch reused the resident. Session evidence remains RDP, primary 2160 x 3840 at 150% scaling. The learner has now accepted the observed feeding experience for continuation; this is not final release approval or clean-environment certification.

A speed-invariant test exposed a boundary snap after edge feeding; clamping target positions rather than the current fish fixes it without changing the approved depth behavior. Detailed hardware/OS coverage, input-loss cases, performance and ZIP delivery still need later slices.

The feeder/icon remain reproducible from scripts/Generate-Assets.py. The current fish resources are regenerated from approved independent PNGs by Pack-FishAtlas.py and validated by Generate-Assets.py; the historical 640x192 cell atlas is no longer loaded. All resources are local and require no runtime download. `Create-FeederShortcut.ps1` passed workspace-local tests. After explicit Desktop access was granted, it also created the actual Desktop `Feed Fish.lnk`; idempotent reuse and two launches against the same running resident/feeder were verified. The development link targets the current Release build folder. Details and the local-only receipt are recorded in `docs/feeding-verification.md`. Earlier grant failures were not bypassed and are no longer a blocker.

The established G0 internals remain: code-only WPF windows, geometry-version-based mask caching, inactive XAML-island region masking, slower hidden watcher and the documented narrow WFO0003 DPI-manifest exception. The application does not inject input or capture other applications; those operations exist only in controlled test scripts against test-owned surfaces. See `docs/feeding-verification.md` for exact passes and remaining work. Slice 2 is accepted for continuation after launcher verification and positive review; G3 and final review remain.

## G3 implementation evidence

`SimulationClock.cs` supplies bounded fixed steps and discards hidden time. Its `SessionAvailability` flags preserve lock/disconnect independently. Native environment notifications and WM_CANCELMODE cancel a held tool; current tray interactions respect the same guard policy. The production instance broker still accepts only the fixed feeder command, now with dispatcher-completion acknowledgement, bounded retries and correct mutex ownership. No extra public control interface was added.

The live host has passed 64 core tests, the prior 25 G0/18 feeding regression checks, 25 lifecycle native checks, 7 actual isolated-profile Edge F11 checks and 3 malformed-client protocol checks. Hidden queued drawing was repaired after a failing native freeze assertion. No actual display setting or session was changed by these tests. Native evidence remains RDP-only; games, real reconnect/DPI changes and clean offline packaging remain unrun. See `docs/g3-verification.md`; neither planned target support nor these results are final release acceptance.

## G4 package candidate evidence

The corrected `scripts/Publish-Windows.ps1` now creates a self-contained folder/ZIP with explicit runtime 10.0.10, bundled assets, app launch/setup helpers, source checkpoint and file hashes. The current candidate is `artifacts/packages/g4-d26b420-r2/DesktopAquarium-win-x64.zip`. Its application/runtime files match the tested first candidate; only README line endings changed. Package startup was rerun after R2 extraction.

Packaged feeding (18 checks), packaged lifecycle (25 checks), 482 file-hash checks and package-local host/runtime module loading are verified. The host is still SDK-equipped and connected; invalid child DOTNET_ROOT/PATH is not a clean/offline environment. Resource data is a five-second-per-phase RDP sample: about 20 render frames/s when visible and zero hidden redraw, not a performance guarantee. Sustained CPU/GPU/frame latency and local-console/no-SDK/offline tests remain.

An initial publish modified normal source lockfiles and caused NU1004 on locked restore. Publish restore now uses a fresh artifact-only lock path with lock generation disabled, while canonical file hashes are guarded. Source locked restore/build/64 tests pass after republishing. See `docs/g4-verification.md`. G4 remains incomplete, and final review, redistribution-notice/source-license checks and ship are not complete.

## Pre-submission candidate preparation

Current runtime pin: 10.0.12, released 2026-09-08 in the live official 10.0 metadata fetched during this pass. The previous web cache showed 10.0.10; do not use that stale snapshot as current servicing evidence. The host SDK/shared runtime remain unchanged.

`Collect-RuntimeNotices.py` validates official binary archive SHA-512 and preserves extracted runtime notices. WPF/WinForms v10.0.12 source notice files are separately identified; the Windows Desktop binary ZIP itself supplied none. Publishing bundles the matching notices and records exact source-input hashes plus worktree state. Dependency notices do not choose a license for the new application.

`Rendering/RenderMetrics.cs` adds opt-in bounded diagnostic samples for OnRender callback intervals and callback CPU elapsed time. It does not measure compositor/GPU display latency. No new visual feature or runtime service is added. `Measure-Prototype.py` supports an explicitly bounded longer sample when the interactive desktop is available.

`New-CleanRoomKit.ps1` builds a guest-network-disabled WSB configuration with read-only package/scripts and only a dedicated results folder writable. It does not install Sandbox or change host networking/policies. `Run-OfflineAcceptance.ps1` records environment checks and the participant's actual manual outcomes; not-run stays not-run.

The runtime-10.0.12 candidate is `artifacts/packages/pre-submit-01/DesktopAquarium-win-x64.zip`, built from source `12baa4d`; all 489 payload hashes match. The current session denies access to its input desktop, so new native rendering/input/video/long-sample checks have not run. Current app behavior remains protected by session suppression. The isolated source build and 64 core tests passed; previous native passes are historical evidence, not new-runtime acceptance. See `docs/pre-submit-verification.md` for this distinction.

## Documentation Sources

Official documentation consulted for technical claims on 2026-09-25. Proposed algorithms, component boundaries and defaults above are design decisions, not claims that Microsoft certifies this application.

- [D1 — WPF overview](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/)
- [D2 — Window.AllowsTransparency](https://learn.microsoft.com/en-us/dotnet/api/system.windows.window.allowstransparency?view=windowsdesktop-10.0)
- [D3 — WPF 2D graphics and imaging performance](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-2d-graphics-and-imaging)
- [D4 — NotifyIcon](https://learn.microsoft.com/en-us/dotnet/api/system.windows.forms.notifyicon?view=windowsdesktop-10.0)
- [D5 — PipeOptions / CurrentUserOnly](https://learn.microsoft.com/en-us/dotnet/api/system.io.pipes.pipeoptions?view=net-10.0)
- [D6 — MSTest with .NET](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-csharp-with-mstest)
- [D7 — .NET publishing](https://learn.microsoft.com/en-us/dotnet/core/deploying/)
- [D8 — EnumWindows](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumwindows)
- [D9 — DWM window attributes](https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute)
- [D10 — GetWindowRect and DPI](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowrect)
- [D11 — Window features / z-order / layered hit testing](https://learn.microsoft.com/en-us/windows/win32/winmsg/window-features)
- [D12 — SetWinEventHook](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwineventhook)
- [D13 — WM_NCHITTEST](https://learn.microsoft.com/en-us/windows/win32/inputdev/wm-nchittest)
- [D14 — SetCapture](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setcapture)
- [D15 — SHQueryUserNotificationState](https://learn.microsoft.com/en-us/windows/win32/api/shellapi/nf-shellapi-shqueryusernotificationstate)
- [D16 — Notification state values](https://learn.microsoft.com/en-us/windows/win32/api/shellapi/ne-shellapi-query_user_notification_state)

## RDP candidate recheck

The user chose RDP rather than console transfer. The unchanged pre-submit-01/runtime-10.0.12 package has fresh 18 feeding, 25 lifecycle, 7 actual Edge F11 and package-local loader passes; 64 source core tests pass. A cropped 7.95-second silent local rehearsal was recorded from actual input, not a simulated aquarium. No upload/final video approval occurred. Sparse fixture coordinates were replaced by verified test-owned activation/placement, without product z-order changes.

Long-run ordinary/feeding measurements have two 60-second phase samples but the full attempt failed in test setup before hidden sampling. A later five-second-per-phase three-state run completed; no GPU or compositor latency guarantee. See `docs/rdp-candidate-verification.md`. Remaining clean/offline, local-console and final owner review requirements are unchanged; earlier input-access-denial statements above are historical, no longer the current blocker.

## G4-only latest validation

The owner requested G4 only. `docs/g4-verification.md > G4-only verification pass ? 2026-09-26` records one completed 60/60/60-second ordinary/feeding/hidden run with eight assertions and normal exit, replacing the earlier incomplete measurement as latest evidence. Source Release build/64 core tests and the 489-file runtime-10.0.12 package inventory were rechecked. Per-process GPU queries produced no instances; do not claim 0% GPU. No product feature or code change occurred.

The SDK-free, runtime-network-unavailable separate Windows test still has not run. Host optional-feature checks found Sandbox disabled; no feature enablement, restart, console transfer or networking change was performed. G4 is not complete, and final review/learning/shipping remain outside this request. The previously generated clean-room kit is preparation, not acceptance evidence.

Rebuilt G4 package: `artifacts/g4-only-20260926/package-02/DesktopAquarium-win-x64.zip` from source `0f500a5`. ZIP inventory 489 entries, fresh 18 feeding / 25 lifecycle / bundled-runtime startup checks, and post-publish locked restore/build/64 core tests passed. The real no-SDK/offline guest run remains unperformed. Rebuilding changed revision metadata and binary hashes despite identical application source input hashes; native evidence was regenerated rather than inferred. No app behavior, artwork or supported-platform expansion was introduced.

## Sandbox activation awaiting restart

The owner authorized the G4 test-environment feature and explicitly requested a retry. The first UAC request ended without activating the feature. The retry ran `Enable-WindowsOptionalFeature -Online -FeatureName Containers-DisposableClientVM -All -NoRestart` through normal administrator consent. Its receipt reports Enabled, RestartNeeded=true and exit code 3010. No reboot command was issued. The owner has chosen to restart manually after other work and requested saving only; pause all project operations until they return. No assistant-initiated reboot, scheduled restart or automatic guest-test continuation is authorized. The offline guest test remains unrun and G4 is still unchecked. App behavior/source and the existing running aquarium were not changed. Evidence: `artifacts/g4-only-20260926/sandbox-enable-02/activation-result.json`.

## G4 clean-environment result

After owner-authorized Windows Sandbox activation and reboot, package-02 passed a separate Windows 11 x64 clean-environment run with no global dotnet/SDK and no runtime networking before or after testing. All 489 payload hashes matched, the app initialized five fish before any test-only Python extraction, package-local .NET 10.0.12 loader/runtime modules were observed, 18 feeding and 25 lifecycle native assertions passed with zero recorded test exit codes, no resident app/capture remained, and payload hashes were unchanged. Evidence is artifacts/g4-only-20260926/offline-native-05/results/acceptance.json and docs/g4-verification.md.

Earlier Sandbox runs found verifier readiness/exit-code races and are preserved as failed harness attempts. No product source, artwork, architecture or support scope changed. Locked restore, Release build and 64 core tests passed again after the successful guest run. G4 mechanical verification is complete; the checklist still awaits the actual-package learner check before marking the slice complete.
