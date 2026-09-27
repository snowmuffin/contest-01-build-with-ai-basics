"""Pack only approved individual PNGs; never crop sprites from the preview sheet.

Use --build to write runtime resources, or --verify to audit them without writes.
Development-only Pillow. Packing preserves every RGBA pixel and does not rotate,
resize, regenerate, or re-extract approved artwork.
"""
import argparse
import hashlib
import json
from pathlib import Path
import runpy

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FRAMES = ROOT / "assets/fish/extracted-v1"
ATLAS = ROOT / "src/Aquarium.Windows/Assets/fish-sprites.png"
METADATA = ROOT / "src/Aquarium.Windows/Assets/fish-sprites.json"


def inputs():
    extractor = runpy.run_path(str(ROOT / "scripts/Extract-FishFrames.py"))
    source, config = extractor["load_inputs"](ROOT / "assets/fish/source/preview-sheet.png",
                                            ROOT / "assets/fish/extraction-regions.json")
    receipt = json.loads((FRAMES / "extraction-receipt.json").read_text(encoding="utf-8"))
    if receipt["annotations_sha256"] != extractor["annotation_digest"](config):
        raise ValueError("Source annotations changed since extraction")
    extractor["verify"](source, config, FRAMES, receipt)
    approval = json.loads((ROOT / "assets/fish/approval.json").read_text(encoding="utf-8"))
    frame_set = {f["id"]: f["frame_sha256"] for f in receipt["frames"]}
    fingerprint = hashlib.sha256(json.dumps(frame_set, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if (approval["status"] != "approved-for-runtime-integration" or
            approval["source_sha256"] != receipt["source_sha256"] or
            approval["frame_set_sha256"] != fingerprint):
        raise ValueError("Participant approval does not match these frames")
    return receipt, fingerprint


def packed(receipt, fingerprint):
    width, gutter = 1024, 2
    x = y = gutter
    row_height = 0
    frames = []
    canvases = {}
    for item in receipt["frames"]:
        species = item["id"].split("-")[0]
        w, h = item["size"]
        old_w, old_h = canvases.get(species, (0, 0))
        canvases[species] = (max(old_w, w), max(old_h, h))
    species_names = {"goldfish": "Goldfish", "tetra": "Tetra", "angelfish": "Angelfish", "guppy": "Guppy"}
    facing_names = {"left": "Left", "right": "Right", "front": "TowardViewer", "back": "AwayFromViewer"}
    for item in receipt["frames"]:
        species, facing, index = item["id"].split("-")
        w, h = item["size"]
        if x + w + gutter > width:
            x, y, row_height = gutter, y + row_height + gutter, 0
        cw, ch = canvases[species]
        frames.append({"id": item["id"], "species": species_names[species],
                       "facing": facing_names[facing], "frame": int(index)-1,
                       "x": x, "y": y, "width": w, "height": h,
                       "canvasWidth": cw, "canvasHeight": ch,
                       "offsetX": (cw-w)/2, "offsetY": (ch-h)/2,
                       "sourceFrameSha256": item["frame_sha256"]})
        x += w + gutter
        row_height = max(row_height, h)
    height = y + row_height + gutter
    atlas = Image.new("RGBA", (width, height))
    for entry in frames:
        image = Image.open(FRAMES / "frames" / (entry["id"] + ".png"))
        atlas.paste(image, (entry["x"], entry["y"]))
    metadata = {"version": 1, "width": width, "height": height, "gutter": gutter,
                "approvedFrameSetSha256": fingerprint,
                "layout": "variable rectangles; unscaled approved PNGs; centered per-species canvas",
                "frames": frames}
    return atlas, metadata


def verify(receipt, fingerprint):
    expected_atlas, expected_metadata = packed(receipt, fingerprint)
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    atlas = Image.open(ATLAS)
    if metadata != expected_metadata or atlas.mode != "RGBA" or atlas.size != expected_atlas.size:
        raise ValueError("Runtime atlas/metadata differ from approved packing")
    if atlas.tobytes() != expected_atlas.tobytes():
        raise ValueError("Packed RGBA pixels differ from approved frames or gutters")
    bounds = []
    for entry in metadata["frames"]:
        x, y, w, h = (entry[k] for k in ("x", "y", "width", "height"))
        box = (x, y, x+w, y+h)
        if any(max(x, a) < min(x+w, c) and max(y, b) < min(y+h, d) for a, b, c, d in bounds):
            raise ValueError("Overlapping sprite rectangles")
        bounds.append(box)
        original = Image.open(FRAMES / "frames" / (entry["id"] + ".png"))
        if atlas.crop(box).tobytes() != original.tobytes():
            raise ValueError(f"Frame round-trip failed: {entry['id']}")
    return {"passed": True, "frames": len(bounds), "atlas_size": list(atlas.size),
            "rgba_round_trip": True, "overlapping_rectangles": 0,
            "gutter_and_padding_preserved": True, "approval_fingerprint": fingerprint}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--build", action="store_true")
    mode.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    receipt, fingerprint = inputs()
    if args.build:
        atlas, metadata = packed(receipt, fingerprint)
        atlas.save(ATLAS)
        METADATA.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(verify(receipt, fingerprint), indent=2))


if __name__ == "__main__":
    main()
