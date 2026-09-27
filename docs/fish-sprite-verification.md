# Independent fish-frame extraction — 2026-09-27

Status update: **The participant inspected and approved all 32 PNGs and instructed runtime integration.** `../assets/fish/approval.json` pins the approved frame set. See `fish-runtime-verification.md` for integration evidence. The extraction-time results below are preserved as history; their pending-review wording describes that earlier checkpoint.
Classification: optional visual polish within accepted Final Review. The feeding PoC scope is unchanged.

## Source and preserved work

The participant supplied `ChatGPT Image Sep 27, 2026, 04_41_16 PM.png` for this task. Its unchanged repository copy is `assets/fish/source/preview-sheet.png`, 1448x1086 RGBA8, SHA-256 `0d41ac55d8e23f51816d15ef151b08f9e07e23b5b9a8fb6f0d19ad3c1df619e5`. Source/usage details are in `assets/fish/source/provenance.json`. The preview contains a background, headings, dividing rules and frame numbers. Every original alpha value is 255; it is not a transparent sprite atlas.

At task entry `src/Aquarium.Windows/Assets/fish-atlas.png` already had uncommitted changes (SHA-256 `fb9a2770a556bede61427137d543e1540cf9692a15d5a62f52c9c8f2755e415b`) and `scripts/Clean-FishAtlas.py` was untracked. Both were preserved. The existing cleaner works inside 80x48 cells of an already processed atlas. The new extractor reads only the original preview and explicit annotations; it never runs the cleaner or changes the runtime atlas.

## Deliverables and method

- `assets/fish/extraction-regions.json`: 32 separate source ownership rectangles with exclusive right/bottom coordinates. They are manually selected for actual silhouettes and exclude labels, rules and adjacent fish; they are not derived by dividing the sheet into equal cells.
- `scripts/Extract-FishFrames.py`: local deterministic extraction/review helper, using the already installed development-only Pillow 11.0.0. No runtime dependencies, model calls or network calls were added.
- `assets/fish/extracted-v1/frames/`: 32 independent RGBA PNGs at native source resolution, trimmed individually and padded with four transparent pixels on each side.
- `assets/fish/extracted-v1/masks/`: 32 grayscale masks in their respective source-region dimensions, so every retained/deleted source pixel can be inspected.
- `assets/fish/extracted-v1/extraction-receipt.json`: IDs, original coordinates, sizes and source/output/mask hashes. This is extraction audit data, not runtime atlas metadata or UV/pivot data.
- `assets/fish/extracted-v1/verification.json`: machine-check result; human review stays pending.
- `devpost/fish-sprite-review.html`: local-only review page, ignored by Git. It contains numbered original/PNG/mask comparisons, 3x nearest-neighbour display and checker/light/dark backgrounds. This is an asset review, not an HTML build checklist.
- `artifacts/fish-sprite-review-v1/`: labelled light/dark contact sheets, source annotation map and headless-browser evidence. These review documents are ignored and never used as an application atlas.

Frame order is Goldfish, Tetra, Angelfish, Guppy; within each species: Left 01/02, Right 01/02, Front 01/02, Back 01/02. Front/Back correspond to the existing TowardViewer/AwayFromViewer presentation; this does not change fish behavior.

Mask recipe: retain pixels whose maximum RGB channel is above 30, then fill enclosed dark background components of at most 64 pixels using four-neighbour connectivity. This protects dark eye/body detail while preserving larger gaps. Detached foreground fragments are all retained; there is no largest-component deletion, morphological erosion, uniform cell crop or resizing. Masks and source comparisons expose the heuristic to review.

## Executed verification

`python scripts/Extract-FishFrames.py` produced the first review candidate. `python scripts/Extract-FishFrames.py --verify` checks the saved outputs without writing files.

| Check | Result |
| --- | --- |
| Original SHA-256 and dimensions | Match the pinned source |
| Complete identity matrix | 4 species x 4 directions x 2 frames = 32 |
| Output completeness | 32 independent PNGs, 32 masks; no missing/extra files |
| Duplicate PNG hashes | None; 32 distinct hashes |
| Source ownership rectangles | In bounds and mutually non-overlapping |
| Selected silhouette touches source-region edge | None; at least two clear pixels to each region edge |
| Output alpha and padding | True RGBA, binary alpha 0/255, four clear pixels on each side |
| Source RGB preservation | 225,983 selected pixels, zero RGB changes; cropped patch RGB compared directly |
| Mask and PNG reproduction | All masks recomputed and output PNG bytes reproduced in memory |
| Review page in isolated headless Edge | 32 cards, 32 source regions, 97 images loaded, zero broken images or page errors |
| Review controls | Checker/light/dark selection and 3x expansion passed |
| Visual inspection | Light/dark contact sheets inspected; long angelfish fins and all 32 silhouettes visible |
| Runtime source/asset changes by this pass | None; pre-existing dirty atlas preserved |

The existing Core/native app suites were not rerun: there was no application code, runtime asset, packaging or dependency change in this extraction pass. Earlier 66-core/18-feeding/25-lifecycle results are historical evidence, not tests executed here and not proof of sprite correctness.

## Reproduce safely

Python with Pillow is needed only for the extraction tool. Verify committed results with:

```powershell
python scripts/Extract-FishFrames.py --verify
```

To regenerate all PNGs and a local review page without overwriting the reviewed candidate, use fresh paths:

```powershell
python scripts/Extract-FishFrames.py --output assets/fish/reproduced --preview-dir artifacts/fish-reproduced --review-page devpost/fish-reproduced.html
python scripts/Extract-FishFrames.py --verify --output assets/fish/reproduced
```

The extractor refuses existing output/review paths. Review HTML uses only local files; there is no server or CDN.

## Remaining review and limits

The original background is flattened into RGB, so exact original semitransparent alpha and uncomposited edge colors cannot be recovered from this file. RGB-preserving binary masks may leave dark edge pixels visible on a light desktop; hole filling may also retain small enclosed background gaps. These are explicit visual-review points, not mechanically proven absence of defects. Look especially at fish 17–24 (fine angelfish fins), fish 05–08 (goldfish front/back edges), and dark eye/outline regions. Report any correction by the page's frame number/ID.

No runtime atlas or runtime metadata has been created. No app integration, final artwork acceptance, new package verification, publication or submission is claimed. Only after participant frame review may a follow-up pack approved PNGs, define their runtime mapping/placement, replace the fixed crop lookup, and run the existing relevant build/core/native/package checks while preserving movement, feeding, depth and occlusion.
