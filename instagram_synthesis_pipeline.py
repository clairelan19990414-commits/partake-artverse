#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
import textwrap
import fcntl
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import browser_cookie3
import requests

ROOT = Path('/Users/cicilan/Desktop/partake_notes')
TRANSCRIPTS_DIR = ROOT / 'transcripts'
ASSETS_DIR = ROOT / 'assets'
INDEX_PATH = ROOT / 'index.html'
SHARED_CSS = ROOT / 'shared.css'
VIDEOS_ROOT = Path.home() / 'Desktop' / 'partake_videos'
COOKIE_CACHE_PATH = TRANSCRIPTS_DIR / 'instagram_cookie_cache.json'
LOCK_PATH = ROOT / '.instagram_pipeline.lock'

HANDLES: List[str] = [
    'eugbrandstrat', 'etymologynerd', 'willfrancis', 'fakeplasticbrands',
    'kaburbank', 'lhuijuni.ldn', 'davidkylechoe', 'maalivikabhat',
    'didoriot', 'h_miller76', 'bjornd.al', 'sihaam', 'musingsofacrouton',
    'codebynordveritas', 'fastfoodledgendofficial', 'eyes_of_apoorva',
    'maryisalien', 'kai_rehagen', 'bubsonline', 'g.a.works', 'itsvicchang',
    'culturalfingerprints', 'noteswnat', 'dan_dug_', 'aidanetcetera',
    'thewaronbeauty', 'andreyazizov', 'stylebykvn', 'vinny_creative',
]

# requested 30 handles include this one too; preserve explicit queue ordering
EXTRA_HANDLE = 'art_lust'
if EXTRA_HANDLE not in HANDLES:
    HANDLES.insert(24, EXTRA_HANDLE)

CURATION_SCHEMA: Dict[str, Any] = {
    'type': 'object',
    'properties': {
        'core_thesis': {'type': 'string'},
        'content_type': {
            'type': 'string',
            'enum': [
                'talking-head/spoken',
                'visual-reference heavy',
                'caption-text heavy',
            ],
        },
        'distinct_post_ids': {
            'type': 'array',
            'items': {'type': 'string'},
            'minItems': 5,
            'maxItems': 8,
        },
        'key_ideas': {
            'type': 'array',
            'items': {'type': 'string'},
            'minItems': 5,
            'maxItems': 8,
        },
    },
    'required': ['core_thesis', 'content_type', 'distinct_post_ids', 'key_ideas'],
    'additionalProperties': False,
}

NOTES_SCHEMA: Dict[str, Any] = {
    'type': 'object',
    'properties': {
        'creator_thesis': {'type': 'string'},
        'key_concepts': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'definition': {'type': 'string'},
                    'via_posts': {'type': 'array', 'items': {'type': 'string'}},
                },
                'required': ['name', 'definition', 'via_posts'],
                'additionalProperties': False,
            },
            'minItems': 5,
            'maxItems': 8,
        },
        'references': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'type': {'type': 'string'},
                    'referenced_in': {'type': 'array', 'items': {'type': 'string'}},
                },
                'required': ['name', 'type', 'referenced_in'],
                'additionalProperties': False,
            },
        },
        'positions': {
            'type': 'array',
            'items': {'type': 'string'},
            'minItems': 3,
            'maxItems': 5,
        },
        'tags': {
            'type': 'array',
            'items': {'type': 'string'},
            'minItems': 2,
            'maxItems': 3,
        },
    },
    'required': ['creator_thesis', 'key_concepts', 'references', 'positions', 'tags'],
    'additionalProperties': False,
}

SYNTHESIS_SCHEMA: Dict[str, Any] = {
    'type': 'object',
    'properties': {
        'clusters': {
            'type': 'array',
            'minItems': 3,
            'maxItems': 5,
            'items': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'slug': {'type': 'string'},
                    'description': {'type': 'string'},
                    'creators': {'type': 'array', 'items': {'type': 'string'}, 'minItems': 3},
                    'shared_ideas': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'name': {'type': 'string'},
                                'definition': {'type': 'string'},
                                'via_handles': {'type': 'array', 'items': {'type': 'string'}},
                            },
                            'required': ['name', 'definition', 'via_handles'],
                            'additionalProperties': False,
                        },
                        'minItems': 3,
                        'maxItems': 5,
                    },
                    'tensions': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'tension': {'type': 'string'},
                                'side_a': {'type': 'string'},
                                'side_b': {'type': 'string'},
                            },
                            'required': ['tension', 'side_a', 'side_b'],
                            'additionalProperties': False,
                        },
                        'minItems': 1,
                        'maxItems': 2,
                    },
                    'voices': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'handle': {'type': 'string'},
                                'quote': {'type': 'string'},
                            },
                            'required': ['handle', 'quote'],
                            'additionalProperties': False,
                        },
                    },
                    'references': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'name': {'type': 'string'},
                                'type': {'type': 'string'},
                                'referenced_by': {'type': 'array', 'items': {'type': 'string'}},
                            },
                            'required': ['name', 'type', 'referenced_by'],
                            'additionalProperties': False,
                        },
                    },
                    'is_visual_heavy': {'type': 'boolean'},
                },
                'required': [
                    'name', 'slug', 'description', 'creators', 'shared_ideas',
                    'tensions', 'voices', 'references', 'is_visual_heavy',
                ],
                'additionalProperties': False,
            },
        },
        'cross_cutting_themes': {'type': 'array', 'items': {'type': 'string'}},
    },
    'required': ['clusters', 'cross_cutting_themes'],
    'additionalProperties': False,
}


