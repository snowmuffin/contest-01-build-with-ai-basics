# Submission record and technical handoff

Portable release follow-up (2026-09-28): the owner requested publishing a ready-to-run ZIP and download link. Work is authorized for v0.1.0, with complete source/asset/runtime notices and a fresh check of the exact archive in Windows Sandbox, including Desktop extraction and the **Feed Fish** shortcut. See [release verification](release-v0.1.0.md). This is optional distribution of the accepted app, not a change to contest scope or a replacement for the required source-repository URL.

Submission confirmed (2026-09-28): the participant reported completing the submission and supplied [Desktop Aquarium on Devpost](https://devpost.com/software/desktop-aquarium). Anonymous HTML retrieval returned HTTP 200, the title Desktop Aquarium, the “Submitted to” association with Build With AI: Basics, the public GitHub URL and the [YouTube demo](https://www.youtube.com/watch?v=KZNpCvBXBvw). YouTube's anonymous oEmbed endpoint returned the title “Desktop Aquarium — Build With AI: Basics Demo” and type `video`. This establishes the public links and contest association, not an organizer eligibility ruling or a fresh review of full hosted-video playback. The participant completed the form; no submission copy or personal survey answers were authored by the agent. Exact submitted commit/tag, hosted-video equivalence to local take-05 and private exit-survey completion are not independently established.

The dated preparation and verification notes below remain historical evidence. This update records submission status only; no runtime, asset, license, package or product scope change is made.

Implementation checkpoint (2026-09-27): G0–G4, the original G4 package learner check and the current source/Release Final Review are complete. After the updated app was launched, the participant accepted this implementation level and requested final documentation and GitHub synchronization. The accepted source includes the 32 approved fish frames, 100% Front display size and transparent falling/pickable feeder. See [fish verification](fish-runtime-verification.md), [feeder verification](feeder-object-verification.md) and the canonical [checklist](../devpost/checklist.md).

The current source displays Front at 100%, Middle at 86% and Rear at 72%, preserving simulation rules. Existing ZIPs predate the final size/feeder changes and are historical candidates. They are not the accepted current source and are not published release downloads.

Historical publication pass (2026-09-27): the participant selected the noncommercial/source-available licensing strategy, authorized the original public repository and authorized updating it. That pass changed technical documents and published already verified implementation; it did not add features, change licensing, publish a binary, upload a video, choose the final project name, create the contest tag or submit the Devpost form.

The local learning map was refreshed and linked with a brief evidence-based recap of the feeder transparency/input refinement. This records technical guidance tied to the owner's actual feedback and acceptance, not an invented personal reflection or new hands-on code tour.

Subsequent recording work: the owner requested a Windows Sandbox demo, then a shorter and clearer silent retake without product changes. The reviewed local candidate is take-05, 47.50 seconds at 1192×718 / 30 fps, using the unchanged Release payload and recording wallpaper. It shows a real desktop shortcut, pickup, two-second shake, food response/consumption, release, ordinary window interaction and feeder close. [Recording evidence](demo-recording.md) records all requested checks, rejected takes and review limits. Uploading and submission were outside that filming task; the participant's later submitted page and hosted link are recorded above.

## Submission checklist and archival follow-up

- [x] Current source/Release implementation accepted for the PoC; no further feature refinement requested.
- [x] Public repository exists with source, assets, instructions and separated licensing terms. This update carries the accepted feeder improvement and synchronized documents through the existing noreply history.
- [x] Technical final review and evidence recap recorded in `../devpost/checklist.md`; the HTML reference map remains local-only.
- [x] Local Windows Sandbox demo draft recorded and mechanically reviewed; [recording evidence](demo-recording.md) distinguishes it from the required public video.
- [x] Participant completed their submission; the public page uses Desktop Aquarium as its project name. The agent did not author or rewrite the submission answers.
- [x] Public project page contains the YouTube demo and GitHub repository links; anonymous project-page access and YouTube oEmbed metadata checked on 2026-09-28. Full hosted playback and exact equivalence to the local recording have not been independently verified.
- [x] Participant reported submission; the public page associates the entry with Build With AI: Basics under “Submitted to”. Private exit-survey completion is not independently visible.
- [ ] Archival follow-up: identify the exact submitted commit and create a fixed `v0.1-contest-submission` tag. No such commit is guessed or tag created by this status update.
- [ ] Optional binary distribution only: refresh the ZIP, include root licensing and matching third-party notices, verify the exact package in the intended environment and obtain package acceptance before publishing it.

The previously verified Rules' submission deadline is October 26, 2026 at 5:00 p.m. Eastern Time (October 27 at 06:00 Korea Standard Time). Submission and video links are now recorded above; no final contest tag is claimed.

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
| Screen recording | Reviewed local take-05: 47.50 seconds, 1192×718 / 30 fps, real shortcut/feeding/window interaction/close, same Release payload and wallpaper. Full decode, chronological whole-timeline frame review and dense feeding inspection passed; 12 emitted / 12 consumed / zero expired. The participant's public entry now embeds a YouTube demo; exact equivalence to this local recording is not independently established. See [recording evidence](demo-recording.md). Earlier takes/rehearsals remain historical. |
| Source/history audit | Pre-change scan: 20 commits, 156 tracked files, 278 historical blobs; no configured credential-pattern hits or private learner HTML/profile in history. Final publication scan is recorded below. Git history includes ordinary author metadata; scanning is not proof of absence of every secret. |
| App map | Local-only reference refreshed against the accepted source; feeder evidence recap recorded. No personal learning claim or new interactive code tour inferred. |

## Participant-owned submission items and repository access

Final project name: **Desktop Aquarium**, as shown on the participant's submitted public page.

Final description and required form answers: **completed by the participant as part of their reported submission**. No draft submission or narration was generated here; private form answers are not independently inspected.

Project license/publication choice: **selected by participant** — PolyForm Noncommercial 1.0.0 for project-owned code, separate assets and upstream terms. See `../LICENSING.md`; this is not OSI open source.

Public repository URL: [snowmuffin/contest-01-build-with-ai-basics](https://github.com/snowmuffin/contest-01-build-with-ai-basics) is **public and populated** on branch `master`. After reviewing the publication contents and contest requirements, the owner authorized posting on 2026-09-27 and stated that asset rights had been reviewed separately. This records the owner's decision, not an organizer ruling on eligibility or a new legal determination.

GitHub initially rejected the original history with GH007 email privacy protection. Publication now uses a separate copy with `77647785+snowmuffin@users.noreply.github.com` as the author/committer email. The first published source head is `39937d99369db2a317f44a9ac57bf4ed10d217c7`. All 22 original commits were compared: trees, names, dates, full messages and parent relationships are preserved, with email metadata and resulting commit IDs changed. The original local history and unfinished work remain intact, and email protection remains enabled. No force-push was used. Historical local commit identifiers elsewhere in these records refer to the original history and can differ from public identifiers.

At the initial publication checkpoint, anonymous access verification passed for repository visibility, all 22 public commit identities, and exact raw bytes of README, LICENSE, scope, PRD and spec. A following publication-status commit brought that public history to 23 commits. The accepted feeder source and this documentation update extend the same history without force-push; the private mapping and current access receipts remain in ignored `artifacts/publication-export/`. This is source publication only: no binary release, video upload, Devpost submission or final contest tag.

Demo video URL: [YouTube demo](https://www.youtube.com/watch?v=KZNpCvBXBvw), embedded in the public entry. Anonymous oEmbed metadata returned successfully on 2026-09-28; full hosted playback was not re-reviewed. The reviewed local candidate is `artifacts/sandbox-demo/run-02/results/take-05/aquarium-demo-take-05.mp4`; exact equivalence to the hosted version is not claimed. Take-01 and rejected retakes remain local.

Exit survey: **participant-owned; completion is not independently visible**. No answer or completion is inferred from the public project page.

Final package use/review: **only needed before a new binary release**. The original G4 package learner check and current source/Release acceptance are complete; neither certifies a future package.

Devpost Submit: **completed by the participant**, confirmed by their report and the public contest association. The agent did not submit or edit the entry.

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
