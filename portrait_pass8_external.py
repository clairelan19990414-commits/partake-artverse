"""
Eighth portrait pass: follow Wikipedia article's "External Links" section
to the artist's official website (or Instagram), then grab the og:image.

Most artists' personal sites use their og:image as a portrait or hero shot.
Same for Instagram profile pages (Instagram serves og:image meta tags for
public profiles without auth).

For each artist with no portrait AND valid Wikipedia slug:
  1. Fetch Wikipedia article HTML
  2. Find external link URLs (skip social-media bots that gate behind auth
     except Instagram, and skip gallery/dealer URLs we already failed on)
  3. For each candidate URL, fetch the page and extract og:image
  4. Take the first non-empty og:image as the portrait
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

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# Skip domains we already tried via other passes, or that block bots
SKIP_DOMAINS = [
    'wikipedia.org', 'wikidata.org', 'commons.wikimedia.org',
    'facebook.com', 'twitter.com', 'youtube.com', 'pinterest',
    'gagosian.com', 'pacegallery.com', 'whitecube.com',
    'spruethmagers.com', 'lissongallery.com', 'massimodecarlo.com',
    'sadiecoles.com', 'davidzwirner.com', 'hauserwirth.com',
    'mariangoodman.com', 'ropac.net', 'perrotin.com', 'galleriacontinua.com',
    'amazon.com', 'ebay.com', 'archive.org',  # noisy
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
    """Return ordered list of external URLs from a Wikipedia article."""
    safe = urllib.parse.quote(slug)
    html = get_text(f'https://en.wikipedia.org/wiki/{safe}')
    if not html:
        return []
    # External links section: usually inside <h2 id="External_links"> ... <ol> ...
    # Or just any <a href="http..."> with class="external"
    out = []
    seen = set()
    # Pattern: <a rel="nofollow" class="external text" href="...">
    for m in re.finditer(r'<a[^>]+class="external[^"]*"[^>]+href="(https?://[^"]+)"', html):
        url = m.group(1)
        # Strip anchors and tracking params
        url_clean = url.split('#')[0].split('?')[0]
        if url_clean in seen:
            continue
        seen.add(url_clean)
        domain = urllib.parse.urlparse(url).netloc.lower()
        if any(d in domain for d in SKIP_DOMAINS):
            continue
        out.append(url)
        if len(out) >= 8:
            break
    return out


def og_image(url):
    """Get og:image or twitter:image from a URL's HTML."""
    html = get_text(url)
    if not html:
        return None
    for pat in [
        r'<meta\s+property="og:image"\s+content="([^"]+)"',
        r'<meta\s+name="og:image"\s+content="([^"]+)"',
        r'<meta\s+property="og:image:url"\s+content="([^"]+)"',
        r'<meta\s+name="twitter:image"\s+content="([^"]+)"',
        r'<meta\s+name="twitter:image:src"\s+content="([^"]+)"',
    ]:
        m = re.search(pat, html, re.IGNORECASE)
        if m:
            img = m.group(1)
            # Skip obvious placeholders
            if any(s in img.lower() for s in ['logo', 'favicon', 'default', 'placeholder', 'share-image']):
                continue
            # Resolve relative URLs
            if img.startswith('//'):
                img = 'https:' + img
            elif img.startswith('/'):
                parts = urllib.parse.urlparse(url)
                img = f'{parts.scheme}://{parts.netloc}{img}'
            elif not img.startswith('http'):
                continue
            return img
    return None


def main():
    extracts = json.loads(EXTRACTS.read_text())
    portraits = json.loads(PORTRAITS.read_text())
    facts = extract_facts()

    targets = []
    for aid, info in facts.items():
        if portraits.get(aid, {}).get('url'):
            continue
        slug = info.get('wiki_slug')
        if not slug:
            continue
        if extracts.get(aid, {}).get('status') != 'ok':
            continue
        targets.append((aid, info))

    print(f'Targets (no portrait + valid wiki): {len(targets)}')

    hits = 0
    for i, (aid, info) in enumerate(targets, 1):
        if i % 20 == 0:
            print(f'  ...{i}/{len(targets)} (hits: {hits})')
            # Periodic save
            PORTRAITS.write_text(json.dumps(portraits, indent=2, ensure_ascii=False))

        slug = info['wiki_slug']
        name = info['name']

        ext_urls = wikipedia_external_links(slug)
        time.sleep(0.1)
        if not ext_urls:
            continue

        for ext_url in ext_urls[:5]:
            try:
                img = og_image(ext_url)
            except Exception:
                img = None
            time.sleep(0.1)
            if img:
                portraits[aid] = {
                    'url': img,
                    'source': f'External link og:image — {urllib.parse.urlparse(ext_url).netloc}',
                }
                hits += 1
                print(f'  [{aid}] {name}: ← {urllib.parse.urlparse(ext_url).netloc}')
                break

    PORTRAITS.write_text(json.dumps(portraits, indent=2, ensure_ascii=False))
    total = sum(1 for v in portraits.values() if v and v.get('url'))
    print()
    print(f'New portraits: {hits}')
    print(f'Total portrait coverage: {total}/857')


if __name__ == '__main__':
    main()
