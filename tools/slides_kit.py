"""Build Google Slides batchUpdate requests for a lesson deck.

The template is the Lesson 19 deck from course_v2 (copied into the target Drive folder
once per lesson). Layout, colours and cards stay untouched; only text is replaced.

    python tools/slides_kit.py slides/lesson01.py --out-dir /tmp/l01

Writes req_00.json, req_01.json, ... Send them in order with the Google Slides
connector's update_presentation tool (the `requests` array of each file).

A lesson spec is a Python file that defines LESSON ("01"), SERIES and SLIDES, built
from the helpers below. Editing one slide later means editing that entry only.
"""

from __future__ import annotations

import argparse
import json
import runpy
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "slides/l19_template_catalog.json").read_text(encoding="utf-8"))

TEMPLATE_SERIES = "PYTHON 資料分析實戰"
TEMPLATE_LESSON = "Lesson 19"
SECTION_SOURCES = {"p5", "p11"}
NO_PAGE_NUMBER = {"p1", "p5", "p11"}
MAX_CHUNK_BYTES = 14_000


@dataclass
class Slide:
    src: str
    texts: dict[str, str] = field(default_factory=dict)


def _pairs(prefix_ids: list[tuple[str, str]], items: list[tuple[str, str]]) -> dict[str, str]:
    assert len(prefix_ids) == len(items), "wrong number of items for this layout"
    texts = {}
    for (title_id, body_id), (title, body) in zip(prefix_ids, items):
        texts[title_id] = title
        texts[body_id] = body
    return texts


def title_slide(title, subtitle, badge, badge_caption, tagline) -> Slide:
    return Slide("p1", {"i4": title, "i5": subtitle, "i7": badge, "i8": badge_caption, "i10": tagline})


def cards4(kicker, title, items) -> Slide:
    texts = {"i2": kicker, "i3": title}
    texts.update(_pairs([("i10", "i11"), ("i15", "i16"), ("i20", "i21"), ("i25", "i26")], items))
    return Slide("p2", texts)


def statement(title, big, sub, kicker=None) -> Slide:
    texts = {"i3": title, "i9": big, "i10": sub}
    if kicker:
        texts["i2"] = kicker
    return Slide("p3", texts)


def flow5(kicker, title, steps) -> Slide:
    texts = {"i2": kicker, "i3": title}
    texts.update(_pairs([("i9", "i10"), ("i14", "i15"), ("i19", "i20"), ("i24", "i25"), ("i29", "i30")], steps))
    return Slide("p4", texts)


def section(letter, title, sub, tagline, src="p5") -> Slide:
    assert src in SECTION_SOURCES
    return Slide(src, {"i3": letter, "i4": title, "i5": sub, "i7": tagline})


def cards3_numbered(kicker, title, items, src="p6") -> Slide:
    texts = {"i2": kicker, "i3": title}
    texts.update(_pairs([("i10", "i11"), ("i15", "i16"), ("i20", "i21")], items))
    return Slide(src, texts)


def cards3_labeled(title, items, kicker=None) -> Slide:
    """items: (label, title, body); labels should be two characters."""
    texts = {"i3": title}
    if kicker:
        texts["i2"] = kicker
    for (label_id, title_id, body_id), (label, item_title, body) in zip(
        [("i9", "i10", "i11"), ("i14", "i15", "i16"), ("i19", "i20", "i21")], items
    ):
        texts.update({label_id: label, title_id: item_title, body_id: body})
    return Slide("p7", texts)


def checks5(title, items, src="p8", kicker=None) -> Slide:
    assert src in {"p8", "p23"}
    texts = {"i3": title}
    if kicker:
        texts["i2"] = kicker
    texts.update(_pairs([("i9", "i10"), ("i13", "i14"), ("i17", "i18"), ("i21", "i22"), ("i25", "i26")], items))
    return Slide(src, texts)


def compare2(title, left, right, src="p9", kicker=None) -> Slide:
    """left/right: (label, title, body, note)."""
    assert src in {"p9", "p10", "p12", "p20"}
    texts = {"i3": title}
    if kicker:
        texts["i2"] = kicker
    for ids, side in zip([("i8", "i9", "i10", "i12"), ("i14", "i15", "i16", "i18")], [left, right]):
        texts.update(dict(zip(ids, side)))
    return Slide(src, texts)


def code(title, label, code_text, panel_title, panel_body, note=None, src="p15") -> Slide:
    assert src in {"p15", "p16", "p18", "p19", "p21"}
    texts = {"i3": title, "i8": label, "i9": code_text, "i11": panel_title, "i12": panel_body}
    if note is not None:
        assert src != "p18", "p18 has no note box"
        texts["i14"] = note
    return Slide(src, texts)


def checkpoint(big, sub) -> Slide:
    return Slide("p24", {"i9": big, "i10": sub})


