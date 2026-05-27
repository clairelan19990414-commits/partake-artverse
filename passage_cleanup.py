"""
Targeted passage cleanup: tighten placeholder/weak phrasing without
changing factual content. Gallery info lives in facts.cohort so it
doesn't need to appear in the message body.

Replacements (only applied where they leave a grammatical sentence):
  - "and is represented by [gallery]" → ""  (trailing clause)
  - "; he/she is represented by [gallery]" → ""  (trailing semicolon)
  - " he/she is represented by [gallery]." → " "  (mid-sentence)
"""

import re
from pathlib import Path

HERE = Path(__file__).parent
MESSAGES_JS = HERE / 'quiz_messages.js'


REPLACEMENTS = [
    # "and is represented by Gagosian and Lisson Gallery"
    (r',?\s+and\s+is represented by [A-Z][\w\s&éüöäáàâèêïíó.]+(?:\s+(?:and|since)\s+[A-Z][\w\s&éüöäáàâèêïíó.]+)?(?=\s*[.;,])', ''),
    # "; he/she/they is/are represented by Gagosian"  (trailing semicolon clause)
    (r';\s*(?:he|she|they)\s+(?:is|are)\s+represented by [A-Z][\w\s&éüöäáàâèêïíó.]+(?=\s*[.])', ''),
    # " He/She is represented by Gallery."  (standalone sentence)
    (r'(?:^|\s)(?:He|She|They)\s+(?:is|are)\s+represented by [A-Z][\w\s&éüöäáàâèêïíó.]+\s*\.\s*', ' '),
    # Drop "is among the youngest artists on the X roster" hedge
    (r'\s+is among the youngest artists on the [A-Z][\w\s&]+ roster[,;]?\s*', ' '),
    # Drop "works in a contemporary register"
    (r"\s+(?:Her|His|Their)?\s*(?:painting|practice|work)s?\s+work\s+in\s+a\s+contemporary\s+register[^.]*\.", '.'),
    # Drop "A fuller account ... awaits ..."
    (r"\s*A fuller account[^.]+awaits[^.]+\.", ''),
]


def main():
    text = MESSAGES_JS.read_text()
    pattern = re.compile(
        r'(    message:\s*")(.+?)(")',
        re.DOTALL,
    )

    changes = 0
    out_chunks = []
    last_end = 0
    for m in pattern.finditer(text):
        prefix, msg, suffix = m.group(1), m.group(2), m.group(3)
        new_msg = msg
        before_len = len(new_msg)
        for pat, rep in REPLACEMENTS:
            new_msg = re.sub(pat, rep, new_msg)
        # Collapse double spaces / leftover punctuation issues
        new_msg = re.sub(r'\s+', ' ', new_msg)
        new_msg = re.sub(r'\s+([.,;:])', r'\1', new_msg)
        new_msg = re.sub(r'\.\s*\.', '.', new_msg)
        new_msg = new_msg.strip()
        if new_msg != msg:
            changes += 1
        out_chunks.append(text[last_end:m.start()])
        out_chunks.append(prefix + new_msg + suffix)
        last_end = m.end()
    out_chunks.append(text[last_end:])

    new_text = ''.join(out_chunks)
    MESSAGES_JS.write_text(new_text)
    print(f'Cleaned up {changes} messages')


if __name__ == '__main__':
    main()
