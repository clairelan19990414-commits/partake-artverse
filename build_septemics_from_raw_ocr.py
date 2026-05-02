#!/usr/bin/env python3
"""
Build app-ready Septemics JSON from raw OCR pages.

Usage:
  python build_septemics_from_raw_ocr.py \
    --input septemics_full_book_raw_ocr.json \
    --output septemics_content.json \
    --full-output septemics_content_full.json
"""

from __future__ import annotations

import argparse
import json
import re
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Optional, Tuple


STOPWORDS = {"of", "and", "the", "for", "to", "in", "on", "with", "a", "an"}
PARTS_OF_SPEECH = {
    "noun",
    "verb",
    "adjective",
    "adj",
    "adverb",
    "adv",
    "pronoun",
    "pron",
    "preposition",
    "prep",
    "conjunction",
    "conj",
    "interjection",
    "interj",
}

ROMAN_MAP = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
    "VIII": 8,
    "IX": 9,
    "X": 10,
}


def normalize_ws(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def roman_to_int(token: str) -> Optional[int]:
    return ROMAN_MAP.get(normalize_ws(token).upper())


def parse_level_number(token: str) -> Optional[int]:
    token = normalize_ws(token)
    if token.isdigit():
        return int(token)
    return roman_to_int(token)


def titleize_phrase(phrase: str) -> str:
    words = normalize_ws(phrase).split(" ")
    out = []
    for idx, w in enumerate(words):
        if not w:
            continue
        lw = w.lower()
        if idx > 0 and lw in STOPWORDS:
            out.append(lw)
        else:
            out.append(w[:1].upper() + w[1:].lower())
    return " ".join(out)


def normalize_scale_name(raw: str) -> str:
    raw = normalize_ws(raw)
    raw = raw.strip(" .:;|[]()")
    raw = re.sub(r"^[Tt]he\s+[Ss]cale\s+[Oo]f\s+", "", raw)
    raw = re.sub(r"^[Ss]cale\s+[Oo]f\s+", "", raw)
    raw = normalize_ws(raw)
    return f"The Scale Of {titleize_phrase(raw)}"


def is_plausible_scale_name(name: str) -> bool:
    name = normalize_ws(name)
    if not name.lower().startswith("the scale of "):
        return False
    if len(name) > 64:
        return False
    if name.count(".") > 0 or name.count(",") > 0 or name.count(":") > 0:
        return False
    tail = name[len("The Scale Of ") :]
    if len(tail.split()) > 8:
        return False
    return True


def extract_scale_hint(lines: List[str]) -> Optional[str]:
    joined = "\n".join(lines)
    patterns = [
        r"Glossary\s+for\s+(?:The\s+)?Scale\s+Of\s+([A-Za-z][A-Za-z \-.'/&]+)",
        r"(?:^|\n)(?:The\s+)?Scale\s+Of\s+([A-Za-z][A-Za-z \-.'/&]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, joined, flags=re.IGNORECASE)
        if match:
            candidate = normalize_scale_name(match.group(1))
            if is_plausible_scale_name(candidate):
                return candidate

    # Handle split OCR lines: "The Scale of" + next line "Personal Influence"
    for i in range(len(lines) - 1):
        if re.fullmatch(r"(?:The\s+)?Scale\s+Of", normalize_ws(lines[i]), flags=re.IGNORECASE):
            next_line = normalize_ws(lines[i + 1])
            if re.fullmatch(r"[A-Za-z][A-Za-z \-.'/&]{2,80}", next_line):
                candidate = normalize_scale_name(next_line)
                if is_plausible_scale_name(candidate):
                    return candidate

    return None


def letters_only(value: str) -> str:
    return "".join(ch for ch in value if ch.isalpha())


def uppercase_ratio(value: str) -> float:
    letters = letters_only(value)
    if not letters:
        return 0.0
    upper = sum(1 for ch in letters if ch.isupper())
    return upper / len(letters)


def looks_like_level_heading(rest: str) -> bool:
    text = normalize_ws(rest)
    if not text:
        return False
    if "." in text and "(" not in text:
        return False
    if "%" in text:
        return False
    if len(letters_only(text)) < 3:
        return False
    if len(text.split()) > 15:
        return False
    lower = text.lower()
    if lower.startswith(("has ", "is ", "are ", "was ", "were ", "the ", "this ", "one ", "we ", "you ")):
        return False
    if text[:1].islower():
        return False
    if "(" in text:
        return True
    return uppercase_ratio(text) >= 0.40


def clean_level_label(rest: str) -> str:
    text = normalize_ws(rest)
    text = re.sub(r"\s+\d+\.\d+$", "", text)  # strip trailing numeric table values
    text = text.strip(" .:;|")
    return text


def get_or_create_scale(scales: "OrderedDict[str, Dict[str, object]]", name: str) -> Dict[str, object]:
    if name not in scales:
        scales[name] = {"name": name, "glossary": [], "levels": []}
    return scales[name]


def append_glossary_entry(scale: Dict[str, object], term: str, definition: str) -> None:
    term = normalize_ws(term).strip(" .:;|")
    definition = normalize_ws(definition)
    if not term:
        return
    scale["glossary"].append({"term": term, "definition": definition})


def upsert_level(scale: Dict[str, object], number: int, label: str, description: str = "") -> None:
    levels: List[Dict[str, object]] = scale["levels"]
    for level in levels:
        if int(level["number"]) == int(number):
            if label and (not level.get("label") or len(label) > len(str(level.get("label", "")))):
                level["label"] = label
            if description:
                existing = normalize_ws(str(level.get("description", "")))
                incoming = normalize_ws(description)
                if incoming and incoming not in existing:
                    level["description"] = normalize_ws(f"{existing} {incoming}")
            return
    levels.append({"number": int(number), "label": label or f"Level {number}", "description": normalize_ws(description)})


def parse_glossary_line(line: str) -> Optional[Tuple[str, str]]:
    # Term, noun: definition...
    m = re.match(
        r"^([A-Za-z][A-Za-z0-9' /&\-]{1,70}),\s*([A-Za-z.]+)\s*:?\s*(.*)$",
        line,
        flags=re.IGNORECASE,
    )
    if m:
        pos = m.group(2).rstrip(".").lower()
        if pos in PARTS_OF_SPEECH:
            term = m.group(1)
            tail = normalize_ws(m.group(3))
            return term, tail

    # Term: definition...
    m = re.match(r"^([A-Za-z][A-Za-z0-9' /&\-]{1,70})\s*:\s*(.+)$", line)
    if m:
        return m.group(1), m.group(2)
    return None


def parse_raw_ocr(raw_pages: List[Dict[str, object]]) -> Dict[str, object]:
    scales: "OrderedDict[str, Dict[str, object]]" = OrderedDict()
    current_scale_name: Optional[str] = None
    parse_stats = {
        "pages_seen": 0,
        "pages_with_scale_hint": 0,
        "level_headings": 0,
        "level_descriptions": 0,
        "glossary_entries": 0,
    }

    level_heading_re = re.compile(r"^\s*([IVX]{1,4}|\d{1,2})\s*\)?\s*[)\].:\-]?\s*(.+?)\s*$", re.IGNORECASE)
    at_level_re = re.compile(r"^\s*(?:At\s+)?Level\s+([IVX]{1,4}|\d{1,2})\s*[,:\-)]?\s*(.*)$", re.IGNORECASE)

    for page in raw_pages:
        parse_stats["pages_seen"] += 1
        text = str(page.get("text", "") or "")
        lines = [normalize_ws(ln) for ln in text.splitlines() if normalize_ws(ln)]

        scale_hint = extract_scale_hint(lines)
        if scale_hint:
            current_scale_name = scale_hint
            get_or_create_scale(scales, current_scale_name)
            parse_stats["pages_with_scale_hint"] += 1

        if not current_scale_name:
            continue

        scale = get_or_create_scale(scales, current_scale_name)
        in_glossary = any("glossary for" in ln.lower() for ln in lines)
        pending_term: Optional[str] = None

        for line in lines:
            low = line.lower()
            if "glossary for" in low:
                in_glossary = True
                continue
            if re.search(r"(?:^|\b)(?:the\s+)?scale\s+of\s+", line, flags=re.IGNORECASE):
                # Keep current scale context but don't treat heading line as glossary/description.
                continue

            lvl_desc = at_level_re.match(line)
            if lvl_desc:
                lvl_num = parse_level_number(lvl_desc.group(1))
                if lvl_num is not None:
                    snippet = normalize_ws(lvl_desc.group(2))
                    upsert_level(scale, lvl_num, f"Level {lvl_num}", snippet)
                    parse_stats["level_descriptions"] += 1
                continue

            lvl_head = level_heading_re.match(line)
            if lvl_head:
                lvl_num = parse_level_number(lvl_head.group(1))
                rest = clean_level_label(lvl_head.group(2))
                if lvl_num is not None and looks_like_level_heading(rest):
                    upsert_level(scale, lvl_num, rest)
                    parse_stats["level_headings"] += 1
                    pending_term = None
                    continue

            if in_glossary:
                parsed = parse_glossary_line(line)
                if parsed:
                    term, maybe_def = parsed
                    append_glossary_entry(scale, term, maybe_def)
                    parse_stats["glossary_entries"] += 1
                    pending_term = term
                    continue

                if pending_term and len(line.split()) >= 3:
                    glossary_list = scale["glossary"]
                    if glossary_list and glossary_list[-1]["term"] == pending_term:
                        existing = normalize_ws(glossary_list[-1].get("definition", ""))
                        if line not in existing:
                            glossary_list[-1]["definition"] = normalize_ws(f"{existing} {line}")

    # Dedupe and sort levels/glossary in each scale
    cleaned_scales: List[Dict[str, object]] = []
    for scale in scales.values():
        level_map: Dict[int, Dict[str, object]] = {}
        for level in scale["levels"]:
            number = int(level["number"])
            if number not in level_map:
                level_map[number] = {
                    "number": number,
                    "label": normalize_ws(str(level.get("label", f"Level {number}"))),
                    "description": normalize_ws(str(level.get("description", ""))),
                }
            else:
                if len(str(level.get("label", ""))) > len(str(level_map[number]["label"])):
                    level_map[number]["label"] = normalize_ws(str(level.get("label", "")))
                incoming = normalize_ws(str(level.get("description", "")))
                if incoming and incoming not in level_map[number]["description"]:
                    level_map[number]["description"] = normalize_ws(
                        f"{level_map[number]['description']} {incoming}"
                    )

        glossary_map: Dict[str, Dict[str, str]] = {}
        for item in scale["glossary"]:
            term = normalize_ws(str(item.get("term", "")))
            definition = normalize_ws(str(item.get("definition", "")))
            if not term:
                continue
            key = term.lower()
            if key not in glossary_map:
                glossary_map[key] = {"term": term, "definition": definition}
            else:
                existing = glossary_map[key]["definition"]
                if definition and definition not in existing:
                    glossary_map[key]["definition"] = normalize_ws(f"{existing} {definition}")

        cleaned_scales.append(
            {
                "name": scale["name"],
                "glossary": list(glossary_map.values()),
                "levels": [level_map[k] for k in sorted(level_map.keys())],
            }
        )

    # App-ready subset: avoid empty cards with no level/glossary signal.
    app_ready_scales = [
        s
        for s in cleaned_scales
        if is_plausible_scale_name(s["name"])
        and (len(s["levels"]) >= 2 or (len(s["levels"]) >= 1 and len(s["glossary"]) >= 4))
    ]

    cleaned_scales = [s for s in cleaned_scales if is_plausible_scale_name(s["name"])]

    return {
        "app_ready": {"scales": app_ready_scales},
        "full": {"scales": cleaned_scales, "stats": parse_stats},
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Septemics content JSON from raw OCR pages.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("septemics_full_book_raw_ocr.json"),
        help="Raw OCR JSON input file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("septemics_content.json"),
        help="App-ready output JSON path.",
    )
    parser.add_argument(
        "--full-output",
        type=Path,
        default=Path("septemics_content_full.json"),
        help="Full output JSON path with stats and all parsed scales.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw = json.loads(args.input.read_text(encoding="utf-8"))
    pages = raw.get("pages", [])
    if not isinstance(pages, list):
        raise ValueError("Input raw OCR file does not contain a pages array.")

    built = parse_raw_ocr(pages)
    args.output.write_text(json.dumps(built["app_ready"], indent=2, ensure_ascii=False), encoding="utf-8")
    args.full_output.write_text(json.dumps(built["full"], indent=2, ensure_ascii=False), encoding="utf-8")

    app_scales = built["app_ready"]["scales"]
    full_scales = built["full"]["scales"]
    stats = built["full"]["stats"]

    print(f"Wrote app-ready JSON: {args.output}")
    print(f"Wrote full JSON: {args.full_output}")
    print(
        "Summary:",
        f"pages={stats['pages_seen']}",
        f"scale_hints={stats['pages_with_scale_hint']}",
        f"level_headings={stats['level_headings']}",
        f"level_descriptions={stats['level_descriptions']}",
        f"glossary_entries={stats['glossary_entries']}",
        f"app_scales={len(app_scales)}",
        f"full_scales={len(full_scales)}",
    )


if __name__ == "__main__":
    main()
