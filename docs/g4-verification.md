# G4 package candidate verification

> Latest environment update: Windows Sandbox is enabled after the owner-managed reboot, and the offline-native-05 no-SDK/no-network guest verification passed. G4 mechanical verification is complete; only the actual-package learner check remains.

## Actual-package learner check - PASS

After the clean-room pass, the owner used the actual package-02 build in the RDP session and reported that it worked well. The diagnostic receipt at artifacts/g4-only-20260926/learner-check-state.json showed five fish, the feeder in Resting mode, nine food items emitted and nine consumed, and the application still alive after the check. This records the G4 learner check without inferring a more detailed manual sequence than the owner reported.

With this learner check plus the completed mechanical verification above, G4 is complete. Final kick-the-tires, Final Review, the learning wrap-up and submission work remain separate later steps and were not started.

## Final SDK-free/offline Sandbox result - PASS

The rebuilt package-02 candidate passed the remaining clean-environment gate after Windows Sandbox activation and reboot. Final evidence is artifacts/g4-only-20260926/offline-native-05/results/acceptance.json.

The guest was Windows 11 Enterprise x64 10.0.26100. Before application execution, global dotnet was absent, SDK-directory count was zero, default-route count was zero, non-loopback-address count was zero, enabled-network-adapter count was zero, and Python was not on PATH. The same SDK/network conditions were rechecked after the native tests.

All 489 package payload entries matched after extraction. The app initialized five fish and feeding support before the test-only Python driver was extracted. hostfxr.dll, hostpolicy.dll and coreclr.dll all loaded from the package app directory and reported .NET 10.0.12. Feeding passed all 18 existing native assertions with reported exit code 0; lifecycle passed all 25 with reported exit code 0. Each test left no resident aquarium process or captured input, and package payload hashes still matched after all testing.

Earlier guest attempts are retained rather than rewritten. offline-native-01 exposed a startup-readiness race; offline-native-02 proved the 18 feeding assertions while PowerShell process exit-code capture returned null; offline-native-04 exposed an empty exit-code side-file race. These were verifier defects. The final harness waits for five-fish readiness and uses each native report's own recorded exit code. No product source, artwork or behavior changed.

After the successful guest run the host source was again restored in locked mode, built Release with zero warnings/errors, and all 64 core tests passed. Windows Sandbox was then stopped. G4 mechanical verification is complete; the checklist still waits for the actual-package learner check before marking G4 complete.

## G4-only verification pass ? 2026-09-26

**Current gate: partial G4; only separate SDK-free/offline environment execution remains technically blocked.** The owner asked to stop at G4. Final owner review, learning wrap-up, video/publication and submission steps were not started or marked complete in this pass.

The measured package is the unchanged `pre-submit-01` Windows x64/runtime-10.0.12 candidate, application checkpoint `12baa4d`. All 489 inventory hashes/lengths and the original ZIP hash were checked again. Source locked restore, Release build and 64 core tests passed. The application source and artwork have not changed.

### Completed finite three-phase measurement

A single run completed ordinary habitat, held shaking/feeding and manual hidden, each for the requested 60 seconds, followed by safe restoration and normal tray Exit. All eight verification assertions passed: phase durations, stable five-fish identity, food cap/accounting, hidden rendering/simulation/emission stop, resting recovery, and normal exit. This supersedes the earlier partial benchmark as the latest completed finite run; it does not erase the failed earlier attempts.

Environment: Windows 11 host, RDP session, 1512 x 949 at 100% scale, 32 logical processors. Diagnostic output was enabled; unrelated host work was not isolated. CPU is this process normalized across all logical processors, not one-core utilization. Whole-system baseline was 3.991% for 4.05 seconds; it is not subtracted to invent an incremental cost.

| Phase | Seconds | App CPU | End working set (MiB) | Render callbacks/s |
| --- | ---: | ---: | ---: | ---: |
| ordinary habitat | 60.01 | 0.4760% | 134.11 | 19.86 |
| held shaking / feeding | 60.02 | 0.1936% | 139.87 | 20.58 |
| manual hidden | 60.04 | 0.0407% | 146.09 | 0.00 |

The feeding interval emitted 799 new pellets and consumed 717, with up to 64 alive concurrently. At every sampled point, total emitted equalled consumed + expired + currently live food. Hidden samples had zero new frames, no time advancement, and no new emission. Working set figures include runtime/cache effects; three minutes does not establish absence of leaks or a battery/low-end performance guarantee. Visible render rate remains around 20 callbacks/s in this RDP setting rather than a verified 30-fps presentation guarantee.

A read-only per-process GPU companion made 80 observations without a query error, but the Windows provider returned no engine instances for this PID. GPU utilization is therefore **unavailable, not 0%**. WPF callback metrics are available in the local receipt; they measure recent callback timing, not compositor/GPU presentation latency. The hidden state's cached callback statistics are historical and must not be interpreted as hidden rendering.

Evidence: `artifacts/g4-only-20260926/measurement-01/report.json`, `gpu-samples.json`, `tests/g4-only.trx`, `summary.json`.

### Environment gate, not an application failure

