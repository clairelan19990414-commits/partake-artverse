#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TRANSCRIPTS = ROOT / 'transcripts'
VIDEOS_ROOT = Path.home() / 'Desktop' / 'partake_videos'
ID_RE = re.compile(r'^[A-Za-z0-9_-]{5,}$')


def ids_from_curation_json(handle: str) -> list[str]:
    p = TRANSCRIPTS / f'{handle}_curation.json'
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text())
    except Exception:
        return []
    ids = data.get('distinct_post_ids') or data.get('post_ids') or []
    return [x for x in ids if isinstance(x, str) and ID_RE.match(x)]


def ids_from_curation_txt(handle: str) -> list[str]:
    p = TRANSCRIPTS / f'{handle}_curation.txt'
    if not p.exists():
        return []
    text = p.read_text(errors='ignore')
    ids: list[str] = []
    in_block = False
    for line in text.splitlines():
        low = line.lower()
        if 'distinct post ids' in low:
            in_block = True
            continue
        if in_block and line.strip().endswith(':') and 'distinct' not in low:
            break
        if in_block:
            m = re.search(r'[-*]\s*([A-Za-z0-9_-]{5,})', line)
            if m:
                ids.append(m.group(1))
    return ids


def ids_from_captions(handle: str, limit: int) -> list[str]:
    p = TRANSCRIPTS / f'{handle}_captions.txt'
    if not p.exists():
        return []
    ids = []
    for line in p.read_text(errors='ignore').splitlines():
        first = line.split('|', 1)[0].strip()
        if ID_RE.match(first):
            ids.append(first)
        if len(ids) >= limit:
            break
    return ids


def unique(seq: list[str]) -> list[str]:
    out, seen = [], set()
    for x in seq:
        if x not in seen:
            out.append(x); seen.add(x)
    return out


def gather_ids(handle: str, limit: int) -> list[str]:
    ids = ids_from_curation_json(handle) or ids_from_curation_txt(handle)
    if len(ids) < min(8, limit):
        ids.extend(ids_from_captions(handle, limit))
    return unique(ids)[:limit]


def download(handle: str, ids: list[str]) -> None:
    out_dir = VIDEOS_ROOT / handle
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f'========== @{handle}: {len(ids)} ids ==========', flush=True)
    for i, post_id in enumerate(ids, 1):
        existing = list(out_dir.glob(f'{post_id}.*'))
        if any(p.suffix == '.mp4' for p in existing):
            print(f'[{i}/{len(ids)}] {post_id}: already have mp4', flush=True)
            continue
        url = f'https://www.instagram.com/reel/{post_id}/'
        print(f'[{i}/{len(ids)}] {post_id}: downloading {url}', flush=True)
        cmd = [
            'yt-dlp',
            '--cookies-from-browser', 'chrome',
            '--no-overwrites',
            '--output', str(out_dir / '%(id)s.%(ext)s'),
            '--format', 'best[ext=mp4]/bestvideo+bestaudio/best',
            '--merge-output-format', 'mp4',
            url,
        ]
        proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if proc.returncode != 0:
            print(proc.stdout.strip().split('\n')[-1] if proc.stdout.strip() else f'{post_id}: failed', flush=True)
    count = len(list(out_dir.glob('*.mp4')))
    print(f'@{handle}: local_mp4s={count}', flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('handles', nargs='+')
    parser.add_argument('--limit', type=int, default=12)
    args = parser.parse_args()
    for handle in args.handles:
        ids = gather_ids(handle, args.limit)
        if not ids:
            print(f'========== @{handle}: no ids found ==========', flush=True)
            continue
        download(handle, ids)


if __name__ == '__main__':
    main()
