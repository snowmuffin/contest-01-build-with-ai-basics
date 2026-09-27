---
doc: prd
status: approved
---

# Desktop Aquarium — Product Requirements

A local desktop habitat for someone who works at a computer for long periods and wants small, optional moments of life and interaction on a familiar screen.

Source: `scope.md > Who It's For`, `The Unique Kernel`, `The Core Loop`, and the learner's subsequent PRD interview answers. The learner approved this PRD, including the five remaining product defaults presented for review. This is an approved product plan, not final submission copy or evidence of working software. The participant subsequently submitted it as Desktop Aquarium.

Portable distribution (2026-09-28): optional delivery improvement authorized by the owner. A user extracts the whole Windows x64 ZIP, optionally onto their Desktop, runs `Start-Aquarium.cmd`, and can create a Desktop **Feed Fish** icon with `Setup-FeederShortcut.cmd`. The runtime is bundled; no admin installation, startup registration or security-policy change is added. The complete extracted folder must remain together. This is delivery of the accepted interaction, not a new aquarium feature; see `../docs/release-v0.1.0.md`.

## Platform and Documentation Decisions

The learner selected Windows for the first prototype. macOS/Linux remain possible future targets, not first-delivery requirements. The subsequently approved spec selects C#/.NET 10 with WPF/Win32 and a Windows 11 x64 primary-display target. Actual tested coverage and remaining environment limitations are recorded in `spec.md` and the verification documents; platform selection is not a broad compatibility claim.

Current acceptance (2026-09-27): after the updated app was launched, the owner accepted the present implementation and chose to proceed to submission preparation. This closes the source/Release visual and feeding-interaction review, including native-size fish and the falling feeder. It does not claim a new extracted-ZIP review, exhaustive visual alignment measurements or a submitted Devpost entry.

Keep canonical Markdown documents in the repository. HTML review companions and other generated HTML learning documents under `devpost/` are local-only and Git-ignored. Continue visual reviews locally; this policy does not exclude HTML used as actual application source elsewhere.

## The Core Journey

Source: `scope.md > The Core Loop` and `What "Working" Looks Like`.

1. Start the aquarium. Fish swim across the user's real desktop/display; there is no separate tank container or replacement underwater background.
2. Continue ordinary work. Fish usually inhabit the middle/rear space and occasionally show interest in the cursor.
3. Double-click the aquarium's desktop feeder launcher. A small unheld feeder appears near the cursor inside the visible screen and falls toward the work-area floor. Opening it does not automatically mean holding it; an already open feeder is reused rather than duplicated.
4. Press and drag the feeder body to pick it up. The cursor/feeder appearance communicates that it is held.
5. Shake while holding it. Food is released, responding to the user's movement. Fish approach the foreground food and visibly eat it.
6. Release the mouse button. The feeder falls vertically to the bottom of the primary work area above the taskbar, the cursor returns to ordinary use, and new food emission stops. Previously released food remains available to fish.
7. Pick up the feeder again from the floor or catch it while falling, or click its small X to close only the feeder. Fish continue their autonomous behavior.

Steps 3–4 refine the approved scope's earlier shorthand: opening the tool and holding it are now distinct, as explicitly accepted in the PRD interview. The feeding-only prototype boundary has not changed.

## Screens and Layout

Source: `scope.md > Inspiration & Identity` and `The POC Boundary`.

- **Desktop habitat:** the existing display is the aquarium. Existing desktop items and application windows remain the user's work environment.
- **Desktop feeder launcher:** an app-owned icon/launcher, not a request to read, consume, or alter arbitrary desktop files.
- **Feeder object:** the existing opaque canister sprite with no surrounding panel, border or permanent instruction text, plus a small separate X. Transparent areas let input reach the underlying application; grabbing the body moves the object and releasing drops it. Only its own controls respond to direct manipulation; fish do not block normal clicks.
- **Aquarium control menu:** a small menu attached to a resident/status icon offers Hide, Show again, and Exit for the aquarium as a whole. The concrete OS-specific placement belongs in spec.
- A dashboard, collection screen, or settings suite is not part of the agreed prototype.

