"""
Sixth portrait pass: gallery og:image as fallback portrait.

For each artist with no portrait, fetch their gallery's artist page,
grab the og:image (or twitter:image), and use it as the portrait.

This is less reliable than a Wikipedia portrait — the hero may be a curated
work rather than a photo of the artist. But it's gallery-quality imagery
and removes the "first-letter placeholder" fallback on the card UI.

Source label includes "(gallery hero — may be work)" so it's clear in
quiz_portraits.json which entries are uncertain.
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

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'


def _slug(name):
    n = name.lower().replace("'", "").replace(".", "")
    n = re.sub(r'[àáâãäå]', 'a', n)
    n = re.sub(r'[èéêë]', 'e', n)
    n = re.sub(r'[ìíîï]', 'i', n)
    n = re.sub(r'[òóôõö]', 'o', n)
    n = re.sub(r'[ùúûü]', 'u', n)
    n = re.sub(r'[ñ]', 'n', n)
    n = re.sub(r'[ç]', 'c', n)
    n = re.sub(r'[ß]', 'ss', n)
    n = re.sub(r'[^a-z0-9 -]', '', n)
    return n.replace(' ', '-')


GALLERY_URL = {
    'g1': lambda n: f'https://gagosian.com/artists/{_slug(n)}/',
    'g4': lambda n: f'https://www.pacegallery.com/artists/{_slug(n)}/',
    'g5': lambda n: f'https://whitecube.com/artists/{n.lower().replace(" ", "_").replace("-", "_")}',
    'g7': lambda n: f'https://spruethmagers.com/artists/{_slug(n)}/',
    'g8': lambda n: f'https://www.lissongallery.com/artists/{_slug(n)}',
    'g12': lambda n: f'https://www.massimodecarlo.com/artist/{_slug(n)}',
    'g13': lambda n: f'https://www.sadiecoles.com/artists/{_slug(n)}',
}

GALLERY_NAMES = {
    'g1': 'Gagosian', 'g4': 'Pace Gallery', 'g5': 'White Cube',
    'g7': 'Sprüth Magers', 'g8': 'Lisson Gallery',
    'g12': 'Massimo De Carlo', 'g13': 'Sadie Coles HQ',
}


def get_text(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        return urllib.request.urlopen(req, timeout=15, context=_CTX).read().decode('utf-8', errors='ignore')
    except Exception:
        return None


def extract_facts():
    text = FACTS_JS.read_text()
    out = {}
    pattern = re.compile(r"^  (a\d+):\s*\{\s*//\s*(.+?)$", re.MULTILINE)
    for m in pattern.finditer(text):
        aid = m.group(1)
        name = m.group(2).strip().split(' — LOW-CONTEXT')[0]
        out[aid] = name
    return out


def main():
    portraits = json.loads(PORTRAITS.read_text())
    facts = extract_facts()
    artists = json.load(open('/tmp/artists_full.json'))
    artist_gallery = {a['id']: a.get('gallery', '') for a in artists}

    targets = [(aid, n, artist_gallery.get(aid)) for aid, n in facts.items()
               if not portraits.get(aid, {}).get('url')
               and artist_gallery.get(aid) in GALLERY_URL]
    print(f'Targets (no portrait + supported gallery): {len(targets)}')

    hits = 0
    for i, (aid, name, gid) in enumerate(targets, 1):
        if i % 25 == 0:
            print(f'  ...{i}/{len(targets)} (hits: {hits})')
        url_fn = GALLERY_URL[gid]
        html = get_text(url_fn(name))
        time.sleep(0.1)
        if not html:
            continue
        og = re.search(r'<meta\s+(?:property|name)="(?:og:image|twitter:image)"\s+content="([^"]+)"', html)
        if not og:
            continue
        img = og.group(1)
        # Sanity: skip logos, placeholders, default share images
        if any(s in img.lower() for s in ['logo', 'placeholder', 'default-share', 'fallback']):
            continue
        portraits[aid] = {
            'url': img,
            'source': f'{GALLERY_NAMES[gid]} hero (may be work)',
        }
        hits += 1

    PORTRAITS.write_text(json.dumps(portraits, indent=2, ensure_ascii=False))
    print()
    print(f'New portraits: {hits}')
    total = sum(1 for v in portraits.values() if v and v.get('url'))
    print(f'Total portrait coverage: {total}/857')


if __name__ == '__main__':
    main()
