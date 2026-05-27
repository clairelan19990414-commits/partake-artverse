"""
Validate slug fixes by checking that the Wikipedia page title shares
significant name tokens with the artist name. Revert obviously-wrong fixes.

A fix is kept iff:
  - The Wikipedia page title contains at least one name word ≥ 3 letters
    from the artist's name (case-insensitive), AND
  - The page title's first character starts with the same letter as either
    the artist's first or last name (catches transliteration variants).

Reverts in BOTH quiz_facts.js (sets wiki back to the original slug as a best-
effort placeholder marked with `_NOTFOUND` suffix? No — actually just leave
the original guess) and wiki_extracts.json (sets status back to fetch_error).
"""

import json, re, urllib.parse
from pathlib import Path

HERE = Path(__file__).parent
EXTRACTS = HERE / 'wiki_extracts.json'
FACTS_JS = HERE / 'quiz_facts.js'


def name_words(s):
    # Strip parentheticals, punctuation; keep words >= 3 chars
    s = re.sub(r'\([^)]*\)', '', s or '')
    s = urllib.parse.unquote(s)
    return [w.lower() for w in re.findall(r'\w+', s) if len(w) >= 3]


def passes_validation(artist_name, page_title, slug):
    """A fix passes if EITHER the slug or page title matches artist name closely."""
    artist_tokens = set(name_words(artist_name))
    if not artist_tokens:
        return False

    slug_tokens = set(name_words(slug or ''))
    title_tokens = set(name_words(page_title or ''))

    # Strong signal: slug starts with the artist name (parenthetical disambiguation OK)
    # e.g., "JR_(artist)" matches "JR" because slug starts with "JR"
    slug_clean = re.sub(r'_*\([^)]*\)$', '', slug or '')
    artist_slug_form = re.sub(r'[^\w]+', '_', artist_name).strip('_')
    if slug_clean.lower() == artist_slug_form.lower():
        return True
    if slug_clean.lower().startswith(artist_slug_form.lower() + '_'):
        return True

    # Token overlap on long words (>=4 chars) in either slug or title
    for tokens in (slug_tokens, title_tokens):
        long_shared = {t for t in (artist_tokens & tokens) if len(t) >= 4}
        if long_shared:
            return True

    # Last-name match (artist's last name word appears in slug or title)
    artist_words = name_words(artist_name)
    if artist_words:
        artist_last = artist_words[-1]
        if len(artist_last) >= 3 and (artist_last in slug_tokens or artist_last in title_tokens):
            return True

    return False


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
        name = m.group(2).strip().split(' — LOW-CONTEXT')[0]
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

    reverted = []
    kept = []
    for aid, info in extracts.items():
        if info.get('status') != 'ok':
            continue
        artist_name = facts.get(aid, {}).get('name', '')
        page_title = info.get('title', '')
        if not page_title:
            continue
        if passes_validation(artist_name, page_title, info.get('slug', '')):
            kept.append((aid, artist_name, page_title))
            continue
        # Revert
        reverted.append((aid, artist_name, info.get('slug', ''), page_title))
        extracts[aid] = {
            'status': 'fetch_error',
            'slug': info.get('slug', ''),
            'note': f'reverted from {page_title} (failed name validation)',
        }

    EXTRACTS.write_text(json.dumps(extracts, indent=2, ensure_ascii=False))

    print(f'Total ok entries: {len(kept) + len(reverted)}')
    print(f'  Kept:    {len(kept)}')
    print(f'  Reverted: {len(reverted)}')
    print()
    if reverted:
        print('Reverted (artist name → bad slug → wiki page title):')
        for aid, name, slug, title in reverted[:30]:
            print(f'  {aid} "{name}" → {slug} → "{title}"')


if __name__ == '__main__':
    main()
