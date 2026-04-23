#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import browser_cookie3
import requests
from faster_whisper import WhisperModel

PROJECT_DIR = Path('/Users/cicilan/Desktop/partake_notes')
INDEX_PATH = PROJECT_DIR / 'index.html'
TRANSCRIPTS_DIR = PROJECT_DIR / 'transcripts'
SAVE_DIR = Path.home() / 'Desktop' / 'partake_videos'

PATREON_COLLECTION_API = 'https://www.patreon.com/api/collection/1920733?include=posts'
KNOWN_PROCESSED_IDS = {'131069177', '80981674'}  # Zirpslop + Post Internet already in repo

EXTRACTION_PROMPT_PREFIX = (
    'Extract structured notes from this video transcript. Return: key concepts with definitions, '
    'people mentioned with roles and Wikipedia name slugs, books/works referenced with ISBNs if possible, '
    'historical movements or periods with date ranges, and memorable direct quotes.\n'
    'Return only JSON following this schema exactly. Use concise entries and avoid hallucinating details. '
    'Include up to 12 key concepts, 12 people, 8 books/works, 10 movements, and 12 quotes.\n\n'
    'Transcript:\n'
)

SCHEMA: Dict[str, Any] = {
    'type': 'object',
    'properties': {
        'subject_summary': {'type': 'string'},
        'key_concepts': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'definition': {'type': 'string'},
                    'role': {'type': 'string'},
                },
                'required': ['name', 'definition', 'role'],
                'additionalProperties': False,
            },
        },
        'people': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'role': {'type': 'string'},
                    'wiki_slug': {'type': 'string'},
                    'note': {'type': 'string'},
                },
                'required': ['name', 'role', 'wiki_slug', 'note'],
                'additionalProperties': False,
            },
        },
        'books': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'author': {'type': 'string'},
                    'year': {'type': 'string'},
                    'isbn': {'type': 'string'},
                    'note': {'type': 'string'},
                },
                'required': ['title', 'author', 'year', 'isbn', 'note'],
                'additionalProperties': False,
            },
        },
        'movements': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'period': {'type': 'string'},
                    'name': {'type': 'string'},
                    'description': {'type': 'string'},
                },
                'required': ['period', 'name', 'description'],
                'additionalProperties': False,
            },
        },
        'quotes': {'type': 'array', 'items': {'type': 'string'}},
        'tags': {'type': 'array', 'items': {'type': 'string'}},
    },
    'required': ['subject_summary', 'key_concepts', 'people', 'books', 'movements', 'quotes', 'tags'],
    'additionalProperties': False,
}


@dataclass
class PostItem:
    id: str
    title: str
    post_type: str
    post_url: str
    embed_url: str
    duration_seconds: float


@dataclass
class ReportEntry:
    number: int
    filename: str
    title: str
    summary: str
    tags: List[str]
    duration_minutes: int
    concepts: int
    people: int
    books: int
    movements: int
    quotes: int


def slugify(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '_', s)
    s = re.sub(r'_+', '_', s).strip('_')
    return s or 'report'


def normalize_title(title: str) -> str:
    t = title.lower()
    t = t.replace('post-internet', 'post internet')
    t = re.sub(r'[^a-z0-9]+', ' ', t)
    return ' '.join(t.split())


def shell_escape_for_printf(text: str) -> str:
    return text.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$')


