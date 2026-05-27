"""
Audit Wikipedia slug → artist name match across all entries with status=ok.
Flags entries where the Wikipedia page title looks like a different person.
"""

import json, re, urllib.parse
from pathlib import Path

HERE = Path(__file__).parent
EXTRACTS = HERE / 'wiki_extracts.json'
FACTS_JS = HERE / 'quiz_facts.js'


def name_tokens(s):
    s = re.sub(r'\([^)]*\)', '', s or '')
    s = urllib.parse.unquote(s)
    return [w.lower() for w in re.findall(r'\w+', s) if len(w) >= 2]


def extract_facts():
    text = FACTS_JS.read_text()
    out = {}
    pattern = re.compile(r"^  (a\d+):\s*\{\s*//\s*(.+?)$", re.MULTILINE)
    for m in pattern.finditer(text):
        out[m.group(1)] = m.group(2).strip().split(' — LOW-CONTEXT')[0]
    return out


def is_strong_match(artist_name, page_title):
    """Strong match: page title's main name tokens overlap with artist name's
    main tokens, with at least one shared token of length >= 4."""
    artist_t = set(name_tokens(artist_name))
    title_t = set(name_tokens(page_title))
    if not artist_t or not title_t:
        return False
    long_shared = {t for t in (artist_t & title_t) if len(t) >= 4}
    if long_shared:
        return True
    # If artist's last name (most identifying) matches title last name
    a_words = name_tokens(artist_name)
    t_words = name_tokens(page_title)
    if a_words and t_words and len(a_words[-1]) >= 3:
        return a_words[-1] in title_t
    return False


def main():
    extracts = json.loads(EXTRACTS.read_text())
    facts = extract_facts()

    suspicious = []
    for aid, info in extracts.items():
        if info.get('status') != 'ok':
            continue
        artist_name = facts.get(aid, '')
        title = info.get('title', '')
        if not is_strong_match(artist_name, title):
            suspicious.append({
                'aid': aid, 'name': artist_name,
                'title': title,
                'slug': info.get('slug', ''),
                'desc': info.get('description', '')[:80],
                'first': info.get('extract', '').split('.')[0][:120],
            })

    print(f'Suspicious slug matches: {len(suspicious)}')
    print()
    suspicious.sort(key=lambda x: x['name'].lower())
    for s in suspicious[:50]:
        print(f"  {s['aid']} \"{s['name']}\" → \"{s['title']}\"")
        print(f"      desc: {s['desc']}")
        print(f"      first: {s['first']}")
        print()


if __name__ == '__main__':
    main()