@dataclass
class HandleResult:
    handle: str
    ok: bool
    reason: str
    content_type: str = ''
    harvested: int = 0
    downloaded: int = 0


class RateLimitError(RuntimeError):
    pass


class AuthError(RuntimeError):
    pass


class SingleRunLock:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.fd: Optional[int] = None

    def __enter__(self) -> "SingleRunLock":
        self.fd = os.open(self.path, os.O_CREAT | os.O_RDWR, 0o644)
        try:
            fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise RuntimeError(f'Another pipeline run is already active ({self.path}).')
        os.ftruncate(self.fd, 0)
        os.write(self.fd, str(os.getpid()).encode('utf-8'))
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if self.fd is None:
            return
        try:
            fcntl.flock(self.fd, fcntl.LOCK_UN)
        finally:
            os.close(self.fd)
            self.fd = None


def _save_cookie_cache(cookiejar: Any) -> None:
    records: List[Dict[str, Any]] = []
    for c in cookiejar:
        records.append(
            {
                'name': c.name,
                'value': c.value,
                'domain': c.domain,
                'path': c.path or '/',
                'secure': bool(c.secure),
                'expires': c.expires,
            }
        )
    if not records:
        return
    COOKIE_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    COOKIE_CACHE_PATH.write_text(json.dumps(records, indent=2))


def _load_cookie_cache() -> Optional[requests.cookies.RequestsCookieJar]:
    if not COOKIE_CACHE_PATH.exists():
        return None
    try:
        records = json.loads(COOKIE_CACHE_PATH.read_text())
    except Exception:
        return None
    if not isinstance(records, list) or not records:
        return None
    jar = requests.cookies.RequestsCookieJar()
    for c in records:
        if not isinstance(c, dict):
            continue
        name = c.get('name')
        value = c.get('value')
        if not name or value is None:
            continue
        jar.set(
            name,
            value,
            domain=c.get('domain'),
            path=c.get('path', '/'),
            secure=bool(c.get('secure', False)),
            expires=c.get('expires'),
        )
    return jar if len(jar) > 0 else None


def load_instagram_cookies() -> requests.cookies.RequestsCookieJar:
    try:
        fresh = browser_cookie3.chrome(domain_name='instagram.com')
        jar = requests.cookies.RequestsCookieJar()
        for c in fresh:
            jar.set(c.name, c.value, domain=c.domain, path=c.path or '/', secure=bool(c.secure), expires=c.expires)
        if len(jar) > 0:
            _save_cookie_cache(fresh)
            return jar
    except Exception:
        pass

    cached = _load_cookie_cache()
    if cached is not None:
        return cached
    raise RuntimeError(
        'Instagram cookies unavailable. Unlock Keychain/Chrome once to refresh session cache.'
    )


def ensure_claude_ready() -> None:
    cmd = [
        'claude',
        '-p',
        'ping',
        '--output-format',
        'json',
        '--permission-mode',
        'bypassPermissions',
    ]
    proc = subprocess.run(cmd, text=True, capture_output=True)
    payload: Dict[str, Any] = {}
    raw = (proc.stdout or '').strip()
    if raw:
        try:
            payload = json.loads(raw)
        except Exception:
            payload = {}

    if proc.returncode != 0 or payload.get('is_error'):
        status = payload.get('api_error_status')
        msg = str(payload.get('result') or payload.get('error') or proc.stderr or '').strip()
        lowered = msg.lower()
        if 'not logged in' in lowered or '/login' in lowered:
            raise AuthError('Claude CLI not logged in. Run: claude /login')
        if status == 429 or 'hit your limit' in lowered or 'resets' in lowered:
            raise RateLimitError(msg or 'Claude rate limited')
        raise RuntimeError(f'Claude preflight failed: {msg or "unknown error"}')