def fetch_collection_posts() -> List[PostItem]:
    cookies = browser_cookie3.chrome(domain_name='patreon.com')
    headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.api+json'}
    resp = requests.get(PATREON_COLLECTION_API, cookies=cookies, headers=headers, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    posts: List[PostItem] = []
    for item in data.get('included', []):
        if item.get('type') != 'post':
            continue
        attrs = item.get('attributes', {})
        embed = attrs.get('embed') or {}
        post_file = attrs.get('post_file') or {}
        duration = 0.0
        if isinstance(post_file, dict):
            duration = float(post_file.get('full_content_duration') or post_file.get('duration') or 0.0)
        posts.append(
            PostItem(
                id=str(item.get('id')),
                title=attrs.get('title', '').strip() or f"Post {item.get('id')}",
                post_type=attrs.get('post_type', ''),
                post_url=attrs.get('url', ''),
                embed_url=(embed.get('url', '') if isinstance(embed, dict) else ''),
                duration_seconds=duration,
            )
        )

    posts.sort(key=lambda p: int(p.id), reverse=True)
    return posts


def get_existing_titles_from_html() -> List[str]:
    titles: List[str] = []
    for path in PROJECT_DIR.glob('*.html'):
        if path.name == 'index.html':
            continue
        text = path.read_text(errors='ignore')
        m = re.search(r'<h1 class="header-title">(.*?)</h1>', text, re.DOTALL)
        if m:
            titles.append(normalize_title(html.unescape(m.group(1))))
    return titles


def max_report_number(index_html: str) -> int:
    nums = [int(x) for x in re.findall(r'Report\s+(\d+)', index_html)]
    return max(nums) if nums else 0


def detect_downloaded_file(before: Dict[str, float], after: Dict[str, float], combined_output: str) -> Optional[Path]:
    dest_match = re.findall(r'Destination:\s*(.+)', combined_output)
    if dest_match:
        candidate = Path(dest_match[-1].strip())
        if candidate.exists():
            return candidate

    new_files = []
    for p in SAVE_DIR.glob('*.mp4'):
        mt = p.stat().st_mtime
        if p.name not in before or mt > before[p.name] + 0.5:
            new_files.append((mt, p))
    if new_files:
        new_files.sort(key=lambda t: t[0], reverse=True)
        return new_files[0][1]

    # fallback: latest mp4 in folder
    all_files = [(p.stat().st_mtime, p) for p in SAVE_DIR.glob('*.mp4')]
    if not all_files:
        return None
    all_files.sort(key=lambda t: t[0], reverse=True)
    return all_files[0][1]


def run_download(video_url: str) -> Path:
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    before = {p.name: p.stat().st_mtime for p in SAVE_DIR.glob('*.mp4')}
    escaped = shell_escape_for_printf(video_url)
    cmd = f'printf "{escaped}\\n\\n" | ./download_video.sh'
    proc = subprocess.run(
        ['zsh', '-lc', cmd],
        cwd=PROJECT_DIR,
        text=True,
        capture_output=True,
    )
    combined = (proc.stdout or '') + '\n' + (proc.stderr or '')

    if proc.returncode != 0:
        raise RuntimeError(f'download_video.sh failed for {video_url}\n{combined[-4000:]}')

    downloaded = detect_downloaded_file(before, {p.name: p.stat().st_mtime for p in SAVE_DIR.glob('*.mp4')}, combined)
    if not downloaded:
        raise RuntimeError(f'Could not detect downloaded file for {video_url}')
    return downloaded


def transcribe_with_faster_whisper(video_path: Path, transcript_path: Path) -> None:
    model = WhisperModel('tiny', device='cpu', compute_type='int8')
    segments, _info = model.transcribe(str(video_path), language='en', vad_filter=True)
    with transcript_path.open('w') as f:
        for seg in segments:
            text = (seg.text or '').strip()
            if text:
                f.write(text + ' ')


def run_claude_extraction(transcript_path: Path, notes_path: Path) -> None:
    transcript = transcript_path.read_text(errors='ignore')
    prompt = EXTRACTION_PROMPT_PREFIX + transcript

    cmd = [
        'claude',
        '-p',
        '--output-format',
        'json',
        '--json-schema',
        json.dumps(SCHEMA, separators=(',', ':')),
        '--permission-mode',
        'bypassPermissions',
    ]
    proc = subprocess.run(cmd, input=prompt, text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(f'Claude extraction failed for {transcript_path.name}\n{proc.stderr[-4000:]}')

    payload = json.loads(proc.stdout)
    structured = payload.get('structured_output')
    if not structured:
        raise RuntimeError(f'Claude did not return structured_output for {transcript_path.name}')

    notes_path.write_text(json.dumps(structured, indent=2, ensure_ascii=False))


def ffprobe_duration_minutes(video_path: Path) -> int:
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(video_path),
    ]
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode != 0:
        return 0
    try:
        sec = float(proc.stdout.strip())
        return max(1, round(sec / 60))
    except ValueError:
        return 0


def esc(x: str) -> str:
    return html.escape(x or '', quote=True)


def maybe_wiki_slug(name: str, provided: str) -> str:
    if provided:
        return provided
    if not name:
        return ''
    # fallback slug heuristic
    return re.sub(r'\s+', '_', name.strip())


def clean_isbn(raw: str) -> str:
    if not raw:
        return ''
    digits = re.sub(r'[^0-9Xx]', '', raw)
    return digits


def build_report_html(post: PostItem, notes: Dict[str, Any], report_num: int, duration_minutes: int, filename: str) -> str:
    report_label = f'Report {report_num:02d}'
    page_title = f"{post.title} · partake notes"
    header_title = post.title.upper()
    tags = notes.get('tags') or []
    category = (tags[0] if tags else 'Media Analysis').title()

    concepts_html = []
    for c in notes.get('key_concepts', []):
        concepts_html.append(
            '<div class="concept-card">'
            f'<div class="concept-name">{esc(c.get("name", ""))}</div>'
            f'<div class="concept-body">{esc(c.get("definition", ""))}</div>'
            f'<div class="concept-role">{esc(c.get("role", ""))}</div>'
            '</div>'
        )

    people_html = []
    for p in notes.get('people', []):
        name = p.get('name', '')
        slug = maybe_wiki_slug(name, p.get('wiki_slug', ''))
        wiki_link = f'https://en.wikipedia.org/wiki/{slug}' if slug else ''
        img_attrs = f'class="portrait-img" data-wiki="{esc(slug)}" alt="{esc(name)}"' if slug else f'class="portrait-img" alt="{esc(name)}"'
        wiki_btn = f'<a class="portrait-wiki" href="{esc(wiki_link)}" target="_blank">Wikipedia ↗</a>' if slug else ''
        people_html.append(
            '<div class="portrait-card">'
            '<div class="portrait-img-wrap">'
            f'<img {img_attrs}>'
            '<div class="portrait-placeholder">loading…</div>'
            '</div>'
            '<div class="portrait-info">'
            f'<div class="portrait-name">{esc(name)}</div>'
            f'<div class="portrait-role">{esc(p.get("role", ""))}</div>'
            f'<div class="portrait-body">{esc(p.get("note", ""))}</div>'
            f'{wiki_btn}'
            '</div>'
            '</div>'
        )

    books_html = []
    for b in notes.get('books', []):
        isbn = clean_isbn(b.get('isbn', ''))
        cover_img = (
            f'<img class="book-cover" data-isbn="{esc(isbn)}" alt="{esc(b.get("title", ""))}">'
            if len(isbn) >= 10
            else '<img class="book-cover" alt="">'
        )
        books_html.append(
            '<div class="book-card">'
            '<div class="book-cover-wrap">'
            f'{cover_img}'
            f'<div class="book-cover-placeholder">{esc(b.get("title", ""))}</div>'
            '</div>'
            '<div class="book-info">'
            f'<div class="book-title">{esc(b.get("title", ""))}</div>'
            f'<div class="book-author">{esc((b.get("author", "") + " · " + b.get("year", "")).strip(" ·"))}</div>'
            f'<div class="book-body">{esc(b.get("note", ""))}</div>'
            '</div>'
            '</div>'
        )

    movements_html = []
    for m in notes.get('movements', []):
        movements_html.append(
            '<div class="movement-row">'
            f'<div class="movement-period">{esc(m.get("period", ""))}</div>'
            '<div class="movement-content">'
            f'<div class="movement-name">{esc(m.get("name", ""))}</div>'
            f'<div class="movement-desc">{esc(m.get("description", ""))}</div>'
            '</div>'
            '</div>'
        )

    quotes_html = []
    for q in notes.get('quotes', []):
        quotes_html.append(
            '<div class="quote-item">'
            '<div class="quote-mark">"</div>'
            f'<div class="quote-text">{esc(q)}</div>'
            '</div>'
        )

    nav_links = [
        '<a class="nav-link" href="index.html">home</a>',
        '<a class="nav-link" href="zerp_slop.html">zerp slop</a>',
        '<a class="nav-link" href="post_internet.html">post-internet</a>',
        f'<a class="nav-link active" href="{esc(filename)}">{esc(slugify(post.title).replace("_", " "))}</a>',
    ]

    html_doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(page_title)}</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="shared.css">
