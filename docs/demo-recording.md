# Windows Sandbox demo recording — 2026-09-27

Status: take-05 is the reviewed local final-submission candidate, pending the participant's selection. It supersedes take-01 for the current recommendation; earlier footage is retained. Nothing has been uploaded or submitted. This is a technical recording receipt, not submission copy or narration.

## Current candidate: shorter silent demonstration

The participant requested a 45–60-second improvement focused on camera composition and clear real interaction. This is submission preparation only. Application code, assets, dependencies, movement, feeding and depth logic are unchanged; scope and PRD remain accurate without a product revision.

Local candidate: `artifacts/sandbox-demo/run-02/results/take-05/aquarium-demo-take-05.mp4`.

| Property | Verified result |
| --- | --- |
| Duration / image | 47.50 seconds; 1192×718; 30 fps CFR; 1,425 frames |
| Encoding | H.264, yuv420p, CRF 18; 4,590,477 bytes; no audio, captions or music |
| Application | Same Release payload from public commit `88ed4f6d282b3a6080cf95865373102b6a8b1235`, .NET 10.0.12 |
| Environment | Fresh Windows Sandbox with the same build 26100, disabled networking/vGPU, isolated mappings and unchanged generated wallpaper as take-01; two real Edge windows with original English dummy pages |
| Integrity | All 499 staged and guest payload files match the prior recording's manifest; 150 protected source/asset/script/license files, including original unfinished work, are unchanged |
| Input | Actual mouse motion/buttons on the desktop shortcut, feeder and ordinary windows; no product test mode, state injection or synthetic NotifyIcon callback |
| Observation | Existing read-only `--diagnostics` output remains off-screen; 12 emitted, 12 consumed, zero expired; emission remains at 12 after release |
| Editing | Continuous recording at real time; no cuts, zooms, substituted frames, speed changes or extra visual overlays |
| Review method | Full decode passed. Entire timeline inspected through 95 chronological frames at 2 fps; 42 additional feeding frames at 6 fps and every frame of the 22.1–23.1-second consumption interval inspected. Review crops are separate from the unchanged movie. This is not a claim that every frame of the full movie was manually viewed. |

SHA-256: `d10e30e66d75b6a657c735e83885f29d306e59e2da0ff4c9423f744d0f080d33`.

### Candidate review

PASS below is the agent's visual/technical assessment, not participant acceptance or an organizer decision. Times are approximate video positions; diagnostics support, but do not replace, visual evidence.

| Requested check | Result and evidence |
| --- | --- |
| Desktop aquarium apparent in the first eight seconds | PASS — normal desktop, taskbar, icons and two overlapping browsers with free-swimming fish |
| Multiple species visible | PASS — Goldfish, Guppy and Angelfish in the opening, with Tetra also visible later |
| Normal windows and fish visible together | PASS — both remain visible throughout; a normal page checkbox toggles at about 34 seconds |
| Depth/occlusion conspicuous | PASS — changing the foreground browser at about 8 and 12 seconds covers/reveals a middle fish; front and rear presentation also appears |
| Feeder pickup visible | PASS — real Feed Fish shortcut at about 16 seconds, followed by falling, grabbing and lifting the object |
| Shake visible | PASS — deliberate two-second horizontal shake at about 21–23 seconds |
| Food emission visible | PASS — individual pellets fall beneath the canister before the fish converge, particularly at about 21.5–22.2 seconds |
| Fish respond to food | PASS — visible turns and approach from multiple directions at about 22–24 seconds |
| Consumption visible | PASS — arriving Guppy, disappearing pellets and meal flash at about 22.3 seconds; food later clears. Diagnostics independently record 12 consumed, zero expired. Exact individual mouth contact remains subtle. |
| Normal after release/close | PASS — drop at about 25 seconds; no additional emission; close at about 41 seconds; swimming continues to the end |
| No unnecessary idle repetition | PASS — one feeding cycle; brief waits show actual approach, consumption and stable post-close swimming |
| No private/debug/unnecessary UI exposure | PASS in reviewed frames — only guest dummy content and normal shell/browser chrome; no accounts, host paths, terminal, debug panels, notifications or snap prompts |
| Actual product behavior only | PASS — unchanged production Release payload and real mouse events; no simulated result or timing manipulation |

