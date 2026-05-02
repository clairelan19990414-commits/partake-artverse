#!/usr/bin/env python3
"""
Enrich septemics_content.json with assessment-friendly choice text.

The OCR/parser output can leave some level descriptions blank. This pass keeps
book descriptions where they exist, then builds practical "choose this if..."
guidelines from the level label and glossary terms so the local app can behave
like a guided assessment instead of a raw reference table.
"""

from __future__ import annotations

import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
CONTENT_PATH = ROOT / "septemics_content.json"
EMBEDDED_PATH = ROOT / "septemics_data.js"
BACKUP_PATH = ROOT / "septemics_content.before_guidelines.json"

ROMAN_BY_NUMBER = {
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "V",
    6: "VI",
    7: "VII",
}

LABEL_FIXES = {
    ("The Scale Of Basic Purposes", 1): "SAINT (-)",
    ("The Scale Of Belief", 1): "BELIEF (Complete Faith)",
    ("The Scale Of Relationships", 1): "UNITY (Duplication)",
    ("The Scale Of Thought", 1): "CREATE (Inspiration)",
    ("The Scale Of Identity", 1): "NO NEED FOR IDENTITY (Congruence)",
    ("The Scale Of Stopping", 1): "WON'T STOP (Determination)",
    ("The Scale Of Human Ability", 1): "GENIUS (Mastery)",
    ("The Scale Of Memory", 1): "NO MEMORY NEEDED (Present Creation)",
    ("The Scale Of Spiritual Identity", 2): "DIFFERENTIATED SPIRITUAL IDENTITY",
    ("The Scale Of Mental Deletion", 1): "DELETION BY WILL",
    ("The Scale Of Physical Fitness", 1): "SUPERHUMAN (Legendary Health)",
    ("The Scale Of Physical Fitness", 2): "ATHLETIC (Splendid Physical Specimen)",
    ("The Scale Of Justification", 2): "BY RESPONSIBILITY",
    ("The Scale Of Justification", 3): "BY ACCEPTANCE",
    ("The Scale Of Justification", 7): "NO ATTEMPT AT JUSTIFICATION",
    ("The Scale Of Attack", 3): "UNWILLING TO ATTACK (Pacifism)",
    ("The Scale Of Life Spheres", 1): "LIFE SPHERE (All Life Forms)",
    ("The Scale Of Life Spheres", 3): "CULTURAL SPHERE",
    ("The Scale Of Life Spheres", 4): "TEAM SPHERE",
    ("The Scale Of Life Spheres", 5): "INTERPERSONAL SPHERE",
    ("The Scale Of Life Spheres", 6): "INDIVIDUAL SPHERE",
    ("The Scale Of Government", 5): "FASCISM (Elite Control)",
    ("The Scale Of Exchange", 1): "HONOR (Complete Trust)",
    ("The Scale Of Exchange", 2): "CREDIT (Deferred Exchange)",
    ("The Scale Of Exchange", 3): "CASH (Money)",
    ("The Scale Of Exchange", 4): "COIN (Portable Medium)",
    ("The Scale Of Exchange", 6): "BARTER (Direct Trade)",
    ("The Scale Of Exchange", 7): "TAKING (Theft)",
    ("The Scale Of Communication", 1): "PRESENCE",
    ("The Scale Of Communication", 2): "INSPECTION",
    ("The Scale Of Sexuality", 1): "NO NEED FOR SEX (Transcendence)",
    ("The Scale Of Sexuality", 2): "SUBLIMATION",
}

