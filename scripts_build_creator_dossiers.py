from pathlib import Path
from urllib.parse import quote_plus
import json
import re
import html

ROOT = Path('/Users/cicilan/Desktop/partake_notes')
TRANSCRIPTS = ROOT / 'transcripts'
CREATOR_DIR = ROOT / 'creator_notes'
CONTENT_DIR = ROOT / 'content' / 'creator_dossiers'
CONTENT_DIR.mkdir(parents=True, exist_ok=True)

ROLE_RULES = [
    (('creative','creativity','idea','ideas','pitch','research','mood board','moodboard','inspiration','taste','juxtaposition','friction','design'), 'creative practice'),
    (('surveillance','camera','cameras','police','flock','privacy','data broker','government','4th amendment','city council','foia'), 'surveillance / civic power'),
    (('money','stocks','currency','finance','wealth','rich','capital','class','housing','salary','tax','earn','income','affluence'), 'money / class'),
    (('identity','gender','woman','girl','boyfriend','body','self','dating','beauty'), 'identity scripts'),
    (('brand','marketing','logo','product','campaign','advertis','consumer','company'), 'brand systems'),
    (('city','cities','place','suburb','borough','district','neighborhood','map','paris','montreal','singapore','baltimore','geography'), 'place names / geography'),
    (('brain','medicine','science','species','fish','birds','flowers','trees','butterflies','taxonomy','botany','anatomy'), 'classification systems'),
    (('book','read','essay','journal','study','research','theory','philosophy'), 'research / theory'),
    (('ai','algorithm','platform','internet','tiktok','instagram','social media','creator','content','meme'), 'platform behavior'),
    (('art','artist','museum','gallery','design','aesthetic','architecture','visual','style','fashion','typeface','font','film','anime'), 'visual culture'),
    (('food','restaurant','spices','candy','cuisine','cooking'), 'food culture'),
    (('language','word','etymolog','linguistic','name','algospeak','phrase','slang'), 'language systems'),
]

STOP = set('the a an and or but to of in on for with by from is are was were be been being it this that as at into about not your you we they he she i our their his her its'.split())


def words(text):
    return re.findall(r"[A-Za-z][A-Za-z'\-]+", text)


