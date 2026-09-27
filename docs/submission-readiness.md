# Pre-submission handoff — not a submitted entry

Current state (2026-09-27): G0–G4, the original G4 package learner check and the current source/Release Final Review are complete. After the updated app was launched, the participant accepted this implementation level and requested final documentation and GitHub synchronization. The accepted source includes the 32 approved fish frames, 100% Front display size and transparent falling/pickable feeder. See [fish verification](fish-runtime-verification.md), [feeder verification](feeder-object-verification.md) and the canonical [checklist](../devpost/checklist.md).

The current source displays Front at 100%, Middle at 86% and Rear at 72%, preserving simulation rules. Existing ZIPs predate the final size/feeder changes and are historical candidates. They are not the accepted current source and are not published release downloads.

The participant selected the noncommercial/source-available licensing strategy, authorized the original public repository and now authorized updating it. This pass changes technical documents and publishes already verified implementation; it does not add features, change licensing, publish a binary, upload a video, choose the final project name, create the contest tag or submit the Devpost form.

The local learning map was refreshed and linked with a brief evidence-based recap of the feeder transparency/input refinement. This records technical guidance tied to the owner's actual feedback and acceptance, not an invented personal reflection or new hands-on code tour.

## Remaining submission checklist

- [x] Current source/Release implementation accepted for the PoC; no further feature refinement requested.
- [x] Public repository exists with source, assets, instructions and separated licensing terms. This update carries the accepted feeder improvement and synchronized documents through the existing noreply history.
- [x] Technical final review and evidence recap recorded in `../devpost/checklist.md`; the HTML reference map remains local-only.
- [ ] Participant chooses the final project name and writes the required description/form answers.
- [ ] Record the accepted app working end-to-end; upload a publicly visible YouTube/Vimeo demo and verify anonymous access. Under three minutes is recommended. Provide English materials or English translations, including video captions where needed.
- [ ] Participant completes the actual submission form and exit survey.
- [ ] Select the final submission commit, create a fixed `v0.1-contest-submission` tag, check final links, then submit with explicit owner authorization.
- [ ] Optional binary distribution only: refresh the ZIP, include root licensing and matching third-party notices, verify the exact package in the intended environment and obtain package acceptance before publishing it.

The Rules' submission deadline is October 26, 2026 at 5:00 p.m. Eastern Time (October 27 at 06:00 Korea Standard Time). Recheck the actual form before submission. No video URL, final submission or tag is claimed here.

## Requirement basis

