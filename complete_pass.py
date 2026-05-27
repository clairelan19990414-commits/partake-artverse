"""
Quality completion pass: close image gaps using authoritative slug from quiz_facts.js
+ Wikidata P18 fallback + Wikimedia Commons fallback.

Reads quiz_facts.js to extract { aid: wiki_slug } and uses that to look up:
  - Portrait: Wikipedia REST summary (by exact slug, not name-guess) -> Wikidata P18 -> Commons
  - Works: Wikimedia Commons category search (more aggressive than current)

Updates quiz_portraits.json and quiz_images.json in place. Idempotent.
"""

import json, ssl, urllib.parse, urllib.request, re, time, sys
from pathlib import Path
try:
    import certifi
    _CTX = ssl.create_default_context(cafile=certifi.where())
except Exception:
    _CTX = ssl.create_default_context()

HERE = Path(__file__).parent
FACTS_JS = HERE / 'quiz_facts.js'
PORTRAITS_JSON = HERE / 'quiz_portraits.json'
IMAGES_JSON = HERE / 'quiz_images.json'

UA = 'Mozilla/5.0 (compatible; PartakeQuizBot/1.0)'
WIKI_UA = 'PartakeQuiz/1.0 (https://partake-artverse.vercel.app; clairelan19990414@gmail.com)'


def _get(url, ua=UA, timeout=20):
    req = urllib.request.Request(url, headers={'User-Agent': ua, 'Accept': 'application/json'})
    return urllib.request.urlopen(req, timeout=timeout, context=_CTX).read()


def get_json(url, ua=UA):
    try:
        return json.loads(_get(url, ua))
    except Exception:
        return None


def extract_facts():
    """Return {aid: {name, wiki_slug}}."""
    text = FACTS_JS.read_text()
    out = {}
    # Match blocks: aid: { // Name ... wiki: 'slug' ... }
    pattern = re.compile(
        r"^  (a\d+):\s*\{\s*//\s*(.+?)$"
        r"(.*?)"
        r"^  \},",
        re.MULTILINE | re.DOTALL,
    )
    for m in pattern.finditer(text):
        aid = m.group(1)
        name = m.group(2).strip()
        block = m.group(3)
        wm = re.search(r"wiki:\s*'([^']*)'", block)
        out[aid] = {
            'name': name,
            'wiki_slug': wm.group(1) if wm else None,
        }
    return out


def wiki_portrait_by_slug(slug):
    if not slug:
        return None
    safe = urllib.parse.quote(slug)
    d = get_json(f'https://en.wikipedia.org/api/rest_v1/page/summary/{safe}', ua=WIKI_UA)
    if not d or d.get('type') == 'disambiguation':
        return None
    orig = (d.get('originalimage') or {}).get('source')
    thumb = (d.get('thumbnail') or {}).get('source')
    return orig or thumb


def wikidata_portrait_by_slug(slug):
    """Look up the Wikipedia article's Wikidata Q-ID, then fetch P18 (image)."""
    if not slug:
        return None
    safe = urllib.parse.quote(slug)
    # First get the wikibase_item from page props
    d = get_json(
        f'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageprops'
        f'&titles={safe}&redirects=1'
    )
    if not d:
        return None
    pages = (d.get('query') or {}).get('pages') or {}
    qid = None
    for p in pages.values():
        qid = (p.get('pageprops') or {}).get('wikibase_item')
        if qid:
            break
    if not qid:
        return None
    # Fetch the Wikidata entity
    e = get_json(f'https://www.wikidata.org/wiki/Special:EntityData/{qid}.json')
    if not e:
        return None
    ent = (e.get('entities') or {}).get(qid) or {}
    claims = (ent.get('claims') or {}).get('P18') or []
    if not claims:
        return None
    mainsnak = claims[0].get('mainsnak') or {}
    filename = (mainsnak.get('datavalue') or {}).get('value')
    if not filename:
        return None
    # Build a Commons URL (filename is unencoded, may have spaces)
    f_enc = urllib.parse.quote(filename.replace(' ', '_'))
    return f'https://commons.wikimedia.org/wiki/Special:FilePath/{f_enc}?width=800'


