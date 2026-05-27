"""
Second portrait pass: for artists with valid Wikipedia slugs but no portrait,
use Wikipedia's media-list endpoint to find the first plausibly-portrait image
on the article page.

A "plausibly portrait" image is one where:
  - The caption / alt text contains the artist's surname OR "portrait" OR "photo"
  - File doesn't look like a work title or generic Wikipedia chrome
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


def get_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': WIKI_UA, 'Accept': 'application/json'})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=20, context=_CTX).read())
    except Exception:
        return None


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


def article_first_image(slug, artist_name):
    """Find the first image in the article that looks like a portrait."""
    safe = urllib.parse.quote(slug)
    html = get_text(f'https://en.wikipedia.org/wiki/{safe}')
    if not html:
        return None

    # Find all <img> with srcset or src to upload.wikimedia.org
    # Capture both src and surrounding alt+caption text
    img_block_re = re.compile(
        r'<img[^>]+?src="(//upload\.wikimedia\.org/[^"]+\.(?:jpg|jpeg|png|JPG|JPEG|PNG))"[^>]*?(?:alt="([^"]*)")?',
        re.IGNORECASE,
    )

    # Build name-token set
    name_words = [w.lower() for w in re.findall(r'\w+', artist_name) if len(w) > 2]
    surname = name_words[-1] if name_words else ''

    skip_substrings = [
        'ic_', '_icon', 'wiki-logo', 'commons-logo', 'wikimedia-button',
        'magnify-clip', 'symbol_', 'flag_of', 'crystal_clear', 'red_pog',
        'noun_', 'oojs-ui', 'mediawiki', 'audio-x', 'speakerlink',
        'signature', '_sig.', '_sig_', 'ambox', 'commons-icon',
    ]

    for m in img_block_re.finditer(html):
        src = m.group(1)
        alt = (m.group(2) or '').lower()

        # Reconstruct full-res URL
        full = 'https:' + src
        thumb_match = re.search(r'/thumb/(.+?)/\d+px-[^/]+$', src)
        if thumb_match:
            sub = thumb_match.group(1)
            prefix = 'wikipedia/commons' if '/wikipedia/commons/' in src else 'wikipedia/en'
            full = f'https://upload.wikimedia.org/{prefix}/{sub}'

        filename = full.rsplit('/', 1)[-1].lower()
        if any(s in filename for s in skip_substrings):
            continue
        if filename.endswith('.svg'):
            continue
        if re.search(r'/\d{1,2}px-', src):
            continue

        # Portrait-positive signals: filename or alt contains artist surname
        positive = False
        if surname and len(surname) >= 4:
            if surname in filename or surname in alt:
                positive = True
        for keyword in ['portrait', 'photo_of', 'self_portrait', 'photograph_of']:
            if keyword in filename or keyword in alt:
                positive = True
                break

        if positive:
            return full

    return None


def main():
    extracts = json.loads(EXTRACTS.read_text())
    portraits = json.loads(PORTRAITS.read_text()) if PORTRAITS.exists() else {}
    facts = extract_facts()

    targets = []
    for aid, info in extracts.items():
        if info.get('status') != 'ok':
            continue
        if portraits.get(aid, {}).get('url'):
            continue
        targets.append((aid, info))

    print(f'Targets (valid slug + no portrait): {len(targets)}')

    hits = 0
    for i, (aid, info) in enumerate(targets, 1):
        if i % 25 == 0:
            print(f'  ...{i}/{len(targets)} (hits: {hits})')
        slug = info['slug']
        name = facts.get(aid, {}).get('name', info.get('title', ''))
        url = article_first_image(slug, name)
        time.sleep(0.05)
        if url:
            portraits[aid] = {'url': url, 'source': f'Wikipedia body: {slug}'}
            hits += 1

    PORTRAITS.write_text(json.dumps(portraits, indent=2, ensure_ascii=False))
    print()
    print(f'New portraits: {hits}')
    total = sum(1 for v in portraits.values() if v.get('url'))
    print(f'Total portrait coverage: {total}/857')


if __name__ == '__main__':
    main()
