# Pre-submission preparation evidence

## Result boundary

Technical preparation in progress; not a final accepted release and not a submitted entry.
The participant requested preparing the submission first and deferring additional polish. No public
repository/video upload, visibility change, final project name, project license or submission prose
was created on the participant's behalf.

## Performed

- Inspected canonical approved scope/PRD/spec/checklist, Git state, installed official 5-build/6-ship guides and actual implementation before modification.
- Fetched the live official .NET 10.0 release metadata: latest listed runtime 10.0.12, release date 2026-09-08. A cached web response still showed 10.0.10; the live response was used for this candidate.
- Downloaded the exact official win-x64 runtime and Windows Desktop archives for 10.0.12; both SHA-512 values match official metadata.
- Preserved two binary-distribution runtime notice texts and four version-tagged WPF/WinForms source notice texts. Provenance identifies which came from archives and which from source repositories.
- Added bounded, opt-in renderer callback metrics; no rendering style or interaction design changes.
- Isolated Release build passed with zero reported warnings/errors, and all 64 existing core tests passed. Existing WFO0003 project-specific exception remains as documented; no additional suppression was added.
- Parsed Python/PowerShell verification helpers. Created a static app-map preview and verified five paths/symbol anchors against real code. Runtime execution of newly added helpers is distinguished from syntax checks.

## Interactive checks blocked in this pass

The running tool is in session 2, identified as remote. `OpenInputDesktop` returned 0 with error 5
(access denied), and `GetForegroundWindow` returned no window. A bounded attempt to operate the
application's own tray menu received `SendInput` access denied. No unlock, elevation, security
change, user-program manipulation or alternate input route was attempted.

The old running app remains alive and reports Session suppression with a resting feeder. It was
not killed just to manufacture a new startup/interaction result. The new source was built under
`artifacts/pre-submit/build`, leaving the old running binaries intact.

Fresh candidate mouse/native regression, real screen recording and the longer performance sample
are pending an accessible interactive desktop. Prior 25 G0 / 18 feeding / 25 G3 / 7 Edge / 3 protocol
results remain scoped to their recorded earlier binaries, runtime and RDP session.

## Separate environment

`WindowsSandbox.exe` and `WindowsSandboxClient.exe` were not found in System32. No Windows
feature, reboot, firewall setting, network adapter or host SDK installation was changed. The
prepared WSB kit disables only guest networking and maps package/scripts read-only; its dedicated
results folder is the only writable host mapping. Kit creation is not a clean-room execution result.

## Sources

- Live metadata: https://builds.dotnet.microsoft.com/dotnet/release-metadata/10.0/releases.json
- Exact archive/source license URLs and hashes: `notices/dotnet-10.0.12/provenance.json`.
- Official configuration reference: https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file
- Installed official guide and public curriculum: https://github.com/challengepost/learn-ai-basics
- Current Rules re-fetch: web unavailable; direct request returned HTTP 403. Current form-specific constraints have NOT been reverified and require the participant's accessible form before submission.

Candidate hashes, clean-room configuration generation and source-audit receipts are appended after
those operations complete. Unavailable checks remain open in `devpost/checklist.md`.

## Created candidate and audit

- Candidate ZIP: `artifacts/packages/pre-submit-01/DesktopAquarium-win-x64.zip`.
- Candidate source checkpoint: `12baa4d72d75c629bf67ff98f1f12325b8435ddb`; source worktree was clean at publish.
- ZIP bytes: `73839304`; SHA-256: `C9FEB59FA731C6C812247E45964F42CBDE27B637F5BD16ABE331AFD20874A8B8`.
- Extracted copy: `artifacts/pre-submit/extracted/DesktopAquarium/`.
- All 489 file hashes/lengths matched after safe-path extraction. The inventory includes six upstream notice texts plus their provenance; case-insensitive globbing is not used to double-count them.
- Read-only audit inspected 109 historical Git blobs across 5 commits. It found zero configured credential-pattern hits and no tracked private profile/HTML. This is not an absolute secret-free or legal certification. Git author metadata is present in the local bundle and must be approved for public exposure.
- App code dependency isolation remains intact. Normal locked restore after publish passes.
- Clean-room kit created: `artifacts/pre-submit/clean-room/Offline-Aquarium.wsb`. Package/script mounts are read-only; only the dedicated results folder is writable. Networking is disabled in the guest configuration. It has not executed; the host does not have Sandbox installed.
- Source snapshot: `artifacts/pre-submit/DesktopAquarium-source-12baa4d.zip`; complete local recovery bundle: `artifacts/pre-submit/DesktopAquarium-checkpoint.bundle`. Bundle verification passed. Neither was uploaded.
- Recording helper ran its preflight and refused capture due to input-desktop access denial. No video is accepted or uploaded. Longer interactive measurements were not run.
- App-map paths/anchors and no-script/no-network structure are checked. Isolated headless Edge produced a DOM dump containing the map; this is not a completed learner walkthrough or visual acceptance of the actual app.

Remaining: normal interactive session for candidate feeding/lifecycle and recording, separate SDK-free/offline acceptance, final package review, participant-authored fields/survey, project license and public links. Actual submission remains explicitly prohibited in this preparation pass.

## Superseding RDP-reconnection result

The user reconnected RDP and chose to continue there. The access-denial blocker above is resolved. See `rdp-candidate-verification.md` for fresh runtime-10.0.12 package checks, the real local rehearsal and exact short/partial-long resource measurements. Clean-room/final review/publication gates remain. The earlier blocked recording receipt is retained separately; the current recording-status receipt identifies the successful local rehearsal, not an approved/uploaded final demo.