DESCRIPTION_FIXES = {
    ("The Scale Of Basic Purposes", 1): "The book places Saint at Level I: a person whose basic purpose is transcendence, with courage, wisdom, ethics, humility, and concern extending beyond ordinary self-interest.",
    ("The Scale Of Basic Purposes", 2): "The book places Leader at Level II: a natural leader who can relate to humanity broadly, seeks conquest in the constructive sense, and carries great courage and reach.",
    ("The Scale Of Basic Purposes", 3): "The book places Winner at Level III: a person seeking wealth, excellence, and success, able to play a larger social or cultural game without the higher universal reach of a Leader.",
    ("The Scale Of Basic Purposes", 4): "The book places Normal at Level IV: the average citizen who values conformity, teamwork, safety, and a stable ordinary life without making waves.",
    ("The Scale Of Basic Purposes", 5): "The book places Loser at Level V: a self-defeating pattern organized around suffering, guilt, and frustration of help even when help is offered.",
    ("The Scale Of Basic Purposes", 6): "The book places Criminal at Level VI: a pleasure-seeking, self-first pattern with little conscience or fair exchange, controlled mainly by consequences.",
    ("The Scale Of Basic Purposes", 7): "The book places Subversive at Level VII: a destructive, fear-driven pattern whose basic purpose is to undermine or destroy rather than merely get personal benefit.",
    ("The Scale Of Belief", 1): "Complete faith or belief: the person approaches the area with full trust and a strong sense of control or possibility.",
    ("The Scale Of Belief", 2): "Great faith or confidence: the person expects success and speaks from belief rather than doubt.",
    ("The Scale Of Belief", 3): "Much faith or ingenuousness: the person tends to believe readily, sometimes with more trust than discrimination.",
    ("The Scale Of Belief", 4): "Impartial neutrality: the person tries to stay unbiased and neither believes nor disbelieves strongly.",
    ("The Scale Of Belief", 5): "Little faith or skepticism: the person doubts, questions, and withholds belief unless convinced.",
    ("The Scale Of Belief", 6): "Very little faith or cynicism: the person expects bad motives, failure, or disappointment and interprets the area through distrust.",
    ("The Scale Of Belief", 7): "No faith or disbelief: the person has lost trust in the area and treats success, goodness, or possibility as unavailable.",
    ("The Scale Of Relationships", 1): "Unity or duplication: the relationship is experienced as near-complete understanding and responsibility, with almost no felt distance.",
    ("The Scale Of Relationships", 2): "Harmony or love: the relationship has warmth, closeness, and constructive responsibility while still preserving healthy distance.",
    ("The Scale Of Relationships", 3): "Friendship or liking: the relationship is positive, friendly, and cooperative, though not as intimate or responsible as harmony.",
    ("The Scale Of Relationships", 4): "Association or neutrality: the relationship is workable but neutral, more like coexistence or ordinary association than affection.",
    ("The Scale Of Relationships", 5): "Disassociation or dislike: the person pulls away, avoids, or dislikes the other party.",
    ("The Scale Of Relationships", 6): "Enmity or hatred: the relationship has active opposition, hostility, or enemy-like framing.",
    ("The Scale Of Relationships", 7): "Obsession or fixation: the person is trapped in a compulsive fixation that can imitate closeness while actually showing no healthy distance.",
    ("The Scale Of Management", 1): "Establishment or creation: the work is at the founding/creating level, setting up the organization, project, or system itself.",
    ("The Scale Of Management", 2): "Interaction or communication: the work centers on coordinating people and information so the system can function.",
    ("The Scale Of Management", 3): "Promotion or sales: the work centers on making the product, service, or organization known and wanted.",
    ("The Scale Of Management", 4): "Finance or accounting: the work centers on money, accounting, viability, and exchange flows.",
    ("The Scale Of Management", 5): "Production or manufacturing: the work centers on producing the thing itself reliably.",
    ("The Scale Of Management", 6): "Refinement or correction: the work centers on quality control, correction, and improving what is already being produced.",
    ("The Scale Of Management", 7): "Marketing or exporting: the work centers on getting the product outward to its market or audience.",
}

NOISY_STARTS = (
    "n all relevant scales",
    "or ii, as",
    "you do not open your own franchise",
    "you try to telephone",
    "you show up to apply",
    "when you run into difficulties",
    "even though you create",
    "ignoring levels",
    "goes up to level i",
)

SCALE_QUESTION_OVERRIDES = {
    "The Scale Of Basic Purposes": "What seems to be your underlying purpose or operating motive in this area?",
    "The Scale Of Personal Influence": "How do you most often influence people in this area?",
    "The Scale Of Choice": "How do you usually experience choice and decision-making in this area?",
    "The Scale Of Belief": "How much faith, confidence, or doubt do you usually have in this area?",
    "The Scale Of Relationships": "What is the actual quality of this relationship or connection right now?",
    "The Scale Of Management": "Which management function best describes what this area needs from you right now?",
    "The Scale Of Physical Fitness": "Which description best matches your present physical condition?",
}


def clean_text(value: Any) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    text = text.replace("(she", "(s)he").replace("(She", "(S)he")
    return text


def is_noisy_description(text: str) -> bool:
    low = text.lower().strip()
    if not low:
        return True
    if low[0] in ".,;:)]}":
        return True
    if any(low.startswith(prefix) for prefix in NOISY_STARTS):
        return True
    if len(text) < 24:
        return True
    if re.search(r"\bLevels?\s+[IVX]+", text[:120]) and "," not in text[:80]:
        return True
    return False


def clamp_sentence(text: str, limit: int = 440) -> str:
    text = clean_text(text)
    if len(text) <= limit:
        if text and text[-1] not in ".!?":
            return text.rstrip(" ,;:") + "..."
        return text
    cut = text[:limit]
    sentence_end = max(cut.rfind(". "), cut.rfind("; "), cut.rfind(", "))
    if sentence_end > 180:
        return cut[: sentence_end + 1].strip()
    return cut.rstrip(" ,;") + "..."


def label_terms(label: str) -> list[str]:
    cleaned = re.sub(r"\bLevel\s+\d+\b", "", label, flags=re.I)
    pieces = re.split(r"[()/,+-]+", cleaned)
    terms = []
    for piece in pieces:
        term = clean_text(piece).strip(" -")
        if not term or term.upper() in {"I", "II", "III", "IV", "V", "VI", "VII"}:
            continue
        if len(term) <= 1:
            continue
        terms.append(term)
    return terms[:4]


