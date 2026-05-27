"""
Filter external-link og:image portraits to remove obvious artworks,
icons, and generic mastheads.

Drop if URL contains:
  - "untitled" (artwork title)
  - "/icons/", "_icon", "masthead", "logo" (UI chrome)
  - very small files (thumbnail patterns)
  - "/artworks/" in path
  - work-title-like dash chains

Keep:
  - Files with portrait-positive keywords
  - Larger CDN files where filename is opaque (ambiguous but plausible)
"""

import json, re
from pathlib import Path

HERE = Path(__file__).parent
PORTRAITS = HERE / 'quiz_portraits.json'

ARTWORK_SIGNALS = [
    'untitled', '/artworks/', '_artwork', 'artwork_',
    '_painting_', 'painting_', '_sculpture_', 'sculpture_',
    '_installation_', 'installation_',
]
CHROME_SIGNALS = [
    'masthead', '/logo', '_logo', 'logo_', 'logo.',
    'favicon', 'icon-', '_icon', 'placeholder', 'default-share',
    'share-image', 'social-share', 'opengraph-default',
    'twitter-default',
]
# File names that are too generic/small (e.g., 't_wb_75.gif')
GENERIC_PATTERNS = [
    r'^t_[a-z]{2,3}_\d{1,3}\.gif$',  # NYTimes icon
    r'^[a-z]_\d{1,3}\.gif$',
    r'^harpers-[a-z]-\d',  # harpers magazine masthead
]


def is_keepable(url):
    lower = url.lower()
    filename = url.rsplit('/', 1)[-1].lower().split('?')[0]

    # Hard drops
    for sig in ARTWORK_SIGNALS + CHROME_SIGNALS:
        if sig in lower:
            return False
    # Year-bearing filename = likely artwork (Hannah-Levy_Untitled-2017)
    if re.search(r'_20[0-2]\d[_.\-]', filename) or re.search(r'-20[0-2]\d-', filename):
        return False
    # Generic small icons
    for pat in GENERIC_PATTERNS:
        if re.search(pat, filename):
            return False
    # .gif is almost always an icon, not a portrait
    if filename.endswith('.gif'):
        return False
    # Files with no extension at end (like filepicker URLs) — keep, ambiguous
    return True


def main():
    portraits = json.loads(PORTRAITS.read_text())
    ext_entries = [(aid, v) for aid, v in portraits.items()
                   if v and 'External link' in (v.get('source') or '')]
    print(f'External-link portraits to review: {len(ext_entries)}')

    kept = 0
    dropped = 0
    dropped_examples = []
    for aid, v in ext_entries:
        if is_keepable(v['url']):
            kept += 1
        else:
            dropped += 1
            dropped_examples.append((aid, v['url']))
            del portraits[aid]

    PORTRAITS.write_text(json.dumps(portraits, indent=2, ensure_ascii=False))

    print(f'  Kept:    {kept}')
    print(f'  Dropped: {dropped}')
    print()
    print('Sample drops:')
    for aid, url in dropped_examples[:12]:
        print(f'  {aid}: {url[:100]}')

    total = sum(1 for v in portraits.values() if v and v.get('url'))
    print()
    print(f'New portrait total: {total}/857')


if __name__ == '__main__':
    main()
