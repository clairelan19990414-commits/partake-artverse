"""
Generate a clean hand-curation list of artists who need image fixes:
  - Missing portrait (still showing initial-letter placeholder)
  - < 3 work images (sparse grid)
  - Portrait from suspicious source (external link og:image where the
    URL filename looks like a generic site hero rather than a person photo)

Outputs MANUAL_IMAGES_QUEUE.md
"""

import json, re
from pathlib import Path

HERE = Path(__file__).parent

# Sources that are HIGH-confidence portrait (not flagged)
GOOD_SOURCES = ['Wikipedia:', 'Wikipedia body:', 'Commons depicts', 'Wikidata P18']

# Sources that are LOWER-confidence (might be artwork or generic image)
SUSPICIOUS_HINTS = [
    'External link og:image',  # often a generic site hero
    'hero (may be work)',      # gallery hero — could be artwork
    'caption-match',           # caption match — usually reliable but worth flagging
]


def load_facts_meta():
    text = (HERE / 'quiz_facts.js').read_text()
    out = {}
    pattern = re.compile(r"^  (a\d+):\s*\{\s*//\s*(.+?)$"
                         r"(.*?)^  \},", re.MULTILINE | re.DOTALL)
    for m in pattern.finditer(text):
        aid = m.group(1)
        name_raw = m.group(2).strip()
        name = name_raw.split(' — LOW-CONTEXT')[0]
        low_context = '— LOW-CONTEXT' in name_raw
        block = m.group(3)
        gallery = re.search(r"// Gallery: ([^\n]+)", block)  # may not exist
        based = re.search(r"based:\s*'([^']*)'", block)
        out[aid] = {
            'name': name,
            'low_context': low_context,
            'based': based.group(1) if based else '',
        }
    return out