## Look and Feel

- **Confirmed:** no drawn tank, glass enclosure, tank border, or underwater background is required. The screen itself is the habitat.
- **Confirmed:** fish can appear in front of, between, and behind ordinary application windows using the bounded three-band behavior below.
- **Accepted:** use pixel-art fish for the first prototype. Exact sprite size, frame count, species count, and rendering technique will be tuned later. Pixel art is a visual choice, not proof of low resource use.
- **Final-review refinement:** keep five fish but use at least four visibly different silhouettes/species. Species identity is stable per fish; this is visual diversity, not a collection/rarity system.
- **Asset review completed (2026-09-27):** the participant inspected and approved 32 independently extracted PNGs (four visual families, four directions, two frames each) for atlas/metadata construction and integration. Source comparisons and masks remain inspectable. Following the participant's request for 100% display size, Front now shows the frames at their native dimensions, preserving aspect ratio instead of fitting them into the smaller logical fish bounds. Movement, feeding, depth and occlusion rules remain unchanged; final running-package acceptance remains separate.
- **Final-review refinement:** fish may visually face left, right, toward the viewer, or away from the viewer. Toward/away poses communicate movement between the existing Rear/Middle/Front depth bands and occasional curiosity; this does not introduce free 3D navigation.
- **Final-review refinement:** make depth readable with restrained perspective scaling. Front displays at 100% of the approved source frame, Middle at 86%, and Rear at 72%, while retaining the same logical collision/occlusion rules. These are logical display sizes; Windows display scaling still applies.
- **Final-review refinement:** the feeder must read as a solid app-owned pixel object. Its body must not visually reveal the work window behind it; pixels outside its silhouette are transparent. The owner subsequently requested removal of the visible rectangular panel and gravity after release; the current refinement implements that behavior.

- Fish should feel autonomous rather than constantly following the pointer. The main interaction should be understandable without developer knowledge.
- The HTML companion illustrates approved requirements and states; its decorative graphics are not final aquarium artwork or an application demo.

## Features and Behavior

### Desktop presence and cursor curiosity — MVP value

Source: `scope.md > The Unique Kernel` and `The POC Boundary`.

Fish swim autonomously and sometimes notice the ordinary cursor. Ordinary pointer motion alone never dispenses food. The habitat coexists with work and does not rearrange application windows or steal focus merely to make fish visible.

Observable criteria:
- Fish move without the user feeding them; curiosity is intermittent, not continuous pursuit.
- Normal clicks reach the user's work except when deliberately interacting with the feeder itself.

### Window depth — accepted direction, MVP value

Source: `scope.md > Inspiration & Identity`; approved PRD interview refinement.

Use three logical visual bands for the first prototype:
- Front: ahead of ordinary work windows.
- Middle: behind the frontmost ordinary work window but ahead of the remaining ordinary work windows.
- Rear: behind ordinary work windows, visible where not covered.

Windows occlude fish; they are not physical obstacles in this prototype. Use a consistent front-to-back relationship at any instant. Keep a fish's band stable during ordinary swimming and avoid having the entire fish suddenly pop through a window's center when it changes depth. Prefer transitions near uncovered edges. Changes to the user's window ordering take precedence over preserving visibility of a fish.

Feeder and food inhabit the front interaction band. Responding fish join that space before eating foreground food; hidden rear fish must not consume it invisibly. Not every fish must respond, and feeding must not teleport all fish to the front. After feeding, fish return to autonomous behavior.

When an ordinary maximized window leaves no exposed rear-space route, a reacting existing fish may re-enter the front band from a screen edge before approaching the food. This is a visual depth transition, not a new visiting-fish or spawning feature. It must not pop through the center or consume food while invisible. Fullscreen suppression takes precedence over this exception.

Observable criterion: with two overlapping ordinary windows, a middle fish is hidden where the foremost window covers it while remaining visible over the rear window. This is a product target to validate on Windows, not a verified implementation or a cross-platform capability claim.

### Feeder handling — accepted, MVP value

