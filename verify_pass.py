"""
Wikipedia verification pass.

For each artist in quiz_facts.js:
  - Fetch the Wikipedia REST summary using the wiki slug.
  - Extract: extract text, birth year, description.
  - Compare to my facts entry's `born` field; flag year mismatches.
  - Flag any slug that 404s or hits disambiguation.

Outputs:
  - wiki_extracts.json: { aid: {extract, description, slug_ok} }
  - wiki_discrepancies.md: markdown report of flagged entries for hand-review
"""

import json, ssl, urllib.parse, urllib.request, re, time
from pathlib import Path
try:
    import certifi
    _CTX = ssl.create_default_context(cafile=certifi.where())
except Exception:
    _CTX = ssl.create_default_context()

HERE = Path(__file__).parent
FACTS_JS = HERE / 'quiz_facts.js'
OUT_EXTRACTS = HERE / 'wiki_extracts.json'
OUT_REPORT = HERE / 'wiki_discrepancies.md'

WIKI_UA = 'PartakeQuiz/1.0 (https://partake-artverse.vercel.app; clairelan19990414@gmail.com)'


def get_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': WIKI_UA, 'Accept': 'application/json'})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=20, context=_CTX).read())
    except Exception:
        return None


def extract_facts():
    text = FACTS_JS.read_text()
    out = {}
    pattern = re.compile(
        r"^  (a\d+):\s*\{\s*//\s*(.+?)$"
        r"(.*?)"
        r"^  \},",
        re.MULTILINE | re.DOTALL,
    )
    for m in pattern.finditer(text):
        aid = m.group(1)
        name = m.group(2).strip()
        block = m.group(3)
        born = re.search(r"born:\s*'([^']*)'", block)
        wiki = re.search(r"wiki:\s*'([^']*)'", block)
        out[aid] = {
            'name': name,
            'born': born.group(1) if born else '',
            'wiki_slug': wiki.group(1) if wiki else None,
        }
    return out


def fetch_summary(slug):
    if not slug:
        return None
    safe = urllib.parse.quote(slug)
    d = get_json(f'https://en.wikipedia.org/api/rest_v1/page/summary/{safe}')
    if not d:
        return {'status': 'fetch_error'}
    if d.get('type') == 'disambiguation':
        return {'status': 'disambiguation'}
    if d.get('type') == 'no-extract' or 'extract' not in d:
        return {'status': 'no_extract'}
    return {
        'status': 'ok',
        'extract': d.get('extract', ''),
        'description': d.get('description', ''),
        'title': d.get('title', ''),
    }


def parse_my_birth_year(born_field):
    """Pull a 4-digit year from my 'born' field text."""
    m = re.search(r'\b(1[6-9]\d{2}|20[0-2]\d)\b', born_field)
    return int(m.group(1)) if m else None


def parse_wiki_birth_year(extract):
    """Pull birth year from the Wikipedia extract."""
    # Common patterns: "born March 5, 1962", "(born 1962)", "(1923-1971)"
    patterns = [
        r'born[^.,]{0,30}?\b(1[6-9]\d{2}|20[0-2]\d)\b',
        r'\(born[^)]*?(1[6-9]\d{2}|20[0-2]\d)\)',
        r'\((1[6-9]\d{2}|20[0-2]\d)[\s–—-]',  # (1923–1971)
        r'\b(1[6-9]\d{2}|20[0-2]\d)–(1[6-9]\d{2}|20[0-2]\d)\b',  # 1923–1971
    ]
    for p in patterns:
        m = re.search(p, extract, re.IGNORECASE)
        if m:
            return int(m.group(1))
    return None


def main():
    facts = extract_facts()
    extracts = {}
    issues = []

    for i, (aid, info) in enumerate(facts.items(), 1):
        if i % 50 == 0:
            print(f'  ...{i}/{len(facts)}')
        result = fetch_summary(info['wiki_slug'])
        if not result:
            issues.append({
                'aid': aid, 'name': info['name'], 'kind': 'no_slug',
                'detail': 'no wiki slug in facts',
            })
            extracts[aid] = {'status': 'no_slug', 'slug': info['wiki_slug']}
            continue
        if result['status'] != 'ok':
            issues.append({
                'aid': aid, 'name': info['name'], 'kind': result['status'],
                'detail': f"slug: {info['wiki_slug']}",
            })
            extracts[aid] = {'status': result['status'], 'slug': info['wiki_slug']}
            time.sleep(0.05)
            continue

        # OK status — store and verify year
        extracts[aid] = {
            'status': 'ok',
            'slug': info['wiki_slug'],
            'title': result['title'],
            'description': result['description'],
            'extract': result['extract'],
        }
        my_year = parse_my_birth_year(info['born'])
        wiki_year = parse_wiki_birth_year(result['extract'])
        if my_year and wiki_year and my_year != wiki_year:
            issues.append({
                'aid': aid, 'name': info['name'], 'kind': 'year_mismatch',
                'detail': f"my facts say {my_year}, Wikipedia says {wiki_year}",
            })
        time.sleep(0.05)

    OUT_EXTRACTS.write_text(json.dumps(extracts, indent=2, ensure_ascii=False))

    # Build report
    lines = [
        '# Wikipedia verification report',
        '',
        f'Verified {len(facts)} artists. Found **{len(issues)}** issues to review.',
        '',
    ]

    by_kind = {}
    for issue in issues:
        by_kind.setdefault(issue['kind'], []).append(issue)

    for kind, label in [
        ('year_mismatch', 'Birth-year mismatches (my facts vs Wikipedia)'),
        ('disambiguation', 'Slug resolves to a disambiguation page (wrong slug)'),
        ('fetch_error', 'Wikipedia fetch failed (slug may not exist)'),
        ('no_extract', 'Wikipedia page has no extract'),
        ('no_slug', 'No wiki slug in facts entry'),
    ]:
        items = by_kind.get(kind, [])
        if not items:
            continue
        lines.append(f'## {label} ({len(items)})')
        lines.append('')
        lines.append('| ID | Name | Detail |')
        lines.append('|----|------|--------|')
        items.sort(key=lambda x: x['name'].lower())
        for it in items:
            lines.append(f"| {it['aid']} | {it['name']} | {it['detail']} |")
        lines.append('')

    OUT_REPORT.write_text('\n'.join(lines))

    print()
    print(f'Wrote {OUT_EXTRACTS} ({len(extracts)} entries)')
    print(f'Wrote {OUT_REPORT} ({len(issues)} issues)')
    print()
    for kind, items in by_kind.items():
        print(f'  {kind}: {len(items)}')


if __name__ == '__main__':
    main()
