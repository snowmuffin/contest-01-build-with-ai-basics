# Pre-submission handoff — not a submitted entry

The participant requested preparation up to, but not including, submission; refinements follow that checkpoint. Do not expand aquarium scope or infer permission to publish repositories/videos, change visibility, choose the final project name/license, or submit the Devpost form.

## Requirement basis

- Installed official Devpost Learn `6-ship/SKILL.md` and the public curriculum README describe a working demo video, a public GitHub repository, participant-written project name/short description/required form answers, and participant-written exit survey. Deployment/peer feedback are optional there.
- The official Rules URL was requested again during this task. The web fetch was unavailable and the direct public request returned HTTP 403. Therefore exact current form fields, video constraints, deadline and any change to Rules were **not reverified** here. Do not replace them with guessed limits. Recheck the current Rules/form in the participant's browser before actual submission.
- Public curriculum: https://github.com/challengepost/learn-ai-basics
- Rules to recheck: https://learn-ai-basics.devpost.com/rules

## Technical preparation

| Item | State |
| --- | --- |
| Core desktop feeding loop and Windows coexistence | Implemented; earlier G2/G3 evidence is recorded in verification documents |
| Candidate runtime | 10.0.12 from live official metadata, release date 2026-09-08; host SDK/shared runtime unchanged |
| Upstream notices | Exact distribution/source-version notice texts and hashes collected under notices/dotnet-10.0.12 |
| Release candidate | `artifacts/packages/pre-submit-01/DesktopAquarium-win-x64.zip`; 489 hashes match; fresh 18 feeding / 25 lifecycle / 7 browser checks passed in RDP |
| Core tests | 64 passing after the candidate diagnostics change; Release build has zero reported warnings/errors |
| Clean/offline test kit | Prepared; absence of Windows Sandbox on this host means not executed |
| Screen recording | A 7.95-second cropped local rehearsal recorded; sampled-frame review done, final owner review/recording and upload still pending |
| Source/history audit | 109 history blobs scanned with zero configured credential-pattern hits; owner metadata review still required |
| App map | Local-only technical reference, not a claim of completed final review or learning activity |

## Owner items intentionally left blank

Final project name: **participant to provide**. “Desktop Aquarium” remains a working label.

Final description and required form answers: **participant to write**. No draft submission or narration is generated here.

Project license/publication choice: **participant decision pending**. Dependency notices do not license the new application.

Public repository URL: **not published**. Public visibility and push require explicit authorization.

Demo video URL: **not uploaded**. Confirm the actual final recording and public access without exposing private desktop contents.

Exit survey: **participant to complete**.

Final package use/review: **pending**. Do not reuse acceptance of earlier feeding tests as acceptance of the release package.

Devpost Submit: **DO NOT EXECUTE** in this preparation pass.

## Internal quality gates, not extra contest rules

Separate SDK-free/offline execution, local-console display validation, sustained resource checks, and a clean extracted-package run are this project's verification plan. They were not established as organizer-mandated submission fields. Keep missing evidence explicit; obtaining a ZIP does not complete these checks.

## Refinements after readiness review

The first follow-up should address actual observed issues, not add species/rarity/growth, other operating systems, or multi-monitor scope. Optional polishing candidates are feeder visual weight, fish turning/eating animation, and measured rendering cost. None is implemented or committed as a new requirement by this document.

## Latest RDP recheck

Input access is restored. Fresh candidate verification and a real local rehearsal are recorded in `rdp-candidate-verification.md`. No console transfer, owner licensing/naming decision, public posting or final submission occurred. The longer benchmark was partial; do not report all three 60-second phases as passed.
