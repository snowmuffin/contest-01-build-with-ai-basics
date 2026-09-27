# Pre-submission handoff — not a submitted entry

Current state (2026-09-27): G0–G4, the original G4 package learner check and final exploratory feedback are complete. The participant approved the 32 independently extracted fish frames, which are now packed with exact metadata and integrated into source and a fresh package candidate. Final running-package acceptance remains open. See `fish-runtime-verification.md` and the canonical `../devpost/checklist.md`. Earlier dated checkpoint notes below remain historical evidence.

Subsequent requested size adjustment: current source/Release displays Front at 100% native size, Middle at 86% and Rear at 72%, preserving simulation rules. The existing artwork ZIP predates this change; package refresh and participant visual retry are pending.

The participant subsequently selected the noncommercial/source-available licensing strategy and requested public GitHub repository preparation. This supersedes the earlier hold on source licensing/publication only. Do not expand aquarium scope, upload a video, choose the final project name, mark Final Review complete, or submit the Devpost form.

Current feeder refinement: source now removes the visible panel and lets the unheld canister fall to the primary work-area floor, with pickup during falling or at rest. The previous public source and archived ZIPs predate this work; source mechanical checks and participant acceptance are recorded separately in `feeder-object-verification.md`. No final submission readiness is implied.

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
| Release candidate | `artifacts/fish-runtime/package-01/DesktopAquarium-win-x64.zip`; 489 inventory entries verified at the integration checkpoint. This archive predates 100% display size; refresh pending. Source and historical package evidence are distinguished in `fish-runtime-verification.md`. |
| Core tests | 73 passing after the feeder-object refinement, including seven new falling/re-pickup cases; Release build has zero warnings/errors. |
| Feeder object refinement | Panel removed, unheld falling and floor/in-flight pickup implemented; 23 native feeding/transparency checks and 27 lifecycle checks passed. Participant appearance/fall-speed review remains pending; see `feeder-object-verification.md`. |
| Clean/offline verification | G4 package-02 passed offline-native-05, followed by its learner check. This evidence does not certify future artwork/package changes. |
| Fish artwork | All 32 extracted PNGs approved by participant; exact RGBA atlas round trips and 73 current WPF checks pass, including native-size visible-pixel equality, clipping and edge culling. No Core/behavior changes. Participant retry of the new size is pending. |
| Screen recording | A 7.95-second cropped local rehearsal recorded; sampled-frame review done, final owner review/recording and upload still pending |
| Source/history audit | Pre-change scan: 20 commits, 156 tracked files, 278 historical blobs; no configured credential-pattern hits or private learner HTML/profile in history. Final publication scan is recorded below. Git history includes ordinary author metadata; scanning is not proof of absence of every secret. |
| App map | Local-only technical reference, not a claim of completed final review or learning activity |

## Owner items intentionally left blank

Final project name: **participant to provide**. “Desktop Aquarium” remains a working label.

Final description and required form answers: **participant to write**. No draft submission or narration is generated here.

Project license/publication choice: **selected by participant** — PolyForm Noncommercial 1.0.0 for project-owned code, separate assets and upstream terms. See `../LICENSING.md`; this is not OSI open source.