</head>
<body>

<nav class="site-nav">
  <a class="nav-logo" href="index.html">partake</a>
  <div class="nav-links">
    {''.join(nav_links)}
  </div>
</nav>

<header class="page-header">
  <div class="header-eyebrow">{esc(report_label)} · 2026 · {esc(category)}</div>
  <h1 class="header-title">{esc(header_title)}</h1>
  <p class="header-subject">{esc(notes.get('subject_summary', ''))}</p>
  <div class="header-meta">
    <span>⏱ ~{duration_minutes} min</span>
    <span>✦ Brad Troemel</span>
    <span>📍 Patreon</span>
  </div>
</header>

<div class="page-body">

  <section>
    <div class="section-label">Key Concepts</div>
    <div class="concepts-grid">{''.join(concepts_html)}</div>
  </section>

  <section>
    <div class="section-label">People Mentioned</div>
    <div class="portraits-grid">{''.join(people_html)}</div>
  </section>

  <section>
    <div class="section-label">Books & Works Referenced</div>
    {''.join(books_html) if books_html else '<div class="concept-card"><div class="concept-body">No books or works were clearly identified in this transcript.</div></div>'}
  </section>

  <section>
    <div class="section-label">Movements & Periods</div>
    <div class="movements-list">{''.join(movements_html)}</div>
  </section>

  <section>
    <div class="section-label">Memorable Quotes</div>
    <div class="quotes-list">{''.join(quotes_html)}</div>
  </section>

