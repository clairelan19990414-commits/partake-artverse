# Prompt for Claude (Vocabulary First)

Use the attached files to build a high-quality Septemics vocabulary artifact.

Files:
- `septemics_claude_packet_clean.json`
- `septemics_vocabulary_clean.csv`
- `septemics_vocabulary_clean.txt`
- `septemics_rejected_terms.csv`
- `septemics_full_book_raw_ocr.txt` (fallback OCR corpus)

Requirements:
- Produce a canonical vocabulary table with columns: term, canonical_definition, alternate_definitions, source_scales, confidence, notes.
- Normalize OCR noise (hyphenation, punctuation artifacts, case inconsistencies).
- Preserve provenance to source scales.
- Return both JSON and Markdown outputs.
- Include a concise "needs human review" list for ambiguous entries.