Public repository URL: [snowmuffin/contest-01-build-with-ai-basics](https://github.com/snowmuffin/contest-01-build-with-ai-basics) is **public and populated** on branch `master`. After reviewing the publication contents and contest requirements, the owner authorized posting on 2026-09-27 and stated that asset rights had been reviewed separately. This records the owner's decision, not an organizer ruling on eligibility or a new legal determination.

GitHub initially rejected the original history with GH007 email privacy protection. Publication now uses a separate copy with `77647785+snowmuffin@users.noreply.github.com` as the author/committer email. The first published source head is `39937d99369db2a317f44a9ac57bf4ed10d217c7`. All 22 original commits were compared: trees, names, dates, full messages and parent relationships are preserved, with email metadata and resulting commit IDs changed. The original local history and unfinished work remain intact, and email protection remains enabled. No force-push was used. Historical local commit identifiers elsewhere in these records refer to the original history and can differ from public identifiers.

Anonymous access verification passed for repository visibility, all 22 public commit identities, and exact raw bytes of README, LICENSE, scope, PRD and spec. This is source publication only: no binary release, video upload, Devpost submission or final contest tag was created. This publication-status update follows that verified source push.

Demo video URL: **not uploaded**. Confirm the actual final recording and public access without exposing private desktop contents.

Exit survey: **participant to complete**.

Final package use/review: **pending for the final artwork/release**. The original G4 package learner check is complete; it does not accept the new extracted frames or a future package.

Devpost Submit: **DO NOT EXECUTE** in this preparation pass.

## Final submission and later commercial work

Publication document checks on 2026-09-27: official PolyForm text matches its pinned source SHA-256; 30 relative links/anchors resolve; all existing application/script/test/asset-pixel and upstream-notice hashes are unchanged; the 20-package development inventory matches the lockfile. The staged publication contains 165 tracked files, no application code changes, no configured credential-pattern hits and no local profile/HTML/agent/artifact files. The legacy uncommitted atlas and untracked cleaner remain local. Evidence: ignored `artifacts/licensing/{audit-before.json,document-validation.json,index-audit.json}`. These checks do not establish legal title or guarantee detection of every secret.

Historical before-push audit at original local commit `3478c5b`: 21 commits, 165 tracked files and 298 historical blobs; no configured credential-pattern or private-document findings. A subsequent pre-publication review at original local commit `8d3989b` covered 22 commits, 165 tracked files and 300 historical blobs, finding no additional configured credential/private-path matches. Private commit email metadata was addressed in the owner-approved public copy described above. The existing audit script's publication/owner-pending fields are static checklist hints, not live GitHub status.

Local publication evidence is excluded from Git under `artifacts/publication-review/` and `artifacts/publication-export/`, including the redacted audit, original-history backup, commit mapping and anonymous-access receipt. Only committed source was exported: the dirty legacy atlas version and untracked cleaner were not added. The already committed legacy atlas remains historical project material and is not used by the current application. Optional file cleanup was not part of this publication pass.

When the owner approves the actual submitted version, record its exact commit, create a fixed tag such as `v0.1-contest-submission`, and preserve it through judging. No tag is created in this pass. Later Steam work may continue on another branch or in a private commercial repository. The owner can separately license only rights the owner holds; existing license grants and upstream obligations remain. Contribution/relicensing policy remains an internal owner consideration, not a CLA system added for this contest.

The current source publication does not publish a binary ZIP. `../THIRD_PARTY_NOTICES.md` records the remaining package notice-copy/inventory work. This documentation-only task does not rerun builds or native input tests; application source/assets are checked for unchanged bytes instead.

## Internal quality gates, not extra contest rules

Separate SDK-free/offline execution, local-console display validation, sustained resource checks, and a clean extracted-package run are this project's verification plan. They were not established as organizer-mandated submission fields. Keep missing evidence explicit; obtaining a ZIP does not complete these checks.

## Refinements after readiness review

The approved Final Review includes solid feeder presentation, four stable fish silhouettes, directional poses and restrained depth perspective; see the canonical PRD/checklist. The approved artwork is now integrated with proportional regression checks; no rarity/growth, other operating systems or multi-monitor scope was added. Participant frame approval is recorded explicitly; final running-package acceptance must still be supplied by the participant.

## Latest RDP recheck

Input access is restored. Fresh candidate verification and a real local rehearsal are recorded in `rdp-candidate-verification.md`. No console transfer, owner licensing/naming decision, public posting or final submission occurred. The longer benchmark was partial; do not report all three 60-second phases as passed.

## G4-only update

The latest G4 pass completed ordinary, feeding and hidden measurements for 60 seconds each and normal exit (eight assertions). This supersedes the earlier partial-long benchmark as current evidence; it is not a long-duration certification. GPU counters returned no PID instances and cannot be reported as zero. See `g4-verification.md`. G4 remains open only for the real separate SDK-free/offline environment test among the unfinished mechanical tasks; final user review is a subsequent owner checkpoint. No later submission work was performed.

## G4 clean-room update

The separate Windows Sandbox run is complete. offline-native-05 passed with no global dotnet/SDK, no guest runtime networking, 489 verified payload hashes, package-local .NET 10.0.12 loading, 18 feeding checks, 25 lifecycle checks, clean process/capture teardown and unchanged payload hashes. Final source locked restore, Release build and 64 core tests passed again. Actual-package learner feedback, Final Review, learning wrap-up, public links and submission remain pending.
