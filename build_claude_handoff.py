#!/usr/bin/env python3
"""
Create a Claude-friendly handoff bundle from parsed Septemics content.

Outputs in ./claude_handoff:
- septemics_claude_packet_clean.json
- septemics_vocabulary_clean.csv
- septemics_vocabulary_clean.txt
- septemics_rejected_terms.csv
- claude_vocab_handoff.md
- claude_prompt_template.md
"""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


def normalize_ws(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def looks_like_noise_term(term: str) -> Tuple[bool, str]:
    t = normalize_ws(term)
    if not t:
        return True, "empty"
    if len(t) > 70:
        return True, "too_long_chars"
    words = t.split()
    if len(words) > 8:
        return True, "too_many_words"
    if len(words) >= 6 and words[0].lower() in {"a", "an", "the"}:
        return True, "long_article_phrase"
    if any(ch in t for ch in ".!?;:"):
        return True, "sentence_punctuation"
    if t.lower().startswith(("if ", "when ", "because ", "therefore ", "however ")):
        return True, "sentence_starter"
    letters = "".join(ch for ch in t if ch.isalpha())
    if len(letters) < 2:
        return True, "too_few_letters"
    return False, ""


def build_handoff() -> None:
    base = Path(".")
    content_path = base / "septemics_content.json"
    raw_ocr_path = base / "septemics_full_book_raw_ocr.txt"
    out_dir = base / "claude_handoff"
    out_dir.mkdir(exist_ok=True)

    data = json.loads(content_path.read_text(encoding="utf-8"))
    scales = data.get("scales", [])

    vocab = defaultdict(
        lambda: {"term": "", "definitions": set(), "scales": set(), "occurrences": 0}
    )
    rejected_rows: List[Tuple[str, str, str]] = []

    for scale in scales:
        scale_name = normalize_ws(str(scale.get("name", "")))
        for entry in scale.get("glossary", []) or []:
            term = normalize_ws(str(entry.get("term", "")))
            definition = normalize_ws(str(entry.get("definition", "")))
            is_noise, reason = looks_like_noise_term(term)
            if is_noise:
                rejected_rows.append((term, reason, scale_name))
                continue

            key = term.lower()
            vocab[key]["term"] = term
            if definition:
                vocab[key]["definitions"].add(definition)
            if scale_name:
                vocab[key]["scales"].add(scale_name)
            vocab[key]["occurrences"] += 1

    flat_vocab: List[Dict[str, object]] = []
    for _, item in sorted(vocab.items(), key=lambda kv: kv[0]):
        flat_vocab.append(
            {
                "term": item["term"],
                "definitions": sorted(item["definitions"]),
                "scales": sorted(item["scales"]),
                "occurrences": item["occurrences"],
            }
        )

    packet = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_files": {
            "parsed_scales": str(content_path.resolve()),
            "raw_ocr_text": str(raw_ocr_path.resolve()) if raw_ocr_path.exists() else None,
        },
        "summary": {
            "scales": len(scales),
            "unique_terms_clean": len(flat_vocab),
            "rejected_terms": len(rejected_rows),
            "total_glossary_entries": sum(
                len(s.get("glossary", []) or []) for s in scales
            ),
        },
        "scales": scales,
        "vocabulary_clean": flat_vocab,
    }

    packet_path = out_dir / "septemics_claude_packet_clean.json"
    packet_path.write_text(
        json.dumps(packet, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    csv_path = out_dir / "septemics_vocabulary_clean.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["term", "definition", "scales", "occurrences"])
        for row in flat_vocab:
            writer.writerow(
                [
                    row["term"],
                    " | ".join(row["definitions"]),
                    " | ".join(row["scales"]),
                    row["occurrences"],
                ]
            )

    txt_path = out_dir / "septemics_vocabulary_clean.txt"
    with txt_path.open("w", encoding="utf-8") as f:
        f.write("Septemics Clean Vocabulary Export\n\n")
        for row in flat_vocab:
            f.write(f"TERM: {row['term']}\n")
            defs = row["definitions"] or [""]
            for d in defs:
                f.write(f"DEF: {d}\n")
            f.write(f"SCALES: {', '.join(row['scales'])}\n")
            f.write(f"OCCURRENCES: {row['occurrences']}\n\n")

    rejected_path = out_dir / "septemics_rejected_terms.csv"
    with rejected_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["term", "reason", "scale"])
        writer.writerows(rejected_rows)

    handoff_md = out_dir / "claude_vocab_handoff.md"
    with handoff_md.open("w", encoding="utf-8") as f:
        f.write("# Septemics Vocabulary Handoff\n\n")
        f.write("## Best Files To Give Claude\n")
        f.write(f"- `claude_handoff/{packet_path.name}`\n")
        f.write(f"- `claude_handoff/{csv_path.name}`\n")
        f.write(f"- `claude_handoff/{txt_path.name}`\n")
        f.write(f"- `claude_handoff/{rejected_path.name}`\n")
        if raw_ocr_path.exists():
            f.write(f"- `{raw_ocr_path.name}` (fallback raw corpus)\n")
        f.write("\n")
        f.write("## Quality Summary\n")
        f.write(f"- Scales: **{packet['summary']['scales']}**\n")
        f.write(f"- Clean unique terms: **{packet['summary']['unique_terms_clean']}**\n")
        f.write(f"- Rejected noisy terms: **{packet['summary']['rejected_terms']}**\n")
        f.write("\n")
        f.write("## Notes\n")
        f.write("- Clean CSV is the primary input for vocabulary normalization.\n")
        f.write("- Rejected terms CSV helps manual review of OCR artifacts.\n")
        f.write("- Full packet JSON includes both scale structure and clean vocabulary.\n")

    prompt_path = out_dir / "claude_prompt_template.md"
    with prompt_path.open("w", encoding="utf-8") as f:
        f.write("# Prompt for Claude (Vocabulary First)\n\n")
        f.write("Use the attached files to build a high-quality Septemics vocabulary artifact.\n\n")
        f.write("Files:\n")
        f.write(f"- `{packet_path.name}`\n")
        f.write(f"- `{csv_path.name}`\n")
        f.write(f"- `{txt_path.name}`\n")
        f.write(f"- `{rejected_path.name}`\n")
        if raw_ocr_path.exists():
            f.write(f"- `{raw_ocr_path.name}` (fallback OCR corpus)\n")
        f.write("\nRequirements:\n")
        f.write("- Produce a canonical vocabulary table with columns: term, canonical_definition, alternate_definitions, source_scales, confidence, notes.\n")
        f.write("- Normalize OCR noise (hyphenation, punctuation artifacts, case inconsistencies).\n")
        f.write("- Preserve provenance to source scales.\n")
        f.write("- Return both JSON and Markdown outputs.\n")
        f.write("- Include a concise \"needs human review\" list for ambiguous entries.\n")

    print("Wrote clean handoff bundle:")
    for p in [packet_path, csv_path, txt_path, rejected_path, handoff_md, prompt_path]:
        print("-", p)


if __name__ == "__main__":
    build_handoff()
