# Project asset notice

Project assets are separate from the source-code license. This notice covers `assets/` and `src/Aquarium.Windows/Assets/`, including source previews, individual sprites, masks, runtime atlases, sprite metadata and icons. Any identified third-party content remains subject to its original terms instead.

## Provenance

| Asset | Origin and record |
| --- | --- |
| Current fish preview and 32 extracted frames; `fish-sprites.png` / `fish-sprites.json` | AI-assisted artwork generated for this project during the contest period using the developer's own ChatGPT account, as declared by the developer. No external reference image was supplied; no specific character, work or brand was requested. Text instructions described ordinary fish species, directions and desired appearance. See [source provenance](assets/fish/source/provenance.json), [frame approval](assets/fish/approval.json) and [extraction verification](docs/fish-sprite-verification.md). |
| `feeder.png` and `feeder.ico`, also used for the resident icon | Original project-specific procedural pixel artwork produced by the project's [asset generator](scripts/Generate-Assets.py), rather than the ChatGPT fish-image workflow. No external artwork was incorporated. |
| Legacy `fish-atlas.png` and earlier fish artwork in Git history | Superseded project artwork. Earlier procedural assets and the participant-directed AI atlas are recorded in the repository history; the legacy atlas is not embedded or loaded by the current app. The specific no-external-reference declaration above concerns the current preview, not a retrospective claim about every historical generation. |

The current preview was supplied by the developer on 2026-09-27. Its SHA-256 is `0d41ac55d8e23f51816d15ef151b08f9e07e23b5b9a8fb6f0d19ad3c1df619e5`. Extraction preserves source RGB at native resolution, with reproducible binary masks and transparent padding. Runtime packing preserves the approved frames without redrawing or resampling. The generation account/prompt circumstances are the developer's declaration; the image contains no embedded generation metadata independently proving those circumstances.

## Permitted use and commercial reuse

To the extent the project owner holds applicable rights, the owner permits you to use, copy, modify and redistribute these project-created assets with this project or its noncommercial derivatives for noncommercial purposes, retaining this notice and provenance attribution. This permits building, running, reviewing and noncommercially modifying the public contest version. [LICENSING.md](LICENSING.md#contest-access-and-rights) separately addresses official contest testing and organizer permissions.

**Project-created assets are not offered for third-party commercial reuse without separate permission from the project owner, to the extent applicable rights exist.** This includes use in a commercially sold copy of this project or another commercial product. Seek separate permission from [the project owner](https://github.com/snowmuffin) for uses outside the permission above. The owner may use different terms for the owner's future commercial edition.

AI-assisted generation does not establish that every resulting pixel is protected by copyright, that output is unique, or that exclusive rights exist in every jurisdiction. This notice asserts only rights the owner actually holds; it does not create rights in public-domain or otherwise unprotectable material, restrict statutory exceptions, or guarantee freedom from third-party claims. The facts recorded here are provenance information, not a legal determination of copyrightability.