Read-only discovery found `Containers-DisposableClientVM` and `Microsoft-Hyper-V-All` in state 2 (Disabled), no WindowsSandbox executable/package, and a Linux Docker Desktop context with no existing Windows guest candidate found. No feature was enabled, no VM was installed, no RDP/console transfer was attempted, and host networking/security policies were not changed. The existing clean-room kit remains prepared but unexecuted.

The required separate Windows test without an SDK and without runtime networking has **not run**. A bundled-runtime test on this SDK-equipped host is not substituted for that requirement. Enabling Windows Sandbox requires an administrator action and may require a restart; obtain owner consent before doing so. G4 remains unchecked until that actual environment test passes. Final review/learning/submission remain later work and are not authorized by this G4-only request.

Official feature-state reference: https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-optionalfeature
Sandbox installation: https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-install

### Repackaging retry

Repackaging from checkpoint `3ee50d5` compiled successfully, but Windows PowerShell's `Compress-Archive` failed in `Write-Progress` with `IndexOutOfRangeException` under the noninteractive tool host. `package-01` is an unsuccessful partial artifact, not an accepted ZIP. The publish wrapper now suppresses only archive progress display inside a scoped try/finally; real compression failures still propagate. Retry uses a fresh `package-02` folder and must pass full extraction/hash verification. The previously measured pre-submit-01 candidate is unchanged.

### Rebuilt G4 candidate result

The repaired wrapper successfully produced `artifacts/g4-only-20260926/package-02/DesktopAquarium-win-x64.zip` from clean checkpoint `0f500a5b3e8557edf33b57e8d948eb9ca6ba7e03`. ZIP size: 73839296 bytes; SHA-256: `9D81CE80BD5DE715606C842A88D5D0DA41BF617F00F4C548F5C08F9BE07A52D2`. All 489 inventory entries were verified after extraction into `artifacts/g4-only-20260926/extracted-02/DesktopAquarium/`.

All 26 application source-input hashes match the measured pre-submit-01 source. The rebuilt EXE/DLL/PDB files are not byte-identical; generated assembly informational versions include the newer Git revision. The initial byte-equivalence expectation was rejected, rather than used to transfer test passes. The rebuilt executable was separately tested: 18 actual feeding checks, 25 lifecycle checks, package-local .NET 10.0.12 module loading and normal smoke-test exit passed. A post-publish normal locked restore, Release build and all 64 core tests passed. The resource table above remains a measurement of pre-submit-01, not a fresh performance run on these rebuilt bytes.

A fresh `artifacts/g4-only-20260926/offline-kit/Offline-Aquarium.wsb` targets this rebuilt candidate. Guest networking is disabled; package/script folders are mapped read-only and only the dedicated result folder is writable. Configuration and paths were checked, but Sandbox has not run because the host feature is disabled. This is still the remaining mechanical G4 environment gate.

### Measurement-tool changes

The test now preserves requested duration separately from summary variables, refuses to overwrite an existing report, writes its current phase/PID for a bounded GPU sampler, and asserts behavior across all sampled states. Only test tools were changed; the product was not modified. The older owner instance was exited normally using keyboard navigation on its verified active tray menu after a pointer target overlapped a shell region. No unowned window received synthetic input.


> Historical runtime-10.0.10 candidate evidence. The newer runtime-10.0.12 preparation pass and its still-pending native/clean-room checks are in `pre-submit-verification.md`. Do not transfer these old runtime test passes to the new package automatically.

## Historical 10.0.10 candidate status

**Partial G4 checkpoint, not a completed release.** G2 live feeding is saved as `d2f35a4`; G3 recovery as `d26b420`. The self-contained candidate is built and tested on the existing RDP host. A genuinely separate no-SDK/offline environment, sustained GPU/frame-time testing and final hands-on review are still outstanding. No repository was published, visibility changed, final license selected, or competition entry submitted.

## Historical 10.0.10 candidate

Relative to the project root:

- ZIP: `artifacts/packages/g4-d26b420-r2/DesktopAquarium-win-x64.zip`
- Extracted verification copy: `artifacts/g4/extracted-r2/DesktopAquarium/`
- Source application checkpoint: `d26b420935744e4824e304882b51cffec80ae954`.
- Bundled .NET Core and Windows Desktop runtime: `10.0.10`.
- ZIP bytes: `73718239` (70.30 MiB).
- ZIP SHA-256: `A031758C62309273205DC273E22D066421D24670829476941365F08B7F93E369`.
- Inventory: 482 payload file hashes and lengths checked after extraction; unsafe archive paths rejected.

The R2 republish changes the packaging-restore behavior, not application code. All application/runtime payloads match the originally tested candidate byte-for-byte. The only payload byte difference was README line endings; normalized text is identical. `artifacts/g4/r2-comparison.json` records this. The ZIP hash differs because archives include their own metadata/content representation. R2 startup was rerun explicitly.

The package uses a full `app/` runtime folder, not a promise of one EXE. `Start-Aquarium.cmd` starts the packaged executable directly. Optional `Setup-FeederShortcut.cmd` refuses an existing shortcut pointing to another executable. The installed Desktop link still targets the development Release build; it was deliberately not migrated or overwritten by package tests.

