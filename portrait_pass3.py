"""
Third portrait pass: Wikimedia Commons direct file search for "Artist Name"
to find portrait photos that aren't on the artist's Wikipedia article.
"""

import json, ssl, urllib.parse, urllib.request, re, time
from pathlib import Path
try:
    import certifi
    _CTX = ssl.create_default_context(cafile=certifi.where())
except Exception:
    _CTX = ssl.create_default_context()

HERE = Path(__file__).parent
PORTRAITS = HERE / 'quiz_portraits.json'
FACTS_JS = HERE / 'quiz_facts.js'

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
        name = m.group(2).strip().split(' — LOW-CONTEXT')[0]
        out[aid] = {'name': name}
    return out


def commons_portrait_search(name):
    """Search Commons for image files with the artist's name in the filename."""
    q = urllib.parse.quote(name)
    d = get_json(
        f'https://commons.wikimedia.org/w/api.php?action=query&format=json'
        f'&list=search&srsearch={q}&srnamespace=6&srlimit=15'
    )
    if not d:
        return None

    results = (d.get('query') or {}).get('search') or []
    name_words = [w.lower() for w in re.findall(r'\w+', name) if len(w) > 2]
    if not name_words:
        return None
    surname = name_words[-1]

    skip_substrings = [
        'logo', 'symbol', 'flag', 'icon', 'works_by', 'painting_by',
        'sculpture_by', 'untitled', '.svg', '_book', '_cover',
    ]

    for r in results:
        title = r.get('title', '')
        if not title.startswith('File:'):
            continue
        fname = title[len('File:'):]
        lower = fname.lower()
        if not any(lower.endswith(ext) for ext in ('.jpg', '.jpeg', '.png')):
            continue
        if any(s in lower for s in skip_substrings):
            continue

        # Require the surname to appear in the filename
        if len(surname) >= 4 and surname not in lower:
            continue

        # Bonus: prefer files containing "portrait", "photo", "headshot"
        # but accept any if surname matches.
        f_enc = urllib.parse.quote(fname.replace(' ', '_'))
        url = f'https://commons.wikimedia.org/wiki/Special:FilePath/{f_enc}?width=800'
        return url, fname

    return None


def main():
    portraits = json.loads(PORTRAITS.read_text())
    facts = extract_facts()

    targets = [aid for aid in facts if not portraits.get(aid, {}).get('url')]
    print(f'Targets (no portrait): {len(targets)}')

    hits = 0
    for i, aid in enumerate(targets, 1):
        if i % 25 == 0:
            print(f'  ...{i}/{len(targets)} (hits: {hits})')
        name = facts[aid]['name']
        result = commons_portrait_search(name)
        time.sleep(0.05)
        if result:
            url, fname = result
            portraits[aid] = {'url': url, 'source': f'Commons file search: {fname}'}
            hits += 1

    PORTRAITS.write_text(json.dumps(portraits, indent=2, ensure_ascii=False))
    total = sum(1 for v in portraits.values() if v.get('url'))
    print()
    print(f'New portraits: {hits}')
    print(f'Total portrait coverage: {total}/857')


if __name__ == '__main__':
    main()
