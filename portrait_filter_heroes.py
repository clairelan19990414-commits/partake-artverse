"""
Filter gallery_hero portraits to remove obvious artworks.

Reject if filename contains strong artwork signals:
  - "untitled" (most likely a work title)
  - "Artworks/" in URL path
  - Year + "-thumbnail" or year-only patterns suggesting work-image labelling
  - Specific work-title-like phrases

Keep:
  - Files with portrait-positive keywords (portrait, headshot, photo, bio, press, official)
  - Ambiguous CDN UUIDs (could be either — leave for hand-review)
"""

import json, re
from pathlib import Path

HERE = Path(__file__).parent
PORTRAITS = HERE / 'quiz_portraits.json'


ARTWORK_SIGNALS = [
    'untitled',
    '/artworks/',
    'header-image',  # White Cube uses this for work headers
    '_artwork',
    'artwork_',
]
PORTRAIT_SIGNALS = [
    'portrait', 'headshot', 'photo', 'bio-', 'press-', 'official',
    'pae_thumb_artist', 'a_photo', 'a-photo',
]


def classify(url):
    """Return 'portrait', 'artwork', or 'ambiguous'."""
    lower = url.lower()
    for sig in PORTRAIT_SIGNALS:
        if sig in lower:
            return 'portrait'
    for sig in ARTWORK_SIGNALS:
        if sig in lower:
            return 'artwork'
    # Year pattern as standalone signal — e.g., "Blue-Cryptobiosis-10-2021"
    if re.search(r'-(20[0-2]\d)(-|$|\.)', lower):
        return 'artwork'
    # Long work-title-like path: lots of dashes after artist segment
    return 'ambiguous'


def main():
    portraits = json.loads(PORTRAITS.read_text())
    heroes = [(aid, v) for aid, v in portraits.items() if v and 'hero' in (v.get('source') or '')]
    print(f'Total gallery-hero portraits to review: {len(heroes)}')

    keep_portrait = 0
    keep_ambiguous = 0
    drop_artwork = 0
    artwork_examples = []
    portrait_examples = []

    for aid, v in heroes:
        cls = classify(v['url'])
        if cls == 'artwork':
            drop_artwork += 1
            artwork_examples.append((aid, v['url']))
            del portraits[aid]  # remove the bad entry
        elif cls == 'portrait':
            keep_portrait += 1
            portrait_examples.append((aid, v['url']))
            # Update source label to reflect confidence
            portraits[aid]['source'] = portraits[aid]['source'].replace('(may be work)', '(portrait-keyword)')
        else:
            keep_ambiguous += 1

    PORTRAITS.write_text(json.dumps(portraits, indent=2, ensure_ascii=False))

    print(f'  Kept (portrait keyword): {keep_portrait}')
    print(f'  Kept (ambiguous):        {keep_ambiguous}')
    print(f'  Dropped (artwork):       {drop_artwork}')
    print()
    print('Sample portrait-keyword keeps:')
    for aid, url in portrait_examples[:5]:
        print(f'  {aid}: {url[:100]}')
    print()
    print('Sample artwork drops:')
    for aid, url in artwork_examples[:5]:
        print(f'  {aid}: {url[:100]}')

    total = sum(1 for v in portraits.values() if v and v.get('url'))
    print()
    print(f'New portrait total: {total}/857')


if __name__ == '__main__':
    main()
