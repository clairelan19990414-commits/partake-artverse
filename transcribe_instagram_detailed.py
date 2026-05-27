#!/usr/bin/env python3
"""Create fuller Instagram transcripts from local downloaded reels.

Outputs:
  transcripts/<handle>_transcript_detailed.txt
  transcripts/<handle>_transcript_detailed.json

This intentionally does not overwrite the older <handle>_transcript.txt file.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from dataclasses import asdict, dataclass
from datetime import timedelta
from pathlib import Path
from typing import Any

from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parent
TRANSCRIPTS = ROOT / "transcripts"
VIDEOS_ROOT = Path.home() / "Desktop" / "partake_videos"


@dataclass
class WordItem:
    start: float
    end: float
    word: str
    probability: float | None


@dataclass
class SegmentItem:
    start: float
    end: float
    text: str
    avg_logprob: float | None
    no_speech_prob: float | None
    words: list[WordItem]


@dataclass
class ClipTranscript:
    file: str
    path: str
    duration: float | None
    language: str | None
    language_probability: float | None
    mode: str
    text: str
    segments: list[SegmentItem]
    error: str | None = None


def stamp(seconds: float | None) -> str:
    if seconds is None:
        return "--:--:--.---"
    ms = int(round(seconds * 1000))
    td = timedelta(milliseconds=ms)
    total_seconds = int(td.total_seconds())
    hours, rem = divmod(total_seconds, 3600)
    minutes, secs = divmod(rem, 60)
    millis = ms % 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def clip_id(path: Path) -> str:
    return path.stem.split("_")[-1]


def probe_duration(path: Path) -> float | None:
    try:
        out = subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            text=True,
            timeout=20,
        ).strip()
        return float(out) if out else None
    except Exception:
        return None


def transcribe_file(model: WhisperModel, path: Path, language: str | None, long_clip_seconds: int) -> ClipTranscript:
    duration_hint = probe_duration(path)
    max_duration = getattr(transcribe_file, "max_duration_seconds", 0)
    if max_duration and duration_hint and duration_hint > max_duration:
        raise RuntimeError(f"clip is {stamp(duration_hint)}; queued for separate long-video transcription")
    is_long_clip = bool(duration_hint and duration_hint > long_clip_seconds)
    mode = "long-segment-timestamps" if is_long_clip else "full-word-timestamps"
    beam_size = 1 if is_long_clip else 5
    best_of = 1 if is_long_clip else 5
    segments_iter, info = model.transcribe(
        str(path),
        language=language,
        beam_size=beam_size,
        best_of=best_of,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 350},
        word_timestamps=not is_long_clip,
        condition_on_previous_text=False,
        temperature=[0.0, 0.2, 0.4],
        compression_ratio_threshold=2.4,
        log_prob_threshold=-1.0,
        no_speech_threshold=0.6,
    )
    segments: list[SegmentItem] = []
    parts: list[str] = []
    for seg in segments_iter:
        text = (seg.text or "").strip()
        words = []
        for w in seg.words or []:
            words.append(WordItem(
                start=float(w.start or 0),
                end=float(w.end or 0),
                word=(w.word or "").strip(),
                probability=float(w.probability) if w.probability is not None else None,
            ))
        if text:
            parts.append(text)
        segments.append(SegmentItem(
            start=float(seg.start),
            end=float(seg.end),
            text=text,
            avg_logprob=float(seg.avg_logprob) if seg.avg_logprob is not None else None,
            no_speech_prob=float(seg.no_speech_prob) if seg.no_speech_prob is not None else None,
            words=words,
        ))
    return ClipTranscript(
        file=path.name,
        path=str(path),
        duration=float(getattr(info, "duration", 0) or 0),
        language=getattr(info, "language", None),
        language_probability=float(getattr(info, "language_probability", 0) or 0),
        mode=mode,
        text=" ".join(parts).strip(),
        segments=segments,
    )


def write_outputs(handle: str, clips: list[ClipTranscript], model_name: str, source_files: list[Path]) -> None:
    TRANSCRIPTS.mkdir(exist_ok=True)
    txt_path = TRANSCRIPTS / f"{handle}_transcript_detailed.txt"
    json_path = TRANSCRIPTS / f"{handle}_transcript_detailed.json"

    payload: dict[str, Any] = {
        "handle": handle,
        "model": model_name,
        "source_dir": str(VIDEOS_ROOT / handle),
        "source_files": [str(p) for p in source_files],
        "clip_count": len(clips),
        "clips": [asdict(c) for c in clips],
    }
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    lines: list[str] = []
    lines.append(f"@{handle} · detailed transcript")
    lines.append(f"model: faster-whisper {model_name}")
    lines.append(f"clips: {len(clips)}")
    lines.append("format: per-clip transcript with segment timestamps; generated from local mp4 files")
    lines.append("")
    for idx, clip in enumerate(clips, 1):
        reel_id = clip_id(Path(clip.file))
        lines.append("=" * 88)
        lines.append(f"CLIP {idx:02d} · {clip.file}")
        lines.append(f"instagram_url: https://www.instagram.com/reel/{reel_id}/")
        lines.append(f"duration: {stamp(clip.duration)} · language: {clip.language or 'unknown'} ({clip.language_probability or 0:.2f})")
        lines.append(f"transcription_mode: {clip.mode}")
        if clip.error:
            lines.append(f"ERROR: {clip.error}")
            lines.append("")
            continue
        lines.append("")
        lines.append("FULL TEXT")
        lines.append(clip.text or "[no speech detected]")
        lines.append("")
        lines.append("TIMESTAMPED SEGMENTS")
        for seg in clip.segments:
            if not seg.text:
                continue
            confidence_note = ""
            if seg.no_speech_prob is not None and seg.no_speech_prob > 0.45:
                confidence_note = f" [possible low-speech/noisy segment: {seg.no_speech_prob:.2f}]"
            lines.append(f"[{stamp(seg.start)} → {stamp(seg.end)}]{confidence_note} {seg.text}")
        lines.append("")
    txt_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {txt_path}")
    print(f"wrote {json_path}")


def run(handle: str, model_name: str, language: str | None, limit: int | None, force: bool, long_clip_seconds: int, max_duration_seconds: int) -> None:
    video_dir = VIDEOS_ROOT / handle
    if not video_dir.exists():
        raise SystemExit(f"Missing video folder: {video_dir}")
    files = sorted(video_dir.glob("*.mp4"))
    if limit:
        files = files[:limit]
    if not files:
        raise SystemExit(f"No mp4 files found in {video_dir}")

    txt_path = TRANSCRIPTS / f"{handle}_transcript_detailed.txt"
    json_path = TRANSCRIPTS / f"{handle}_transcript_detailed.json"
    if not force and txt_path.exists() and json_path.exists():
        print(f"skipping @{handle}; detailed transcript already exists. Use --force to regenerate.")
        return

    print(f"loading faster-whisper model: {model_name}")
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    transcribe_file.max_duration_seconds = max_duration_seconds
    clips: list[ClipTranscript] = []
    for i, path in enumerate(files, 1):
        print(f"[{i}/{len(files)}] @{handle} · {path.name}", flush=True)
        try:
            clips.append(transcribe_file(model, path, language=language, long_clip_seconds=long_clip_seconds))
        except Exception as exc:  # keep the batch moving; record failures visibly.
            clips.append(ClipTranscript(
                file=path.name,
                path=str(path),
                duration=None,
                language=None,
                language_probability=None,
                mode="error",
                text="",
                segments=[],
                error=str(exc),
            ))
            print(f"  skipped with error: {exc}", flush=True)
    write_outputs(handle, clips, model_name, files)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create detailed transcripts for a downloaded Instagram handle.")
    parser.add_argument("handle", help="Instagram handle / folder name under ~/Desktop/partake_videos")
    parser.add_argument("--model", default=os.environ.get("PARTAKE_WHISPER_MODEL", "small"), help="faster-whisper model name, default: small")
    parser.add_argument("--language", default="en", help="language code; use 'auto' for detection")
    parser.add_argument("--limit", type=int, default=None, help="optional number of clips for a test run")
    parser.add_argument("--force", action="store_true", help="overwrite existing detailed outputs")
    parser.add_argument("--long-clip-seconds", type=int, default=900, help="disable word timestamps and use a faster mode above this duration")
    parser.add_argument("--max-duration-seconds", type=int, default=3600, help="queue clips longer than this for a separate long-video pass")
    args = parser.parse_args()
    language = None if args.language == "auto" else args.language
    run(args.handle, args.model, language, args.limit, args.force, args.long_clip_seconds, args.max_duration_seconds)


if __name__ == "__main__":
    main()