</div>

<footer class="site-footer">
  partake · notes · <a href="index.html">← back to home</a> · images via wikimedia commons · open library
</footer>

<script>
async function loadWikiImage(img) {{
  try {{
    if (!img.dataset.wiki) return;
    const res = await fetch(`https://en.wikipedia.org/api/rest_v1/page/summary/${{img.dataset.wiki}}`);
    const data = await res.json();
    if (data.thumbnail?.source) {{
      img.src = data.thumbnail.source;
      img.onload = () => {{ img.classList.add('loaded'); img.nextElementSibling.style.display = 'none'; }};
    }}
  }} catch(e) {{}}
}}
async function loadBookCover(img) {{
  if (!img.dataset.isbn) return;
  img.src = `https://covers.openlibrary.org/b/isbn/${{img.dataset.isbn}}-M.jpg?default=false`;
  img.onload = () => {{ img.classList.add('loaded'); if (img.nextElementSibling) img.nextElementSibling.style.display = 'none'; }};
  img.onerror = () => {{}};
}}
document.querySelectorAll('.portrait-img[data-wiki]').forEach(loadWikiImage);
document.querySelectorAll('.book-cover[data-isbn]').forEach(loadBookCover);
</script>
</body>
</html>
'''
    return html_doc


def build_report_card(entry: ReportEntry) -> str:
    tags = entry.tags[:5]
    tag_html = ''.join(f'<span class="report-tag">{esc(t.lower())}</span>' for t in tags)
    return f'''

    <a class="report-card" href="{esc(entry.filename)}">
      <div class="report-card-header">
        <div class="report-number">Report {entry.number:02d} · 2026</div>
        <div class="report-title">{esc(entry.title.upper())}</div>
      </div>
      <div class="report-body">
        <p class="report-subject">{esc(entry.summary)}</p>
        <div class="report-stats">
          <div class="report-stat"><strong>{entry.concepts}</strong> key concepts</div>
          <div class="report-stat"><strong>{entry.people}</strong> people</div>
          <div class="report-stat"><strong>{entry.books}</strong> books</div>
          <div class="report-stat"><strong>{entry.movements}</strong> movements</div>
          <div class="report-stat"><strong>{entry.quotes}</strong> quotes</div>
        </div>
        <div class="report-tags">{tag_html}</div>
      </div>
      <div class="report-footer">
        <span>Brad Troemel · Patreon · ~{entry.duration_minutes} min</span>
        <span>open →</span>
      </div>
    </a>
