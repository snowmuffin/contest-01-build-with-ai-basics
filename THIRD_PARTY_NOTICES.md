# Third-party notices and dependency record

The root [LICENSE](LICENSE) covers only the project-owned scope described in [LICENSING.md](LICENSING.md). It does **not** relicense Microsoft software, other dependencies, upstream boilerplate, the Devpost Skill Pack or third-party notice texts. Project assets have separate terms in [ASSET_NOTICE.md](ASSET_NOTICE.md).

Application code was created for this project during the contest period. The solution and initial project files were bootstrapped with .NET SDK 10.0.202 templates, then adapted to the approved plan. No earlier application codebase is claimed as newly created work. SDK/template material retains any applicable upstream terms; invoking a template does not transfer ownership of the SDK.

## Actual application and runtime dependencies

The application projects have no external application NuGet dependencies beyond the .NET desktop framework. The archived self-contained candidate's `Aquarium.Windows.deps.json` identifies these two runtime packs at 10.0.12, alongside Aquarium.Core and Aquarium.Windows:

| Component | Upstream terms and provenance |
| --- | --- |
| [Microsoft.NETCore.App.Runtime.win-x64 10.0.12](https://www.nuget.org/packages/Microsoft.NETCore.App.Runtime.win-x64/10.0.12) | NuGet package declares MIT. Exact package [license](notices/dotnet-10.0.12/nuget-core-LICENSE.TXT) and [third-party notices](notices/dotnet-10.0.12/nuget-core-THIRD-PARTY-NOTICES.TXT) are preserved. Component-specific third-party terms remain applicable. |
| [Microsoft.WindowsDesktop.App.Runtime.win-x64 10.0.12](https://www.nuget.org/packages/Microsoft.WindowsDesktop.App.Runtime.win-x64/10.0.12) | NuGet package declares MIT. Exact package [license](notices/dotnet-10.0.12/nuget-desktop-LICENSE) is preserved. WPF and Windows Forms source notices are retained separately below. |
| Windows APIs / SDK / tooling | Win32 calls use the user's operating system. No separate Windows SDK redistributable package appears in the application lockfiles or inspected publish dependency manifest. SDK/tool terms are not replaced by PolyForm. Native files supplied by the runtime packs, including D3DCompiler_47_cor3.dll, remain upstream components. Recheck terms if another SDK redistributable is introduced. |

[runtimepack-provenance.json](notices/dotnet-10.0.12/runtimepack-provenance.json) records exact NuGet package SHA-512, preserved notice hashes and seven representative binary matches against the archived publish output. Both downloaded official package archives matched the restored cache on 2026-09-27. This identifies the actual publish inputs; it is not a claim that every .NET distribution has identical licensing files.

The existing [distribution provenance](notices/dotnet-10.0.12/provenance.json) is retained unchanged. Its standalone runtime ZIP contains **Microsoft .NET Library terms**, whereas the NuGet runtime packs used by `dotnet publish` contain MIT license text. These different distribution sources must not be conflated. The existing runtime ZIP LICENSE/ThirdPartyNotices and supplementary WPF/WinForms v10.0.12 source notices remain unmodified historical evidence. The Windows Desktop ZIP had no standalone notice files; the WPF/WinForms source notices are labelled as supplementary rather than extracted from that ZIP.

Microsoft documents [self-contained publishing](https://learn.microsoft.com/en-us/dotnet/core/deploying/) as including the runtime, and [distribution packaging](https://learn.microsoft.com/en-us/dotnet/core/distribution-packaging) distinguishes framework/reference/runtime packs and upstream licensing files. A project license cannot override those terms. The public Git repository contains source and notices, not the Microsoft runtime binaries.

## Development-only dependencies

[notices/development-dependencies.json](notices/development-dependencies.json) inventories all 20 packages and exact resolved versions from [the test lockfile](tests/Aquarium.Core.Tests/packages.lock.json), with corresponding NuGet license metadata. These test dependencies are not included in the aquarium application package.

| Package family | Resolved versions | Declared package terms |
| --- | --- | --- |
| MSTest, MSTest.TestAdapter, MSTest.TestFramework, MSTest.Analyzers | 4.0.2 | MIT; [microsoft/testfx](https://github.com/microsoft/testfx) |
| Microsoft.Testing.Platform / MSBuild and Telemetry, TrxReport, TrxReport.Abstractions, VSTestBridge extensions | 2.0.2 | MIT; [microsoft/testfx](https://github.com/microsoft/testfx) |
| Microsoft.NET.Test.Sdk, Microsoft.CodeCoverage, Microsoft.TestPlatform.AdapterUtilities / ObjectModel / TestHost | 18.0.1 | MIT as declared by their package metadata; [microsoft/vstest](https://github.com/microsoft/vstest) |
| Microsoft.Testing.Extensions.CodeCoverage | 18.1.0 | Separate Microsoft .NET Library terms, **not MIT**; exact [package license](notices/development/Microsoft.Testing.Extensions.CodeCoverage-18.1.0-LICENSE.txt) and [official package page](https://www.nuget.org/packages/Microsoft.Testing.Extensions.CodeCoverage/18.1.0) |
| Microsoft.ApplicationInsights | 2.23.0 | MIT; [Microsoft/ApplicationInsights-dotnet](https://github.com/Microsoft/ApplicationInsights-dotnet) |
| Microsoft.DiaSymReader / Microsoft.Extensions.DependencyModel | 2.0.0 / 6.0.2 | MIT; [dotnet/symreader](https://github.com/dotnet/symreader), [dotnet/runtime](https://github.com/dotnet/runtime) |
| Newtonsoft.Json | 13.0.3 | MIT; [JamesNK/Newtonsoft.Json](https://github.com/JamesNK/Newtonsoft.Json) |

Pillow 11.0.0 is used only for development-time asset generation/extraction/review; its installed metadata identifies MIT-CMU. See the [upstream license](https://github.com/python-pillow/Pillow/blob/11.0.0/LICENSE). Python, FFmpeg and browser tools used in local verification retain their own licenses and are not bundled with the application. The application makes no runtime call to ChatGPT or another AI service.

## Devpost curriculum

The [Devpost Learn Skill Pack](https://github.com/challengepost/learn-ai-basics) is separately installed development curriculum, not original application code. [skills-lock.json](skills-lock.json) records its source and hashes. No repository-wide license was declared in the upstream repository metadata inspected on 2026-09-27; do not assume MIT or offer the curriculum under PolyForm. Local `.agents/`, `.claude/` and `agent/` installations are excluded from public commits. The project-specific planning documents remain in `devpost/` as required by the contest. The official install command is documented in the upstream README.

## Project-created assets

The feeder PNG/ICO are deterministic project artwork from [Generate-Assets.py](scripts/Generate-Assets.py); the resident icon uses that ICO. The approved fish preview was supplied by the participant, with the subsequently declared ChatGPT generation circumstances recorded in [provenance.json](assets/fish/source/provenance.json). Independent extraction preserved source RGB; approved PNGs were packed unchanged into the current runtime atlas. No external fish artwork was fetched for that extraction/integration pass. The legacy `fish-atlas.png` is not used by the current runtime. These are asset provenance facts; applicable reuse permissions and AI-rights limitations are in [ASSET_NOTICE.md](ASSET_NOTICE.md).

## Binary distribution plan — separate from public source

Existing ZIPs are local historical candidates. They predate the current licensing documents and are **not approved for public redistribution by this documentation pass**. Before a public binary release, include `LICENSE`, `LICENSING.md`, `ASSET_NOTICE.md`, this file and the exact notices for all shipped upstream components, preserve attribution, and recheck the actual package inventory and distribution obligations. Keep the three licensing scopes explicit to recipients. If distributing Microsoft-library-terms components, separately satisfy those terms, including their downstream protection requirements; an application PolyForm license alone is not a substitute.

The updated publish script copies all four root licensing documents (`LICENSE`, `LICENSING.md`, `ASSET_NOTICE.md`, this file), the selected `notices/dotnet-<version>/` folder and the development-dependency notice records. It verifies the preserved distribution and actual NuGet runtime-pack notice hashes. Development notice records do not mean development tools are bundled. The owner authorized a separate portable release on 2026-09-28; its exact package and validation are recorded in [release verification](docs/release-v0.1.0.md). Earlier source-publication passes did not authorize their historical ZIPs. Self-contained distribution is a project choice, not an extra contest requirement.

## Earlier G4 publication checkpoint (superseded by the pre-submission candidate below)

The self-contained candidate includes .NET Core and Windows Desktop runtime 10.0.10 and the bundled original fish/feeder assets. Its app/ publish output did not automatically include standalone runtime license/notice text files. The project's final source license and required runtime/dependency redistribution notices must be collected/reviewed before public distribution. This dependency summary alone is not a completed license audit, and no public release was made.

## Pre-submission runtime candidate

The current candidate is pinned to .NET 10.0.12 (live official metadata release date 2026-09-08).
`notices/dotnet-10.0.12/` preserves the exact runtime distribution LICENSE and ThirdPartyNotices bytes,
with archive SHA-512 verification and per-file SHA-256 provenance. The Windows Desktop ZIP did not
contain standalone notice files; any supplementary source notices are identified separately in the
manifest and are not misrepresented as extracted binary-distribution files.

These files describe upstream dependencies only. The subsequent source-publication decision is
recorded in LICENSING.md; it does not relicense these components. Test-only FFmpeg/Python/browser
tools are not included in the application package. The archive observations above remain historical.