The candidate is 41.23 seconds shorter than take-01. The shortcut-to-object sequence, isolated food emission and single feeding cycle improve the causal story. Foreground activation replaces window dragging to avoid Windows snap UI. A normal page interaction demonstrates continued desktop use; closing only the feeder provides a stable ending. No captions were needed for the basic shake → food → approach sequence.

Remaining visual limits: individual pellet-to-mouth contact is small and sometimes covered as fish converge; the exact Front/Middle/Rear terminology is not explained by the silent video. Fullscreen priority and tray Exit are omitted to keep the demonstration focused; they must not be claimed as demonstrated by this footage.

### Retakes and local evidence

Take-02 and take-03 were aborted at approximately 25 seconds after remote pointer interference opened unrelated Windows UI or missed the shortcut. Take-04 completed but was rejected because window dragging exposed the snap strip and an Angelfish immediately covered the emission area. None is marked as a final candidate. The next take uses a lower, initially clear feeding position and ordinary window activation.

Minimizing only the host's Sandbox client resolved the observed input interference in subsequent guest input/cursor checks. Capture still ran inside the active guest. No host security/display settings, product code or fish state were changed. Exact root cause of the remote-client interference is not claimed.

Inputs, timeline, read-only observations, rejected footage, review frames and `recording-verification.json` remain in ignored `artifacts/sandbox-demo/run-02/`. The participant retains final selection; no GitHub push, public upload, contest tag or Devpost submission is part of this filming pass.

## Take-01: historical draft

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

## Wallpaper and recording tools shared by the takes

The wallpaper was generated on 2026-09-27 with Codex's built-in `image_gen` tool: a quiet abstract navy/teal desktop background with negative space, no fish, aquarium scene, UI, text, logo or reference image. It is a recording backdrop, not a new aquarium feature or bundled application asset. The exact prompt and image SHA-256 are recorded in local `wallpaper-provenance.json`; the unchanged generated PNG is `input/wallpaper.png`. This records AI-assisted provenance without asserting legal copyright certainty. Existing fish/feeder assets and their notices are unchanged.

The guest uses the previously checksum-verified Python 3.13.15 embedded driver and the preinstalled imageio-ffmpeg FFmpeg 7.1 executable as recording tools. They are separate from the application and are not added to the public repository or app runtime. Tool versions and local hashes are recorded with the footage. The staged application folder includes the root licensing documents and original dependency notices; it is a local filming build, not a verified public ZIP release.

## Take-01 setup observations and historical limits

An initial Sandbox connection attempt with vGPU enabled disconnected before login. The recorded session used vGPU disabled. This sequence does not establish the cause of the first connection failure or general GPU compatibility. The guest's default PowerShell file-execution policy blocked the first bootstrap; the policy was left unchanged, and the existing portable Python driver was initialized with standard guest executable commands. No host security/display/background setting was changed.

A guest-only request for 1920×1080 did not change the active remote-desktop dimensions despite successful API return codes. The recorded resolution is therefore explicitly 1192×718. Full media decode and sampled visual review are not a frame-by-frame participant acceptance or a full package regression pass. Korean Windows/Edge chrome remains visible; the final submission's explanation/translation needs participant review. No fresh broad performance, DPI or complete clean-room certification is inferred from this recording.

The next step is participant selection of the current candidate, followed by any participant-authored explanation/translation and a separately authorized public YouTube/Vimeo upload. The [submission checklist](submission-readiness.md) continues to distinguish local footage from the required accessible video URL.
