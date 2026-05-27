# Partake quiz pool — final quality report

## Where we are

| Dimension | Coverage | Notes |
|-----------|----------|-------|
| Total artists | **857** | Full roster from 13 blue-chip galleries |
| Quiz-eligible (non-red-chip) | **761** | Red-chip artists excluded from quiz pool |
| Portraits | **595 / 857 (69%)** | Wikipedia + Wikidata + Commons depicts + gallery hero |
| Works ≥ 1 image | **708 / 857 (83%)** | Gallery scrape + AIC + Wikipedia body + gallery hero |
| Works ≥ 3 images | **629 / 857 (73%)** | |
| Working Wikipedia extract | **731 / 857 (85%)** | Card UI fetches live extract using this slug |
| Message ≥ 600 chars | **725 / 857 (85%)** | Substantive 3-sentence drafts |
| Message ≥ 900 chars | **261 / 857 (30%)** | Comparable to richest of original 50 |
| **Tier F (complete on every dimension)** | **468 / 857 (55%)** | Portrait + ≥3 works + Wikipedia + complete facts + not LOW-CONTEXT |

## The remaining gap

| Tier | What it means | Count |
|------|---------------|-------|
| A | LOW-CONTEXT — thin source, no Wikipedia coverage | 15 |
| B | Required fact field empty | 0 |
| C | Missing portrait | 250 |
| D | < 3 work images | 103 |
| E | No working Wikipedia extract | 21 |
| F | Complete on every dimension | **468** |

### Why portraits topped out at 69%

| Source tried | Result |
|---|---|
| Wikipedia REST summary (by slug) | 471 hits |
| Wikidata P18 (image property) fallback | 1 valid hit (false-positive Yu/Yukie Nishimura cleared) |
| Wikipedia article-body images by surname filename | +50 |
| Commons P180 (depicts) structured search | +10 (high confidence) |
| Wikipedia figure-caption full-name match | +5 |
| Gallery og:image (7 scrapable galleries) | +57 (after artwork-filter) |
| DDG search → page scrape with full-name validation | +2 |
| Commons direct file search by surname | **reverted** (~30% false positives — Charles Gaines the football player ≠ the artist) |

**Hard blockers for the remaining 250:**
- ~187 artists are at SPA-only galleries (David Zwirner, Hauser & Wirth, Marian Goodman, Thaddaeus Ropac, Galerie Perrotin, Galleria Continua) whose pages are JS-rendered with no extractable HTML
- ~50 artists have no Wikipedia article or one without an infobox photo
- Remaining gap = same-name-different-person ambiguity that filename/alt validation alone can't resolve

**To close further would require:**
- Headless browser (Playwright/Puppeteer) for SPA galleries → +80-150 portraits
- Paid image-search API (Google CSE, Bing, SerpAPI) → +50-100
- Hand-curation for the LOW-CONTEXT and SPA-gallery remainders

### Why works coverage caps at 73% / quality varies

- Gallery scrape provided ~221 new work-images but they come without titles → labeled "Untitled"
- **74% of all 3,282 work-images are titled "Untitled"** because gallery CDN paths don't expose titles
- **Only 186 artists (22%) have all-named works** like the hand-curated original 50
- Museum-API works pass (Met, Cleveland) returned 0 hits — contemporary international artists aren't in those collections
- AIC was already exhausted in the original 17 batch cycles

**To close further would require:** per-gallery custom HTML parsers to extract artwork titles from artist-page captions, OR Artsy commercial API.

### Messages: distribution

- **261 (30%)** are 900+ chars — comparable to the richest of the original 50
- **464 (54%)** are 600–900 chars — substantive, slightly more compressed
- **132 (15%)** are 300–600 chars — adequate but on the thin side
- **0** are below 345 chars

Lowest 25 are tracked in `message_audit.md` with their Wikipedia extract availability for hand-rewrite reference. Spot-checked — the short ones still hit all three beats (whereabouts / lineage / thesis), they're just compact.

## Hand-review queues

| File | What's in it |
|------|--------------|
| `quality_audit.md` | All 389 non-Tier-F artists grouped by which gap they have |
| `message_audit.md` | Bottom 60 messages by length + Wikipedia extract length to reference |
| `wiki_discrepancies.md` | 221 Wikipedia verification flags (mostly false-positive year-regex hits, sift for real issues) |
| `FINAL_QUALITY_REPORT.md` | This file |

## What changed this session

| Pass | What it did | Yield |
|------|-------------|-------|
| `complete_pass.py` | Wikipedia portrait by exact slug + Wikidata P18 | +260 portraits |
| `verify_pass.py` | Cached Wikipedia extracts for all 857 | 731 valid |
| `slug_fix.py` + `slug_validate.py` + `slug_recheck.py` | Variant-trial + opensearch + name validation | +105 slugs (21 false matches reverted) |
| `wiki_works_pass.py` | Wikipedia article-body image scrape | +186 works across 85 artists |
| `portrait_pass2.py` | Article-body images with surname/portrait keyword | +50 portraits |
| `portrait_pass3.py` | Commons file search (rolled back — false positives) | 155 candidates, all reverted |
| `portrait_pass4_depicts.py` | Commons P180 structured search | +10 high-confidence |
| `portrait_pass5_caption.py` | Wikipedia figure caption full-name match | +5 |
| `gallery_scrape.py` | og:image + CDN works across 7 scrapable galleries | +221 works across 37 artists |
| `portrait_pass6_gallery_hero.py` + `portrait_filter_heroes.py` | Gallery hero as portrait + artwork filter | +57 net portraits |
| `portrait_pass7_ddg.py` | DDG search → page scrape | +2 |
| `quality_audit.py` + `message_audit.py` | Tiered review queues | Reports for hand-review |

## Summary line

From 50 user-approved + ~700 placeholder-bio drafts at session start → **468 artists fully complete on every dimension** (55% of total, 61% of quiz-eligible). The remaining 389 fall into specific gaps with known closing strategies that all require either paid APIs, a headless browser, or your hand-curation.
