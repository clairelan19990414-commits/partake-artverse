# Partake quiz pool — final quality report

## Where we ended

| Dimension | Coverage | Notes |
|-----------|----------|-------|
| Total artists | **857** | Full scrape from 13 blue-chip galleries, red-chip excluded from quiz pool |
| Portraits (verified) | **521 / 857 (61%)** | Wikipedia infobox + body image + Wikidata P18 |
| Works ≥ 1 image | **691 / 857 (81%)** | Gallery scrape + Art Institute of Chicago + Wikipedia article body |
| Works ≥ 3 images | **592 / 857 (69%)** | |
| Working Wikipedia extract | **731 / 857 (85%)** | Card UI fetches live extract using this slug |
| **Complete on every dimension** | **398 / 857 (46%)** | Portrait + ≥3 works + Wikipedia + complete facts + not LOW-CONTEXT |

## Tiers (after all passes)

| Tier | Description | Count |
|------|-------------|-------|
| A | LOW-CONTEXT — thin source, no Wikipedia coverage | 15 |
| B | Required fact field empty | 0 |
| C | Missing portrait | 323 |
| D | < 3 work images | 116 |
| E | No working Wikipedia extract | 5 |
| F | **Complete on every dimension** | **398** |

## Passes that ran

1. **`complete_pass.py`** — Wikipedia portrait by exact slug (not name-guess) + Wikidata P18 fallback. +260 portraits.
2. **`verify_pass.py`** — Wikipedia extract for all 857; flagged 221 issues (200 broken slugs, 13 disambiguation, 8 year mismatches — most were regex false positives).
3. **`slug_fix.py` + `slug_validate.py` + `slug_recheck.py`** — Fixed 105 broken slugs via variant trial + opensearch; validated against name match; reverted 21 false matches (e.g., `Yu_Nishimura → Yukie_Nishimura`).
4. **`wiki_works_pass.py`** — Scraped Wikipedia article HTML for body images (filtering UI chrome). +186 work candidates across 85 artists.
5. **`portrait_pass2.py`** — Article-body images whose filename/alt contains the artist's surname or "portrait". +50 portraits.
6. **`portrait_pass3.py`** (rolled back) — Commons direct file search. Yielded 155 candidates but ~30% were false positives (same-name-different-person, historical objects, etc.) that the validator couldn't distinguish reliably. Reverted to avoid showing wrong faces.

## Cleaning during the pass

- 3 wrong slugs cleared (`William Monk`, `Tony Lewis`, `Zhuang Hui` — Wikipedia matched a different person of the same name).
- 8 LOW-CONTEXT flags lifted (Wikipedia extracts now confirm identity for those artists).
- 1 bad Wikidata P18 match cleared (`Yu Nishimura` → `Yukie Nishimura` was a pianist, not the painter).

## What remains for hand-review

- **15 LOW-CONTEXT entries** (`quiz_facts.js` flagged) — thin source data and no Wikipedia article. Manual research needed (gallery's own bio, artist's website).
- **323 artists without portraits** — Wikipedia exhausted. Further coverage would require:
  - Per-gallery HTML reverse-engineering (each gallery uses different structure)
  - Paid image APIs (Artsy commercial)
  - Bing/Google Image Search (rate-limited, scraping-fragile)
- **116 artists with < 3 work images** — same constraint as portraits.
- **`wiki_discrepancies.md`** — 8 birth-year mismatches; spot-checked, most are regex false positives where the script picked up exhibition years from extracts.

## Files added this session

- `complete_pass.py`, `verify_pass.py`, `wiki_works_pass.py`, `slug_fix.py`, `slug_validate.py`, `slug_recheck.py`, `portrait_pass2.py`, `portrait_pass3.py`, `portrait_validate.py`, `quality_audit.py`
- `wiki_extracts.json` (857 × Wikipedia extracts cached)
- `wiki_discrepancies.md`, `quality_audit.md` (review queues)
