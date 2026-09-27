---
doc: scope
status: approved
---

# Desktop Aquarium — working label

A local desktop experience in which the display itself becomes a living aquarium, and a desktop feeder icon lets the user shake the mouse to feed its fish.

The learner approved this scope after review and chose an additional visual HTML planning companion. Feeding interaction is the first-prototype boundary. The final project name remains undecided. This document defines approved scope, not implementation completion. Its interaction wording is synchronized with the approved PRD; the feeding-only prototype boundary is unchanged.

Current bounded refinement (2026-09-27): the participant approved the 32 independently extracted fish-art frames, which are now integrated through a variable-rectangle runtime atlas and metadata. This is optional visual polish within the accepted Final Review, with no new product capability or scope expansion. The existing movement, feeding, depth and occlusion logic remains unchanged. Artwork approval is not final package acceptance. Evidence: `../docs/fish-sprite-verification.md` and `../docs/fish-runtime-verification.md`.

The participant subsequently requested 100% display size. Front now displays the approved frames at one source pixel per logical display unit, with the existing Middle 86% and Rear 72% perspective retained. This is a renderer-only size adjustment within the same optional refinement; simulation geometry and product scope are unchanged.

Publication preparation (2026-09-27): the owner requested a public contest repository with original project code under PolyForm Noncommercial 1.0.0, separate project-asset terms, and unchanged third-party terms. See `../LICENSING.md`, `../ASSET_NOTICE.md` and `../THIRD_PARTY_NOTICES.md`. This is submission preparation, not a product feature or scope expansion. The repository is source-available/noncommercial, not OSI open source. A future proprietary Steam edition remains outside this PoC; only the owner's applicable rights can be separately licensed. No contest-submission tag is created before the final submitted commit is selected.

## The Unique Kernel

The aquarium is the user's desktop, not a tank confined to a conventional app window. Opening a real feeder icon makes a virtual food shaker available. The user picks it up by pressing/dragging it: holding is visually apparent, shaking releases food, and the fish approach and eat it. Opening, holding, putting down, and closing are distinct actions.

Occasional curiosity toward the ordinary cursor supports the feeling that the fish inhabit the same space as the user, rather than playing a repeating wallpaper animation.

## Who It's For

Someone who spends long hours working at a computer and wants a small change of mood in an otherwise static, stark, or overly familiar screen. They want something living and interactive alongside their work. The value is a livelier familiar workspace, not a promised improvement in productivity or health.

## The Core Loop

1. Start the aquarium and see fish swimming autonomously across the desktop/display.
2. During ordinary use, fish sometimes show interest in the cursor without constantly following it.
3. Double-click the aquarium's desktop feeder icon to make the resting feeder available.
4. Press/drag the feeder to hold it, then shake the mouse while holding to release food particles.
5. Watch fish notice the food, approach it, and eat it.
6. Release the mouse button to put the feeder down and resume ordinary cursor use, or click its X to close only the feeder. The aquarium continues; a separate small resident-icon menu can hide, show, or exit the aquarium.

The repeatable experience is a brief, optional interaction with something living on an otherwise familiar work screen.

## Inspiration & Identity

The learner's direction is an interactive desktop habitat, with the entire display treated as an ecosystem. It should feel alive even when the user is not deliberately feeding it, and its main interaction should be understandable to a non-developer just by watching it.

The approved PRD chooses pixel-art fish and a bounded front/middle/rear relationship to ordinary work windows, with fullscreen work taking priority. There is no separate drawn tank or replacement underwater background. Detailed artwork and technical rendering remain for implementation planning. No third-party character or artwork has been selected for reuse.

## Why This Matters to the Learner

The learner wants to make a small, visually memorable software submission while learning desktop overlays and operating-system integration. They are shaping the idea incrementally. The first prototype now targets Windows; other desktop operating systems remain a possible later expansion, not a requirement for the first delivery.

## What "Working" Looks Like

On a real desktop, the user launches the aquarium, opens its feeder icon, picks up the feeder, sees the holding appearance, and shakes the mouse while holding it. Food appears and the fish visibly move toward it and consume it. The user can leave feeding mode and continue normal desktop work.

The defining demonstration is the complete transition from an ordinary desktop icon to a virtual shaker and then to a visible response from the fish. A canned animation alone is not sufficient: feeding must respond to the user's actual movement.

The same feeding interaction can be repeated locally without an external service, account, or API. Completing this loop is the first prototype's finish line; new-fish discovery, settling, and rarity are not required for this milestone.

## The POC Boundary

### MVP value

- A habitat spanning the desktop/display rather than an aquarium confined to a conventional app window.
- Autonomous fish movement with occasional interest in the normal cursor.
- An app-owned desktop feeder icon/launcher, a resting feeder, and visible feedback when it is held.
- Shake-to-feed input, food particles, and fish approaching and eating the food.
- Putting down or closing the feeder restores ordinary interaction; a small resident-icon menu handles aquarium hide/show/exit. Fullscreen work takes priority.
- Non-destructive interaction: fish do not consume desktop files or arbitrary icons, and feeding does not delete, move, or alter the user's files.

### Constraints and decisions carried forward

- Core functionality has zero external runtime-service dependency. Standard development libraries are not excluded by this condition.
- Build a new project for this hackathon rather than use an existing project as the submission's codebase.
- First-prototype target: Windows, as selected by the learner during technical planning. macOS and Linux are deferred potential targets. Exact Windows versions, architectures, display configurations, permissions, and working support must be established in spec/build; selecting a target is not a claim of tested compatibility.
- The approved PRD defines pixel-art presentation, feeder controls, window-layer behavior, and fullscreen recovery. Exact sprite sizes, fish count, shake thresholds, OS integration, and rendering mechanics remain spec/build decisions.
- The official planning documents, public repository, working-project demonstration, and submission materials remain contest deliverables, not aquarium features.
- Canonical planning Markdown belongs in the repository. Generated visual review/learning documents under `devpost/*.html` remain local and Git-ignored. Continue HTML reviews without committing the generated HTML; this does not exclude HTML that is actual application source elsewhere.

## Later

These are retained directions, not commitments for the first prototype:

- Randomly visiting fish and an interaction that lets a visitor become a resident.
- Continuing to raise resident fish, rare visitors, and a broader variety of species. These are deferred because the learner chose feeding as the first finish line, not because the longer-term product must remain passive.
- Application windows as obstacles or terrain, additional cursor interactions, and individual fish personalities.
- Growth/hunger systems, plants, day/night cycles, more elaborate water effects, and multi-monitor-specific behavior. None is needed to prove the initial feeding loop.

## Explicitly Cut

- Treating the user's existing files or desktop icons as edible objects: the learner clarified that the icon is a feeder launcher, not the food.
- External AI APIs, cloud accounts, and hosted backend services for the core interaction: they conflict with the zero-external-runtime-dependency constraint.
- Requiring a full collection, rarity, or ecosystem-management system to call the first prototype complete: that would exceed the feeding milestone the learner selected.
- Reusing an existing application or third-party character as the finished entry: the submission is a new project and no such reuse has been chosen.
