"""
Gallery artist-page scraper for portraits + works.

For each artist with missing portrait OR < 3 works, hit their primary gallery's
artist page and extract:
  - og:image (hero image — sometimes portrait, sometimes lead work)
  - All other images on the page that look like artworks (gallery CDN URLs)

Adds candidates to quiz_images.json. For portrait, only fill if missing AND
the og:image filename looks more portrait-like than work-like.

Per-gallery URL patterns are from batch_fetch.py GALLERY_URL. Only galleries
that serve real HTML (not pure SPAs) are attempted: Gagosian (works),
White Cube, Pace, Lisson, Sadie Coles, Sprüth Magers, Massimo De Carlo.
"""

import json, ssl, urllib.parse, urllib.request, re, time
from pathlib import Path
try:
    import certifi
    _CTX = ssl.create_default_context(cafile=certifi.where())
except Exception:
    _CTX = ssl.create_default_context()

HERE = Path(__file__).parent
IMAGES = HERE / 'quiz_images.json'
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

# CDN image URL regex per gallery
GALLERY_CDN = {
    'g1': r'https://gagosian\.com/media/images/artists/[^"\s]+?\.(?:jpg|jpeg|png|webp)',
    'g4': r'https://www\.pacegallery\.com/media/images/[^"\s]+?\.(?:jpg|jpeg|png|webp)',
    'g5': r'https://white-cube\.transforms\.svdcdn\.com/production/[^"\s]+?\.(?:jpg|jpeg|png|webp)(?:\?[^"\s]*)?',
    'g7': r'https://(?:spruethmagers\.com/files|res\.cloudinary\.com/smimagebank/image/upload/[^"\s]+?/sprueth_magers)[^"\s]+?\.(?:jpg|jpeg|png|webp)',
    'g8': r'https://lisson-art\.s3\.amazonaws\.com/uploads/attachment/image/body/\d+/[^"\s]+?\.(?:jpg|jpeg|png|webp)',
    'g12': r'https://mdc-space\.fra1\.cdn\.digitaloceanspaces\.com/[^"\s]+?\.(?:jpg|jpeg|png|webp)',
    'g13': r'https://sadie-coles\.transforms\.svdcdn\.com/production/images/Artists/[^"\s]+?\.(?:jpg|jpeg|png|webp)(?:\?[^"\s]*)?',
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


def looks_portrait(url):
    """Heuristic: portrait file names often include 'portrait', 'photo', 'bio',
    'headshot', or 'press'. Returns True/False/None (unsure)."""
    lower = url.lower()
    for kw in ['portrait', 'headshot', 'photo-of', 'photo_of', 'bio-photo', 'press-photo']:
        if kw in lower:
            return True
    return None  # unsure — use as work candidate, not portrait


def scrape_gallery_page(gallery_id, name):
    url_fn = GALLERY_URL.get(gallery_id)
    cdn_pat = GALLERY_CDN.get(gallery_id)
    if not url_fn or not cdn_pat:
        return None, []

    url = url_fn(name)
    html = get_text(url)
    if not html:
        return None, []

    # og:image and twitter:image are the gallery's chosen hero image
    og = re.search(r'<meta\s+(?:property|name)="(?:og:image|twitter:image)"\s+content="([^"]+)"', html)
    hero = og.group(1) if og else None

    # All CDN-pattern images on the page
    all_urls = re.findall(cdn_pat, html)
    seen = set()
    unique = []
    for u in all_urls:
        # Strip query string + width-variant suffixes for dedupe
        base = re.sub(r'\.width-\d+|\.original|-\d+x\d+(?=\.\w+$)', '', u.split('?')[0])
        if base in seen:
            continue
        seen.add(base)
        unique.append(u.replace('&amp;', '&'))

    return hero, unique


def main():
    images = json.loads(IMAGES.read_text())
    portraits = json.loads(PORTRAITS.read_text())
    facts = extract_facts()

    # artists_full has gallery field already as 'g1', 'g4', etc.
    artists = json.load(open('/tmp/artists_full.json'))
    artist_gallery = {a['id']: a.get('gallery', '') for a in artists}

    targets = []
    for aid, name in facts.items():
        gid = artist_gallery.get(aid)
        if gid not in GALLERY_URL:
            continue
        needs_portrait = not portraits.get(aid, {}).get('url')
        needs_works = len(images.get(aid, {}).get('candidates', [])) < 3
        if needs_portrait or needs_works:
            targets.append((aid, name, gid, needs_portrait, needs_works))

    print(f'Targets (missing media + supported gallery): {len(targets)}')
    by_gallery = {}
    for _, _, gid, _, _ in targets:
        by_gallery[gid] = by_gallery.get(gid, 0) + 1
    print('Per gallery:')
    for gid, n in sorted(by_gallery.items(), key=lambda x: -x[1]):
        print(f'  {GALLERY_NAMES.get(gid, gid)}: {n}')

    portrait_hits = 0
    works_hits = 0
    total_works_added = 0

    for i, (aid, name, gid, np_, nw) in enumerate(targets, 1):
        if i % 25 == 0:
            print(f'  ...{i}/{len(targets)} (portraits +{portrait_hits}, works +{works_hits})')
        try:
            hero, all_urls = scrape_gallery_page(gid, name)
        except Exception:
            time.sleep(0.05)
            continue

        # PORTRAIT: only update if missing AND hero filename hints portrait
        if np_ and hero:
            if looks_portrait(hero):
                portraits[aid] = {
                    'url': hero,
                    'source': f'{GALLERY_NAMES.get(gid)} hero (portrait-keyword)',
                }
                portrait_hits += 1

        # WORKS: add all other unique URLs as work candidates
        if nw and all_urls:
            gallery_label = GALLERY_NAMES.get(gid, gid)
            existing = images.get(aid, {}).get('candidates', [])
            existing_urls = {c.get('image') for c in existing}
            new_cands = []
            for u in all_urls[:6]:
                if u in existing_urls:
                    continue
                # Skip if it's the portrait we just chose
                if u == portraits.get(aid, {}).get('url'):
                    continue
                # Skip portrait-keyword files when collecting works
                if looks_portrait(u):
                    continue
                new_cands.append({
                    'source': gallery_label,
                    'title': 'Untitled work',
                    'year': '',
                    'image': u,
                    'credit': f'Courtesy {gallery_label}',
                    'url': '',
                })
            if new_cands:
                if aid not in images:
                    images[aid] = {'name': name, 'dates': '', 'gallery': gallery_label, 'candidates': []}
                # Pad up to 6 total
                images[aid]['candidates'] = (existing + new_cands)[:6]
                works_hits += 1
                total_works_added += len(new_cands)

        time.sleep(0.1)

    PORTRAITS.write_text(json.dumps(portraits, indent=2, ensure_ascii=False))
    IMAGES.write_text(json.dumps(images, indent=2, ensure_ascii=False))

    print()
    print(f'New portraits: {portrait_hits}')
    print(f'Artists with new works: {works_hits} (+{total_works_added} candidates total)')
    p_total = sum(1 for v in portraits.values() if v and v.get('url'))
    w_3plus = sum(1 for v in images.values() if len(v.get('candidates', [])) >= 3)
    print(f'Coverage: portraits {p_total}/857, works 3+ {w_3plus}/857')


if __name__ == '__main__':
    main()
