"""
Fourth portrait pass: Wikimedia Commons "depicts" structured search.

Files on Commons have P180 (depicts) statements that explicitly tag what
or whom the file shows. If we can resolve an artist to their Wikidata Q-ID
(via their Wikipedia article's page props), we can find files that say
"depicts: this artist" — a near-zero-false-positive portrait source.
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
EXTRACTS = HERE / 'wiki_extracts.json'
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
        block = m.group(3)
        wm = re.search(r"wiki:\s*'([^']*)'", block)
        out[aid] = {'name': name, 'wiki_slug': wm.group(1) if wm else None}
    return out


def get_qid(slug):
    """Resolve a Wikipedia slug to its Wikidata Q-ID via page props."""
    if not slug:
        return None
    safe = urllib.parse.quote(slug)
    d = get_json(
        f'https://en.wikipedia.org/w/api.php?action=query&format=json'
        f'&prop=pageprops&titles={safe}&redirects=1'
    )
    if not d:
        return None
    pages = (d.get('query') or {}).get('pages') or {}
    for p in pages.values():
        qid = (p.get('pageprops') or {}).get('wikibase_item')
        if qid:
            return qid
    return None


def commons_depicts(qid):
    """Find Commons files whose P180 (depicts) includes this Q-ID."""
    if not qid:
        return []
    d = get_json(
        f'https://commons.wikimedia.org/w/api.php?action=query&format=json'
        f'&list=search&srsearch=haswbstatement:P180={qid}'
        f'&srnamespace=6&srlimit=20'
    )
    if not d:
        return []
    out = []
    for r in (d.get('query') or {}).get('search') or []:
        title = r.get('title', '')
        if not title.startswith('File:'):
            continue
        fname = title[len('File:'):]
        if not any(fname.lower().endswith(ext) for ext in ('.jpg', '.jpeg', '.png')):
            continue
        # Skip obvious non-portraits
        lower = fname.lower()
        skip = ['painting', 'sculpture', 'untitled', '_work_', 'artwork', 'exhibition']
        if any(s in lower for s in skip):
            continue
        f_enc = urllib.parse.quote(fname.replace(' ', '_'))
        out.append({
            'url': f'https://commons.wikimedia.org/wiki/Special:FilePath/{f_enc}?width=800',
            'filename': fname,
        })
    return out


def main():
    portraits = json.loads(PORTRAITS.read_text())
    extracts = json.loads(EXTRACTS.read_text())
    facts = extract_facts()

    targets = []
    for aid, info in facts.items():
        if portraits.get(aid, {}).get('url'):
            continue
        slug = info.get('wiki_slug')
        if not slug:
            continue
        # Only try if Wikipedia slug resolves
        ext = extracts.get(aid, {})
        if ext.get('status') != 'ok':
            continue
        targets.append((aid, info))

    print(f'Targets (no portrait + valid wiki slug): {len(targets)}')

    hits = 0
    for i, (aid, info) in enumerate(targets, 1):
        if i % 25 == 0:
            print(f'  ...{i}/{len(targets)} (hits: {hits})')
        slug = info['wiki_slug']
        qid = get_qid(slug)
        time.sleep(0.05)
        if not qid:
            continue
        files = commons_depicts(qid)
        time.sleep(0.05)
        if not files:
            continue
        # Use the first file
        first = files[0]
        portraits[aid] = {
            'url': first['url'],
            'source': f'Commons depicts {qid}: {first["filename"]}',
        }
        hits += 1
        print(f'  [{aid}] {info["name"]}: ← Commons depicts {qid}')

    PORTRAITS.write_text(json.dumps(portraits, indent=2, ensure_ascii=False))
    print()
    print(f'New portraits: {hits}')
    total = sum(1 for v in portraits.values() if v and v.get('url'))
    print(f'Total portrait coverage: {total}/857')


if __name__ == '__main__':
    main()