def commons_category_works(name, n=4):
    """Aggressive Wikimedia Commons category search for works by this artist."""
    q = urllib.parse.quote(f'Paintings by {name}')
    # Try Category:Paintings by NAME first
    out = []
    for cat_prefix in ['Paintings by', 'Works by', 'Sculptures by', 'Photographs by']:
        cat = urllib.parse.quote(f'Category:{cat_prefix} {name}')
        d = get_json(
            f'https://commons.wikimedia.org/w/api.php?action=query&format=json'
            f'&list=categorymembers&cmtitle={cat}&cmtype=file&cmlimit=20'
        )
        if not d:
            continue
        members = (d.get('query') or {}).get('categorymembers') or []
        for m in members[:6]:
            title = m.get('title', '')
            if not title.startswith('File:'):
                continue
            fname = title[len('File:'):]
            if not any(fname.lower().endswith(ext) for ext in ('.jpg', '.jpeg', '.png')):
                continue
            f_enc = urllib.parse.quote(fname.replace(' ', '_'))
            url = f'https://commons.wikimedia.org/wiki/Special:FilePath/{f_enc}?width=1200'
            display_title = fname.rsplit('.', 1)[0]
            out.append({
                'source': 'Wikimedia Commons',
                'title': display_title[:80],
                'year': '',
                'image': url,
                'credit': 'Wikimedia Commons',
                'url': f'https://commons.wikimedia.org/wiki/{title.replace(" ", "_")}',
            })
            if len(out) >= n:
                return out
    return out


def main():
    facts = extract_facts()
    portraits = json.loads(PORTRAITS_JSON.read_text()) if PORTRAITS_JSON.exists() else {}
    images = json.loads(IMAGES_JSON.read_text())

    portrait_hits = 0
    works_hits = 0
    portrait_attempts = 0
    works_attempts = 0

    for aid, info in facts.items():
        name = info['name']
        wiki_slug = info['wiki_slug']

        # ---- Portrait gap fill ----
        has_portrait = portraits.get(aid, {}).get('url')
        if not has_portrait:
            portrait_attempts += 1
            url = None
            source = None
            # Try Wikipedia by exact slug
            url = wiki_portrait_by_slug(wiki_slug)
            if url:
                source = f'Wikipedia: {wiki_slug}'
            else:
                # Try Wikidata P18
                url = wikidata_portrait_by_slug(wiki_slug)
                if url:
                    source = f'Wikidata P18 via {wiki_slug}'
            if url:
                portraits[aid] = {'url': url, 'source': source}
                portrait_hits += 1
                print(f'  [{aid}] {name}: portrait ← {source.split(":")[0]}')
            time.sleep(0.1)

        # ---- Works gap fill (only for entries with < 3 candidates) ----
        current_candidates = images.get(aid, {}).get('candidates', [])
        if len(current_candidates) < 3:
            works_attempts += 1
            new_works = commons_category_works(name, n=4)
            if new_works:
                # Dedupe by image URL
                existing_urls = {c.get('image') for c in current_candidates}
                added = [w for w in new_works if w.get('image') not in existing_urls]
                if added:
                    if aid not in images:
                        images[aid] = {'name': name, 'dates': '', 'gallery': '', 'candidates': []}
                    images[aid]['candidates'] = current_candidates + added
                    works_hits += 1
                    print(f'  [{aid}] {name}: +{len(added)} works ← Commons category')
            time.sleep(0.1)

    PORTRAITS_JSON.write_text(json.dumps(portraits, indent=2, ensure_ascii=False))
    IMAGES_JSON.write_text(json.dumps(images, indent=2, ensure_ascii=False))

    print()
    print(f'Portrait gap-fill: tried {portrait_attempts}, hit {portrait_hits}')
    print(f'Works gap-fill:    tried {works_attempts}, hit {works_hits}')
    new_portrait_total = sum(1 for v in portraits.values() if v.get('url'))
    new_works_total = sum(1 for v in images.values() if v.get('candidates'))
    print(f'New portrait coverage: {new_portrait_total}/857')
    print(f'New works coverage:    {new_works_total}/857')


if __name__ == '__main__':
    main()