Source: `scope.md > The Core Loop`; approved PRD interview refinement.

| State | Visible behavior | Transition |
| --- | --- | --- |
| Closed | Fish remain; feeder is absent | Launch feeder to make it available |
| Unheld (core mode: Resting) | Feeder falls vertically, then rests at the work-area floor; ordinary pointer; no new food | Pick up either during a fall or at rest; click X to close |
| Held | Feeder follows the captured pointer with the holding cursor; gravity stops | Shake to dispense; release button to drop |

Observable criteria:
- Only shaking while the feeder is held produces new food.
- Releasing stops new food but does not delete food already released.
- A resting or falling feeder can be picked up again. Falling alone never feeds fish, captures input, or steals focus.
- The floor is the primary display work-area bottom, so the feeder does not cover the taskbar. No bounce, throw momentum or collision with application windows is introduced.
- Hidden/fullscreen time does not advance falling; restoration is unheld and resumes falling only while visible.
- Clicking X does not also start dragging or emit food.
- Closing the feeder does not stop the aquarium or modify desktop files.

Additional shortcut keys are optional improvements, not a second mandatory control mode.

### Aquarium controls and feeder activation — accepted, MVP value

Source: `scope.md > The Core Loop` and the five product defaults accepted after PRD review.

A small resident/status-icon menu offers Hide, Show again, and Exit. There is no additional dashboard. The aquarium-wide controls are distinct from closing the feeder with X.

When opened for the first time, the feeder appears near the cursor, within the screen, and is not held; it falls to the work-area floor. If already open, activating its launcher reuses it rather than creating another feeder. These actions do not count as shaking or picking it up.

Observable criteria:
- The aquarium can be hidden and shown again, or exited, without using the feeder X as the aquarium exit.
- Repeated launcher activation does not produce multiple feeders.
- A newly visible or restored feeder does not dispense food until deliberately picked up and shaken.

### Fullscreen work takes priority — accepted, MVP value

Source: `scope.md > Who It's For` and the learner's response that the fullscreen task/program should have priority.

**Learner direction:** do not let the aquarium interfere with an application the user deliberately runs fullscreen. The interview distinguished fullscreen video/game/presentation use from merely maximizing an ordinary work window.

**Accepted product behavior:**
- In fullscreen, hide fish, food, and the feeder over the protected fullscreen view. Do not bring them forward to attract attention.
- Stop new food emission and cancel any held-feeder interaction. Leave the user with ordinary pointer/input behavior.
- Do not steal focus, change the other application's window order, or take its ordinary mouse/keyboard input.
- When fullscreen ends, allow the habitat to return automatically. A previously open feeder returns resting, never automatically held; fresh deliberate interaction is required to feed again.
- Merely maximizing an ordinary work window continues to use the agreed depth behavior; it is not automatically treated as fullscreen suppression.

Observable check: switch to fullscreen while holding the feeder. No aquarium object should cover the fullscreen view and no food should continue to be emitted. On returning, moving the ordinary cursor must not restart feeding.

Automatic detection, system UI handling, and how this behaves on each supported display/OS require technical validation. This approved plan does not promise universal detection. Whether hidden simulation is paused or throttled is a performance investigation for spec/build, not a confirmed user-facing rule.

## States and Boundaries

- **Ordinary work:** autonomous fish, occasional curiosity, and existing window ordering are preserved.
- **Feeding:** open/hold/shake/release/close follows the accepted interaction, without a cloud service or account.
- **Fullscreen:** hide the aquarium over the protected view, stop emission, and cancel holding. On return, an open feeder is resting and needs a fresh pickup.
- **No exposed path from rear space:** when a maximized ordinary window hides rear fish, reacting existing fish may re-enter the front band from a screen edge. Do not spawn new fish for this effect, pop through the center, teleport all fish forward, or allow invisible consumption of front-band food.
- **Interrupted holding:** stop new food emission, cancel holding, and require a fresh deliberate pickup. Exact OS interruption detection belongs in spec.
- **First/repeated feeder launch:** first appearance is near the cursor and inside the visible screen, resting. Reuse an open feeder without creating duplicates or stealing unrelated focus; ordinary cursor movement must not start feeding.
- **Aquarium hide/show/exit:** use the small resident-icon menu. Hide temporarily removes the habitat from view, Show again restores it, and Exit stops the aquarium. This is separate from the feeder X, which closes only the feeder. Restoring visibility is not a fresh pickup gesture.
- Persistent fish collection, growth, or absence penalties are not part of this milestone. Do not invent them to fill a persistence section.

