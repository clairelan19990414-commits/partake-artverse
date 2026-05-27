"""
Works pass: query multiple museum open-access APIs for artists below 3 works.

APIs queried (free, no auth needed):
  - The Met Museum
  - Smithsonian Open Access (excludes the National Gallery)
  - Cleveland Museum of Art
  - Harvard Art Museums (key-less search via Artsy-like endpoint — actually
    skip this without a key)
  - Walker Art Center (no public API — skip)
  - Tate (no public API anymore — skip)

For each artist:
  1. Query each museum's search endpoint with the artist's name.
  2. Filter results that share a strong artist-name match.
  3. Pull up to N works' images.
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
FACTS_JS = HERE / 'quiz_facts.js'
UA = 'PartakeQuiz/1.0 (https://partake-artverse.vercel.app; clairelan19990414@gmail.com)'


def get_json(url, timeout=20):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=timeout, context=_CTX).read())
    except Exception:
        return None


def met_works(name, n=4):
    """Met Museum: search by artist, then fetch each object."""
    q = urllib.parse.quote(name)
    d = get_json(
        f'https://collectionapi.metmuseum.org/public/collection/v1/search'
        f'?artistOrCulture=true&q={q}'
    )
    if not d or not d.get('objectIDs'):
        return []
    out = []
    for oid in (d['objectIDs'] or [])[:15]:
        obj = get_json(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{oid}')
        time.sleep(0.05)
        if not obj:
            continue
        artist_name = obj.get('artistDisplayName', '')
        # Strict name match
        if name.lower() not in artist_name.lower() and artist_name.lower() not in name.lower():
            continue
        img = obj.get('primaryImage') or obj.get('primaryImageSmall')
        if not img:
            continue
        out.append({
            'source': 'Met Museum',
            'title': obj.get('title', 'Untitled'),
            'year': obj.get('objectDate', ''),
            'image': img,
            'credit': obj.get('creditLine', 'Courtesy The Met'),
            'url': obj.get('objectURL', ''),
        })
        if len(out) >= n:
            break
    return out


def smithsonian_works(name, n=4):
    """Smithsonian Open Access: search by name, return image-bearing objects."""
    q = urllib.parse.quote(f'"{name}"')
    # Smithsonian requires online_media_type:Images filter
    d = get_json(
        f'https://api.si.edu/openaccess/api/v1.0/search?api_key=jwfMmcOEcF7UTNjLcRaa9SOfXfRu5sGGE5XzeARq'
        f'&q={q}+AND+online_media_type%3AImages&rows=15'
    )
    if not d:
        # No public-only fallback; skip
        return []
    rows = (d.get('response') or {}).get('rows') or []
    out = []
    for r in rows:
        content = r.get('content') or {}
        descriptive = (content.get('descriptiveNonRepeating') or {})
        name_field = descriptive.get('online_media', {})
        # Check artist matches
        related_freetext = (content.get('freetext') or {}).get('name') or []
        names_in_record = [n.get('content', '') for n in related_freetext]
        if not any(name.lower() in nn.lower() for nn in names_in_record):
            continue
        # Find the first image URL
        media = ((descriptive.get('online_media') or {}).get('media') or [])
        if not media:
            continue
        img_url = None
        for m in media:
            if m.get('type') == 'Images':
                img_url = (m.get('content') or '').replace('400,/', '1200,/')
                break
        if not img_url:
            continue
        title = (descriptive.get('title') or {}).get('content', 'Untitled')
        out.append({
            'source': 'Smithsonian',
            'title': title,
            'year': '',
            'image': img_url,
            'credit': 'Smithsonian Open Access',
            'url': '',
        })
        if len(out) >= n:
            break
    return out


def cleveland_works(name, n=4):
    """Cleveland Museum of Art: open API, no auth."""
    q = urllib.parse.quote(name)
    d = get_json(
        f'https://openaccess-api.clevelandart.org/api/artworks/?artists={q}&has_image=1&limit=15'
    )
    if not d:
        return []
    out = []
    for item in (d.get('data') or []):
        # Verify name match against creators
        creators = item.get('creators') or []
        creator_names = [c.get('description', '') for c in creators]
        if not any(name.lower() in cn.lower() for cn in creator_names):
            continue
        images = item.get('images') or {}
        img = ((images.get('web') or {}).get('url')
               or (images.get('full') or {}).get('url')
               or (images.get('print') or {}).get('url'))
        if not img:
            continue
        out.append({
            'source': 'Cleveland Museum of Art',
            'title': item.get('title', 'Untitled'),
            'year': item.get('creation_date', ''),
            'image': img,
            'credit': item.get('creditline', 'Cleveland Museum of Art'),
            'url': item.get('url', ''),
        })
        if len(out) >= n:
            break
    return out


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
    images = json.loads(IMAGES.read_text())
    facts = extract_facts()

    targets = []
    for aid, name in facts.items():
        current = len(images.get(aid, {}).get('candidates', []))
        if current < 3:
            targets.append((aid, name, current))
    print(f'Targets (< 3 works): {len(targets)}')

    hits = 0
    total_added = 0
    for i, (aid, name, current) in enumerate(targets, 1):
        if i % 25 == 0:
            print(f'  ...{i}/{len(targets)} (hits: {hits}, +works: {total_added})')

        new_works = []
        # Try Met first (most reliable for famous artists)
        try:
            new_works += met_works(name, n=3)
        except Exception:
            pass
        # Then Cleveland
        if len(new_works) < 3:
            try:
                new_works += cleveland_works(name, n=3 - len(new_works))
            except Exception:
                pass

        if not new_works:
            time.sleep(0.05)
            continue

        existing = images.get(aid, {}).get('candidates', [])
        existing_urls = {c.get('image') for c in existing}
        added = [w for w in new_works if w['image'] not in existing_urls][:5]
        if added:
            if aid not in images:
                images[aid] = {'name': name, 'dates': '', 'gallery': '', 'candidates': []}
            images[aid]['candidates'] = existing + added
            hits += 1
            total_added += len(added)
        time.sleep(0.05)

    IMAGES.write_text(json.dumps(images, indent=2, ensure_ascii=False))
    new_any = sum(1 for v in images.values() if v.get('candidates'))
    new_3plus = sum(1 for v in images.values() if len(v.get('candidates', [])) >= 3)
    print()
    print(f'Hits: {hits} artists got new works ({total_added} added total)')
    print(f'New works coverage: any={new_any}/857, 3+={new_3plus}/857')


if __name__ == '__main__':
    main()
