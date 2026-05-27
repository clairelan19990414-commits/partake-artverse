"""
Slug-fix pass: for every artist whose wiki slug failed verification,
try common variants and the Wikipedia opensearch endpoint to find the
correct slug. Update quiz_facts.js in place.

Strategies for each failed slug:
  1. URL-decode the slug (some are double-encoded)
  2. Try adding/removing disambiguation suffixes: '', '(artist)', '(painter)',
     '(photographer)', '(sculptor)', '(filmmaker)', '(architect)', '(artist_collective)'
  3. Use Wikipedia's opensearch to find candidates; pick the first whose summary
     description mentions an artist-relevant keyword.
"""

import json, ssl, urllib.parse, urllib.request, re, time
from pathlib import Path
try:
    import certifi
    _CTX = ssl.create_default_context(cafile=certifi.where())
except Exception:
    _CTX = ssl.create_default_context()

HERE = Path(__file__).parent
EXTRACTS = HERE / 'wiki_extracts.json'
FACTS_JS = HERE / 'quiz_facts.js'

WIKI_UA = 'PartakeQuiz/1.0 (https://partake-artverse.vercel.app; clairelan19990414@gmail.com)'

ART_KEYWORDS = re.compile(
    r'\b(artist|painter|sculptor|photographer|filmmaker|installation|'
    r'conceptual|contemporary|video artist|performance artist|architect|'
    r'designer|composer|choreographer|art collective|art duo|gallery|'
    r'art movement|art group|fashion|illustrator|printmaker|ceramic)\b',
    re.IGNORECASE,
)


def get_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': WIKI_UA, 'Accept': 'application/json'})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=20, context=_CTX).read())
    except Exception:
        return None


def fetch_summary(slug):
    if not slug:
        return None
    safe = urllib.parse.quote(slug)
    return get_json(f'https://en.wikipedia.org/api/rest_v1/page/summary/{safe}')


def is_valid_artist_summary(d, name):
    if not d:
        return False
    if d.get('type') in ('disambiguation', 'no-extract'):
        return False
    desc = d.get('description', '') or ''
    extract = d.get('extract', '') or ''
    blob = f'{desc} {extract[:400]}'
    if not ART_KEYWORDS.search(blob):
        return False
    # Sanity-check that the page title or extract mentions a word from the artist's name
    name_words = [w for w in re.findall(r'\w+', name) if len(w) > 2]
    if not name_words:
        return True
    return any(w.lower() in blob.lower() for w in name_words)


def try_variants(name, original_slug):
    """Return (new_slug, summary) or (None, None)."""
    # Strip URL-encoding to canonical (Wikipedia accepts unicode in URLs)
    decoded = urllib.parse.unquote(original_slug) if original_slug else ''

    # Base candidates
    base = decoded.split('_(')[0]  # strip existing parenthetical
    base = base.rstrip('_')

    variants_to_try = []
    if decoded != original_slug:
        variants_to_try.append(decoded)
    variants_to_try.extend([
        base,
        f'{base}_(artist)',
        f'{base}_(painter)',
        f'{base}_(photographer)',
        f'{base}_(sculptor)',
        f'{base}_(filmmaker)',
        f'{base}_(designer)',
        f'{base}_(architect)',
    ])
    # Try with hyphen-removed and with hyphen-preserved
    if '-' in base:
        variants_to_try.append(base.replace('-', '_'))

    seen = set()
    for v in variants_to_try:
        if v in seen or v == original_slug:
            continue
        seen.add(v)
        d = fetch_summary(v)
        time.sleep(0.05)
        if is_valid_artist_summary(d, name):
            return v, d

    # Fall back to Wikipedia opensearch by name
    q = urllib.parse.quote(name)
    d = get_json(
        f'https://en.wikipedia.org/w/api.php?action=opensearch&format=json'
        f'&search={q}&limit=10&namespace=0'
    )
    if d and len(d) >= 2:
        for title in d[1]:
            slug = title.replace(' ', '_')
            if slug in seen or slug == original_slug:
                continue
            seen.add(slug)
            summary = fetch_summary(slug)
            time.sleep(0.05)
            if is_valid_artist_summary(summary, name):
                return slug, summary

    return None, None


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
        name = m.group(2).strip().split(' — LOW-CONTEXT')[0]  # clean up comment annotations
        block = m.group(3)
        wm = re.search(r"wiki:\s*'([^']*)'", block)
        out[aid] = {
            'name': name,
            'wiki_slug': wm.group(1) if wm else None,
        }
    return out


def main():
    extracts = json.loads(EXTRACTS.read_text())
    facts = extract_facts()

    # Targets: status in (fetch_error, disambiguation, no_slug, no_extract)
    targets = [(aid, info) for aid, info in extracts.items() if info.get('status') != 'ok']
    print(f'Targets to fix: {len(targets)}')

    fixes = {}  # aid -> new_slug
    failed = []

    for i, (aid, info) in enumerate(targets, 1):
        if i % 25 == 0:
            print(f'  ...{i}/{len(targets)} (fixes so far: {len(fixes)})')
        original_slug = info.get('slug')
        name = facts.get(aid, {}).get('name', '')
        if not name:
            failed.append(aid)
            continue
        new_slug, summary = try_variants(name, original_slug)
        if new_slug and summary:
            fixes[aid] = {
                'new_slug': new_slug,
                'old_slug': original_slug,
                'name': name,
            }
            # Update the extracts file with the new working summary
            extracts[aid] = {
                'status': 'ok',
                'slug': new_slug,
                'title': summary.get('title', ''),
                'description': summary.get('description', ''),
                'extract': summary.get('extract', ''),
            }
        else:
            failed.append(aid)

    EXTRACTS.write_text(json.dumps(extracts, indent=2, ensure_ascii=False))

    # Now patch quiz_facts.js: for each fix, replace the old wiki slug with the new one
    facts_text = FACTS_JS.read_text()
    patched = 0
    for aid, fix in fixes.items():
        old = fix['old_slug']
        new = fix['new_slug']
        if old == new:
            continue
        # Decode any URL-encoded old slug to match what's in the file
        # The file stores the slug as written, which may be URL-encoded or not
        old_in_file_candidates = [old, urllib.parse.unquote(old)]
        # Try each form
        block_re = re.compile(
            rf"(^  {re.escape(aid)}:\s*\{{.*?wiki:\s*')([^']*?)('.*?^  \}},)",
            re.MULTILINE | re.DOTALL,
        )
        def _replace(m):
            return f"{m.group(1)}{new}{m.group(3)}"
        new_text, n = block_re.subn(_replace, facts_text, count=1)
        if n:
            facts_text = new_text
            patched += 1
    FACTS_JS.write_text(facts_text)

    print()
    print(f'Fixed slugs: {len(fixes)}')
    print(f'Failed to fix: {len(failed)}')
    print(f'Patched facts entries: {patched}')

    # Show a few fixes
    print()
    print('Sample fixes:')
    for aid, fix in list(fixes.items())[:8]:
        print(f"  {aid} {fix['name']}: {fix['old_slug']} -> {fix['new_slug']}")


if __name__ == '__main__':
    main()