def build_glossary_map(glossary: list[dict[str, Any]]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for item in glossary:
        term = clean_text(item.get("term"))
        definition = clean_text(item.get("definition"))
        if term and definition:
            lookup[term.lower()] = definition
    return lookup


def definitions_for_label(label: str, glossary_lookup: dict[str, str]) -> list[str]:
    definitions = []
    seen = set()
    for term in label_terms(label):
        key = term.lower()
        definition = glossary_lookup.get(key)
        if not definition:
            # Try singular/simple first token for noisy OCR glossary matches.
            definition = glossary_lookup.get(key.split()[0])
        if definition and key not in seen:
            definitions.append(f"{term}: {clamp_sentence(definition, 180)}")
            seen.add(key)
    return definitions[:2]


def area_name(scale_name: str) -> str:
    return re.sub(r"^The Scale Of\s+", "", scale_name, flags=re.I).strip().lower()


def build_question(scale_name: str) -> str:
    if scale_name in SCALE_QUESTION_OVERRIDES:
        return SCALE_QUESTION_OVERRIDES[scale_name]
    return f"Which Level {ROMAN_BY_NUMBER.get(1, 'I')} to {ROMAN_BY_NUMBER.get(7, 'VII')} statement best describes your current pattern for {area_name(scale_name)}?"


def build_guideline(scale_name: str, level: dict[str, Any], glossary_lookup: dict[str, str]) -> tuple[str, str]:
    number = int(level.get("number", 0) or 0)
    label = clean_text(level.get("label")) or f"Level {number}"
    fixed_desc = DESCRIPTION_FIXES.get((scale_name, number), "")
    existing = clean_text(level.get("description"))

    if fixed_desc:
        return f"Choose this if Level {ROMAN_BY_NUMBER.get(number, number)} ({label}) sounds closest: {fixed_desc}", "book-table-guideline"

    if existing and not is_noisy_description(existing):
        return f"Choose this if Level {ROMAN_BY_NUMBER.get(number, number)} ({label}) sounds closest. Book guidance: {clamp_sentence(existing)}", "book-description"

    definitions = definitions_for_label(label, glossary_lookup)
    roman = ROMAN_BY_NUMBER.get(number, str(number))
    base = f"Choose this if your current pattern for {area_name(scale_name)} is closest to Level {roman}: {label}."
    if definitions:
        base += " Key term guidance: " + " ".join(definitions)
    else:
        base += " Use the label as the guide and pick it only if it fits better than the neighboring levels."
    return base, "label-glossary-guideline"


def enrich(data: dict[str, Any]) -> dict[str, Any]:
    scales = data.get("scales") if isinstance(data.get("scales"), list) else []
    for scale in scales:
        scale_name = clean_text(scale.get("name"))
        scale["assessmentQuestion"] = build_question(scale_name)
        glossary_lookup = build_glossary_map(scale.get("glossary") or [])
        for level in scale.get("levels") or []:
            number = int(level.get("number", 0) or 0)
            fixed_label = LABEL_FIXES.get((scale_name, number))
            if fixed_label and (clean_text(level.get("label")).lower().startswith("level ") or scale_name in {"The Scale Of Basic Purposes", "The Scale Of Belief", "The Scale Of Relationships", "The Scale Of Management"}):
                level.setdefault("sourceLabel", level.get("label", ""))
                level["label"] = fixed_label

            guideline, source = build_guideline(scale_name, level, glossary_lookup)
            level["assessmentGuideline"] = guideline
            level["assessmentSource"] = source

    data["assessmentMeta"] = {
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "note": "Assessment guidelines are derived from OCR book descriptions when available, otherwise from level labels and glossary terms for review/correction.",
    }
    return data


def main() -> None:
    data = json.loads(CONTENT_PATH.read_text(encoding="utf-8"))
    if not BACKUP_PATH.exists():
        shutil.copy2(CONTENT_PATH, BACKUP_PATH)
    enriched = enrich(data)
    CONTENT_PATH.write_text(json.dumps(enriched, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    EMBEDDED_PATH.write_text(
        "window.SEPTEMICS_CONTENT = " + json.dumps(enriched, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    total = sum(len(scale.get("levels") or []) for scale in enriched.get("scales") or [])
    missing = sum(
        1
        for scale in enriched.get("scales") or []
        for level in scale.get("levels") or []
        if not clean_text(level.get("assessmentGuideline"))
    )
    print(f"Enriched {len(enriched.get('scales') or [])} scales / {total} levels")
    print(f"Missing guidelines: {missing}")
    print(f"Wrote {CONTENT_PATH.name} and {EMBEDDED_PATH.name}")


if __name__ == "__main__":
    main()
