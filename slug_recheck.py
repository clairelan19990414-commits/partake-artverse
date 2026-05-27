"""
Re-run validation against the current facts slug for entries currently
marked fetch_error in extracts. If the slug actually works and now passes
the stricter validator, re-mark as ok.
"""

import json, ssl, urllib.parse, urllib.request, re, time
from pathlib import Path
try:
    import certifi
    _CTX = ssl.create_default_context(cafile=certifi.where())
except Exception:
    _CTX = ssl.create_default_context()

from slug_validate import passes_validation, extract_facts

HERE = Path(__file__).parent
EXTRACTS = HERE / 'wiki_extracts.json'
WIKI_UA = 'PartakeQuiz/1.0 (https://partake-artverse.vercel.app; clairelan19990414@gmail.com)'


def get_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': WIKI_UA, 'Accept': 'application/json'})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=20, context=_CTX).read())
    except Exception:
        return None


def main():
    extracts = json.loads(EXTRACTS.read_text())
    facts = extract_facts()

    targets = [aid for aid, info in extracts.items() if info.get('status') != 'ok']
    print(f'Re-checking {len(targets)} non-ok entries...')

    restored = 0
    still_bad = 0
    for i, aid in enumerate(targets, 1):
        if i % 25 == 0:
            print(f'  ...{i}/{len(targets)} (restored: {restored})')
        artist_name = facts.get(aid, {}).get('name', '')
        slug = facts.get(aid, {}).get('wiki_slug', '')
        if not slug:
            still_bad += 1
            continue
        safe = urllib.parse.quote(slug)
        d = get_json(f'https://en.wikipedia.org/api/rest_v1/page/summary/{safe}')
        time.sleep(0.05)
        if not d or d.get('type') in ('disambiguation', 'no-extract'):
            still_bad += 1
            continue
        title = d.get('title', '')
        if passes_validation(artist_name, title, slug):
            extracts[aid] = {
                'status': 'ok',
                'slug': slug,
                'title': title,
                'description': d.get('description', ''),
                'extract': d.get('extract', ''),
            }
            restored += 1
        else:
            still_bad += 1

    EXTRACTS.write_text(json.dumps(extracts, indent=2, ensure_ascii=False))
    print()
    print(f'Restored: {restored}')
    print(f'Still bad: {still_bad}')
    new_ok = sum(1 for v in extracts.values() if v.get('status') == 'ok')
    print(f'Total ok slugs: {new_ok}/{len(extracts)}')


if __name__ == '__main__':
    main()