'''


def update_index(entries: List[ReportEntry]) -> None:
    if not entries:
        return

    index_html = INDEX_PATH.read_text()

    nav_insert = ''.join(
        f'\n    <a class="nav-link" href="{esc(e.filename)}">{esc(slugify(e.title).replace("_", " "))}</a>'
        for e in entries
    )
    index_html = index_html.replace('    <a class="nav-link" href="post_internet.html">post-internet</a>', '    <a class="nav-link" href="post_internet.html">post-internet</a>' + nav_insert)

    cards_html = ''.join(build_report_card(e) for e in entries)
    grid_close = '  </div>\n</div>\n\n<footer class="site-footer">'
    index_html = index_html.replace(
        grid_close,
        cards_html + '\n\n  </div>\n</div>\n\n<footer class="site-footer">',
        1,
    )

    INDEX_PATH.write_text(index_html)


def main() -> None:
    TRANSCRIPTS_DIR.mkdir(exist_ok=True)
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

    posts = fetch_collection_posts()
    existing_titles = set(get_existing_titles_from_html())
    index_html = INDEX_PATH.read_text()
    next_report_number = max_report_number(index_html) + 1

    new_entries: List[ReportEntry] = []

    for post in posts:
        normalized = normalize_title(post.title)
        slug = slugify(post.title)
        html_filename = f'{slug}.html'
        html_path = PROJECT_DIR / html_filename
        transcript_path = TRANSCRIPTS_DIR / f'{slug}_transcript.txt'
        notes_path = TRANSCRIPTS_DIR / f'{slug}_notes.json'

        if post.id in KNOWN_PROCESSED_IDS:
            continue
        if normalized in existing_titles or html_path.exists():
            continue

        print(f'Processing {post.id} :: {post.title}')

        source_url = post.post_url
        if post.post_type == 'video_embed' and post.embed_url:
            source_url = post.embed_url

        downloaded_video: Optional[Path] = None
        if not transcript_path.exists() or transcript_path.stat().st_size == 0:
            try:
                downloaded_video = run_download(source_url)
            except Exception as e:
                print(f'  Download failed for {post.title}: {e}')
                continue

        try:
            if not transcript_path.exists() or transcript_path.stat().st_size == 0:
                print(f'  Transcribing -> {transcript_path.name}')
                if downloaded_video is None:
                    # Shouldn't happen, but keep a safe guard.
                    downloaded_video = run_download(source_url)
                transcribe_with_faster_whisper(downloaded_video, transcript_path)
            else:
                print(f'  Transcript exists, skipping: {transcript_path.name}')
        except Exception as e:
            print(f'  Transcription failed for {post.title}: {e}')
            continue

        try:
            if not notes_path.exists() or notes_path.stat().st_size == 0:
                print(f'  Extracting notes with Claude -> {notes_path.name}')
                run_claude_extraction(transcript_path, notes_path)
            else:
                print(f'  Notes exist, skipping: {notes_path.name}')
        except Exception as e:
            print(f'  Claude extraction failed for {post.title}: {e}')
            continue

        try:
            notes = json.loads(notes_path.read_text())
        except Exception as e:
            print(f'  Could not read notes JSON for {post.title}: {e}')
            continue

        duration_minutes = ffprobe_duration_minutes(downloaded_video) if downloaded_video else 0
        if duration_minutes <= 0 and post.duration_seconds > 0:
            duration_minutes = max(1, round(post.duration_seconds / 60))

        report_number = next_report_number
        next_report_number += 1

        report_html = build_report_html(post, notes, report_number, duration_minutes, html_filename)
        html_path.write_text(report_html)

        entry = ReportEntry(
            number=report_number,
            filename=html_filename,
            title=post.title,
            summary=notes.get('subject_summary', ''),
            tags=notes.get('tags', []),
            duration_minutes=duration_minutes,
            concepts=len(notes.get('key_concepts', [])),
            people=len(notes.get('people', [])),
            books=len(notes.get('books', [])),
            movements=len(notes.get('movements', [])),
            quotes=len(notes.get('quotes', [])),
        )
        new_entries.append(entry)
        print(f'  Built report: {html_filename} (Report {report_number:02d})')

    update_index(new_entries)
    print(f'\nDone. Added {len(new_entries)} new report(s).')


if __name__ == '__main__':
    main()
