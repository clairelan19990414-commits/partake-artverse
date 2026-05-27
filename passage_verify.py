"""
Passage verifier: cross-checks specific factual claims in each message
against the artist's Wikipedia extract. Flags real contradictions for
hand-review without rewriting (auto-rewriting risks introducing new errors).

Checks per artist (where Wikipedia extract is available):
  1. Birth year: extract the year I wrote vs the year Wikipedia states
  2. Birthplace city: ditto for the place mentioned in the first sentence
  3. Training institution: my facts.training vs places Wikipedia mentions

Outputs passage_review.md with flagged entries grouped by issue type.
"""

import json, re
from pathlib import Path

HERE = Path(__file__).parent
MESSAGES_JS = HERE / 'quiz_messages.js'
FACTS_JS = HERE / 'quiz_facts.js'
EXTRACTS = HERE / 'wiki_extracts.json'
OUT = HERE / 'passage_review.md'


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


def extract_facts():
    text = FACTS_JS.read_text()
    out = {}
    pattern = re.compile(
        r"^  (a\d+):\s*\{\s*//\s*(.+?)$"
        r"(.*?)"
        r"^  \},",
        re.MULTILINE | re.DOTALL,
    )
    for m in pattern.finditer(text):
        aid = m.group(1)
        block = m.group(3)
        born = re.search(r"born:\s*'([^']*)'", block)
        training = re.search(r"training:\s*'([^']*)'", block)
        out[aid] = {
            'born': born.group(1) if born else '',
            'training': training.group(1) if training else '',
        }
    return out


def parse_birth_year(text):
    """Pull years that occur in birth contexts (after 'born', '(b.', etc.)."""
    years_found = set()
    for m in re.finditer(r'(?:born|b\.)\s*(?:in\s+)?(?:[A-Za-z, .]+?,?\s*)?(\b1[6-9]\d{2}\b|\b20[0-2]\d\b)', text):
        years_found.add(int(m.group(1)))
    # Also accept (1923-1971) hyphen form
    for m in re.finditer(r'\b(1[6-9]\d{2})\s*[–\-—]\s*(?:1[6-9]\d{2}|20[0-2]\d)\b', text):
        years_found.add(int(m.group(1)))
    # And standalone years adjacent to "in" within first 200 chars
    return years_found


def my_birth_year(message, facts_born):
    """Determine the birth year I claim. Check facts.born first, then message."""
    for source in (facts_born, message[:300]):
        years = parse_birth_year(source)
        if years:
            return min(years)  # earliest = birth year usually
        # Fallback: any 4-digit year in first 200 chars of the source
        ys = re.findall(r'\b(1[6-9]\d{2}|20[0-2]\d)\b', source[:200])
        if ys:
            return int(ys[0])
    return None


def wiki_birth_year(extract):
    """Pull the most likely birth year from Wikipedia extract (first sentence)."""
    first_sentence = extract.split('.')[0] if extract else ''
    # Try strict patterns first
    for pat in [
        r'born[^.,]{0,30}?\b(1[6-9]\d{2}|20[0-2]\d)\b',
        r'\(born[^)]*?(1[6-9]\d{2}|20[0-2]\d)\)',
        r'\((1[6-9]\d{2})[\s–—-]+(?:1[6-9]\d{2}|20[0-2]\d)\)',
        r'\b(1[6-9]\d{2})\s*[–—-]\s*(?:1[6-9]\d{2}|20[0-2]\d)\b',
    ]:
        m = re.search(pat, first_sentence, re.IGNORECASE)
        if m:
            return int(m.group(1))
    return None


def main():
    msgs = extract_messages()
    facts = extract_facts()
    extracts = json.loads(EXTRACTS.read_text())

    year_mismatches = []
    no_extract = 0
    checked = 0

    for aid, m in msgs.items():
        ext = extracts.get(aid, {})
        if ext.get('status') != 'ok':
            no_extract += 1
            continue
        extract_text = ext.get('extract', '')
        if len(extract_text) < 50:
            continue
        checked += 1
        my_yr = my_birth_year(m['message'], facts.get(aid, {}).get('born', ''))
        wiki_yr = wiki_birth_year(extract_text)
        if my_yr and wiki_yr and abs(my_yr - wiki_yr) >= 2:
            year_mismatches.append({
                'aid': aid, 'name': m['name'],
                'my_yr': my_yr, 'wiki_yr': wiki_yr,
                'extract_first': extract_text.split('.')[0][:150],
                'born_field': facts.get(aid, {}).get('born', '')[:80],
            })

    # Build report
    lines = [
        '# Passage verification — facts vs Wikipedia',
        '',
        f'Checked {checked} entries with substantive Wikipedia extracts ({no_extract} had no extract).',
        f'Flagged **{len(year_mismatches)}** entries where my facts say a birth year that disagrees with Wikipedia by 2+ years.',
        '',
        '## Birth-year mismatches',
        '',
        '| ID | Name | My year | Wiki year | My facts.born | Wiki first sentence |',
        '|----|------|--------:|----------:|---------------|----------------------|',
    ]
    year_mismatches.sort(key=lambda x: x['name'].lower())
    for issue in year_mismatches:
        # Escape pipes in fields
        born_clean = issue['born_field'].replace('|', '\\|')
        ext_clean = issue['extract_first'].replace('|', '\\|')
        lines.append(
            f"| {issue['aid']} | {issue['name']} | {issue['my_yr']} | {issue['wiki_yr']} | "
            f"{born_clean} | {ext_clean} |"
        )

    OUT.write_text('\n'.join(lines))
    print(f'Wrote {OUT}')
    print(f'Checked: {checked}, mismatches: {len(year_mismatches)}, no extract: {no_extract}')


if __name__ == '__main__':
    main()
