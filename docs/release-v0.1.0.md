# Desktop Aquarium v0.1.0 — portable release verification

Owner request (2026-09-28): publish a downloadable release so reviewers can try the accepted app without building it. Classification: optional distribution improvement. No application behavior, fish assets, dependency version, licensing terms or product scope change is included.

Release page: https://github.com/snowmuffin/contest-01-build-with-ai-basics/releases/tag/v0.1.0

Planned asset: `DesktopAquarium-v0.1.0-win-x64.zip`, a portable Windows 11 x64 folder with .NET 10.0.12 included. Extract the whole folder onto the Desktop or another stable location; `Start-Aquarium.cmd` opens the aquarium and feeder. `Setup-FeederShortcut.cmd` optionally creates **Feed Fish.lnk** on the user's Desktop, preserves unrelated shortcuts and does not alter execution policy or login startup.

Packaging now includes `LICENSE`, `LICENSING.md`, `ASSET_NOTICE.md`, `THIRD_PARTY_NOTICES.md`, matching runtime notices and development notice records. Original code, project assets and third-party binaries retain their separate terms. PDBs and test drivers are not distributed. The official .NET 10 release metadata still reports runtime 10.0.12 on 2026-09-28; the existing exact notice texts are preserved.

## Verification status

Pending in this source checkpoint: build/test, exact ZIP inventory and notice review, SDK-free/offline Windows Sandbox execution, Desktop launcher/shortcut checks, existing native feeding/lifecycle regressions and anonymous release download verification. No result is marked passed before execution. The published release notes and subsequent update to this record will identify exact source and asset hashes.

The v0.1.0 release tag pins the package build source. It is not a claim that the initially submitted Devpost entry referred to that exact commit, and it does not move a contest-submission tag. Original local history and the uncommitted legacy atlas/cleaner remain preserved.

## Limits

- Windows 11 x64, primary display; no new ARM, multi-monitor or other-OS claim.
- Unsigned prototype; Windows may show a reputation warning. Do not disable security protections.
- Keep the entire extracted folder together. Moving only the EXE breaks the portable layout; after moving the folder, recreate its shortcut deliberately.
- Sandbox/RDP verification is not broad physical-device compatibility certification or a new participant hands-on review.
- Devpost's required public source URL remains available separately from the optional download URL.