def clean_text(s):
    s = html.unescape(s or '')
    s = s.replace('\u200b', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def smart_trim(text, max_words=48):
    toks = text.split()
    if len(toks) <= max_words:
        return text
    return ' '.join(toks[:max_words]).rstrip(' ,;:') + '...'


def split_sentences(text):
    text = clean_text(text)
    if not text:
        return []
    rough = re.split(r'(?<=[.!?])\s+', text)
    out = []
    for s in rough:
        s = s.strip()
        if 8 <= len(s.split()) <= 70:
            out.append(s)
    if not out and text:
        out = [smart_trim(text, 45)]
    return out



def clean_title(raw, fallback_id):
    raw = clean_text(raw)
    raw = re.sub(r'#\w+', '', raw)
    raw = re.sub(r'@[\w.]+', '', raw)
    raw = re.sub(r'\s+', ' ', raw).strip(' -–—|.,')
    if not raw:
        return f'Source clip {fallback_id}'
    return smart_trim(raw, 18)

def role_for(text):
    low = text.lower()
    for needles, role in ROLE_RULES:
        if any(n in low for n in needles):
            return role
    return 'source material'


def parse_captions(path):
    if not path.exists():
        return []
    posts = []
    current = None
    pat = re.compile(r'^([^|\s][^|]{2,80}?) \| (.*?) \| (.*)$')
    for line in path.read_text(errors='replace').splitlines():
        m = pat.match(line)
        if m:
            if current:
                posts.append(current)
            current = {'id': m.group(1).strip(), 'title': clean_text(m.group(2)), 'lines': [m.group(3).strip()] if m.group(3).strip() else []}
        elif current and line.strip():
            current['lines'].append(line.strip())
    if current:
        posts.append(current)
    for p in posts:
        p['text'] = clean_text(' '.join(p.pop('lines')))
        p['hashtags'] = re.findall(r'#([\w]+)', p['text'])
    return posts


def parse_transcript(path):
    if not path.exists():
        return []
    text = path.read_text(errors='replace')
    pat = re.compile(r'^\[([^\]]+)\]\s*$', re.M)
    matches = list(pat.finditer(text))
    clips = []
    if not matches:
        if clean_text(text):
            clips.append({'id':'transcript', 'text': clean_text(text), 'source_type':'transcript'})
        return clips
    for i,m in enumerate(matches):
        start = m.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        cid = m.group(1).replace('.mp4','').strip()
        body = clean_text(text[start:end])
        if body:
            clips.append({'id':cid, 'text':body, 'source_type':'transcript'})
    return clips


def load_json(path):
    if path.exists():
        try:
            return json.loads(path.read_text(errors='replace'))
        except Exception:
            return {}
    return {}


def concept_map(notes_json):
    out = {}
    for c in notes_json.get('key_concepts', []) or []:
        name = c.get('name')
        for pid in c.get('via_posts', []) or []:
            out.setdefault(pid, []).append(name)
    return out


def top_terms(text, limit=5):
    counts = {}
    for w in words(text.lower()):
        if len(w) < 4 or w in STOP:
            continue
        counts[w] = counts.get(w, 0) + 1
    return [w for w,_ in sorted(counts.items(), key=lambda kv:(-kv[1], kv[0]))[:limit]]


def best_excerpt(text):
    sentences = split_sentences(text)
    if not sentences:
        return ''
    cues = ['because','the reality','what happens','the point','i think','this is','that means','so instead','the lesson','the question','but']
    scored = []
    for i,s in enumerate(sentences[:18]):
        low=s.lower()
        score = 0
        score += max(0, 8 - i)
        score += sum(3 for c in cues if c in low)
        score += 2 if any(ch.isdigit() for ch in s) else 0
        score += 2 if '?' in s else 0
        score -= 3 if len(s.split()) < 12 else 0
        scored.append((score,s))
    return smart_trim(max(scored, key=lambda x:x[0])[1], 42)


def make_summary(title, text, concepts):
    title = clean_text(title)
    sentences = split_sentences(text)
    if concepts:
        lead = f"Develops {', '.join(concepts[:2])}"
    else:
        lead = f"Develops a {role_for(title + ' ' + text)} thread"
    if sentences:
        setup = smart_trim(sentences[0], 28)
        return f"{lead} through this source: {setup}"
    return f"{lead} through a source post whose caption/title carries the core example."


def why_matters(text, concepts, curation_ideas):
    if concepts:
        return f"This gives the page primary-source backing for {', '.join(concepts[:3])}, turning the concept from a label into an actual clip-level argument."
    terms = top_terms(text, 4)
    if terms:
        return f"This adds texture around {', '.join(terms)}, showing a recurring concern that was easy to flatten in the shorter notes."
    if curation_ideas:
        return f"This supports the creator's broader thesis: {curation_ideas[0]}"
    return "This preserves source texture that was missing from the compressed summary page."


def pick_items(handle, captions, transcript_clips, notes_json, curation_json, limit=8):
    cap_by_id = {p['id']:p for p in captions}
    cmap = concept_map(notes_json)
    distinct = curation_json.get('distinct_post_ids', []) or []
    pool = []
    clip_by_id = {c['id']:c for c in transcript_clips}
    all_ids = []
    for pid in distinct:
        if pid not in all_ids:
            all_ids.append(pid)
    for c in transcript_clips:
        if c['id'] not in all_ids:
            all_ids.append(c['id'])
    for p in captions:
        if p['id'] not in all_ids:
            all_ids.append(p['id'])
    for pid in all_ids:
        cap = cap_by_id.get(pid, {})
        clip = clip_by_id.get(pid)
        source_text = clip['text'] if clip else cap.get('text','')
        title = cap.get('title') or (split_sentences(source_text)[0] if source_text else pid)
        title = clean_title(title, pid)
        concepts = cmap.get(pid, [])
        text_for_score = title + ' ' + source_text + ' ' + cap.get('text','')
        score = 0
        score += 10 if pid in distinct else 0
        score += min(8, len(source_text.split())//80) if clip else 0
        score += 5 if concepts else 0
        score += 3 if cap.get('hashtags') else 0
        score += 2 if role_for(text_for_score) != 'source material' else 0
        pool.append((score, pid, title, source_text or cap.get('text',''), cap, bool(clip), concepts))
    pool.sort(key=lambda x: -x[0])
    selected = []
    seen = set()
    roles = set()
    for item in pool:
        _, pid, title, text, cap, has_transcript, concepts = item
        if pid in seen or not clean_text(title + ' ' + text):
            continue
        role = role_for(title + ' ' + text)
        if len(selected) < 5 or role not in roles or len(selected) < limit:
            selected.append(item)
            seen.add(pid)
            roles.add(role)
        if len(selected) >= limit:
            break
    selected.sort(key=lambda x: all_ids.index(x[1]) if x[1] in all_ids else 999)
    ideas = curation_json.get('key_ideas', []) or []
    dossiers = []
    for n,item in enumerate(selected,1):
        _, pid, title, text, cap, has_transcript, concepts = item
        tags = cap.get('hashtags', [])[:5]
        source_type = 'transcript + caption' if has_transcript and cap else ('transcript' if has_transcript else 'caption')
        dossiers.append({
            'id': pid,
            'title': title,
            'url': f'https://www.instagram.com/reel/{quote_plus(pid)}/',
            'source_type': source_type,
            'word_count': len(words(text)),
            'concepts': concepts,
            'role': role_for(title + ' ' + text),
            'summary': make_summary(title, text, concepts),
            'source_excerpt': best_excerpt(text),
            'why_it_matters': why_matters(text, concepts, ideas),
            'tags': tags,
        })
    return dossiers


def dossier_html(handle, dossiers):
    cards=[]
    for i,d in enumerate(dossiers,1):
        concepts = ''.join(f'<span>{html.escape(c)}</span>' for c in d['concepts'][:3])
        tags = ''.join(f'<span>#{html.escape(t)}</span>' for t in d['tags'][:4])
        excerpt = f'<blockquote>{html.escape(d["source_excerpt"])}</blockquote>' if d['source_excerpt'] else ''
        cards.append(f'''<article class="clip-dossier-card" id="clip-{html.escape(d['id'])}">
          <div class="clip-dossier-topline"><span>{i:02d}</span><a href="{html.escape(d['url'])}" target="_blank" rel="noopener">{html.escape(d['id'])}</a><em>{html.escape(d['source_type'])} · {d['word_count']}w</em></div>
          <h3>{html.escape(d['title'])}</h3>
          <p>{html.escape(d['summary'])}</p>
          {excerpt}
          <p class="clip-dossier-why">{html.escape(d['why_it_matters'])}</p>
          <div class="clip-dossier-tags">{concepts}{tags}<span>{html.escape(d['role'])}</span></div>
        </article>''')
    return f'''  <section id="clip-dossiers" class="clip-dossiers-section">
    <div class="section-label">Clip Dossiers</div>
    <div class="clip-dossiers-intro">
      <p>These cards go back to the raw transcript and caption material. They are intentionally fuller than the concept library: each one keeps the source clip visible, names what it contributes, and preserves a short line from the material without turning the page into a transcript dump.</p>
    </div>
    <div class="clip-dossier-grid">{''.join(cards)}</div>
  </section>
'''

index=[]
changed=0
for page in sorted(CREATOR_DIR.glob('*.html')):
    handle=page.stem
    captions=parse_captions(TRANSCRIPTS/f'{handle}_captions.txt')
    clips=parse_transcript(TRANSCRIPTS/f'{handle}_transcript.txt')
    notes=load_json(TRANSCRIPTS/f'{handle}_notes.json')
    curation=load_json(TRANSCRIPTS/f'{handle}_curation.json')
    dossiers=pick_items(handle,captions,clips,notes,curation,limit=8)
    payload={
        'handle': handle,
        'source_counts': {'captions': len(captions), 'transcript_clips': len(clips)},
        'dossiers': dossiers,
    }
    (CONTENT_DIR/f'{handle}.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    index.append({'handle':handle, **payload['source_counts'], 'dossiers':len(dossiers)})
    section=dossier_html(handle,dossiers)
    text=page.read_text(errors='replace')
    original=text
    text=re.sub(r'shared\.css\?v=creator-notes-guided-\d+', 'shared.css?v=creator-notes-guided-9', text)
    if '<section id="clip-dossiers"' in text:
        text=re.sub(r'  <section id="clip-dossiers" class="clip-dossiers-section">.*?\n  </section>\n', section, text, count=1, flags=re.S)
    elif '  <section id="concepts">' in text:
        text=text.replace('  <section id="concepts">', section+'  <section id="concepts">', 1)
    else:
        print('WARN no insert marker', handle)
    if text != original:
        page.write_text(text)
        changed += 1

(ROOT/'content'/'creator_dossier_index.json').write_text(json.dumps(index, ensure_ascii=False, indent=2))
print(f'wrote {len(index)} dossier files; changed {changed} html pages')
