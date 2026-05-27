"""
Validate Commons file-search portraits more strictly.

Original portrait_pass3 only required the artist's surname in the filename;
that catches many false positives (different people with the same surname).
This pass keeps only Commons portraits where the filename contains BOTH
the artist's first and last name (or, for single-word names, the full name).
"""

import json, re, urllib.parse
from pathlib import Path

HERE = Path(__file__).parent
PORTRAITS = HERE / 'quiz_portraits.json'
FACTS_JS = HERE / 'quiz_facts.js'


def extract_facts():
    text = FACTS_JS.read_text()
    out = {}
    pattern = re.compile(
        r"^  (a\d+):\s*\{\s*//\s*(.+?)$",
        re.MULTILINE,
    )
    for m in pattern.finditer(text):
        aid = m.group(1)
        name = m.group(2).strip().split(' — LOW-CONTEXT')[0]
        out[aid] = name
    return out


def name_tokens(name):
    return [w.lower() for w in re.findall(r'\w+', name) if len(w) > 1]


def is_validated(filename, artist_name):
    """Filename must contain ALL of the artist's name tokens (each >=2 chars)."""
    fname_lower = urllib.parse.unquote(filename).lower()
    # Remove file extension and Wikipedia-image suffixes
    fname_lower = re.sub(r'\.(jpg|jpeg|png)$', '', fname_lower)
    fname_lower = re.sub(r'\(cropped\)|\d{6,}', '', fname_lower)

    tokens = name_tokens(artist_name)
    if not tokens:
        return False

    # Single-word names: require exact match somewhere in filename
    if len(tokens) == 1:
        return tokens[0] in fname_lower

    # Multi-word names: ALL tokens must appear
    for tok in tokens:
        if len(tok) >= 2 and tok not in fname_lower:
            return False
    return True


def main():
    portraits = json.loads(PORTRAITS.read_text())
    facts = extract_facts()

    reverted = 0
    kept = 0
    bad_examples = []

    for aid, v in list(portraits.items()):
        if not v or 'Commons file search' not in (v.get('source') or ''):
            continue
        source = v.get('source', '')
        # source format: "Commons file search: FILENAME.jpg"
        m = re.search(r'Commons file search: (.+)$', source)
        if not m:
            continue
        filename = m.group(1)
        artist_name = facts.get(aid, '')
        if is_validated(filename, artist_name):
            kept += 1
        else:
            bad_examples.append((aid, artist_name, filename))
            # Drop the bad portrait
            del portraits[aid]
            reverted += 1

    PORTRAITS.write_text(json.dumps(portraits, indent=2, ensure_ascii=False))

    print(f'Kept: {kept}')
    print(f'Reverted (failed full-name validation): {reverted}')
    print()
    print('Sample reverted (artist → bad filename):')
    for aid, name, fn in bad_examples[:20]:
        print(f'  {aid} "{name}" → {fn[:80]}')
    new_total = sum(1 for v in portraits.values() if v and v.get('url'))
    print()
    print(f'New portrait total: {new_total}/857')


if __name__ == '__main__':
    main()
