"""
Fifth portrait pass: Wikipedia article HTML alt-text + figcaption matching.

For each artist with valid Wikipedia slug but no portrait, fetch the article
HTML and find images where the alt text OR adjacent figcaption explicitly
contains the artist's full name (first AND last). This catches portrait
photos with GUID-style filenames that pass2 missed.
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
PORTRAITS = HERE / 'quiz_portraits.json'
FACTS_JS = HERE / 'quiz_facts.js'
WIKI_UA = 'PartakeQuiz/1.0 (https://partake-artverse.vercel.app; clairelan19990414@gmail.com)'


def get_text(url):
    req = urllib.request.Request(url, headers={'User-Agent': WIKI_UA})
    try:
        return urllib.request.urlopen(req, timeout=20, context=_CTX).read().decode('utf-8', errors='ignore')
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


def find_portrait_by_alt(slug, artist_name):
    safe = urllib.parse.quote(slug)
    html = get_text(f'https://en.wikipedia.org/wiki/{safe}')
    if not html:
        return None

    name_tokens = [w.lower() for w in re.findall(r'\w+', artist_name) if len(w) > 2]
    if len(name_tokens) < 2:
        # For single-name artists, fall back to single-token check
        if not name_tokens:
            return None

    # Find <figure>...<img>...<figcaption>...</figcaption></figure> blocks
    figure_re = re.compile(
        r'<figure[^>]*?(?:typeof="mw:File/Thumb"[^>]*)?>\s*<a[^>]*>\s*'
        r'<img[^>]+src="(//upload\.wikimedia\.org/[^"]+\.(?:jpg|jpeg|png))"[^>]*?'
        r'(?:alt="([^"]*)")?[^>]*>\s*</a>\s*'
        r'<figcaption[^>]*>(.*?)</figcaption>',
        re.IGNORECASE | re.DOTALL,
    )

    skip_substrings = [
        'logo', 'icon', 'flag_of', 'symbol_', 'magnify-clip', 'mediawiki',
        'wiki-logo', 'commons-logo', 'audio-x', 'speakerlink', 'ambox',
    ]

    for m in figure_re.finditer(html):
        src = m.group(1)
        alt = (m.group(2) or '').lower()
        caption_html = m.group(3) or ''
        caption_text = re.sub(r'<[^>]+>', ' ', caption_html).lower()

        # Reconstruct full-res URL
        full = 'https:' + src
        thumb_match = re.search(r'/thumb/(.+?)/\d+px-[^/]+$', src)
        if thumb_match:
            sub = thumb_match.group(1)
            prefix = 'wikipedia/commons' if '/wikipedia/commons/' in src else 'wikipedia/en'
            full = f'https://upload.wikimedia.org/{prefix}/{sub}'

        fname = full.rsplit('/', 1)[-1].lower()
        if any(s in fname for s in skip_substrings):
            continue
        if fname.endswith('.svg'):
            continue

        # Require ALL artist name tokens to appear in alt OR caption
        combined = f'{alt} {caption_text}'
        if all(tok in combined for tok in name_tokens):
            return full

    return None


def main():
    extracts = json.loads(EXTRACTS.read_text())
    portraits = json.loads(PORTRAITS.read_text())
    facts = extract_facts()

    targets = []
    for aid, info in facts.items():
        if portraits.get(aid, {}).get('url'):
            continue
        if extracts.get(aid, {}).get('status') != 'ok':
            continue
        targets.append((aid, info))

    print(f'Targets (no portrait + valid wiki): {len(targets)}')

    hits = 0
    for i, (aid, info) in enumerate(targets, 1):
        if i % 25 == 0:
            print(f'  ...{i}/{len(targets)} (hits: {hits})')
        slug = info['wiki_slug']
        name = info['name']
        url = find_portrait_by_alt(slug, name)
        time.sleep(0.05)
        if url:
            portraits[aid] = {'url': url, 'source': f'Wikipedia caption-match: {slug}'}
            hits += 1
            print(f'  [{aid}] {name}: ← caption-match')

    PORTRAITS.write_text(json.dumps(portraits, indent=2, ensure_ascii=False))
    total = sum(1 for v in portraits.values() if v and v.get('url'))
    print()
    print(f'New portraits: {hits}')
    print(f'Total portrait coverage: {total}/857')


if __name__ == '__main__':
    main()