## Product Decisions

| Decision | Status and reason |
| --- | --- |
| First prototype finishes at feeding | Accepted; discovery, settling, and rare fish remain later directions |
| Display itself is the habitat | Accepted; not a conventional aquarium window |
| Front/middle/rear bands | Accepted simplification; arbitrary gaps between every window are deferred |
| Open, hold, shake, drop, X-to-close | Owner-requested refinement: release falls to the work-area floor; dropping and closing remain distinct |
| Fullscreen task gets priority | Accepted hide/cancel/restore behavior; restore an open feeder resting, not held |
| Pixel-art fish | Accepted first-prototype appearance; resource use still requires measurement |
| Aquarium hide/show/exit | Accepted small resident-icon menu; no dashboard |
| Feeder first/repeated launch | Accepted cursor-near resting appearance and reuse without duplicates |
| Maximized-window feeding | Accepted edge re-entry for existing fish, preserving visible approach and consumption |
| Interrupted holding | Accepted stop-emission/cancel-hold fail-safe with fresh pickup required |
| No external runtime services | Accepted constraint; standard local libraries are not excluded |
| First-prototype OS | Windows selected; macOS/Linux are potential later work, with no first-delivery support promise |
| Documentation distribution | Canonical Markdown in Git; generated `devpost/*.html` documents are local-only and excluded from commits |

## What We're Building

Source: `scope.md > The POC Boundary`.

One local, repeatable feeding experience: a display habitat, autonomous fish with intermittent curiosity, bounded visual depth, the feeder launcher/object, deliberate shake-to-feed, visible approach/consumption, and a clean return to ordinary work. Fullscreen coexistence is part of making that experience non-disruptive, not an additional game mode.

The public repository, official planning documents, demo, and other contest submission materials are separate submission work, not extra aquarium features.

For the owner-authorized public repository, original project code uses PolyForm Noncommercial 1.0.0 within `../LICENSING.md`'s scope; project assets and third-party components have separate terms. Public access is not an OSI-open-source claim. The contest's open-source recommendation is not fulfilled by this noncommercial choice. The owner may separately license owner-controlled material for a later commercial edition; Steam functionality is not part of this PRD. App behavior and acceptance criteria are unchanged by this documentation task.

## Deferred From the POC

Visiting fish, visitor-to-resident interaction, rarity, growth, a large species collection, window collision/avoidance, elaborate water effects, day/night systems, and advanced multi-monitor-specific behavior remain later work. None is required to demonstrate the selected feeding milestone.

## Possible Later Enhancements

Additional discovery and keeping interactions can make the habitat more personal. Keyboard conveniences and richer visual depth can be considered after the core interaction works; they are not current acceptance criteria.

## Non-Goals

Source: `scope.md > Explicitly Cut`.

Do not eat/delete/move the user's desktop files, use external AI/cloud APIs for the core loop, take over the user's window ordering, promise productivity or health improvements, or present untested platform support/performance as completed work. Do not require a full ecosystem-management game for prototype completion.

## Open Questions

No product-decision blocker remains from the five reviewed defaults. The learner accepted them without changes; do not ask for another PRD sign-off.

Windows is the selected first-prototype OS. The stack and primary-display target are approved in `spec.md`; implementation and test evidence now exist. Other DPI configurations, local-console coverage, games and broader platform compatibility remain unverified as described there. If a supported case cannot deliver an approved behavior, explain the tradeoff rather than silently weakening the product.

Five fish, bounded feeding and the three depth bands are implemented and accepted for this PoC. Further tuning is outside the current submission-preparation task. The final project name and submission wording remain learner-authored.