class InstagramClient:
    def __init__(self) -> None:
        self.s = requests.Session()
        self.s.cookies = load_instagram_cookies()
        self.s.headers.update({
            'User-Agent': 'Mozilla/5.0',
            'X-IG-App-ID': '936619743392459',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/',
            'Accept': 'application/json',
        })

    def get_profile(self, handle: str) -> Dict[str, Any]:
        r = self.s.get(
            f'https://www.instagram.com/api/v1/users/web_profile_info/?username={handle}',
            timeout=30,
        )
        if r.status_code != 200:
            raise RuntimeError(f'profile status {r.status_code}')
        obj = r.json()
        user = obj.get('data', {}).get('user')
        if not user:
            raise RuntimeError('missing user payload')
        return user

    def get_items(self, user_id: str, limit: int = 40) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        seen: set[str] = set()
        max_id: Optional[str] = None

        while len(out) < limit:
            params: Dict[str, Any] = {'count': 12}
            if max_id:
                params['max_id'] = max_id
            r = self.s.get(f'https://www.instagram.com/api/v1/feed/user/{user_id}/', params=params, timeout=30)
            if r.status_code != 200:
                break
            obj = r.json()
            batch = obj.get('items') or []
            if not batch:
                break
            for item in batch:
                code = item.get('code')
                if not code or code in seen:
                    continue
                seen.add(code)
                out.append(item)
                if len(out) >= limit:
                    break
            if not obj.get('more_available'):
                break
            max_id = obj.get('next_max_id')
            if not max_id:
                break

        return out[:limit]



def slugify(text: str) -> str:
    s = re.sub(r'[^a-z0-9]+', '_', text.lower()).strip('_')
    return re.sub(r'_+', '_', s) or 'cluster'



def esc(text: str) -> str:
    return (
        str(text or '')
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
    )



def item_caption(item: Dict[str, Any]) -> str:
    cap = item.get('caption')
    if isinstance(cap, dict):
        return (cap.get('text') or '').strip()
    return ''



def item_title(item: Dict[str, Any]) -> str:
    caption = item_caption(item)
    if not caption:
        return item.get('code') or 'Untitled'
    first = caption.split('\n', 1)[0].strip()
    first = re.sub(r'\s+', ' ', first)
    return first[:90]



def item_video_url(item: Dict[str, Any]) -> Optional[str]:
    vv = item.get('video_versions') or []
    if vv:
        return vv[0].get('url')
    carousel = item.get('carousel_media') or []
    for c in carousel:
        v2 = c.get('video_versions') or []
        if v2:
            return v2[0].get('url')
    return None



def save_caption_file(handle: str, items: List[Dict[str, Any]]) -> Path:
    out = TRANSCRIPTS_DIR / f'{handle}_captions.txt'
    lines: List[str] = []
    for item in items:
        code = item.get('code', '')
        title = item_title(item).replace('|', ' ')
        desc = item_caption(item).replace('|', ' ')
        lines.append(f'{code} | {title} | {desc}')
    out.write_text('\n'.join(lines) + ('\n' if lines else ''))
    return out



