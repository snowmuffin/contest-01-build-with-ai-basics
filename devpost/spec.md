---
doc: spec
status: approved
---

# Desktop Aquarium — Technical Spec (working label)

## How This Works, In Plain Language

The aquarium has two application projects. **Aquarium.Core** decides where fish swim, whether they are curious, whether the feeder is held, and when a food particle is eaten. It knows coordinates and commands, but nothing about Windows handles, WPF, or the screen's contents. **Aquarium.Windows** observes window geometry and pointer activity, translates them into simple inputs, and draws the core's result over the real desktop.

The fish surface is display-only and passes clicks to the user's applications. The feeder is a separate small interactive window. This separation avoids making the entire display interactive just to drag one object. For apparent depth, the renderer leaves out the parts of a fish that should be covered by a nearer work window. It never changes another application's window order. This is the selected geometric-masking approach, not a screenshot of the desktop or a replacement compositor.

This document develops the **approved** `scope.md` and `prd.md`. Windows-first, separate core/OS responsibilities, feeding-only scope, and local-only HTML reviews are learner decisions. **The learner explicitly approved the technical recommendation: C#/.NET 10 with WPF/Win32, the Windows 11 x64 primary-monitor validation envelope, geometric masking with an early feasibility gate, and self-contained ZIP distribution.** This approval completes technical planning; it is not evidence of implementation, compatibility or measured performance. No application has been implemented or runtime-tested. The filenames and commands below are a build blueprint, not existing software.

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
7. **Return to work:** release clears holding and new emission, leaving the feeder resting. Its X closes the feeder only. Tray Hide/Show/Exit controls the aquarium. Fullscreen protection cancels holding and suppresses the habitat without stealing focus; restore never resumes a drag or overrides a manual Hide.

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

The inspected host reports Windows NT build **26200**, x64. UI behavior has not been tested. Validation should record the actual display resolution, scaling and local-vs-remote session; also test a stable supported Windows installation before claiming broad Windows 11 compatibility. Proposed scenarios include 100/125/150/200% scaling where available. Tests in unavailable environments remain explicitly unrun.

Planned source commands, available **after** the build creates the projects:

```powershell
dotnet restore Aquarium.slnx
dotnet test tests/Aquarium.Core.Tests/Aquarium.Core.Tests.csproj -c Release
dotnet run --project src/Aquarium.Windows/Aquarium.Windows.csproj -- --feed

dotnet publish src/Aquarium.Windows/Aquarium.Windows.csproj -c Release -r win-x64 `
  --self-contained true -p:PublishSingleFile=false -p:PublishTrimmed=false `
  -o artifacts/win-x64
```

Planned packaged use: extract the **whole** published directory, run `Aquarium.Windows.exe`, then run the documented `scripts/Create-FeederShortcut.ps1 -ExePath <absolute-exe-path>` once to create the app-owned desktop shortcut. That script must refuse to overwrite an unrelated shortcut; use the OS's current-user Desktop known-folder location rather than a hardcoded path. The shortcut targets the absolute executable path plus `--feed` and its own bundled icon. No startup registration, background service, administrator elevation or security-policy modification is required by the design.

Build/restore can use package servers; the packaged core interaction must work after networking is disconnected. Documentation URLs are research references, not runtime requests. Do not disable antivirus/SmartScreen or ask users to weaken security to run an unsigned test build. If distribution warnings occur, document them honestly and offer source-build instructions.

A real desktop feeding recording and a public repository remain submission work. A browser diagram or local HTML review cannot replace that recording. Final project naming and submission prose remain the learner's decisions.

## Look and Feel

Implements `prd.md > Look and Feel`.

Preserve the user's desktop and applications: no tank border, glass, water tint, replacement wallpaper or decorative underwater scene. Use original pixel-art fish and a compact, visually distinct feeder with a separate X target. Cache/decode sprites once and use nearest-neighbor sampling; quantize drawing coordinates to physical pixels where appropriate without quantizing the simulation itself. Fine sprite dimensions and frame counts are tunable, not promises.

