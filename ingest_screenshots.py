#!/usr/bin/env python3
"""
Setup (macOS):
1) python3 -m venv .venv && source .venv/bin/activate
2) pip install -r requirements.txt
3) brew install tesseract
4) python ingest_screenshots.py --interval 3 --output-json septemics_content.json

Dependencies: pyautogui, pytesseract, Pillow, pyobjc (optional, preferred on macOS).
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import select
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pyautogui
import pytesseract
from PIL import Image, ImageChops, ImageStat


@dataclass
class CaptureConfig:
    interval_seconds: float = 3.0
    diff_threshold: float = 0.004
    stable_frames: int = 2
    screenshots_dir: Path = Path("screenshots")
    output_json: Path = Path("septemics_content.json")
    max_captures: Optional[int] = None
    auto_advance_key: Optional[str] = None
    auto_advance_click: Optional[Tuple[int, int]] = None
    auto_stop_on_stable: bool = False
    use_full_screen_region: bool = False
    startup_delay: float = 3.0
    fixed_region: Optional[Tuple[int, int, int, int]] = None
    manual_trigger: bool = False
    beep_cues: bool = True
    voice_cues: bool = False
    activate_app_name: Optional[str] = None
    raw_ocr_json: Optional[Path] = None
    raw_ocr_txt: Optional[Path] = None


class TerminalKeyReader:
    """Non-blocking key polling from stdin (TTY-only)."""

    def __init__(self) -> None:
        self.enabled = False
        self.fd: Optional[int] = None
        self._old_settings = None

    def __enter__(self) -> "TerminalKeyReader":
        if sys.stdin.isatty():
            import termios
            import tty

            self.fd = sys.stdin.fileno()
            self._old_settings = termios.tcgetattr(self.fd)
            tty.setcbreak(self.fd)
            self.enabled = True
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.enabled and self.fd is not None and self._old_settings is not None:
            import termios

            termios.tcsetattr(self.fd, termios.TCSADRAIN, self._old_settings)

    def poll_key(self, timeout: float = 0.0) -> Optional[str]:
        if not self.enabled or self.fd is None:
            return None
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        if not ready:
            return None
        try:
            return os.read(self.fd, 1).decode("utf-8", errors="ignore")
        except OSError:
            return None


class RegionSelector:
    def __init__(self) -> None:
        self.start_x = 0
        self.start_y = 0
        self.rect = None
        self.selection: Optional[Tuple[int, int, int, int]] = None

    def select(self) -> Tuple[int, int, int, int]:
        try:
            import tkinter as tk
        except ImportError as exc:
            raise RuntimeError("tkinter is required for region selection.") from exc

        root = tk.Tk()
        root.title("Select capture region")
        root.attributes("-fullscreen", True)
        root.attributes("-topmost", True)
        root.attributes("-alpha", 0.24)
        root.configure(bg="black")

        canvas = tk.Canvas(root, cursor="crosshair", bg="black", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        helper = canvas.create_text(
            30,
            30,
            anchor="nw",
            fill="#9ff29a",
            font=("JetBrains Mono", 16, "bold"),
            text="Click and drag to select a capture region. Press Esc to cancel.",
        )

        def on_press(event):
            self.start_x = event.x
            self.start_y = event.y
            if self.rect is not None:
                canvas.delete(self.rect)
            self.rect = canvas.create_rectangle(
                self.start_x,
                self.start_y,
                self.start_x,
                self.start_y,
                outline="#2d8c00",
                width=3,
            )
            canvas.tag_raise(helper)

        def on_drag(event):
            if self.rect is None:
                return
            canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

        def on_release(event):
            x1, y1 = self.start_x, self.start_y
            x2, y2 = event.x, event.y
            left, top = min(x1, x2), min(y1, y2)
            right, bottom = max(x1, x2), max(y1, y2)
            width, height = right - left, bottom - top
            if width < 20 or height < 20:
                print("Selection too small. Please drag a larger region.")
                return
            self.selection = (left, top, width, height)
            root.quit()

        def on_escape(_):
            root.quit()

        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)
        root.bind("<Escape>", on_escape)

        root.mainloop()
        root.destroy()

        if not self.selection:
            raise RuntimeError("No capture region selected.")
        return self.selection


def normalized_image_diff(img_a: Image.Image, img_b: Image.Image) -> float:
    if img_a.size != img_b.size:
        img_b = img_b.resize(img_a.size)
    diff = ImageChops.difference(img_a.convert("RGB"), img_b.convert("RGB"))
    means = ImageStat.Stat(diff).mean
    return (sum(means) / len(means)) / 255.0 if means else 0.0


def capture_region_image(region: Tuple[int, int, int, int]) -> Image.Image:
    """
    Try pyautogui first; fall back to native screencapture if PIL/ImageGrab fails.
    """
    try:
        return pyautogui.screenshot(region=region)
    except Exception as first_exc:
        left, top, width, height = region
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        try:
            cmd = [
                "screencapture",
                "-R",
                f"{left},{top},{width},{height}",
                "-x",
                str(tmp_path),
            ]
            result = subprocess.run(cmd, check=False, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(
                    "Native screencapture failed "
                    f"(code={result.returncode}): {result.stderr.strip()}"
                ) from first_exc
            image = Image.open(tmp_path)
            image.load()
            return image
        finally:
            try:
                tmp_path.unlink(missing_ok=True)
            except Exception:
                pass


def existing_index_start(screenshots_dir: Path) -> int:
    highest = 0
    for path in screenshots_dir.glob("capture_*.png"):
        match = re.search(r"capture_(\d+)\.png$", path.name)
        if match:
            highest = max(highest, int(match.group(1)))
    return highest + 1


def emit_beep(config: CaptureConfig) -> None:
    if config.beep_cues:
        print("\a", end="", flush=True)


def emit_voice(config: CaptureConfig, text: str) -> None:
    if not config.voice_cues or platform.system() != "Darwin":
        return
    try:
        subprocess.run(["say", text], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        return


def activate_app(config: CaptureConfig) -> None:
    """
    Bring a specific app to the foreground to reduce focus drift during capture.
    """
    app_name = (config.activate_app_name or "").strip()
    if not app_name or platform.system() != "Darwin":
        return
    try:
        subprocess.run(
            ["osascript", "-e", f'tell application "{app_name}" to activate'],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # Small settle delay helps key events land in the intended app.
        time.sleep(0.12)
    except Exception:
        return


def wait_for_continue_or_quit(reader: TerminalKeyReader, config: CaptureConfig) -> bool:
    emit_beep(config)
    emit_voice(config, "Page unchanged. Advance page, then press enter.")
    print(
        "[ACTION REQUIRED] Page unchanged.\n"
        "Advance manually, then press Enter to continue, or Q to stop."
    )
    if not reader.enabled:
        answer = input("Press Enter to continue or type Q to stop: ").strip().lower()
        return answer != "q"

    while True:
        key = reader.poll_key(timeout=0.1)
        if not key:
            continue
        if key.lower() == "q":
            return False
        if key in ("\n", "\r"):
            return True


def sleep_with_quit(interval_seconds: float, reader: TerminalKeyReader) -> bool:
    end = time.time() + interval_seconds
    while time.time() < end:
        key = reader.poll_key(timeout=0.1)
        if key and key.lower() == "q":
            return False
    return True


def capture_screenshots(config: CaptureConfig, region: Tuple[int, int, int, int]) -> List[Path]:
    config.screenshots_dir.mkdir(parents=True, exist_ok=True)
    index = existing_index_start(config.screenshots_dir)

    captured: List[Path] = []
    previous_img: Optional[Image.Image] = None
    stable_count = 0

    print(f"Capture region: left={region[0]}, top={region[1]}, width={region[2]}, height={region[3]}")
    if config.manual_trigger:
        mode = "manual-trigger"
    elif config.auto_advance_key or config.auto_advance_click:
        mode = "auto-advance"
    else:
        mode = "manual-advance-diff"
    print(f"Capture mode: {mode}")
    print("Capture started. Focus your reading app now. Press Q in this terminal to stop.")
    emit_beep(config)
    emit_voice(config, "Capture started.")
    if config.startup_delay > 0:
        print(f"Waiting {config.startup_delay:.1f}s before first capture...")
        time.sleep(config.startup_delay)
    activate_app(config)

    if config.manual_trigger:
        print(
            "\nManual trigger mode:\n"
            "- Advance page in Safari first\n"
            "- Press Enter here to capture one page\n"
            "- Type Q then Enter to stop and run OCR\n"
        )
        emit_beep(config)
        emit_voice(config, "Manual mode ready. Advance page, then press enter to capture.")
        try:
            while True:
                prompt = f"[READY] Press Enter to capture page {len(captured)+1}, or Q then Enter to stop: "
                answer = input(prompt).strip().lower()
                if answer == "q":
                    break

                activate_app(config)
                image = capture_region_image(region)
                path = config.screenshots_dir / f"capture_{index:04d}.png"
                image.save(path)
                captured.append(path)
                print(f"[{len(captured):04d}] Saved {path.name}")
                emit_beep(config)
                emit_voice(config, "Captured.")

                index += 1
                if config.max_captures and len(captured) >= config.max_captures:
                    print(f"Reached max captures ({config.max_captures}).")
                    break
        except KeyboardInterrupt:
            print("\nCapture interrupted by keyboard.")

        print(f"Capture complete. {len(captured)} screenshot(s) saved to {config.screenshots_dir}")
        return captured

    with TerminalKeyReader() as reader:
        if not reader.enabled:
            print("TTY key polling unavailable. Use Ctrl+C to stop.")

        try:
            while True:
                activate_app(config)
                image = capture_region_image(region)
                path = config.screenshots_dir / f"capture_{index:04d}.png"
                image.save(path)
                captured.append(path)

                diff_score = None
                if previous_img is not None:
                    diff_score = normalized_image_diff(previous_img, image)
                    if diff_score < config.diff_threshold:
                        stable_count += 1
                    else:
                        stable_count = 0

                msg = f"[{len(captured):04d}] Saved {path.name}"
                if diff_score is not None:
                    msg += f" | diff={diff_score:.6f}"
                print(msg)

                if config.max_captures and len(captured) >= config.max_captures:
                    print(f"Reached max captures ({config.max_captures}).")
                    break

                if stable_count >= config.stable_frames:
                    if config.auto_stop_on_stable and (config.auto_advance_key or config.auto_advance_click):
                        print(
                            "Detected repeated unchanged pages while auto-advancing. "
                            "Stopping capture (likely end of readable content)."
                        )
                        break

                    should_continue = wait_for_continue_or_quit(reader, config)
                    stable_count = 0
                    previous_img = None
                    if not should_continue:
                        break

                previous_img = image
                index += 1

                if config.auto_advance_click:
                    activate_app(config)
                    pyautogui.click(config.auto_advance_click[0], config.auto_advance_click[1])
                elif config.auto_advance_key:
                    activate_app(config)
                    pyautogui.press(config.auto_advance_key)

                if not sleep_with_quit(config.interval_seconds, reader):
                    break
        except KeyboardInterrupt:
            print("\nCapture interrupted by keyboard.")

    print(f"Capture complete. {len(captured)} screenshot(s) saved to {config.screenshots_dir}")
    return captured


def has_vision_ocr() -> bool:
    if platform.system() != "Darwin":
        return False
    try:
        import Vision  # noqa: F401
        from Foundation import NSURL  # noqa: F401
    except Exception:
        return False
    return True


def ocr_with_vision(image_path: Path) -> str:
    import Vision
    from Foundation import NSURL

    request = Vision.VNRecognizeTextRequest.alloc().init()
    request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
    request.setUsesLanguageCorrection_(True)
    request.setRecognitionLanguages_(["en-US"])

    image_url = NSURL.fileURLWithPath_(str(image_path.resolve()))
    handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(image_url, None)

    ok, error = handler.performRequests_error_([request], None)
    if not ok:
        raise RuntimeError(f"Vision OCR failed: {error}")

    lines: List[str] = []
    for observation in request.results() or []:
        candidates = observation.topCandidates_(1)
        if candidates and len(candidates) > 0:
            lines.append(str(candidates[0].string()))
    return "\n".join(lines)


def ocr_with_tesseract(image_path: Path) -> str:
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)


def run_ocr(image_paths: List[Path]) -> List[Dict[str, str]]:
    use_vision = has_vision_ocr()
    engine = "vision" if use_vision else "tesseract"
    print(f"OCR engine: {engine}")

    results: List[Dict[str, str]] = []
    for idx, image_path in enumerate(sorted(image_paths), start=1):
        text = ""
        if use_vision:
            try:
                text = ocr_with_vision(image_path)
            except Exception as exc:
                print(f"Vision OCR failed on {image_path.name}: {exc}. Falling back to Tesseract.")
                text = ocr_with_tesseract(image_path)
                engine = "tesseract"
        else:
            text = ocr_with_tesseract(image_path)

        results.append(
            {
                "file": image_path.name,
                "engine": engine,
                "text": text.strip(),
            }
        )
        print(f"OCR [{idx}/{len(image_paths)}] {image_path.name} ({len(text.strip())} chars)")
    return results


def split_level_text(text: str) -> Tuple[str, str]:
    for sep in (" - ", " — ", " – ", ": "):
        if sep in text:
            left, right = text.split(sep, 1)
            left = left.strip()
            right = right.strip()
            if left and right:
                return left, right
    return text.strip(), ""


def roman_to_int(value: str) -> Optional[int]:
    token = value.strip().upper()
    numerals = {
        "I": 1,
        "II": 2,
        "III": 3,
        "IV": 4,
        "V": 5,
        "VI": 6,
        "VII": 7,
        "VIII": 8,
        "IX": 9,
        "X": 10,
    }
    return numerals.get(token)


def parse_scales_from_ocr(ocr_text: str) -> Dict[str, List[Dict[str, object]]]:
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in ocr_text.splitlines()]
    lines = [ln for ln in lines if ln]

    scale_re = re.compile(r"^(?:the\s+)?scale\s+of\b.*", re.IGNORECASE)
    level_re = re.compile(
        r"^(?:at\s+)?(?:level\s*)?(\d{1,2}|[ivx]+)\s*[\)\].:\-,]\s*(.+)$",
        re.IGNORECASE,
    )
    glossary_entry_re = re.compile(r"^([A-Za-z][A-Za-z0-9 '&()\-/]{1,80})\s*[:\-]\s*(.+)$")

    scales: List[Dict[str, object]] = []
    current_scale: Optional[Dict[str, object]] = None
    current_mode: Optional[str] = None
    current_level: Optional[Dict[str, object]] = None

    for line in lines:
        if scale_re.match(line):
            current_scale = {"name": line.strip(), "glossary": [], "levels": []}
            scales.append(current_scale)
            current_mode = None
            current_level = None
            continue

        if current_scale is None:
            continue

        lower = line.lower()
        if "glossary" in lower and len(line) <= 60:
            current_mode = "glossary"
            current_level = None
            continue

        level_match = level_re.match(line)
        if level_match:
            raw_level = level_match.group(1).strip()
            if raw_level.isdigit():
                number = int(raw_level)
            else:
                number = roman_to_int(raw_level)
            if number is None:
                continue
            label, description = split_level_text(level_match.group(2).strip())
            current_level = {"number": number, "label": label or f"Level {number}", "description": description}
            current_scale["levels"].append(current_level)
            current_mode = "level"
            continue

        if current_mode == "glossary":
            glossary_match = glossary_entry_re.match(line)
            if glossary_match:
                term = glossary_match.group(1).strip()
                definition = glossary_match.group(2).strip()
                current_scale["glossary"].append({"term": term, "definition": definition})
            elif current_scale["glossary"]:
                last = current_scale["glossary"][-1]
                last["definition"] = f"{last['definition']} {line}".strip()
        elif current_mode == "level" and current_level is not None:
            if len(line.split()) > 2:
                current_level["description"] = f"{current_level['description']} {line}".strip()

    if not scales:
        fallback_levels = []
        for line in lines:
            match = level_re.match(line)
            if not match:
                continue
            raw_level = match.group(1).strip()
            if raw_level.isdigit():
                number = int(raw_level)
            else:
                number = roman_to_int(raw_level)
            if number is None:
                continue
            label, description = split_level_text(match.group(2).strip())
            fallback_levels.append(
                {
                    "number": number,
                    "label": label or f"Level {number}",
                    "description": description,
                }
            )

        scales = [
            {
                "name": "Unsorted OCR Import",
                "glossary": [],
                "levels": sorted(fallback_levels, key=lambda item: item["number"]),
            }
        ]

    for scale in scales:
        unique_levels = {}
        for level in scale["levels"]:
            unique_levels[level["number"]] = level
        scale["levels"] = [unique_levels[k] for k in sorted(unique_levels.keys())]

        deduped_terms = {}
        for item in scale["glossary"]:
            key = item["term"].strip().lower()
            deduped_terms[key] = item
        scale["glossary"] = list(deduped_terms.values())

    return {"scales": scales}


def write_output_json(data: Dict[str, object], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def write_raw_ocr_json(
    *,
    ocr_results: List[Dict[str, str]],
    output_json: Path,
    screenshots_dir: Path,
) -> None:
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "screenshots_dir": str(screenshots_dir),
        "page_count": len(ocr_results),
        "pages": [
            {
                "index": idx,
                "file": item["file"],
                "engine": item["engine"],
                "char_count": len(item["text"]),
                "text": item["text"],
            }
            for idx, item in enumerate(ocr_results, start=1)
        ],
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def write_raw_ocr_txt(ocr_results: List[Dict[str, str]], output_txt: Path) -> None:
    output_txt.parent.mkdir(parents=True, exist_ok=True)
    with output_txt.open("w", encoding="utf-8") as f:
        for idx, item in enumerate(ocr_results, start=1):
            f.write(f"===== PAGE {idx:04d} | {item['file']} | {item['engine']} =====\n")
            f.write(item["text"])
            f.write("\n\n")


def parse_args() -> CaptureConfig:
    parser = argparse.ArgumentParser(description="Capture reading-app screenshots and OCR into Septemics JSON.")
    parser.add_argument("--interval", type=float, default=3.0, help="Seconds between captures (default: 3).")
    parser.add_argument(
        "--diff-threshold",
        type=float,
        default=0.004,
        help="Normalized diff threshold below which frames are treated as unchanged (default: 0.004).",
    )
    parser.add_argument(
        "--stable-frames",
        type=int,
        default=2,
        help="How many consecutive low-diff frames trigger pause (default: 2).",
    )
    parser.add_argument(
        "--screenshots-dir",
        type=Path,
        default=Path("screenshots"),
        help="Where region captures are saved (default: ./screenshots).",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("septemics_content.json"),
        help="Output JSON path (default: ./septemics_content.json).",
    )
    parser.add_argument(
        "--max-captures",
        type=int,
        default=None,
        help="Optional hard cap on number of screenshots.",
    )
    parser.add_argument(
        "--auto-advance-key",
        type=str,
        default=None,
        help="Optional key to press after each capture (example: right).",
    )
    parser.add_argument(
        "--auto-advance-click",
        type=str,
        default=None,
        help="Optional click point after each capture in the form x,y (example: 1240,420).",
    )
    parser.add_argument(
        "--auto-stop-on-stable",
        action="store_true",
        help="In auto-advance mode, stop when consecutive frames are unchanged.",
    )
    parser.add_argument(
        "--use-full-screen-region",
        action="store_true",
        help="Capture the full screen instead of prompting to select a region.",
    )
    parser.add_argument(
        "--startup-delay",
        type=float,
        default=3.0,
        help="Seconds to wait before first capture to allow app focus (default: 3).",
    )
    parser.add_argument(
        "--region",
        type=str,
        default=None,
        help="Skip selector overlay and use fixed region: left,top,width,height (example: 70,170,1320,760).",
    )
    parser.add_argument(
        "--manual-trigger",
        action="store_true",
        help="Capture only when you press Enter in terminal (recommended for manual page turns).",
    )
    parser.add_argument(
        "--no-beep",
        action="store_true",
        help="Disable terminal beep cues.",
    )
    parser.add_argument(
        "--voice-cues",
        action="store_true",
        help="Enable macOS spoken cues via 'say'.",
    )
    parser.add_argument(
        "--activate-app",
        type=str,
        default=None,
        help='App name to force to front before each capture step (example: "Safari").',
    )
    parser.add_argument(
        "--raw-ocr-json",
        type=Path,
        default=None,
        help=(
            "Optional path for per-page raw OCR JSON. "
            "If omitted, a sidecar file is written next to --output-json."
        ),
    )
    parser.add_argument(
        "--raw-ocr-txt",
        type=Path,
        default=None,
        help=(
            "Optional path for concatenated raw OCR TXT. "
            "If omitted, a sidecar file is written next to --output-json."
        ),
    )
    args = parser.parse_args()

    auto_advance_click = None
    if args.auto_advance_click:
        try:
            x_str, y_str = args.auto_advance_click.split(",", 1)
            auto_advance_click = (int(x_str.strip()), int(y_str.strip()))
        except Exception as exc:
            raise ValueError("--auto-advance-click must be x,y") from exc

    fixed_region = None
    if args.region:
        try:
            left_s, top_s, width_s, height_s = args.region.split(",", 3)
            fixed_region = (
                int(left_s.strip()),
                int(top_s.strip()),
                int(width_s.strip()),
                int(height_s.strip()),
            )
        except Exception as exc:
            raise ValueError("--region must be left,top,width,height") from exc

    return CaptureConfig(
        interval_seconds=args.interval,
        diff_threshold=args.diff_threshold,
        stable_frames=max(1, args.stable_frames),
        screenshots_dir=args.screenshots_dir,
        output_json=args.output_json,
        max_captures=args.max_captures,
        auto_advance_key=args.auto_advance_key,
        auto_advance_click=auto_advance_click,
        auto_stop_on_stable=args.auto_stop_on_stable,
        use_full_screen_region=args.use_full_screen_region,
        startup_delay=max(0.0, args.startup_delay),
        fixed_region=fixed_region,
        manual_trigger=args.manual_trigger,
        beep_cues=not args.no_beep,
        voice_cues=args.voice_cues,
        activate_app_name=args.activate_app,
        raw_ocr_json=args.raw_ocr_json,
        raw_ocr_txt=args.raw_ocr_txt,
    )


def main() -> None:
    pyautogui.FAILSAFE = True

    config = parse_args()
    if config.fixed_region:
        region = config.fixed_region
        print(f"Using fixed capture region from --region: {region}")
    elif config.use_full_screen_region:
        screen_size = pyautogui.size()
        region = (0, 0, int(screen_size.width), int(screen_size.height))
        print(f"Using full-screen capture region: {region}")
    else:
        print("Select capture region...")
        region = RegionSelector().select()

    screenshots = capture_screenshots(config, region)
    if not screenshots:
        print("No screenshots captured. Exiting.")
        return

    ocr_results = run_ocr(screenshots)
    combined_text = "\n\n".join(item["text"] for item in ocr_results if item["text"])

    raw_json_path = config.raw_ocr_json or config.output_json.with_name(
        f"{config.output_json.stem}_raw_ocr.json"
    )
    raw_txt_path = config.raw_ocr_txt or config.output_json.with_name(
        f"{config.output_json.stem}_raw_ocr.txt"
    )
    write_raw_ocr_json(
        ocr_results=ocr_results,
        output_json=raw_json_path,
        screenshots_dir=config.screenshots_dir,
    )
    write_raw_ocr_txt(ocr_results, raw_txt_path)

    structured = parse_scales_from_ocr(combined_text)
    write_output_json(structured, config.output_json)

    print(f"Wrote {config.output_json} at {datetime.now().isoformat(timespec='seconds')}")
    print(f"Wrote raw OCR JSON: {raw_json_path}")
    print(f"Wrote raw OCR TXT: {raw_txt_path}")
    print("Review and correct the JSON before using it in the web app.")


if __name__ == "__main__":
    main()