def main():
    facts = load_facts_meta()
    portraits = json.loads((HERE / 'quiz_portraits.json').read_text())
    images = json.loads((HERE / 'quiz_images.json').read_text())
    artists = json.loads(open('/tmp/artists_full.json').read())
    gallery_by_id = {a['id']: a.get('gallery', '') for a in artists}
    GALLERY_NAMES = {
        'g1': 'Gagosian', 'g2': 'Hauser & Wirth', 'g3': 'David Zwirner',
        'g4': 'Pace Gallery', 'g5': 'White Cube', 'g6': 'Marian Goodman',
        'g7': 'Sprüth Magers', 'g8': 'Lisson Gallery', 'g9': 'Thaddaeus Ropac',
        'g10': 'Galerie Perrotin', 'g11': 'Galleria Continua',
        'g12': 'Massimo De Carlo', 'g13': 'Sadie Coles HQ',
    }

    rows = []
    for aid, info in facts.items():
        p = portraits.get(aid, {})
        portrait_url = p.get('url', '')
        portrait_src = p.get('source', '')
        works = images.get(aid, {}).get('candidates', [])
        works_count = len(works)
        gallery = GALLERY_NAMES.get(gallery_by_id.get(aid, ''), '?')

        # Classify portrait
        if not portrait_url:
            portrait_status = 'MISSING'
        elif any(s in portrait_src for s in GOOD_SOURCES):
            portrait_status = 'good'
        elif any(s in portrait_src for s in SUSPICIOUS_HINTS):
            portrait_status = 'suspicious'
        else:
            portrait_status = 'ok'

        # Skip if everything is fine
        needs_attention = (portrait_status in ('MISSING', 'suspicious')
                          or works_count < 3)
        if not needs_attention:
            continue

        rows.append({
            'aid': aid,
            'name': info['name'],
            'gallery': gallery,
            'based': info['based'],
            'low_context': info['low_context'],
            'portrait_status': portrait_status,
            'portrait_src': portrait_src,
            'portrait_url': portrait_url,
            'works_count': works_count,
        })

    # Sort: missing portrait first, then suspicious, then thin works
    sort_key = lambda r: (
        0 if r['portrait_status'] == 'MISSING' else (1 if r['portrait_status'] == 'suspicious' else 2),
        -1 if r['low_context'] else 0,
        r['works_count'],
        r['name'].lower(),
    )
    rows.sort(key=sort_key)

    # Build markdown
    out_lines = [
        '# Manual image curation queue',
        '',
        f'**{len(rows)} artists** need at least one of: portrait, additional works, or a portrait swap (current portrait is suspicious — usually a generic site hero, not the person).',
        '',
        'Use the artist\'s **own website**, **gallery bio page**, or **Instagram** to source. For each row, drop the image URL into a CSV or directly into `quiz_portraits.json` keyed by ID.',
        '',
        '## Categories',
        '',
        '| Status | Meaning |',
        '|--------|---------|',
        '| **MISSING** | No portrait at all — card shows initial-letter placeholder |',
        '| **suspicious** | Portrait URL exists but came from an external-link og:image that may be a generic site hero rather than the person (e.g., Sarah Lawrence homepage slideshow for Tishan Hsu) |',
        '| **thin works** | Fewer than 3 work images in the works grid |',
        '',
    ]

    # Category 1: Missing portrait
    missing = [r for r in rows if r['portrait_status'] == 'MISSING']
    out_lines += [
        f'## A. Missing portrait — {len(missing)} artists',
        '',
        'These show only an initial-letter circle on the card. Priority for hand-curation.',
        '',
        '| ID | Name | Gallery | Based | Works | LOW-CONTEXT |',
        '|----|------|---------|-------|------:|-------------|',
    ]
    for r in missing:
        out_lines.append(
            f"| {r['aid']} | **{r['name']}** | {r['gallery']} | {r['based'][:30]} | {r['works_count']} | {'⚠️' if r['low_context'] else ''} |"
        )
    out_lines.append('')

    # Category 2: Suspicious portrait
    suspicious = [r for r in rows if r['portrait_status'] == 'suspicious']
    out_lines += [
        f'## B. Suspicious portrait — {len(suspicious)} artists',
        '',
        'These have a portrait URL but it came from a site\'s og:image — may be a generic site hero, not the person. Verify each on the card and swap if wrong.',
        '',
        '| ID | Name | Current portrait source | Works |',
        '|----|------|-------------------------|------:|',
    ]
    for r in suspicious:
        src = r['portrait_src'][:70]
        out_lines.append(
            f"| {r['aid']} | **{r['name']}** | {src} | {r['works_count']} |"
        )
    out_lines.append('')

    # Category 3: Thin works (portrait OK, but < 3 works)
    thin_works = [r for r in rows if r['portrait_status'] not in ('MISSING', 'suspicious')]
    out_lines += [
        f'## C. Thin works only — {len(thin_works)} artists',
        '',
        'Portrait is fine, but the works grid has fewer than 3 images. Add more from gallery exhibition pages or museum collection records.',
        '',
        '| ID | Name | Gallery | Works |',
        '|----|------|---------|------:|',
    ]
    for r in thin_works:
        out_lines.append(
            f"| {r['aid']} | **{r['name']}** | {r['gallery']} | {r['works_count']} |"
        )
    out_lines.append('')

    out_lines += [
        '## How to update',
        '',
        "1. **For a new portrait**: open `quiz_portraits.json`, find the artist's ID, set `url` to the new image URL and `source` to a brief description (e.g., `\"artist's website\"`).",
        "2. **For a wrong portrait to remove**: delete the entire entry for that ID from `quiz_portraits.json`.",
        "3. **For new works**: open `quiz_images.json`, find the artist's ID, and append to `candidates` array with `{source, title, year, image, credit, url}`.",
        '4. Commit and push — Vercel rebuilds automatically.',
        '',
    ]

    (HERE / 'MANUAL_IMAGES_QUEUE.md').write_text('\n'.join(out_lines))
    print(f'Wrote MANUAL_IMAGES_QUEUE.md')
    print(f'  Missing portrait:    {len(missing)}')
    print(f'  Suspicious portrait: {len(suspicious)}')
    print(f'  Thin works only:     {len(thin_works)}')
    print(f'  Total to review:     {len(rows)}')


if __name__ == '__main__':
    main()
