# Windows Sandbox demo recording — 2026-09-27

Status: a local silent draft was recorded from the accepted, unmodified application. Participant review and public upload remain pending. This is a technical recording receipt, not submission copy or narration.

## Recorded content

The participant requested a real Windows Sandbox desktop with overlapping work windows and a suitable wallpaper. The recording uses two actual Microsoft Edge windows displaying original local workspace pages and a File Explorer window. Calculator was not installed in this guest; no substitute calculator UI or downloaded application was introduced.

The unmodified aquarium runs over that desktop. Automated mouse input picks up and shakes the real feeder; its normal logic emits food, fish approach and consume it, and releasing drops the feeder. The recording changes the foreground work window, closes only the feeder, and uses the application's real Hide/Show again menu. Menu opening uses the existing native fixture's NotifyIcon callback route followed by a physical menu-item click, not an added product test endpoint. The video contains no substituted fish animation, simulated feeding result, narration, captions or music.

| Recording property | Observed value |
| --- | --- |
| Application source | Public commit `88ed4f6d282b3a6080cf95865373102b6a8b1235` |
| Runtime | Fresh local self-contained Windows x64 build, .NET 10.0.12 |
| Guest | Windows build 26100; no global dotnet on PATH; zero default network routes; networking disabled in the Sandbox configuration |
| Work windows | Two Edge windows and File Explorer; guest-only content, no signed-in browser profile |
| Video | H.264 MP4, 1192×718, 88.73 seconds, silent, 8,485,240 bytes |
| Input/results | Two held-shake feeding cycles; 72 pellets emitted and 72 consumed; feeder release/landing, close, Hide and Show again recorded |
| Media verification | Full video decode passed; frames at 1, 20, 24, 50, 55, 79 and 85 seconds inspected |
| Privacy scope | Capture ran inside the guest; only dedicated read-only inputs and a writable results folder were mapped |
| Publication | No video upload, public binary release, submission tag or Devpost submission |

Local movie: `artifacts/sandbox-demo/run-01/results/aquarium-demo-take-01.mp4`.

SHA-256: `6e75fa61acf833d32f3950bc29552702ead432ed0153e800a24ceff36f086b15`.

Timeline, diagnostics, recording verification and review frames remain in ignored `artifacts/sandbox-demo/run-01/`. The initial eight-second probe and failed setup receipts are retained. These local paths are not downloads included in the public source repository.

## Wallpaper and recording tools

The wallpaper was generated on 2026-09-27 with Codex's built-in `image_gen` tool: a quiet abstract navy/teal desktop background with negative space, no fish, aquarium scene, UI, text, logo or reference image. It is a recording backdrop, not a new aquarium feature or bundled application asset. The exact prompt and image SHA-256 are recorded in local `wallpaper-provenance.json`; the unchanged generated PNG is `input/wallpaper.png`. This records AI-assisted provenance without asserting legal copyright certainty. Existing fish/feeder assets and their notices are unchanged.

The guest uses the previously checksum-verified Python 3.13.15 embedded driver and the preinstalled imageio-ffmpeg FFmpeg 7.1 executable as recording tools. They are separate from the application and are not added to the public repository or app runtime. Tool versions and local hashes are recorded with the footage. The staged application folder includes the root licensing documents and original dependency notices; it is a local filming build, not a verified public ZIP release.

## Limits and setup observations

An initial Sandbox connection attempt with vGPU enabled disconnected before login. The recorded session used vGPU disabled. This sequence does not establish the cause of the first connection failure or general GPU compatibility. The guest's default PowerShell file-execution policy blocked the first bootstrap; the policy was left unchanged, and the existing portable Python driver was initialized with standard guest executable commands. No host security/display/background setting was changed.

A guest-only request for 1920×1080 did not change the active remote-desktop dimensions despite successful API return codes. The recorded resolution is therefore explicitly 1192×718. Full media decode and sampled visual review are not a frame-by-frame participant acceptance or a full package regression pass. Korean Windows/Edge chrome remains visible; the final submission's explanation/translation needs participant review. No fresh broad performance, DPI or complete clean-room certification is inferred from this recording.

The next step is participant review of the full draft, followed by any participant-authored explanation/captions and an authorized public YouTube/Vimeo upload. The [submission checklist](submission-readiness.md) continues to distinguish local footage from the required accessible video URL.
