"""
Ninth portrait pass: for artists with NO Wikipedia coverage, DDG search
for art-press URLs (Frieze, Artnet, Artforum, Hyperallergic, Brooklyn Rail,
Artnews, Tate, MoMA, Guardian, etc.) and grab the og:image.

Press articles' og:image is usually a portrait or signature work of the
artist. Apply the same filter as portrait_pass8 to reject obvious artworks.
"""

import json, ssl, urllib.parse, urllib.request, re, time
from pathlib import Path
try:
    import certifi
    _CTX = ssl.create_default_context(cafile=certifi.where())
except Exception:
    _CTX = ssl.create_default_context()

from portrait_filter_external import is_keepable

HERE = Path(__file__).parent
EXTRACTS = HERE / 'wiki_extracts.json'
PORTRAITS = HERE / 'quiz_portraits.json'
FACTS_JS = HERE / 'quiz_facts.js'

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

PRESS_DOMAINS = [
    'frieze.com', 'artnet.com', 'artforum.com', 'hyperallergic.com',
    'artnews.com', 'brooklynrail.org', 'theartnewspaper.com',
    'observer.com', 'galeriemagazine.com', 'culturedmag.com',
    'tate.org.uk', 'moma.org', 'whitney.org', 'guggenheim.org',
    'theguardian.com', 'nytimes.com', 'apollo-magazine.com',
    'studiointernational.com', 'wsj.com', 'newyorker.com',
    'artreview.com', 'aestheticamagazine.com', 'flashartonline.com',
    'kaleidoscope.media', 'numero.com', 'wmagazine.com',
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
    pattern = re.compile(r"^  (a\d+):\s*\{\s*//\s*(.+?)$", re.MULTILINE)
    for m in pattern.finditer(text):
        out[m.group(1)] = m.group(2).strip().split(' — LOW-CONTEXT')[0]
    return out


def ddg_search(query, n=10):
    url = f'https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}'
    html = get_text(url, timeout=10)
    if not html:
        return []
    results = []
    for m in re.finditer(r'class="result__a"[^>]+href="([^"]+)"[^>]*>([^<]+)<', html):
        href = m.group(1)
        title = m.group(2).strip()
        real = re.search(r'uddg=([^&]+)', href)
        target = urllib.parse.unquote(real.group(1)) if real else href
        results.append((target, title))
        if len(results) >= n:
            break
    return results


def og_image(url):
    html = get_text(url)
    if not html:
        return None
    for pat in [
        r'<meta\s+property="og:image"\s+content="([^"]+)"',
        r'<meta\s+name="twitter:image"\s+content="([^"]+)"',
    ]:
        m = re.search(pat, html, re.IGNORECASE)
        if m:
            img = m.group(1)
            if any(s in img.lower() for s in ['logo', 'favicon', 'default', 'placeholder']):
                continue
            if img.startswith('//'):
                img = 'https:' + img
            elif img.startswith('/'):
                parts = urllib.parse.urlparse(url)
                img = f'{parts.scheme}://{parts.netloc}{img}'
            return img
    return None


def main():
    extracts = json.loads(EXTRACTS.read_text())
    portraits = json.loads(PORTRAITS.read_text())
    facts = extract_facts()

    # Targets: no portrait AND no working Wikipedia extract
    targets = []
    for aid, name in facts.items():
        if portraits.get(aid, {}).get('url'):
            continue
        if extracts.get(aid, {}).get('status') == 'ok':
            continue  # skip — pass 8 handled these
        targets.append((aid, name))

    print(f'Targets (no portrait + no Wikipedia): {len(targets)}')

    hits = 0
    for i, (aid, name) in enumerate(targets, 1):
        if i % 10 == 0:
            print(f'  ...{i}/{len(targets)} (hits: {hits})')
            PORTRAITS.write_text(json.dumps(portraits, indent=2, ensure_ascii=False))

        # Broader DDG search — accept any non-SPA-gallery URL
        results = ddg_search(f'"{name}" artist interview', n=8)
        time.sleep(0.3)
        if not results:
            continue

        # Skip known unreliable domains (SPA galleries, social media, etc.)
        skip_domains = ['davidzwirner.com', 'hauserwirth.com', 'mariangoodman.com',
                        'ropac.net', 'perrotin.com', 'galleriacontinua.com',
                        'instagram.com', 'facebook.com', 'twitter.com',
                        'youtube.com', 'pinterest', 'amazon', 'ebay']
        usable = [
            (url, title) for url, title in results
            if not any(d in url for d in skip_domains)
        ]
        if not usable:
            continue

        for press_url, _title in usable[:4]:
            try:
                img = og_image(press_url)
            except Exception:
                img = None
            time.sleep(0.15)
            if img and is_keepable(img):
                portraits[aid] = {
                    'url': img,
                    'source': f'Press og:image — {urllib.parse.urlparse(press_url).netloc}',
                }
                hits += 1
                print(f'  [{aid}] {name}: ← {urllib.parse.urlparse(press_url).netloc}')
                break

    PORTRAITS.write_text(json.dumps(portraits, indent=2, ensure_ascii=False))
    total = sum(1 for v in portraits.values() if v and v.get('url'))
    print()
    print(f'New portraits via press: {hits}')
    print(f'Total: {total}/857')


if __name__ == '__main__':
    main()
