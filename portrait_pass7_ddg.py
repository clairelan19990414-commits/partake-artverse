"""
Seventh portrait pass: DuckDuckGo HTML search + result-page scraping.

For each artist with no portrait, DDG search "[Artist Name] artist portrait",
fetch the top 3 result URLs, scrape each for images whose alt-text or
filename contains the artist's full name. Take the first validated match.

Sources commonly hit: Wikipedia, gallery websites, Frieze/Artnet press
articles, art-fair pages.

Validation: filename OR alt text must contain BOTH first and last name
of the artist. Skip obvious work / installation images.
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

WORK_KEYWORDS = ['installation', 'untitled', 'exhibition', 'artwork', 'sculpture-by', 'painting-by', 'screenshot']
SKIP_DOMAINS = ['pinterest', 'youtube', 'facebook.com', 'instagram.com']  # require auth or unreliable
SKIP_FILE_SUBSTRINGS = ['logo', 'favicon', 'icon-', 'social-', 'sprite']


def get_text(url, timeout=15):
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
        aid = m.group(1)
        name = m.group(2).strip().split(' — LOW-CONTEXT')[0]
        out[aid] = name
    return out


def ddg_search(query, n=5):
    """Return list of (url, title) from DuckDuckGo HTML search."""
    url = f'https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}'
    html = get_text(url, timeout=10)
    if not html:
        return []
    results = []
    # Pattern: <a class="result__a" href="..."> TITLE </a>
    for m in re.finditer(r'class="result__a"[^>]+href="([^"]+)"[^>]*>([^<]+)<', html):
        href = m.group(1)
        title = m.group(2).strip()
        # DDG uses redirects: extract real URL from uddg= param
        real = re.search(r'uddg=([^&]+)', href)
        target = urllib.parse.unquote(real.group(1)) if real else href
        if any(d in target for d in SKIP_DOMAINS):
            continue
        results.append((target, title))
        if len(results) >= n:
            break
    return results


def find_portrait_on_page(page_url, artist_name):
    html = get_text(page_url, timeout=12)
    if not html:
        return None
    name_tokens = [w.lower() for w in re.findall(r'\w+', artist_name) if len(w) >= 3]
    if not name_tokens:
        return None

    # Find all <img> tags + their alt + nearby figcaption
    candidates = []
    # img tags
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
            parts = urllib.parse.urlparse(page_url)
            src = f'{parts.scheme}://{parts.netloc}{src}'
        elif not src.startswith('http'):
            continue

        # Skip svg / icon-sized inline data URIs
        if src.startswith('data:') or src.endswith('.svg'):
            continue
        fname = src.rsplit('/', 1)[-1].lower()
        if any(s in fname for s in SKIP_FILE_SUBSTRINGS):
            continue
        # Reject work-image keywords
        combined = f'{src.lower()} {alt}'
        if any(k in combined for k in WORK_KEYWORDS):
            continue
        # Must contain ALL name tokens in filename or alt
        if not all(t in combined for t in name_tokens):
            continue
        # Skip tiny pixel-size hints
        if re.search(r'[?&-_](\d{1,2})px', src):
            continue
        candidates.append(src)
        if len(candidates) >= 3:
            break

    return candidates[0] if candidates else None


def main():
    portraits = json.loads(PORTRAITS.read_text())
    facts = extract_facts()

    targets = [(aid, name) for aid, name in facts.items()
               if not portraits.get(aid, {}).get('url')]
    print(f'Targets (no portrait): {len(targets)}')

    hits = 0
    fails = 0
    for i, (aid, name) in enumerate(targets, 1):
        if i % 25 == 0:
            print(f'  ...{i}/{len(targets)} (hits: {hits}, fails: {fails})')

        # DDG search
        try:
            results = ddg_search(f'{name} artist portrait', n=4)
        except Exception:
            results = []
        time.sleep(0.3)  # be polite to DDG

        if not results:
            fails += 1
            continue

        portrait_url = None
        for page_url, _title in results:
            try:
                portrait_url = find_portrait_on_page(page_url, name)
            except Exception:
                portrait_url = None
            time.sleep(0.15)
            if portrait_url:
                portraits[aid] = {
                    'url': portrait_url,
                    'source': f'DDG search → {page_url[:80]}',
                }
                hits += 1
                break
        else:
            fails += 1

        # Periodically write progress so we don't lose work on a crash
        if i % 25 == 0:
            PORTRAITS.write_text(json.dumps(portraits, indent=2, ensure_ascii=False))

    PORTRAITS.write_text(json.dumps(portraits, indent=2, ensure_ascii=False))
    total = sum(1 for v in portraits.values() if v and v.get('url'))
    print()
    print(f'New portraits via DDG: {hits} (failed: {fails})')
    print(f'Total portrait coverage: {total}/857')


if __name__ == '__main__':
    main()