def run_claude_json(prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
    cmd = [
        'claude', '-p',
        '--output-format', 'json',
        '--json-schema', json.dumps(schema, separators=(',', ':')),
        '--permission-mode', 'bypassPermissions',
    ]
    try:
        proc = subprocess.run(cmd, input=prompt, text=True, capture_output=True, timeout=1200)
    except subprocess.TimeoutExpired:
        raise RuntimeError('Claude request timed out')
    payload: Dict[str, Any] = {}
    raw_out = (proc.stdout or '').strip()
    if raw_out:
        try:
            payload = json.loads(raw_out)
        except Exception:
            payload = {}

    if proc.returncode != 0 or payload.get('is_error'):
        status = payload.get('api_error_status')
        result_msg = str(payload.get('result') or payload.get('error') or '')
        stderr = (proc.stderr or '')[-2000:]
        combo = f'{result_msg} {stderr}'.lower()
        if 'not logged in' in combo or '/login' in combo:
            raise AuthError('Claude CLI not logged in. Run: claude /login')
        if status == 429 or 'hit your limit' in combo or 'resets' in combo:
            raise RateLimitError(result_msg or 'Claude rate limited')
        raise RuntimeError(f'Claude error: {result_msg or stderr}')

    if not payload:
        raise RuntimeError('Claude returned no JSON payload')
    structured = payload.get('structured_output')
    if not structured:
        raise RuntimeError('Claude missing structured_output')
    return structured



def format_curation_text(handle: str, cur: Dict[str, Any]) -> str:
    ids = '\n'.join(f'- {x}' for x in cur.get('distinct_post_ids', []))
    ideas = '\n'.join(f'- {x}' for x in cur.get('key_ideas', []))
    return textwrap.dedent(f'''\
    @{handle} curation

    Core thesis:
    {cur.get('core_thesis', '').strip()}

    Classification:
    {cur.get('content_type', '').strip()}

    Distinct post IDs:
    {ids}

    Key ideas:
    {ideas}
    ''').strip() + '\n'



def classify(cur: Dict[str, Any]) -> str:
    v = (cur.get('content_type') or '').lower()
    if 'talking' in v or 'spoken' in v:
        return 'talking'
    if 'visual' in v:
        return 'visual'
    return 'caption'



def ensure_downloads(handle: str, selected_codes: List[str], item_map: Dict[str, Dict[str, Any]]) -> int:
    out_dir = VIDEOS_ROOT / handle
    out_dir.mkdir(parents=True, exist_ok=True)
    downloaded = 0

    for code in selected_codes:
        item = item_map.get(code)
        if not item:
            continue
        url = item_video_url(item)
        if not url:
            continue
        out_path = out_dir / f'{code}.mp4'
        if out_path.exists() and out_path.stat().st_size > 1024 * 100:
            downloaded += 1
            continue
        with requests.get(url, stream=True, timeout=120) as r:
            if r.status_code != 200:
                continue
            with out_path.open('wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 512):
                    if chunk:
                        f.write(chunk)
        if out_path.exists() and out_path.stat().st_size > 1024 * 100:
            downloaded += 1
    return downloaded



def run_transcription(handle: str) -> None:
    try:
        proc = subprocess.run(
            ['bash', 'transcribe_instagram.sh', handle],
            cwd=ROOT,
            check=False,
            timeout=7200,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(f'transcription timed out for @{handle}')
    transcript = TRANSCRIPTS_DIR / f'{handle}_transcript.txt'
    if proc.returncode != 0 or not transcript.exists() or transcript.stat().st_size == 0:
        raise RuntimeError(f'transcription failed for @{handle}')



def extract_frames(handle: str) -> List[Path]:
    out_assets = ASSETS_DIR / handle
    out_assets.mkdir(parents=True, exist_ok=True)
    frames: List[Path] = []
    handle_dir = VIDEOS_ROOT / handle
    for mp4 in sorted(handle_dir.glob('*.mp4')):
        base = mp4.stem
        cmd = [
            'ffmpeg', '-y', '-i', str(mp4),
            '-vf', 'select=eq(n\\,30)+eq(n\\,90)+eq(n\\,150)',
            '-vsync', '0',
            str(out_assets / f'{base}_%d.jpg'),
        ]
        subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for p in sorted(out_assets.glob('*.jpg')):
        frames.append(p)
    return frames



def read_transcript_excerpt(handle: str, max_chars: int = 45000) -> str:
    p = TRANSCRIPTS_DIR / f'{handle}_transcript.txt'
    if not p.exists():
        return ''
    txt = p.read_text(errors='ignore')
    return txt[:max_chars]



def build_notes_source(handle: str, cur: Dict[str, Any], selected_items: List[Dict[str, Any]], mode: str) -> str:
    cap_lines: List[str] = []
    for item in selected_items:
        code = item.get('code', '')
        cap = item_caption(item)
        cap_lines.append(f'[{code}] {cap[:1200]}')
    captions_block = '\n\n'.join(cap_lines)

    transcript = read_transcript_excerpt(handle)
    frames_desc = ''
    if mode == 'visual':
        frame_files = sorted((ASSETS_DIR / handle).glob('*.jpg'))
        if frame_files:
            rels = [str(p.relative_to(ROOT)) for p in frame_files[:24]]
            frames_desc = 'Extracted keyframes:\n' + '\n'.join(f'- {x}' for x in rels)

    return textwrap.dedent(f'''\
    Creator: @{handle}
    Creator thesis (from curation): {cur.get('core_thesis', '')}
    Content type: {cur.get('content_type', '')}

    Key ideas from curation:
    {'; '.join(cur.get('key_ideas', []))}

    Selected post captions:
    {captions_block}

    {'Transcript excerpt:\n' + transcript if transcript else ''}

    {frames_desc}
    ''').strip()



def format_notes_txt(handle: str, notes: Dict[str, Any]) -> str:
    concepts = '\n'.join(f"- {c.get('name','')}: {c.get('definition','')} (via {', '.join(c.get('via_posts', []))})" for c in notes.get('key_concepts', []))
    refs = '\n'.join(f"- {r.get('name','')} [{r.get('type','')}] via {', '.join(r.get('referenced_in', []))}" for r in notes.get('references', []))
    pos = '\n'.join(f'- {x}' for x in notes.get('positions', []))
    tags = ', '.join(notes.get('tags', []))
    return textwrap.dedent(f'''\
    @{handle} notes

    Thesis:
    {notes.get('creator_thesis', '').strip()}

    Key concepts:
    {concepts}

    References:
    {refs if refs else '- None explicit'}

    Positions:
    {pos}

    Tags:
    {tags}
    ''').strip() + '\n'



def sanitize_selected_ids(ids: List[str], item_map: Dict[str, Dict[str, Any]]) -> List[str]:
    out: List[str] = []
    for raw in ids:
        code = re.sub(r'[^A-Za-z0-9_-]', '', raw)
        if code and code in item_map and code not in out:
            out.append(code)
    if len(out) < 8:
        for code in item_map.keys():
            if code not in out:
                out.append(code)
            if len(out) >= 8:
                break
    return out[:8]


def load_json_if_exists(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def bundle_from_files(handle: str) -> Optional[Dict[str, Any]]:
    notes = load_json_if_exists(TRANSCRIPTS_DIR / f'{handle}_notes.json')
    if not notes:
        return None
    cur = load_json_if_exists(TRANSCRIPTS_DIR / f'{handle}_curation.json') or {}
    return {
        'handle': handle,
        'content_type': cur.get('content_type', ''),
        'core_thesis': cur.get('core_thesis', ''),
        'key_ideas': cur.get('key_ideas', []),
        'selected_post_ids': cur.get('distinct_post_ids', []),
        'notes': notes,
    }



def run_phase1() -> Tuple[List[HandleResult], List[Dict[str, Any]], bool]:
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    VIDEOS_ROOT.mkdir(parents=True, exist_ok=True)

    ig = InstagramClient()
    results: List[HandleResult] = []
    notes_bundle: List[Dict[str, Any]] = []
    rate_limited = False

    for idx, handle in enumerate(HANDLES):
        existing_bundle = bundle_from_files(handle)
        if existing_bundle:
            notes_bundle.append(existing_bundle)
            results.append(HandleResult(handle=handle, ok=True, reason='cached'))
            continue

        try:
            user = ig.get_profile(handle)
            user_id = str(user.get('id'))
            items = ig.get_items(user_id, limit=40)
            if not items:
                raise RuntimeError('no items returned')
            captions_path = save_caption_file(handle, items)

            cur_json_path = TRANSCRIPTS_DIR / f'{handle}_curation.json'
            cur_txt_path = TRANSCRIPTS_DIR / f'{handle}_curation.txt'
            cur = load_json_if_exists(cur_json_path)
            if not cur:
                captions_text = captions_path.read_text(errors='ignore')
                cur_prompt = textwrap.dedent(f'''\
                This is a list of Instagram post captions from @{handle}.

                1) Describe this creator's core thesis in 2-3 sentences.
                2) Classify exactly one: (a) talking-head/spoken, (b) visual-reference heavy, or (c) caption-text heavy.
                3) List IDs of the 8 most conceptually distinct posts from the provided list.
                4) List 5-8 key ideas/frameworks.

                Return JSON only.

                Captions:
                {captions_text[:120000]}
                ''')
                cur = run_claude_json(cur_prompt, CURATION_SCHEMA)
                cur_txt_path.write_text(format_curation_text(handle, cur))
                cur_json_path.write_text(json.dumps(cur, indent=2))

            item_map = {x.get('code'): x for x in items if x.get('code')}
            selected_codes = sanitize_selected_ids(cur.get('distinct_post_ids', []), item_map)
            selected_items = [item_map[c] for c in selected_codes if c in item_map]

            downloaded = ensure_downloads(handle, selected_codes, item_map)

            mode = classify(cur)
            if mode == 'talking':
                tpath = TRANSCRIPTS_DIR / f'{handle}_transcript.txt'
                if not tpath.exists() or tpath.stat().st_size == 0:
                    run_transcription(handle)
            elif mode == 'visual':
                adir = ASSETS_DIR / handle
                if not adir.exists() or not list(adir.glob('*.jpg')):
                    extract_frames(handle)

            notes_json_path = TRANSCRIPTS_DIR / f'{handle}_notes.json'
            notes_txt_path = TRANSCRIPTS_DIR / f'{handle}_notes.txt'
            notes = load_json_if_exists(notes_json_path)
            if not notes:
                notes_source = build_notes_source(handle, cur, selected_items, mode)
                notes_prompt = textwrap.dedent(f'''\
                These are notes from @{handle}, a creator whose thesis is:
                {cur.get('core_thesis', '')}

                Extract:
                - 5-8 key concepts with one-sentence definitions
                - Any people, books, artworks, or movements referenced
                - 3-5 direct quotes or strong paraphrased positions
                - 2-3 tags describing thematic territory

                Keep concise and grounded in the source.
                Return JSON only.

                Source material:
                {notes_source[:160000]}
                ''')
                notes = run_claude_json(notes_prompt, NOTES_SCHEMA)
                notes_txt_path.write_text(format_notes_txt(handle, notes))
                notes_json_path.write_text(json.dumps(notes, indent=2))
            else:
                if not notes_txt_path.exists():
                    notes_txt_path.write_text(format_notes_txt(handle, notes))

            notes_bundle.append({
                'handle': handle,
                'content_type': cur.get('content_type'),
                'core_thesis': cur.get('core_thesis'),
                'key_ideas': cur.get('key_ideas', []),
                'selected_post_ids': selected_codes,
                'notes': notes,
            })
            results.append(
                HandleResult(
                    handle=handle,
                    ok=True,
                    reason='ok',
                    content_type=cur.get('content_type', ''),
                    harvested=len(items),
                    downloaded=downloaded,
                )
            )
        except RateLimitError as e:
            results.append(HandleResult(handle=handle, ok=False, reason=str(e)))
            rate_limited = True
            for rem in HANDLES[idx + 1:]:
                b = bundle_from_files(rem)
                if b:
                    notes_bundle.append(b)
                    results.append(HandleResult(handle=rem, ok=True, reason='cached'))
                else:
                    results.append(HandleResult(handle=rem, ok=False, reason='pending: rate limit'))
            break
        except AuthError as e:
            results.append(HandleResult(handle=handle, ok=False, reason=str(e)))
            for rem in HANDLES[idx + 1:]:
                b = bundle_from_files(rem)
                if b:
                    notes_bundle.append(b)
                    results.append(HandleResult(handle=rem, ok=True, reason='cached'))
                else:
                    results.append(HandleResult(handle=rem, ok=False, reason='pending: auth required'))
            break
        except Exception as e:
            results.append(HandleResult(handle=handle, ok=False, reason=str(e)))

    (TRANSCRIPTS_DIR / 'instagram_phase1_status.json').write_text(
        json.dumps([r.__dict__ for r in results], indent=2)
    )
    return results, notes_bundle, rate_limited



def run_phase2(notes_bundle: List[Dict[str, Any]]) -> Dict[str, Any]:
    compact_creators: List[Dict[str, Any]] = []
    for c in notes_bundle:
        notes = c.get('notes', {})
        compact_creators.append({
            'handle': c.get('handle'),
            'content_type': c.get('content_type'),
            'core_thesis': c.get('core_thesis'),
            'key_ideas': c.get('key_ideas', [])[:6],
            'tags': notes.get('tags', []),
            'concepts': [
                {
                    'name': x.get('name', ''),
                    'definition': x.get('definition', ''),
                    'via_posts': x.get('via_posts', [])[:3],
                }
                for x in notes.get('key_concepts', [])[:8]
            ],
            'positions': notes.get('positions', [])[:4],
            'references': [
                {
                    'name': r.get('name', ''),
                    'type': r.get('type', ''),
                    'referenced_in': r.get('referenced_in', [])[:3],
                }
                for r in notes.get('references', [])[:20]
            ],
        })
    payload = {'creators': compact_creators}
    prompt = textwrap.dedent('''\
    Here are extracted notes from Instagram creators.
    Group them into 3-5 thematic clusters based on shared ideas, not by creator.

    For each cluster provide:
    - name and URL-safe slug
    - 1-paragraph description of what connects creators
    - contributing creators
    - 3-5 shared ideas that cut across creators
    - 1-2 points of tension/disagreement
    - representative creator voices
    - references (people/books/artworks/movements) mentioned in the cluster
    - whether this cluster is visual-heavy

    Also list cross-cutting themes that appear across multiple clusters.

    Return JSON only.

    Notes:
    ''') + json.dumps(payload, ensure_ascii=False)

    synth = run_claude_json(prompt, SYNTHESIS_SCHEMA)

    map_txt_lines: List[str] = []
    map_txt_lines.append('Instagram synthesis map')
    map_txt_lines.append('')
    for i, c in enumerate(synth.get('clusters', []), 1):
        map_txt_lines.append(f'Cluster {i}: {c.get("name","")}')
        map_txt_lines.append(c.get('description', ''))
        map_txt_lines.append('Creators: ' + ', '.join('@' + h for h in c.get('creators', [])))
        map_txt_lines.append('Shared ideas:')
        for idea in c.get('shared_ideas', []):
            map_txt_lines.append(f"- {idea.get('name')}: {idea.get('definition')}")
        map_txt_lines.append('Tensions:')
        for t in c.get('tensions', []):
            map_txt_lines.append(f"- {t.get('tension')}: {t.get('side_a')} vs {t.get('side_b')}")
        map_txt_lines.append('')
    map_txt_lines.append('Cross-cutting themes:')
    for t in synth.get('cross_cutting_themes', []):
        map_txt_lines.append(f'- {t}')

    (TRANSCRIPTS_DIR / 'synthesis_map.txt').write_text('\n'.join(map_txt_lines).strip() + '\n')
    (TRANSCRIPTS_DIR / 'synthesis_map.json').write_text(json.dumps(synth, indent=2, ensure_ascii=False))

    return synth



def nav_html_for(current_file: str, cluster_pages: List[Tuple[str, str]]) -> str:
    links: List[Tuple[str, str]] = [('index.html', 'home'), ('master.html', 'synthesis')]
    links.extend(cluster_pages)
    if (ROOT / 'timeline.html').exists():
        links.append(('timeline.html', 'timeline'))

    anchors = []
    for href, label in links:
        cls = 'nav-link active' if href == current_file else 'nav-link'
        anchors.append(f'    <a class="{cls}" href="{href}">{esc(label)}</a>')
    return '<div class="nav-links">\n' + '\n'.join(anchors) + '\n  </div>'



def build_cluster_page(cluster: Dict[str, Any], cluster_pages: List[Tuple[str, str]]) -> Tuple[str, str]:
    name = cluster.get('name', 'Cluster')
    slug = slugify(cluster.get('slug') or name)
    filename = f'{slug}.html'

    creators = cluster.get('creators', [])
    creator_line = ', '.join('@' + c for c in creators)

    concepts = []
    for idea in cluster.get('shared_ideas', []):
        via = ', '.join('@' + h for h in idea.get('via_handles', []))
        concepts.append(
            '<div class="concept-card">'
            f'<div class="concept-name">{esc(idea.get("name", ""))}</div>'
            f'<div class="concept-body">{esc(idea.get("definition", ""))}</div>'
            f'<div class="concept-role">via {esc(via)}</div>'
            '</div>'
        )

    voices = []
    for v in cluster.get('voices', []):
        voices.append(
            '<div class="quote-item">'
            '<div class="quote-mark">"</div>'
            f'<div class="quote-text">{esc(v.get("quote", ""))} <span style="font-style:normal;color:var(--accent)">(@{esc(v.get("handle", ""))})</span></div>'
            '</div>'
        )

    tensions = []
    for t in cluster.get('tensions', []):
        tensions.append(
            '<div class="movement-row">'
            f'<div class="movement-period">{esc(t.get("tension", ""))}</div>'
            '<div class="movement-content">'
            f'<div class="movement-name">Side A</div><div class="movement-desc">{esc(t.get("side_a", ""))}</div>'
            f'<div class="movement-name" style="margin-top:8px;">Side B</div><div class="movement-desc">{esc(t.get("side_b", ""))}</div>'
            '</div>'
            '</div>'
        )

    refs = []
    for r in cluster.get('references', []):
        refs.append(
            '<tr>'
            f'<td>{esc(r.get("name", ""))}</td>'
            f'<td>{esc(r.get("type", ""))}</td>'
            f'<td>{esc(", ".join("@" + h for h in r.get("referenced_by", [])))}</td>'
            '</tr>'
        )

    visuals_html = ''
    if cluster.get('is_visual_heavy'):
        figs = []
        used = 0
        for h in creators:
            img_dir = ASSETS_DIR / h
            if not img_dir.exists():
                continue
            for img in sorted(img_dir.glob('*.jpg'))[:2]:
                rel = img.relative_to(ROOT)
                figs.append(
                    '<figure class="visual-ref">'
                    f'<img src="{esc(str(rel))}" alt="{esc(h)} frame">'
                    f'<figcaption>@{esc(h)} · visual argument sample</figcaption>'
                    '</figure>'
                )
                used += 1
                if used >= 12:
                    break
            if used >= 12:
                break
        if figs:
            visuals_html = (
                '<section>\n'
                '  <div class="section-label">Visual References</div>\n'
                f'  <div class="visuals-grid">{"".join(figs)}</div>\n'
                '</section>'
            )

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(name)} · partake notes</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="shared.css">
</head>
<body>

<nav class="site-nav">
  <a class="nav-logo" href="index.html">partake</a>
  {nav_html_for(filename, cluster_pages)}
</nav>

<header class="page-header">
  <div class="header-eyebrow">INSTAGRAM SYNTHESIS · {esc(name.upper())}</div>
  <h1 class="header-title">{esc(name.upper())}</h1>
  <p class="header-subject">{esc(cluster.get('description', ''))}</p>
  <div class="header-meta">
    <span>Contributors: {esc(creator_line)}</span>
    <span>Source: Instagram Reels + captions</span>
  </div>
</header>

<div class="page-body">
  <section>
    <div class="section-label">Cross-Cutting Concepts</div>
    <div class="concepts-grid">{''.join(concepts)}</div>
  </section>

  <section>
    <div class="section-label">Creator Voices</div>
    <div class="quotes-list">{''.join(voices)}</div>
  </section>

  <section>
    <div class="section-label">Points of Tension</div>
    <div class="movements-list">{''.join(tensions)}</div>
  </section>

  <section>
    <div class="section-label">References</div>
    <table class="full-table">
      <thead><tr><th>Name</th><th>Type</th><th>Referenced by</th></tr></thead>
      <tbody>{''.join(refs)}</tbody>
    </table>
  </section>

  {visuals_html}

</div>

<footer class="site-footer">
  partake · instagram synthesis · <a href="index.html">← back to home</a>
</footer>

</body>
</html>
'''
    return filename, page



def ensure_visual_css() -> None:
    css = SHARED_CSS.read_text()
    if '.visuals-grid' in css:
        return
    css += '\n\n.visuals-grid {\n  display: grid;\n  grid-template-columns: repeat(auto-fill, minmax(240px,1fr));\n  gap: 10px;\n}\n.visual-ref {\n  background: var(--bg-1);\n  border: 1px solid var(--border);\n  overflow: hidden;\n}\n.visual-ref img {\n  width: 100%;\n  aspect-ratio: 16/9;\n  object-fit: cover;\n}\n.visual-ref figcaption {\n  padding: 10px 14px;\n  font-size: 0.72rem;\n  color: var(--text-2);\n  line-height: 1.5;\n  border-top: 1px solid var(--border);\n}\n'
    SHARED_CSS.write_text(css)



def replace_nav_in_html(path: Path, cluster_pages: List[Tuple[str, str]]) -> None:
    text = path.read_text(errors='ignore')
    current = path.name
    new_nav = nav_html_for(current, cluster_pages)
    text2 = re.sub(r'<div class="nav-links">[\s\S]*?</div>', new_nav, text, count=1)
    path.write_text(text2)



def update_index_cards(cluster_pages: List[Tuple[str, str]], synth: Dict[str, Any]) -> None:
    idx = INDEX_PATH.read_text(errors='ignore')

    # remove existing cards for these cluster pages
    for href, _label in cluster_pages:
        idx = re.sub(
            rf'\n\s*<a class="report-card" href="{re.escape(href)}">[\s\S]*?</a>\n',
            '\n',
            idx,
            flags=re.M,
        )

    nums = [int(x) for x in re.findall(r'Report\s+(\d+)', idx)]
    n = (max(nums) if nums else 0) + 1

    cluster_by_slug = {f"{slugify(c.get('slug') or c.get('name','cluster'))}.html": c for c in synth.get('clusters', [])}
    cards: List[str] = []
    for href, label in cluster_pages:
        c = cluster_by_slug.get(href, {})
        concepts = len(c.get('shared_ideas', []))
        creators = len(c.get('creators', []))
        tensions = len(c.get('tensions', []))
        refs = len(c.get('references', []))
        desc = c.get('description', '')
        card = f'''

    <a class="report-card" href="{href}">
      <div class="report-card-header">
        <div class="report-number">Report {n:02d} · 2026</div>
        <div class="report-title">{esc(label.upper())}</div>
      </div>
      <div class="report-body">
        <p class="report-subject">{esc(desc)}</p>
        <div class="report-stats">
          <div class="report-stat"><strong>{concepts}</strong> cross-cutting ideas</div>
          <div class="report-stat"><strong>{creators}</strong> creators</div>
          <div class="report-stat"><strong>{tensions}</strong> tensions</div>
          <div class="report-stat"><strong>{refs}</strong> references</div>
        </div>
        <div class="report-tags">
          <span class="report-tag">instagram</span>
          <span class="report-tag">synthesis</span>
        </div>
      </div>
      <div class="report-footer">
        <span>Instagram creators · synthesis cluster</span>
        <span>open →</span>
      </div>
    </a>
'''
        cards.append(card)
        n += 1

    idx = idx.replace('\n  </div>\n</div>\n\n<footer class="site-footer">', ''.join(cards) + '\n\n  </div>\n</div>\n\n<footer class="site-footer">', 1)

    # nav links in index too
    idx = re.sub(r'<div class="nav-links">[\s\S]*?</div>', nav_html_for('index.html', cluster_pages), idx, count=1)

    INDEX_PATH.write_text(idx)



def run_phase3(synth: Dict[str, Any]) -> List[Tuple[str, str]]:
    clusters = synth.get('clusters', [])
    cluster_pages: List[Tuple[str, str]] = []
    for c in clusters:
        slug = slugify(c.get('slug') or c.get('name', 'cluster'))
        cluster_pages.append((f'{slug}.html', slug.replace('_', ' ')))

    ensure_visual_css()

    # build pages
    for c in clusters:
        filename, html = build_cluster_page(c, cluster_pages)
        (ROOT / filename).write_text(html)

    # update nav in every html page
    for html_file in ROOT.glob('*.html'):
        replace_nav_in_html(html_file, cluster_pages)

    update_index_cards(cluster_pages, synth)
    return cluster_pages



def summarize_and_write(results: List[HandleResult], synth: Dict[str, Any]) -> None:
    fails = [r.handle for r in results if not r.ok]
    summary = {
        'total_handles': len(results),
        'ok_handles': [r.handle for r in results if r.ok],
        'failed_handles': fails,
        'clusters': [
            {
                'name': c.get('name'),
                'count': len(c.get('creators', [])),
                'creators': c.get('creators', []),
            }
            for c in synth.get('clusters', [])
        ],
    }
    (TRANSCRIPTS_DIR / 'instagram_run_summary.json').write_text(json.dumps(summary, indent=2))



def git_commit_push() -> None:
    subprocess.run(
        ['bash', '-lc', 'git add *.html shared.css assets/ transcripts/'],
        cwd=ROOT,
        check=False,
    )
    subprocess.run(['git', 'commit', '-m', 'add instagram synthesis pages'], cwd=ROOT, check=False)
    subprocess.run(['git', 'push', 'origin', 'main'], cwd=ROOT, check=False)



def main() -> None:
    try:
        with SingleRunLock(LOCK_PATH):
            ensure_claude_ready()

            results, notes_bundle, rate_limited = run_phase1()
            if rate_limited:
                print('Stopped due to Claude rate limit. Resume after reset.')
                return

            if len(notes_bundle) < 3:
                print('Not enough notes to build synthesis.')
                return

            # Phase 2 must happen before touching HTML
            synth = run_phase2(notes_bundle)
            run_phase3(synth)
            summarize_and_write(results, synth)
            git_commit_push()

            print('Phase 1 complete for', len([r for r in results if r.ok]), 'handles')
            print('Failed:', ', '.join(r.handle for r in results if not r.ok) or 'none')
            print('Clusters:', ', '.join(c.get('name', '') for c in synth.get('clusters', [])))
    except AuthError as e:
        print(str(e))
    except RateLimitError as e:
        print(f'Stopped due to Claude rate limit: {e}')
    except RuntimeError as e:
        print(str(e))


if __name__ == '__main__':
    main()
