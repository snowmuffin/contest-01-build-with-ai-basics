"""Extract annotated source sprites for HUMAN REVIEW, never a runtime atlas.

Development-only Pillow; no AI calls, downloads, resampling, or app changes.
Every visible RGB pixel is copied from the source. The flattened source has no
recoverable original alpha: threshold + small enclosed-hole filling is an
explicit, reproducible binary mask, not a claim of original-alpha recovery.
"""
from pathlib import Path
import argparse
from collections import deque
import hashlib
import html
import io
import json
import os

from PIL import Image, ImageDraw, __version__ as PILLOW_VERSION

ROOT = Path(__file__).resolve().parents[1]
SPECIES = ("goldfish", "tetra", "angelfish", "guppy")
DIRECTIONS = ("left", "right", "front", "back")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def annotation_digest(config):
    # Git may check out JSON with CRLF; fingerprint meaning, not line endings.
    normalized = json.dumps(config, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def relative(path):
    return path.resolve().relative_to(ROOT).as_posix()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def binary_mask(crop, threshold, hole_limit):
    w, h = crop.size
    pixels = list(crop.getdata())
    selected = [max(p[:3]) > threshold for p in pixels]
    visited = bytearray(w * h)
    filled = 0
    # Four-neighbour background flood: preserve enclosed dark eye/body pixels,
    # but keep larger negative spaces between fins transparent. All disconnected
    # foreground fragments survive; there is no largest-component filter.
    for seed in range(w * h):
        if selected[seed] or visited[seed]:
            continue
        pending = deque([seed])
        visited[seed] = 1
        component = []
        edge = False
        while pending:
            i = pending.popleft()
            component.append(i)
            x, y = i % w, i // w
            edge |= x == 0 or y == 0 or x == w - 1 or y == h - 1
            for xx, yy in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
                if 0 <= xx < w and 0 <= yy < h:
                    j = yy * w + xx
                    if not selected[j] and not visited[j]:
                        visited[j] = 1
                        pending.append(j)
        if not edge and len(component) <= hole_limit:
            filled += len(component)
            for i in component:
                selected[i] = True
    mask = Image.new("L", (w, h))
    mask.putdata([255 if v else 0 for v in selected])
    return mask, filled


def load_inputs(source_path, regions_path):
    config = json.loads(regions_path.read_text(encoding="utf-8"))
    if digest(source_path) != config["source_sha256"]:
        raise ValueError("Source hash differs from reviewed coordinate annotations")
    source = Image.open(source_path).convert("RGBA")
    if list(source.size) != config["source_size"]:
        raise ValueError("Source dimensions differ from annotations")
    if source.getchannel("A").getextrema() != (255, 255):
        raise ValueError("This mask recipe is specific to the opaque preview source")
    expected = [f"{s}-{d}-{f:02}" for s in SPECIES for d in DIRECTIONS for f in (1, 2)]
    if [f["id"] for f in config["frames"]] != expected:
        raise ValueError("Expected exactly four species x four directions x two unique frames")
    boxes = []
    for entry in config["frames"]:
        x0, y0, x1, y1 = entry["box"]
        if not (0 <= x0 < x1 <= source.width and 0 <= y0 < y1 <= source.height):
            raise ValueError(f"Out-of-source box: {entry['id']}")
        for a, b, c, d in boxes:
            if max(a, x0) < min(c, x1) and max(b, y0) < min(d, y1):
                raise ValueError(f"Overlapping source ownership: {entry['id']}")
        boxes.append(entry["box"])
    return source, config


def extract(source, config, output):
    output.mkdir(parents=True, exist_ok=False)
    (output / "frames").mkdir()
    (output / "masks").mkdir()
    entries = []
    for number, entry in enumerate(config["frames"], 1):
        box = entry["box"]
        crop = source.crop(box)
        mask, filled = binary_mask(crop, config["background_max_channel"],
                                  config["fill_enclosed_dark_holes_up_to_pixels"])
        bounds = mask.getbbox()
        if bounds is None:
            raise ValueError(f"Empty sprite: {entry['id']}")
        left, top, right, bottom = bounds
        margins = [left, top, crop.width-right, crop.height-bottom]
        if min(margins) < 2:
            raise ValueError(f"Possible cut at annotation boundary: {entry['id']} {margins}")
        padding = config["padding"]
        # Trim each individual silhouette, then add an equal transparent margin.
        # No fixed cell sizes, scaling, mirroring, atlas packing, or pivot inference.
        sprite = Image.new("RGBA", (right-left+2*padding, bottom-top+2*padding))
        cutout = crop.crop(bounds)
        cutout.putalpha(mask.crop(bounds))
        sprite.paste(cutout, (padding, padding))
        frame_path = output / "frames" / (entry["id"] + ".png")
        mask_path = output / "masks" / (entry["id"] + ".png")
        sprite.save(frame_path)
        mask.save(mask_path)
        entries.append({
            "number": number, "id": entry["id"], "source_box": box,
            "source_visible_box": [box[0]+left, box[1]+top, box[0]+right, box[1]+bottom],
            "source_margin_pixels": margins, "size": list(sprite.size),
            "padding": padding, "visible_pixels": sum(v != 0 for v in mask.getdata()),
            "filled_dark_hole_pixels": filled,
            "frame": "frames/" + frame_path.name, "mask": "masks/" + mask_path.name,
            "frame_sha256": digest(frame_path), "mask_sha256": digest(mask_path),
        })
    return entries


def verify(source, config, output, receipt):
    if receipt["source_sha256"] != config["source_sha256"]:
        raise ValueError("Receipt source mismatch")
    if len(receipt["frames"]) != 32:
        raise ValueError("Receipt must contain 32 frames")
    names = {f["id"] + ".png" for f in config["frames"]}
    for directory in ("frames", "masks"):
        if {p.name for p in (output / directory).glob("*.png")} != names:
            raise ValueError(f"Missing or extra {directory}")
    visible_total = 0
    frame_hashes = set()
    for expected, entry in zip(config["frames"], receipt["frames"]):
        if entry["id"] != expected["id"] or entry["source_box"] != expected["box"]:
            raise ValueError("Receipt annotations mismatch")
        frame_path, mask_path = output / entry["frame"], output / entry["mask"]
        if digest(frame_path) != entry["frame_sha256"] or digest(mask_path) != entry["mask_sha256"]:
            raise ValueError(f"Output hash mismatch: {entry['id']}")
        frame_hashes.add(digest(frame_path))
        sprite, mask = Image.open(frame_path), Image.open(mask_path)
        expected_mask, _ = binary_mask(source.crop(expected["box"]),
                                      config["background_max_channel"],
                                      config["fill_enclosed_dark_holes_up_to_pixels"])
        if mask.tobytes() != expected_mask.tobytes():
            raise ValueError(f"Mask does not reproduce: {entry['id']}")
        bounds = expected_mask.getbbox()
        if bounds is None:
            raise ValueError(f"Empty mask: {entry['id']}")
        a, b, c, d = bounds
        x, y, _, _ = expected["box"]
        if entry["source_visible_box"] != [x+a, y+b, x+c, y+d]:
            raise ValueError(f"Visible source coordinates mismatch: {entry['id']}")
        margins = [a, b, expected_mask.width-c, expected_mask.height-d]
        if min(margins) < 2 or margins != entry["source_margin_pixels"]:
            raise ValueError(f"Source boundary contact: {entry['id']}")
        p = entry["padding"]
        if p < 1 or sprite.mode != "RGBA" or list(sprite.size) != entry["size"]:
            raise ValueError(f"Unexpected image format/size: {entry['id']}")
        if sprite.getchannel("A").getbbox() != (p, p, sprite.width-p, sprite.height-p):
            raise ValueError(f"Transparent padding or bounds mismatch: {entry['id']}")
        if set(sprite.getchannel("A").getdata()) != {0, 255}:
            raise ValueError(f"Unexpected alpha: {entry['id']}")
        visible_box = entry["source_visible_box"]
        source_patch = source.crop(visible_box)
        extracted = sprite.crop((p, p, sprite.width-p, sprite.height-p))
        if extracted.convert("RGB").tobytes() != source_patch.convert("RGB").tobytes():
            raise ValueError(f"RGB pixels changed: {entry['id']}")
        if extracted.getchannel("A").tobytes() != expected_mask.crop(bounds).tobytes():
            raise ValueError(f"Sprite does not use its saved mask: {entry['id']}")
        reproduced = Image.new("RGBA", sprite.size)
        patch = source_patch.copy()
        patch.putalpha(expected_mask.crop(bounds))
        reproduced.paste(patch, (p, p))
        encoded = io.BytesIO()
        reproduced.save(encoded, format="PNG")
        if hashlib.sha256(encoded.getvalue()).hexdigest() != entry["frame_sha256"]:
            raise ValueError(f"PNG bytes do not reproduce: {entry['id']}")
        visible_total += sum(a > 0 for a in extracted.getchannel("A").getdata())
    if len(frame_hashes) != 32:
        raise ValueError("Unexpected byte-identical duplicate frames")
    return {"passed": True, "frames": 32, "masks": 32, "unique_frame_hashes": 32,
            "visible_pixels": visible_total, "visible_rgb_changed_pixels": 0,
            "source_regions_non_overlapping": True, "source_boundary_contact": False,
            "mask_reproduction": True, "minimum_transparent_padding": config["padding"],
            "runtime_atlas_created": False, "human_review": "pending"}


def review_artifacts(source, config, output, entries, preview_dir, page):
    preview_dir.mkdir(parents=True, exist_ok=False)
    if page.exists():
        raise FileExistsError(f"Refusing to replace existing review page: {page}")
    annotated = source.convert("RGB")
    draw = ImageDraw.Draw(annotated)
    for entry in entries:
        x0, y0, x1, y1 = entry["source_box"]
        draw.rectangle((x0, y0, x1-1, y1-1), outline="#50ffc6", width=1)
        draw.text((x0+2, y0+2), f"{entry['number']:02}", fill="#50ffc6", stroke_width=1, stroke_fill="#07100e")
    annotated.save(preview_dir / "source-regions.png")
    # Contact sheets are labelled review documents, never runtime assets.
    for theme, bg, ink in (("light", "#f5f1e9", "#18232a"), ("dark", "#15232c", "#e2eff5")):
        sheet = Image.new("RGB", (8*186, 4*245), bg)
        draw = ImageDraw.Draw(sheet)
        for i, entry in enumerate(entries):
            x, y = (i % 8)*186, (i // 8)*245
            sprite = Image.open(output / entry["frame"])
            sheet.paste(sprite, (x+(186-sprite.width)//2, y+26+(205-sprite.height)//2), sprite)
            draw.text((x+8, y+7), f"{i+1:02} {entry['id']}", fill=ink)
            draw.text((x+8, y+230), f"{sprite.width} x {sprite.height} px", fill=ink)
        sheet.save(preview_dir / f"contact-{theme}.png")

    def url(path):
        return html.escape(os.path.relpath(path, page.parent).replace(os.sep, "/"), quote=True)

    cards = []
    for entry in entries:
        x0, y0, x1, y1 = entry["source_box"]
        # The full original sheet as a CSS background gives an unmodified source
        # comparison; no extra derivative source crops are saved or distributed.
        cards.append(f'''<article id="{entry['id']}">
<h2>{entry['number']:02} · {entry['id']}</h2>
<p>{entry['size'][0]}×{entry['size'][1]} px · 원본 영역 {entry['source_box']}</p>
<div class="comparison">
<figure><figcaption>원본 영역 · 1:1</figcaption><div class="source" style="width:{x1-x0}px;height:{y1-y0}px;background-position:-{x0}px -{y0}px"></div></figure>
<figure><figcaption>독립 PNG · 1:1</figcaption><div class="stage"><img alt="{entry['id']} 원배율" src="{url(output / entry['frame'])}" width="{entry['size'][0]}" height="{entry['size'][1]}"></div></figure>
<figure><figcaption>마스크 · 원본 영역 크기</figcaption><img alt="{entry['id']} 마스크" src="{url(output / entry['mask'])}"></figure></div>
<details><summary>픽셀 확대 보기 (3×)</summary><div class="stage enlarged"><img alt="{entry['id']} 3배 확대" src="{url(output / entry['frame'])}" width="{entry['size'][0]*3}" height="{entry['size'][1]*3}"></div></details>
<p><a href="{url(output / entry['frame'])}" download>PNG 다운로드</a> · <a href="{url(output / entry['mask'])}" download>마스크 다운로드</a></p></article>''')
    document = '''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>물고기 32프레임 추출 검수</title><style>
*{box-sizing:border-box}body{margin:0;background:#eff2f4;color:#16222d;font:16px/1.6 system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:28px}h1{font-size:28px}h2{font-size:19px}p{margin:8px 0}.note,article{padding:20px;background:white;border:1px solid #cbd5dd;border-radius:10px;margin:16px 0}nav{position:sticky;top:0;background:#eff2f4f5;padding:12px;z-index:2}button{font:inherit;padding:8px 14px;cursor:pointer;margin:2px}button[aria-pressed=true]{background:#174b66;color:white}a{color:#155674}figure{margin:0}figcaption{font-size:14px;margin-bottom:8px}.comparison{display:flex;gap:30px;flex-wrap:wrap;align-items:start}.stage{background-color:#e4e4e4;background-image:conic-gradient(#bbb 25%,transparent 0 50%,#bbb 0 75%,transparent 0);background-size:16px 16px;display:inline-block;line-height:0;min-width:20px}body.light .stage{background:#fff9ef}body.dark .stage{background:#16232d}.enlarged{max-width:100%;overflow:auto;margin-top:12px}img{image-rendering:pixelated;display:block}details{margin-top:16px}.source{background-image:url('SOURCE_URL')}.overview{max-width:100%;height:auto}summary{cursor:pointer}
</style><main><h1>물고기 32프레임 · 추출 검수</h1>
<div class="note"><strong>검수 대기 · 앱 미적용</strong><p>각 물고기를 독립 PNG로 추출했습니다. 번호로 수정할 프레임을 지정할 수 있습니다. 종별 순서는 금붕어 / 테트라 / 엔젤피시 / 구피, 방향은 Left / Right / Front / Back입니다.</p>
<p>원본은 배경이 합쳐진 불투명 PNG입니다. RGB·원배율은 보존했으며, 투명도는 기록된 이진 마스크로 만들었습니다. 밝은 배경에서 어두운 테두리, 지느러미 끝, 몸 안의 빈틈을 확인해 주세요. 원래의 반투명 알파를 복원한 결과는 아닙니다.</p>
<p>runtime atlas·runtime metadata는 생성하지 않았습니다. 검수 완료 후에만 다음 단계로 진행합니다.</p></div>
<nav aria-label="검수 배경"><button type="button" data-theme="checker" aria-pressed="true">체커</button><button type="button" data-theme="light" aria-pressed="false">밝은 배경</button><button type="button" data-theme="dark" aria-pressed="false">어두운 배경</button><a href="#regions">원본 영역 지도</a></nav>
CARDS
<h2 id="regions">원본 영역 지도 · 01–32</h2><img class="overview" alt="32개 독립 추출 영역이 표시된 원본" src="MAP_URL">
<script>document.querySelectorAll('button[data-theme]').forEach(button=>button.addEventListener('click',()=>{document.body.className=button.dataset.theme;document.querySelectorAll('button[data-theme]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));}));</script></main></html>'''
    page.write_text(document.replace("SOURCE_URL", url(ROOT / "assets/fish/source/preview-sheet.png"))
                    .replace("CARDS", "\n".join(cards))
                    .replace("MAP_URL", url(preview_dir / "source-regions.png")), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "assets/fish/extracted-v1")
    parser.add_argument("--preview-dir", type=Path, default=ROOT / "artifacts/fish-sprite-review-v1")
    parser.add_argument("--review-page", type=Path, default=ROOT / "devpost/fish-sprite-review.html")
    parser.add_argument("--verify", action="store_true", help="Read and verify existing extraction; write nothing")
    args = parser.parse_args()
    source_path = ROOT / "assets/fish/source/preview-sheet.png"
    regions_path = ROOT / "assets/fish/extraction-regions.json"
    source, config = load_inputs(source_path, regions_path)
    output = args.output.resolve()
    if not output.is_relative_to(ROOT / "assets/fish"):
        raise ValueError("Extraction output must stay under assets/fish")
    if args.verify:
        receipt = json.loads((output / "extraction-receipt.json").read_text(encoding="utf-8"))
        if receipt["annotations_sha256"] != annotation_digest(config):
            raise ValueError("Annotation hash differs from saved extraction receipt")
        print(json.dumps(verify(source, config, output, receipt), indent=2))
        return
    if output.exists() or args.preview_dir.exists() or args.review_page.exists():
        raise FileExistsError("Choose new output, preview, and page paths; existing work is never overwritten")
    entries = extract(source, config, output)
    receipt = {"purpose": "Extraction audit; NOT runtime metadata", "status": "awaiting-human-review",
               "source": relative(source_path), "source_sha256": digest(source_path),
               "annotations_sha256": annotation_digest(config),
               "annotations_digest_encoding": "canonical-json-sort-keys-compact-utf8",
               "pillow_version": PILLOW_VERSION,
               "alpha_method": "binary background threshold with small enclosed dark-hole filling",
               "rgb_method": "unaltered source pixels, no resampling", "frames": entries}
    result = verify(source, config, output, receipt)
    write_json(output / "extraction-receipt.json", receipt)
    write_json(output / "verification.json", result)
    review_artifacts(source, config, output, entries, args.preview_dir, args.review_page)
    print(json.dumps(result, indent=2))
    print(f"Review page: {args.review_page}")


if __name__ == "__main__":
    main()