- Installed official Devpost Learn `6-ship/SKILL.md` and the public curriculum README describe a working demo video, a public GitHub repository, participant-written project name/short description/required form answers, and participant-written exit survey. Deployment/peer feedback are optional there.
- The [official Rules](https://learn-ai-basics.devpost.com/rules) were readable through web retrieval on 2026-09-27, although subsequent direct requests were challenged/HTTP 403. Section 4 requires a public repository with necessary source, assets and instructions, while recommending an open-source license; these are different requirements. PolyForm Noncommercial is source-available and does not meet the open-source recommendation. Separate testing access and section 7 organizer rights are addressed in `../LICENSING.md`. No organizer ruling on this project's eligibility has been obtained.
- The Rules require a publicly accessible YouTube/Vimeo demo and recommend a video under three minutes; a self-contained ZIP is not established as mandatory. Source publication does not finish the demo, participant-authored form, ownership or other eligibility requirements. Recheck the live Rules/form before actual submission.
- Public curriculum: https://github.com/challengepost/learn-ai-basics
- Rules to recheck: https://learn-ai-basics.devpost.com/rules

## Technical preparation

| Item | State |
| --- | --- |
| Core desktop feeding loop and Windows coexistence | Implemented; earlier G2/G3 evidence is recorded in verification documents |
| Candidate runtime | 10.0.12 from live official metadata, release date 2026-09-08; host SDK/shared runtime unchanged |
| Upstream notices | Original distribution/source-version notice texts preserved under notices/dotnet-10.0.12; exact NuGet runtime-pack notices added with source hashes, plus a 20-package development dependency inventory |
| Historical local candidate | `artifacts/fish-runtime/package-01/DesktopAquarium-win-x64.zip`; 489 inventory entries verified at its integration checkpoint. This archive predates 100% display size, falling feeder and final licensing documents. Refresh only as a separately verified binary release. |
| Core tests | 73 passing after the feeder-object refinement, including seven new falling/re-pickup cases; Release build has zero warnings/errors. |
| Feeder object refinement | Panel removed, unheld falling and floor/in-flight pickup implemented; 23 native feeding/transparency checks and 27 lifecycle checks passed. Included in participant acceptance of the current source/Release version; see `feeder-object-verification.md`. |
| Clean/offline verification | G4 package-02 passed offline-native-05, followed by its learner check. This evidence does not certify future artwork/package changes. |
| Fish artwork | All 32 extracted PNGs approved; exact RGBA atlas round trips and 73 native-size WPF checks passed, including visible-pixel equality, clipping and edge culling. Current presentation accepted for the PoC; logical-geometry limitations remain documented. |
| Screen recording | A 7.95-second cropped local rehearsal recorded; sampled-frame review done, final owner review/recording and upload still pending |
| Source/history audit | Pre-change scan: 20 commits, 156 tracked files, 278 historical blobs; no configured credential-pattern hits or private learner HTML/profile in history. Final publication scan is recorded below. Git history includes ordinary author metadata; scanning is not proof of absence of every secret. |
| App map | Local-only reference refreshed against the accepted source; feeder evidence recap recorded. No personal learning claim or new interactive code tour inferred. |

## Participant-owned submission items and repository access

Final project name: **participant to provide**. “Desktop Aquarium” remains a working label.

Final description and required form answers: **participant to write**. No draft submission or narration is generated here.

Project license/publication choice: **selected by participant** — PolyForm Noncommercial 1.0.0 for project-owned code, separate assets and upstream terms. See `../LICENSING.md`; this is not OSI open source.

Public repository URL: [snowmuffin/contest-01-build-with-ai-basics](https://github.com/snowmuffin/contest-01-build-with-ai-basics) is **public and populated** on branch `master`. After reviewing the publication contents and contest requirements, the owner authorized posting on 2026-09-27 and stated that asset rights had been reviewed separately. This records the owner's decision, not an organizer ruling on eligibility or a new legal determination.

GitHub initially rejected the original history with GH007 email privacy protection. Publication now uses a separate copy with `77647785+snowmuffin@users.noreply.github.com` as the author/committer email. The first published source head is `39937d99369db2a317f44a9ac57bf4ed10d217c7`. All 22 original commits were compared: trees, names, dates, full messages and parent relationships are preserved, with email metadata and resulting commit IDs changed. The original local history and unfinished work remain intact, and email protection remains enabled. No force-push was used. Historical local commit identifiers elsewhere in these records refer to the original history and can differ from public identifiers.

At the initial publication checkpoint, anonymous access verification passed for repository visibility, all 22 public commit identities, and exact raw bytes of README, LICENSE, scope, PRD and spec. A following publication-status commit brought that public history to 23 commits. The accepted feeder source and this documentation update extend the same history without force-push; the private mapping and current access receipts remain in ignored `artifacts/publication-export/`. This is source publication only: no binary release, video upload, Devpost submission or final contest tag.

Demo video URL: **not uploaded**. Confirm the actual final recording and public access without exposing private desktop contents.

Exit survey: **participant to complete**.

Final package use/review: **only needed before a new binary release**. The original G4 package learner check and current source/Release acceptance are complete; neither certifies a future package.

Devpost Submit: **DO NOT EXECUTE** in this preparation pass.

## Final submission and later commercial work

The audit counts below are historical checkpoint counts. The current documentation/publication pass checks its staged paths, relative links, source and notice byte preservation, new commit contents, public noreply ancestry and source-tree equivalence. It verifies public access after the authorized push and keeps the resulting receipt locally. It does not reinterpret earlier scans as a guarantee that all secrets or legal risks are absent.

Publication document checks on 2026-09-27: official PolyForm text matches its pinned source SHA-256; 30 relative links/anchors resolve; all existing application/script/test/asset-pixel and upstream-notice hashes are unchanged; the 20-package development inventory matches the lockfile. The staged publication contains 165 tracked files, no application code changes, no configured credential-pattern hits and no local profile/HTML/agent/artifact files. The legacy uncommitted atlas and untracked cleaner remain local. Evidence: ignored `artifacts/licensing/{audit-before.json,document-validation.json,index-audit.json}`. These checks do not establish legal title or guarantee detection of every secret.

Historical before-push audit at original local commit `3478c5b`: 21 commits, 165 tracked files and 298 historical blobs; no configured credential-pattern or private-document findings. A subsequent pre-publication review at original local commit `8d3989b` covered 22 commits, 165 tracked files and 300 historical blobs, finding no additional configured credential/private-path matches. Private commit email metadata was addressed in the owner-approved public copy described above. The existing audit script's publication/owner-pending fields are static checklist hints, not live GitHub status.

Local publication evidence is excluded from Git under `artifacts/publication-review/` and `artifacts/publication-export/`, including the redacted audit, original-history backup, commit mapping and anonymous-access receipt. Only committed source was exported: the dirty legacy atlas version and untracked cleaner were not added. The already committed legacy atlas remains historical project material and is not used by the current application. Optional file cleanup was not part of this publication pass.

When the owner approves the actual submitted version, record its exact commit, create a fixed tag such as `v0.1-contest-submission`, and preserve it through judging. No tag is created in this pass. Later Steam work may continue on another branch or in a private commercial repository. The owner can separately license only rights the owner holds; existing license grants and upstream obligations remain. Contribution/relicensing policy remains an internal owner consideration, not a CLA system added for this contest.

The current source publication does not publish a binary ZIP. `../THIRD_PARTY_NOTICES.md` records the remaining package notice-copy/inventory work. Documentation edits preserve application, script, test, asset and license bytes. Existing native evidence is tied to the unchanged implementation; no interactive native tests or new performance claim are needed for these text edits. Source restore/build/tests can be checked in the independent public copy without disturbing the running development app.

## Internal quality gates, not extra contest rules

Separate SDK-free/offline execution, local-console display validation, sustained resource checks, and a clean extracted-package run are this project's verification plan. They were not established as organizer-mandated submission fields. Keep missing evidence explicit; obtaining a ZIP does not complete these checks.

## Refinements after readiness review

The accepted Final Review includes solid feeder presentation, four stable fish silhouettes, directional poses and restrained depth perspective; see the canonical PRD/checklist. The artwork and feeder refinements have proportional regression evidence and current source acceptance. No rarity/growth, other operating systems or multi-monitor scope was added. A future ZIP still needs independent package acceptance.

## Historical RDP recheck

Input access is restored. Fresh candidate verification and a real local rehearsal are recorded in `rdp-candidate-verification.md`. No console transfer, owner licensing/naming decision, public posting or final submission occurred. The longer benchmark was partial; do not report all three 60-second phases as passed.

## Historical G4-only update

The latest G4 pass completed ordinary, feeding and hidden measurements for 60 seconds each and normal exit (eight assertions). This supersedes the earlier partial-long benchmark as current evidence; it is not a long-duration certification. GPU counters returned no PID instances and cannot be reported as zero. See `g4-verification.md`. G4 remains open only for the real separate SDK-free/offline environment test among the unfinished mechanical tasks; final user review is a subsequent owner checkpoint. No later submission work was performed.

## Historical G4 clean-room update

The separate Windows Sandbox run completed for G4 package-02. offline-native-05 passed with no global dotnet/SDK, no guest runtime networking, 489 verified payload hashes, package-local .NET 10.0.12 loading, 18 feeding checks, 25 lifecycle checks, clean process/capture teardown and unchanged payload hashes. Source locked restore, Release build and 64 Core tests passed at that checkpoint. Its package learner check subsequently completed. Current source review, recap and public repository status are recorded above; this old package result does not certify newer bytes.