## What was actually tested

| Check | Result / limit |
| --- | --- |
| Release publish with explicit win-x64 and runtime 10.0.10 | Passed; no shared SDK/runtime installation changed |
| ZIP extraction and 482 payload hashes | Passed for R2 |
| Packaged live feeding integration | 18 passed on R1 payload, which matches R2 app/runtime hashes |
| Packaged lifecycle/tray integration | 25 passed on that same payload |
| Packaged startup with SDK removed from child PATH and intentionally invalid DOTNET_ROOT/X64 | Passed; only the spawned process environment was changed |
| Actual loaded hostfxr / hostpolicy / coreclr modules | All three loaded from the package's own app folder, not the machine's shared runtime |
| R2 startup and normal timed exit | Passed again, exit 0 |
| Normal source locked restore after packaging | Initially failed, repaired, then passed after a new publish |
| Final source Release build and core tests | Passed; 64 tests, no reported build warnings/errors beyond the existing documented WFO0003 exception |
| Truly separate SDK-free computer | Not run |
| Runtime networking unavailable | Not run; the host was not disconnected and no firewall/security policy was changed |

Receipts are local, ignored artifacts:
`artifacts/g4/feeding-native/report.json`, `lifecycle-native/report.json`,
`startup/report.json`, `startup/host-trace.log`, `r2-comparison.json`, and
`test-results/final-source.trx`.

An invalid DOTNET_ROOT plus observing package-local runtime modules proves this process used its bundled runtime. It does **not** make this SDK-equipped machine a clean machine, nor prove network isolation.

## Short resource sample, not a performance certification

`artifacts/g4/performance/report.json` contains a short process sample from the extracted Release package. Conditions: existing RDP session, 2160 x 3840, 150% scaling, 32 logical processors, local diagnostic output enabled. Each app phase was about five seconds. Other host work was not isolated. CPU below is normalized across all 32 logical processors. The whole-system baseline is not subtracted from process CPU.

| Phase | Seconds | App CPU, all logical processors | Working set at end (MiB) | Observed render frames/s |
| --- | ---: | ---: | ---: | ---: |
| ordinary habitat | 5.04 | 1.5221% | 203.59 | 20.25 |
| held shaking / feeding | 5.05 | 1.2870% | 197.86 | 20.41 |
| manual hidden | 5.05 | 0.0290% | 200.59 | 0.00 |

No-aquarium whole-system baseline was about 2.507% over four seconds, with other applications present. This is context, not a causal estimate of aquarium overhead. Visible rendering was about 20 frames/s in this RDP sample, below the nominal 30-update target; local-console and frame-latency evidence is needed before judging perceived smoothness or adjusting the renderer. No GPU utilization or per-frame latency was measured. No battery/low-resource guarantee or leak-free sustained-run claim is made.

The hidden phase produced zero render frames and zero new food; private bytes stayed unchanged during that short phase. The held-shake phase reached but did not exceed the configured 64-pellet limit. These finite samples do not replace long-duration checks.

## Packaging repair

The first RID-specific publish modified the normal Core/Windows lockfiles to include `win-x64`, causing the next plain `dotnet restore Aquarium.slnx --locked-mode` to fail with NU1004. The source project dependencies were re-evaluated explicitly with `--force-evaluate` and then locked restore passed. No user source changes were discarded.

`Publish-Windows.ps1` now routes publish restore to a fresh artifact-only lock path, disables publish-only lock generation, and checks the canonical source lockfile hashes before/after publish. The test-project package versions remain pinned. A second publish followed by locked restore, Release build and 64 tests passed. Canonical source lockfiles are identical to their committed versions. Use the wrapper rather than a bare RID publish that can mutate normal development restore state.

Official restore-property reference: https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files

## Dependency servicing and publication limits

The package includes runtime 10.0.10 from the official 10.0 metadata snapshot consulted during this work, whose latest-release date was July 14, 2026. That observation is not a claim to have established the latest servicing patch for all later dates. Recheck before public distribution. The installed SDK 10.0.202 and shared runtime 10.0.6 were not upgraded.

Metadata: https://builds.dotnet.microsoft.com/dotnet/release-metadata/10.0/releases.json

The generated package includes the project's dependency/provenance record. Publish output did not include separate runtime LICENSE/NOTICE files under app/; collecting the exact required redistribution notices and final source-license review remain publication work. Do not label this local candidate a license-audited public release.

## Remaining completion criteria

- Run the whole extracted folder on a controlled, separate Windows 11 x64 environment without a developer SDK and with networking unavailable. WindowsSandbox was not found on this host's PATH; no Windows feature was installed/enabled in this task.
- Test local-console display behavior and any claimed DPI/session combinations, rather than extrapolate from RDP or simulated notifications.
- Measure sustained resource use and frame latency/GPU where available. The current five-second sample is preliminary.
- Complete the planned final learner exploration, resolve feedback, then perform the one learning wrap-up/app-map and prepare authorized submission/publication.

No new feature, external runtime service, species system or cross-platform promise was added.
