# Septemics Vocabulary Handoff

## Best Files To Give Claude
- `claude_handoff/septemics_claude_packet_clean.json`
- `claude_handoff/septemics_vocabulary_clean.csv`
- `claude_handoff/septemics_vocabulary_clean.txt`
- `claude_handoff/septemics_rejected_terms.csv`
- `septemics_full_book_raw_ocr.txt` (fallback raw corpus)

## Quality Summary
- Scales: **35**
- Clean unique terms: **393**
- Rejected noisy terms: **2**

## Notes
- Clean CSV is the primary input for vocabulary normalization.
- Rejected terms CSV helps manual review of OCR artifacts.
- Full packet JSON includes both scale structure and clean vocabulary.
