"""
Message-length audit. Flags artists whose 3-sentence message is below the
substance bar of the original 50 entries.

Output: message_audit.md with per-artist length + specificity flags.

Specificity proxies (heuristics, not exact):
  - "named work" — message includes a quoted work title or italic title or
    capitalised multi-word noun phrase (e.g., "the Black Mountain")
  - "named institution" — message references a specific museum, gallery, school
  - "specific date" — message contains a year
"""

import json, re
from pathlib import Path

HERE = Path(__file__).parent
MESSAGES_JS = HERE / 'quiz_messages.js'
FACTS_JS = HERE / 'quiz_facts.js'
EXTRACTS = HERE / 'wiki_extracts.json'
OUT = HERE / 'message_audit.md'


def extract_messages():
    text = MESSAGES_JS.read_text()
    out = {}
    pattern = re.compile(
        r'^  (a\d+):\s*\{\s*//\s*(.+?)\n    message:\s*"(.*?)"\n  \}',
        re.MULTILINE | re.DOTALL,
    )
    for m in pattern.finditer(text):
        out[m.group(1)] = {'name': m.group(2).strip(), 'message': m.group(3)}
    return out


def specificity_score(msg):
    """Count specifics: years, institutions, named works."""
    score = 0
    # Year mentions
    years = re.findall(r'\b(?:1[6-9]\d{2}|20[0-2]\d)\b', msg)
    score += min(len(years), 5)
    # Institutions: keywords that often appear in known-good entries
    institutions = re.findall(
        r'\b(?:Venice Biennale|Documenta|MoMA|Tate|Whitney|Guggenheim|Met|LACMA|'
        r'Bauhaus|Black Mountain|Yale|Cooper Union|Cal Arts|Royal Academy|Goldsmiths|'
        r'Düsseldorf|Cranbrook|Chelsea|Rhode Island School|RISD|École|Slade|'
        r'Hauser & Wirth|Gagosian|Pace|White Cube|Zwirner|Marian Goodman|'
        r'Lisson|Sprüth Magers|Sadie Coles|Massimo De Carlo|Continua|Perrotin)\b',
        msg,
    )
    score += len(institutions)
    # Named works in italics-equivalent (TitleCase phrases of 2+ words)
    titles = re.findall(r'\b[A-Z][a-z]+(?: [A-Z][a-z]+){1,5}\b', msg)
    # Filter out generic capitalised words that aren't titles
    real_titles = [t for t in titles if t not in (
        'New York', 'Los Angeles', 'Bay Area', 'East Village',
        'Cold War', 'World War', 'United States', 'Cultural Revolution',
        'Lost Decade', 'New Yorker',
    )]
    score += min(len(real_titles), 6)
    return score


def main():
    msgs = extract_messages()
    extracts = json.loads(EXTRACTS.read_text())

    rows = []
    for aid, m in msgs.items():
        msg = m['message']
        rows.append({
            'aid': aid, 'name': m['name'],
            'length': len(msg),
            'score': specificity_score(msg),
            'has_wiki': extracts.get(aid, {}).get('status') == 'ok',
            'wiki_extract_len': len(extracts.get(aid, {}).get('extract', '')) if extracts.get(aid, {}).get('status') == 'ok' else 0,
        })

    # Sort by need: shortest + lowest score first
    rows.sort(key=lambda r: (r['length'], r['score']))

    lines = [
        '# Message-quality audit',
        '',
        f'Total messages: {len(rows)}.',
        '',
        '## Length distribution',
        f'- < 500 chars: {sum(1 for r in rows if r["length"] < 500)}',
        f'- 500-700:     {sum(1 for r in rows if 500 <= r["length"] < 700)}',
        f'- 700-900:     {sum(1 for r in rows if 700 <= r["length"] < 900)}',
        f'- 900+ (rich): {sum(1 for r in rows if r["length"] >= 900)}',
        '',
        '## Bottom 60 by length + specificity (top of re-write queue)',
        '',
        '| ID | Name | Length | Score | Wiki ext (chars) |',
        '|----|------|-------:|------:|-----------------:|',
    ]
    for r in rows[:60]:
        wiki_marker = r['wiki_extract_len'] if r['has_wiki'] else '—'
        lines.append(f"| {r['aid']} | {r['name']} | {r['length']} | {r['score']} | {wiki_marker} |")

    lines.append('')
    lines.append('## Rich messages (length >= 900, score >= 6 — at original-50 level)')
    rich = [r for r in rows if r['length'] >= 900 and r['score'] >= 6]
    lines.append(f'{len(rich)} entries.')

    OUT.write_text('\n'.join(lines))
    print(f'Wrote {OUT}')
    print(f'Total: {len(rows)}')
    print(f'  Short (< 500): {sum(1 for r in rows if r["length"] < 500)}')
    print(f'  Rich (900+, score>=6): {sum(1 for r in rows if r["length"] >= 900 and r["score"] >= 6)}')


if __name__ == '__main__':
    main()
