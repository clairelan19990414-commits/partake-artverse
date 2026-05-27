"""
Scrape additional images from artists' external-link URLs (their official
website, museum bio page) as work candidates. Reuses the same external-
link logic as portrait_pass8 but pulls more than just og:image.

For each artist with valid Wikipedia + < 3 works:
  1. Get external links from Wikipedia article
  2. Visit each link, extract <img> tags with the artist's name in
     filename, alt, or surrounding context
  3. Add those images as work candidates (skip the existing portrait URL)
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
IMAGES = HERE / 'quiz_images.json'
PORTRAITS = HERE / 'quiz_portraits.json'
FACTS_JS = HERE / 'quiz_facts.js'

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

SKIP_DOMAINS = [
    'wikipedia.org', 'wikidata.org', 'commons.wikimedia.org',
    'facebook.com', 'twitter.com', 'youtube.com', 'pinterest',
    'gagosian.com', 'pacegallery.com', 'whitecube.com',
    'spruethmagers.com', 'lissongallery.com', 'massimodecarlo.com',
    'sadiecoles.com', 'davidzwirner.com', 'hauserwirth.com',
    'mariangoodman.com', 'ropac.net', 'perrotin.com', 'galleriacontinua.com',
]


def get_text(url, timeout=12):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        return urllib.request.urlopen(req, timeout=timeout, context=_CTX).read().decode('utf-8', errors='ignore')
    except Exception:
        return None


def extract_facts():
    text = FACTS_JS.read_text()
    out = {}
    pattern = re.compile(r"^  (a\d+):\s*\{\s*//\s*(.+?)$"
                         r"(.*?)^  \},", re.MULTILINE | re.DOTALL)
    for m in pattern.finditer(text):
        aid = m.group(1)
        name = m.group(2).strip().split(' — LOW-CONTEXT')[0]
        block = m.group(3)
        wm = re.search(r"wiki:\s*'([^']*)'", block)
        out[aid] = {'name': name, 'wiki_slug': wm.group(1) if wm else None}
    return out


def wikipedia_external_links(slug):
    safe = urllib.parse.quote(slug)
    html = get_text(f'https://en.wikipedia.org/wiki/{safe}')
    if not html:
        return []
    out = []
    seen = set()
    for m in re.finditer(r'<a[^>]+class="external[^"]*"[^>]+href="(https?://[^"]+)"', html):
        url = m.group(1)
        url_clean = url.split('#')[0].split('?')[0]
        if url_clean in seen:
            continue
        seen.add(url_clean)
        domain = urllib.parse.urlparse(url).netloc.lower()
        if any(d in domain for d in SKIP_DOMAINS):
            continue
        out.append(url)
        if len(out) >= 5:
            break
    return out


def page_images(url, artist_name, exclude_url=None):
    """Extract image URLs from a page, filtering for plausibly-art images."""
    html = get_text(url)
    if not html:
        return []
    name_tokens = [w.lower() for w in re.findall(r'\w+', artist_name) if len(w) >= 3]

    out = []
    seen = set()
    # Find all <img> tags
    for m in re.finditer(r'<img\s+([^>]+)>', html, re.IGNORECASE):
        attrs = m.group(1)
        src_m = re.search(r'(?:data-src|data-lazy-src|src)\s*=\s*"([^"]+)"', attrs)
        alt_m = re.search(r'alt\s*=\s*"([^"]*)"', attrs)
        if not src_m:
            continue
        src = src_m.group(1)
        alt = (alt_m.group(1) if alt_m else '').lower()

        # Resolve relative URL
        if src.startswith('//'):
            src = 'https:' + src
        elif src.startswith('/'):
            parts = urllib.parse.urlparse(url)
            src = f'{parts.scheme}://{parts.netloc}{src}'
        elif src.startswith('data:'):
            continue
        elif not src.startswith('http'):
            continue

        if src in seen:
            continue
        seen.add(src)
        if exclude_url and src == exclude_url:
            continue

        fname = src.rsplit('/', 1)[-1].lower()
        if fname.endswith('.svg'):
            continue
        if any(s in fname for s in ['logo', 'favicon', 'icon-', 'social-', 'sprite', '_thumb']):
            continue
        # Skip very small images
        if re.search(r'/\d{1,2}px-', src) or 'width=1' in src:
            continue

        # Score: contains artist name in alt/filename?
        combined = f'{src.lower()} {alt}'
        if any(t in combined for t in name_tokens if len(t) >= 4):
            out.append({
                'source': urllib.parse.urlparse(url).netloc,
                'title': alt[:80] if alt else 'Untitled',
                'year': '',
                'image': src,
                'credit': f'Found via Wikipedia external link',
                'url': url,
            })
        if len(out) >= 3:
            break

    return out


def main():
    extracts = json.loads(EXTRACTS.read_text())
    images = json.loads(IMAGES.read_text())
    portraits = json.loads(PORTRAITS.read_text())
    facts = extract_facts()

    targets = []
    for aid, info in facts.items():
        if extracts.get(aid, {}).get('status') != 'ok':
            continue
        current = len(images.get(aid, {}).get('candidates', []))
        if current >= 3:
            continue
        targets.append((aid, info))

    print(f'Targets (valid wiki + < 3 works): {len(targets)}')

    hits = 0
    total_added = 0
    for i, (aid, info) in enumerate(targets, 1):
        if i % 20 == 0:
            print(f'  ...{i}/{len(targets)} (artists with new works: {hits})')
            IMAGES.write_text(json.dumps(images, indent=2, ensure_ascii=False))

        slug = info['wiki_slug']
        name = info['name']
        portrait_url = portraits.get(aid, {}).get('url')

        ext_urls = wikipedia_external_links(slug)
        time.sleep(0.1)
        if not ext_urls:
            continue

        new_cands = []
        for ext_url in ext_urls[:3]:
            try:
                cands = page_images(ext_url, name, exclude_url=portrait_url)
            except Exception:
                cands = []
            time.sleep(0.1)
            new_cands.extend(cands)
            if len(new_cands) >= 4:
                break

        if not new_cands:
            continue

        existing = images.get(aid, {}).get('candidates', [])
        existing_urls = {c.get('image') for c in existing}
        added = [c for c in new_cands if c['image'] not in existing_urls][:5]
        if added:
            if aid not in images:
                images[aid] = {'name': name, 'dates': '', 'gallery': '', 'candidates': []}
            images[aid]['candidates'] = (existing + added)[:6]
            hits += 1
            total_added += len(added)

    IMAGES.write_text(json.dumps(images, indent=2, ensure_ascii=False))
    new_3plus = sum(1 for v in images.values() if len(v.get('candidates', [])) >= 3)
    print()
    print(f'Artists with new works: {hits} (+{total_added} candidates total)')
    print(f'Works ≥ 3 coverage: {new_3plus}/857')


if __name__ == '__main__':
    main()
