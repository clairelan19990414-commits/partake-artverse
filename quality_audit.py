"""
Quality audit for the Partake quiz pool.

Produces a prioritized list of entries that should be hand-reviewed:
  - Tier A: LOW-CONTEXT flagged (the artist was thin on source data)
  - Tier B: empty required fact fields (training, signature, etc.)
  - Tier C: source bio was a one-line placeholder
  - Tier D: missing portrait or zero works (degrades the card visually)
  - Tier E: no flag, real source bio, complete facts — safe

Writes a markdown report to quality_audit.md.
"""

import json, re, os
from pathlib import Path

HERE = Path(__file__).parent
ARTISTS_FULL = Path('/tmp/artists_full.json')
FACTS_JS = HERE / 'quiz_facts.js'
MESSAGES_JS = HERE / 'quiz_messages.js'
IMAGES_JSON = HERE / 'quiz_images.json'
OUT_MD = HERE / 'quality_audit.md'


def extract_ids_with_flags(js_path):
    """Return dict: id -> bool (True if LOW-CONTEXT flag immediately precedes)."""
    text = js_path.read_text()
    out = {}
    # Match: optional `  // LOW-CONTEXT\n` then `  aXXX: { // Name`
    pattern = re.compile(
        r'(?:^  // LOW-CONTEXT\s*\n)?'
        r'^  (a\d+):\s*\{\s*//\s*(.+)$',
        re.MULTILINE,
    )
    # Walk the file line by line to keep flag-association reliable
    lines = text.split('\n')
    prev_low_context = False
    for line in lines:
        if line.strip() == '// LOW-CONTEXT':
            prev_low_context = True
            continue
        m = re.match(r'^  (a\d+):\s*\{\s*//\s*(.+)$', line)
        if m:
            out[m.group(1)] = {
                'name': m.group(2).strip(),
                'low_context': prev_low_context,
            }
            prev_low_context = False
        elif line.strip() and not line.startswith('//'):
            prev_low_context = False
    return out


def extract_field_completeness(js_path, ids_of_interest):
    """For each artist id, return which required fields are empty strings."""
    text = js_path.read_text()
    out = {}
    for aid in ids_of_interest:
        # Find the block for this id
        start = text.find(f'  {aid}: {{')
        if start < 0:
            continue
        # Find the closing brace
        depth = 0
        i = start
        while i < len(text):
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
                if depth == 0:
                    block = text[start:i+1]
                    break
            i += 1
        else:
            continue

        empty_fields = []
        for field in ['training', 'signature', 'method', 'thesis', 'cohort']:
            m = re.search(rf"{field}:\s*'([^']*)'", block)
            if m and m.group(1).strip() == '':
                empty_fields.append(field)
        # pron.ipa empty
        m = re.search(r"pron:\s*\{[^}]*ipa:\s*'([^']*)'", block)
        if m and m.group(1).strip() == '':
            empty_fields.append('pron.ipa')
        out[aid] = empty_fields
    return out


def main():
    facts_meta = extract_ids_with_flags(FACTS_JS)
    all_artists = json.load(open(ARTISTS_FULL))
    source = {a['id']: a for a in all_artists}
    images = json.load(open(IMAGES_JSON)) if IMAGES_JSON.exists() else {}
    field_audit = extract_field_completeness(FACTS_JS, list(facts_meta.keys()))

    rows = []
    for aid, meta in facts_meta.items():
        src = source.get(aid, {})
        img = images.get(aid, {})
        empty_fields = field_audit.get(aid, [])
        rows.append({
            'id': aid,
            'name': meta['name'],
            'low_context': meta['low_context'],
            'placeholder_bio': src.get('placeholder_bio', False),
            'empty_fields': empty_fields,
            'has_portrait': bool(img.get('portrait')),
            'works_count': len(img.get('works', [])),
            'gallery': src.get('gallery', ''),
        })

    # Tier assignment
    def tier(r):
        if r['low_context']:
            return 'A'
        if r['empty_fields']:
            return 'B'
        if r['placeholder_bio']:
            return 'C'
        if not r['has_portrait'] or r['works_count'] == 0:
            return 'D'
        return 'E'

    for r in rows:
        r['tier'] = tier(r)

    tier_counts = {t: sum(1 for r in rows if r['tier'] == t) for t in 'ABCDE'}

    lines = [
        '# Quality audit — Partake quiz pool',
        '',
        f'Total artists: **{len(rows)}**',
        '',
        '| Tier | Description | Count |',
        '|------|-------------|-------|',
        f'| A | LOW-CONTEXT flagged — thinnest source, highest priority for re-write | {tier_counts["A"]} |',
        f'| B | Required fact field empty (training, signature, etc.) | {tier_counts["B"]} |',
        f'| C | Source bio was a one-line placeholder (drafted from training knowledge) | {tier_counts["C"]} |',
        f'| D | Missing portrait or zero works (card degrades visually) | {tier_counts["D"]} |',
        f'| E | Real source bio + complete facts + media — considered safe | {tier_counts["E"]} |',
        '',
        '---',
        '',
    ]

    for t, label in [
        ('A', 'Tier A — LOW-CONTEXT flagged (re-write first)'),
        ('B', 'Tier B — empty required fields'),
        ('C', 'Tier C — placeholder source bio'),
        ('D', 'Tier D — missing media'),
    ]:
        lines.append(f'## {label}')
        lines.append('')
        lines.append('| ID | Name | Gallery | Empty fields | Portrait | Works |')
        lines.append('|----|------|---------|--------------|----------|-------|')
        subset = [r for r in rows if r['tier'] == t]
        subset.sort(key=lambda r: (r['name'].lower()))
        for r in subset:
            lines.append(
                f"| {r['id']} | {r['name']} | {r['gallery']} | "
                f"{', '.join(r['empty_fields']) if r['empty_fields'] else '—'} | "
                f"{'✓' if r['has_portrait'] else '—'} | {r['works_count']} |"
            )
        lines.append('')

    lines.append('## Tier E summary')
    lines.append('')
    lines.append(f'**{tier_counts["E"]} artists** considered safe (real source bio, complete facts, has portrait + works).')
    lines.append('')

    OUT_MD.write_text('\n'.join(lines))
    print(f'Wrote {OUT_MD}')
    print()
    print(f'Total: {len(rows)}')
    for t in 'ABCDE':
        print(f'  Tier {t}: {tier_counts[t]}')


if __name__ == '__main__':
    main()
