"""
Wikipedia article-HTML works scraper.

For artists whose Wikipedia slug resolved successfully in verify_pass.py
but still have < 3 works in quiz_images.json, scrape the article HTML
and extract image URLs from the article body (not infobox).

Skips entries where image filename looks like a portrait of the artist
(matches the artist's name or "portrait" / "photo of").
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
IMAGES_JSON = HERE / 'quiz_images.json'
PORTRAITS_JSON = HERE / 'quiz_portraits.json'

WIKI_UA = 'PartakeQuiz/1.0 (https://partake-artverse.vercel.app; clairelan19990414@gmail.com)'


def get_text(url):
    req = urllib.request.Request(url, headers={'User-Agent': WIKI_UA})
    try:
        return urllib.request.urlopen(req, timeout=20, context=_CTX).read().decode('utf-8', errors='ignore')
    except Exception:
        return None


def scrape_article_images(slug, artist_name, portrait_url):
    """Extract image URLs from the article HTML body. Filter out portraits + UI chrome."""
    safe = urllib.parse.quote(slug)
    html = get_text(f'https://en.wikipedia.org/wiki/{safe}')
    if not html:
        return []

    # Find all <img> tags with src pointing to upload.wikimedia.org
    img_pattern = re.compile(
        r'<img[^>]+src="(//upload\.wikimedia\.org/[^"]+\.(?:jpg|jpeg|png|JPG|JPEG|PNG))"[^>]*(?:alt="([^"]*)")?',
        re.IGNORECASE,
    )
    candidates = []
    seen_files = set()
    portrait_filename = ''
    if portrait_url:
        portrait_filename = portrait_url.rsplit('/', 1)[-1].split('?')[0].lower()

    for m in img_pattern.finditer(html):
        src = m.group(1)
        alt = m.group(2) or ''
        # Reconstruct higher-resolution URL (Wikipedia thumbnails follow /thumb/.../NNNpx-X.ext)
        full = 'https:' + src
        # If it's a thumb, get the original
        thumb_match = re.search(r'/thumb/(.+?)/\d+px-[^/]+$', src)
        if thumb_match:
            full = 'https://upload.wikimedia.org/wikipedia/commons/' + thumb_match.group(1)
            # Heuristic: if the thumb path includes 'wikipedia/en/', use that prefix
            if '/wikipedia/en/' in src:
                full = 'https://upload.wikimedia.org/wikipedia/en/' + thumb_match.group(1)

        filename = full.rsplit('/', 1)[-1].lower()
        if filename in seen_files:
            continue
        seen_files.add(filename)

        # Skip the portrait
        if portrait_filename and filename == portrait_filename:
            continue

        # Skip obvious portrait images
        name_tokens = artist_name.lower().replace('-', ' ').split()
        if any(tok in filename for tok in ['portrait', 'photo_of', 'headshot']):
            continue
        # Skip if alt text says "portrait of" or matches "Artist Name"
        if 'portrait of' in alt.lower():
            continue

        # Skip Wikipedia/Wikimedia UI chrome (icons, badges, audio waveforms, signatures, logos)
        skip_substrings = [
            'ic_', '_icon', 'wiki-logo', 'commons-logo', 'wikimedia-button',
            'magnify-clip', 'symbol_', 'flag_of', 'crystal_clear', 'red_pog',
            'noun_', 'oojs-ui', 'mediawiki', 'audio-x', 'speakerlink',
            'signature', '_sig.', '_sig_', 'ambox', 'commons-icon',
        ]
        if any(s in filename for s in skip_substrings):
            continue
        # Skip SVGs (mostly icons/flags/logos)
        if filename.endswith('.svg'):
            continue
        # Heuristic: very small dimensions in URL hint at icons (e.g., 20px, 30px)
        if re.search(r'/\d{1,2}px-', src):
            continue

        # Build a display title from filename
        raw_name = full.rsplit('/', 1)[-1]
        title = raw_name.rsplit('.', 1)[0].replace('_', ' ')
        title = urllib.parse.unquote(title)
        # Strip common artist-name prefixes from title
        if artist_name.lower() in title.lower():
            title = re.sub(re.escape(artist_name), '', title, flags=re.IGNORECASE).strip(' -–—,')

        candidates.append({
            'source': 'Wikipedia',
            'title': title[:80] if title else 'Untitled',
            'year': '',
            'image': full,
            'credit': f'Wikipedia article: {slug}',
            'url': f'https://en.wikipedia.org/wiki/{safe}',
        })

    return candidates


def main():
    if not EXTRACTS.exists():
        print(f'{EXTRACTS} not found — run verify_pass.py first')
        return

    extracts = json.loads(EXTRACTS.read_text())
    images = json.loads(IMAGES_JSON.read_text())
    portraits = json.loads(PORTRAITS_JSON.read_text())

    targets = []
    for aid, info in extracts.items():
        if info.get('status') != 'ok':
            continue
        current = len(images.get(aid, {}).get('candidates', []))
        if current >= 3:
            continue
        targets.append((aid, info))

    print(f'Targets (slug ok + < 3 works): {len(targets)}')

    hits = 0
    new_works_total = 0
    for i, (aid, info) in enumerate(targets, 1):
        if i % 25 == 0:
            print(f'  ...{i}/{len(targets)} (hits so far: {hits})')

        slug = info['slug']
        title = info.get('title', '')
        artist_name = images.get(aid, {}).get('name') or title
        if not artist_name:
            continue
        portrait_url = portraits.get(aid, {}).get('url', '')

        cands = scrape_article_images(slug, artist_name, portrait_url)
        if not cands:
            time.sleep(0.05)
            continue

        # Dedupe against existing
        existing = images.get(aid, {}).get('candidates', [])
        existing_urls = {c.get('image') for c in existing}
        added = [c for c in cands if c['image'] not in existing_urls][:5]
        if added:
            if aid not in images:
                images[aid] = {'name': artist_name, 'dates': '', 'gallery': '', 'candidates': []}
            images[aid]['candidates'] = existing + added
            hits += 1
            new_works_total += len(added)
        time.sleep(0.05)

    IMAGES_JSON.write_text(json.dumps(images, indent=2, ensure_ascii=False))
    print()
    print(f'Hits: {hits} artists got new works ({new_works_total} added total)')
    new_any = sum(1 for v in images.values() if v.get('candidates'))
    new_3plus = sum(1 for v in images.values() if len(v.get('candidates', [])) >= 3)
    print(f'New works coverage: any={new_any}/857, 3+={new_3plus}/857')


if __name__ == '__main__':
    main()
