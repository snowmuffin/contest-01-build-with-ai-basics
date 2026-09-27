# Desktop Aquarium v0.1.0 — portable release verification

Owner request (2026-09-28): publish a downloadable release so reviewers can try the accepted app without building it. Classification: optional distribution improvement. No application behavior, fish assets, dependency version, licensing terms or product scope change is included.

Release page: https://github.com/snowmuffin/contest-01-build-with-ai-basics/releases/tag/v0.1.0

Published asset: [DesktopAquarium-v0.1.0-win-x64.zip](https://github.com/snowmuffin/contest-01-build-with-ai-basics/releases/download/v0.1.0/DesktopAquarium-v0.1.0-win-x64.zip), a portable Windows 11 x64 folder with .NET 10.0.12 included. Extract the whole folder onto the Desktop or another stable location; `Start-Aquarium.cmd` opens the aquarium and feeder. `Setup-FeederShortcut.cmd` optionally creates **Feed Fish.lnk** on the user's Desktop, preserves unrelated shortcuts and does not alter execution policy or login startup.

Packaging now includes `LICENSE`, `LICENSING.md`, `ASSET_NOTICE.md`, `THIRD_PARTY_NOTICES.md`, matching runtime notices and development notice records. Original code, project assets and third-party binaries retain their separate terms. PDBs and test drivers are not distributed. The official .NET 10 release metadata still reports runtime 10.0.12 on 2026-09-28; the existing exact notice texts are preserved.

## Verification status

Completed on 2026-09-28 (KST). GitHub publication timestamp: 2026-09-27 17:00:53 UTC. Release ID: `397733551`.

| Check | Result |
| --- | --- |
| Source checkpoint | Public commit `a38e8194e07fef0b346ffdcd41e4545a80d24080`; clean public working copy at packaging. Application source, tests and assets match previous public commit `88ed4f6d282b3a6080cf95865373102b6a8b1235`. |
| Build and Core regressions | Locked restore, Release build with zero warnings/errors, 73/73 tests passed. Publish did not modify the source lockfiles. |
| ZIP inventory | 74,839,226 bytes; all 496 inventory entries and the inventory file itself match the archive. No PDBs or test drivers included. |
| Upstream/runtime integrity | 468 runtime files match the exact pinned NuGet runtime packs; both package SHA-512 hashes match recorded provenance. All root licensing documents and shipped notices match repository bytes. |
| Clean environment | Fresh Windows Sandbox, Windows build 26100 x64, no global dotnet/SDK, zero default routes. Execution policy remained `Restricted`. |
| Desktop workflow | Extracted the actual ZIP onto the guest Desktop. Direct `Start-Aquarium.cmd` and the actual Desktop **Feed Fish.lnk** both started the packaged app. |
| Shortcut safety | Create, reuse without changing bytes, and refusal to overwrite an unrelated shortcut all passed. Target, arguments and bundled icon checked. No security-policy change. |
| Runtime loading | `hostfxr.dll`, `hostpolicy.dll` and `coreclr.dll` loaded from the extracted package. |
| Existing native regressions | 23/23 feeding/transparency assertions and 27/27 lifecycle/input/normal-tray-exit assertions passed. |
| Guest orchestration | 24/24 checks passed; complete package hashes remained unchanged. Test Sandbox stopped afterward. |
| Public download | Downloaded both release assets without authentication; ZIP hash matches the tested archive and checksum file. Tag resolves to the exact package source commit. |

ZIP SHA-256: `ab4afb6bcc1cdc393af96574f1208d8b88c01f799bd8f440851bdbacc4a78798`.

Local evidence is retained in ignored `artifacts/release-v0.1.0/`: package verification, Core TRX, `sandbox-02/results/acceptance.json`, native reports, anonymous-download verification and publication mapping. The first guest attempt remains recorded as a verifier failure: a detached GUI inherited captured output pipes, leaving the launch observer waiting while the app was running. The runner was corrected; the package bytes were unchanged for the successful second attempt. Launcher smoke checks stopped only their recorded package-owned PIDs; normal tray Exit was independently verified by the unchanged lifecycle harness.

The v0.1.0 release tag pins the package build source. It is not a claim that the initially submitted Devpost entry referred to that exact commit, and it does not move a contest-submission tag. Original local history and the uncommitted legacy atlas/cleaner remain preserved.

GitHub reported server-enforced release immutability as disabled; this record does not claim immutable-release enforcement. The published tag and assets are to remain fixed. A future binary change requires a new version.

## Limits

- Windows 11 x64, primary display; no new ARM, multi-monitor or other-OS claim.
- Unsigned prototype; Windows may show a reputation warning. Do not disable security protections.
- Keep the entire extracted folder together. Moving only the EXE breaks the portable layout; after moving the folder, recreate its shortcut deliberately.
- Sandbox/RDP verification is not broad physical-device compatibility certification or a new participant hands-on review.
- Devpost's required public source URL remains available separately from the optional download URL.
