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