Use a small number of poses for swimming, turning, curiosity and eating; do not introduce species collection or elaborate mood systems. Use ordinary readable native menu text. No audio or extra notifications are added by this proposal. Temporary test sprites must be labelled placeholders and replaced or explicitly identified before a final demo.

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

Use a second small borderless window; only its body/X region accepts interaction. Show it without automatic foreground activation. A **deliberate user press** on its body may activate this tool and obtain normal mouse capture. A permanently nonactivating feeder plus `SetCapture` cannot be assumed to deliver reliable cross-window dragging: the API documents foreground restrictions. [D14] Do not fake unrestricted capture with global input hooks.

Convert captured movement into core commands and update the feeder's native position without starting an OS title-bar move loop; distinguish its X hit target before any drag. Release/capture loss/deactivation/session interruption must clear holding and pending shake samples. Do not change the system-wide cursor scheme, warp the pointer, or simulate clicks in other apps. Held appearance is local to the feeder/tool interaction.

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
├─ LICENSE                             # choose/confirm a suitable open-source license before publishing
├─ THIRD_PARTY_NOTICES.md               # dependencies, original/third-party asset provenance
├─ src/
│  ├─ Aquarium.Core/                   # net10.0; no Windows or UI references
│  │  ├─ Aquarium.Core.csproj
│  │  ├─ World.cs                      # sole behavior-state owner
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

**Technical recommendation approved:** the learner explicitly accepted C#/.NET 10 plus WPF/Win32, Windows 11 x64 primary-display-first validation, geometric masking subject to the early capability gate, and self-contained ZIP delivery. Do not request a second technical sign-off. The next artifact is the `5-build` Markdown checklist; build-order review and build-mode selection are separate from this completed technical approval.

**Genuine uncertainty being addressed:** the learner asked how a fish can be between ordinary windows without breaking their order. The proposed answer is logical bands plus masks, while keeping a small feeder interactive and the fish layer passive. Evidence must come from the real-window depth/input gate; this remains unverified until build.

**Remaining build-time investigations:** exact compositor behavior and costs of transparent WPF, rounded/translucent-window treatment, fullscreen classification without reacting to our own overlay, DPI correctness, capture loss and system-menu suppression. A failed capability gate requires explicit design revision; it is not permission to remove an approved feature silently.

**Before public release:** choose the final project name, confirm license/provenance, pin and service dependencies, verify clean source/build instructions, check secrets and Git history, and record actual support/test evidence. The user-visible demo must be real and the submitted work must match the documentation. No commit, push, installation or app launch has been performed in this design step.

## Implementation Evidence — G0

The approved blueprint below is no longer wholly unimplemented. Its G0 subset now runs: pure core geometry/feeder/visibility contracts, real Windows observation, geometric clipping, a passive labelled overlay, a captured draggable feeder, tray lifecycle and a restricted local instance broker. Full fish/shake/food behavior is still planned, not implemented.

Release build and 26 core tests pass. A separate-process native fixture recorded 25 passing checks in an **RDP** session at 2160×3840 and 150% scaling. These include actual composited marker pixels, click/wheel/drag delivery, native feeder capture/release, ordinary maximize versus controlled borderless fullscreen, restore and timed cleanup. This does not replace the pending learner/local-console and ordinary-app checks. See `docs/verification.md`; slice 1 is not marked complete.

Current internal mapping refinements preserve the approved architecture: `DesktopOverlay.cs` and `FeederWindow.cs` are code-only WPF windows; `FeederState.cs` holds the minimal G0 core interaction; `G0ContractTests.cs` tests the delivered contracts. The native fixture script is test-only and performs bounded input solely against the probe and its own temporary windows. The application itself does not inject input or capture screen contents.

A visible inactive shell XAML island is treated as a protected region, not unconditional whole-screen suppression. Masks are rebuilt on geometry/order changes rather than every pointer sample. Hidden drawing stops and the watcher interval slows; no resource-use benefit is claimed without a benchmark. The one project-scoped WFO0003 exception is documented in the Windows project: a WPF host uses a DPI manifest and includes WinForms only for NotifyIcon, not the WinForms application bootstrap.

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