def _element_text(src: str, key: str) -> str | None:
    wanted = f"{src}_{key}"
    for element in CATALOG[src]["elements"]:
        if element["id"] == wanted:
            return element["text"]
    raise KeyError(f"{wanted} is not in the template catalog")


def _warn_if_long(src: str, key: str, new: str) -> None:
    old = _element_text(src, key) or ""
    new_lines, old_lines = new.split("\n"), old.split("\n")
    too_long = len(new) > 1.4 * len(old) + 6
    too_tall = len(new_lines) > len(old_lines) + 2
    if too_long or too_tall:
        print(
            f"WARN {src}_{key}: new text may overflow "
            f"({len(new)} chars/{len(new_lines)} lines vs template {len(old)}/{len(old_lines)})",
            file=sys.stderr,
        )


def build(lesson: str, series: str, slides: list[Slide]) -> list[list[dict]]:
    """Return request chunks, to be sent in order."""
    uses: dict[str, int] = {}
    placed: list[tuple[str, str, int]] = []  # (slide object id, src, copy number)
    duplicates: list[dict] = []
    for slide in slides:
        copy = uses.get(slide.src, 0)
        uses[slide.src] = copy + 1
        suffix = "" if copy == 0 else f"_dup{copy}"
        placed.append((slide.src + suffix, slide.src, copy))
        if copy:
            mapping = {slide.src: slide.src + suffix}
            for element in CATALOG[slide.src]["elements"]:
                mapping[element["id"]] = element["id"] + suffix
            duplicates.append({"duplicateObject": {"objectId": slide.src, "objectIds": mapping}})

    head = list(duplicates)
    head.append(_replace_all(TEMPLATE_SERIES, series))
    head.append(_replace_all(TEMPLATE_LESSON, f"Lesson {lesson}"))

    edit_groups: list[list[dict]] = []
    for position, (slide, (sid, src, copy)) in enumerate(zip(slides, placed), start=1):
        suffix = "" if copy == 0 else f"_dup{copy}"
        texts = dict(slide.texts)
        if src in SECTION_SOURCES:
            texts["i8"] = f"LESSON {lesson} · {position:02d}"
        elif src not in NO_PAGE_NUMBER:
            texts["i5"] = f"{position:02d}"
        group = []
        for key, new in texts.items():
            old = _element_text(src, key)
            assert old is not None, f"{src}_{key} is empty in the template; cannot edit it"
            if key not in {"i5"} and not (src in SECTION_SOURCES and key == "i8"):
                _warn_if_long(src, key, new)
            element_id = f"{src}_{key}{suffix}"
            # Insert first so the new text inherits the box's run style, then delete the old
            # text that now sits after it. Deleting everything first would drop the style.
            # The global replacements above already ran, so measure the box as it is now.
            current = old.replace(TEMPLATE_SERIES, series).replace(TEMPLATE_LESSON, f"Lesson {lesson}")
            new_len, old_len = _utf16_len(new), _utf16_len(current)
            group.append({"insertText": {"objectId": element_id, "insertionIndex": 0, "text": new}})
            group.append(
                {
                    "deleteText": {
                        "objectId": element_id,
                        "textRange": {"type": "FIXED_RANGE", "startIndex": new_len, "endIndex": new_len + old_len},
                    }
                }
            )
        edit_groups.append(group)

    tail: list[dict] = []
    keep = {sid for sid, _, _ in placed}
    for src in CATALOG:
        if src not in keep:
            tail.append({"deleteObject": {"objectId": src}})
    for index, (sid, _, _) in enumerate(placed):
        tail.append({"updateSlidesPosition": {"slideObjectIds": [sid], "insertionIndex": index}})

    chunks = [head]
    current: list[dict] = []
    for group in edit_groups:
        if current and _size(current + group) > MAX_CHUNK_BYTES:
            chunks.append(current)
            current = []
        current += group
    if current:
        chunks.append(current)
    chunks.append(tail)
    return chunks


def _utf16_len(text: str) -> int:
    return len(text.encode("utf-16-le")) // 2


def _replace_all(old: str, new: str) -> dict:
    return {"replaceAllText": {"containsText": {"text": old, "matchCase": True}, "replaceText": new}}


def _size(requests: list[dict]) -> int:
    return len(json.dumps(requests, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    sys.path.insert(0, str(Path(__file__).parent))
    spec = runpy.run_path(str(args.spec))
    chunks = build(spec["LESSON"], spec["SERIES"], spec["SLIDES"])

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for old in args.out_dir.glob("req_*.json"):
        old.unlink()
    for index, chunk in enumerate(chunks):
        path = args.out_dir / f"req_{index:02d}.json"
        path.write_text(json.dumps(chunk, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(f"{path.name}: {len(chunk)} requests, {_size(chunk)} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
