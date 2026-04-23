# partake · notes

A video-to-notes pipeline. Each video becomes a structured HTML report page on this site.

## Folder structure

```
partake_notes/
├── index.html              ← home page, lists all reports as cards
├── shared.css              ← all shared component styles (edit this, not individual pages)
├── zerp_slop.html          ← Report 01: ZERP Slop (YouTube, 15 min)
├── post_internet.html      ← Report 02: Post-Internet Art (Patreon, 70 min)
├── download_video.sh       ← downloads video from any URL using yt-dlp + Chrome cookies
├── transcripts/
│   ├── zirpslop_transcript.txt
│   └── post_internet_transcript.txt
└── README.md
```

Videos download to: `~/Desktop/partake_videos/`

## Workflow to add a new report

1. **Download** — run `download_video.sh`, paste a Patreon or YouTube URL when prompted
2. **Transcribe** — run faster-whisper on the downloaded mp4:
   ```bash
   python3 -c "
   from faster_whisper import WhisperModel
   model = WhisperModel('small', device='cpu')
   segments, _ = model.transcribe('~/Desktop/partake_videos/VIDEO.mp4', language='en')
   with open('transcripts/new_transcript.txt', 'w') as f:
       for s in segments: f.write(s.text + ' ')
   "
   ```
3. **Extract notes** — open claude.ai in Chrome (already logged in), paste the transcript with this prompt prepended:
   > "Extract structured notes from this video transcript. Return: key concepts with definitions, people mentioned with roles and Wikipedia name slugs, books/works referenced with ISBNs if possible, historical movements or periods with date ranges, and memorable direct quotes."
4. **Generate HTML** — use the Claude.ai response to build a new report page matching the structure of `post_internet.html` or `zerp_slop.html`, using the same CSS classes from `shared.css`
5. **Update index.html** — add a new report card with stat counts and tags, auto-numbered (Report 03, 04, etc.)

## CSS components available in shared.css

- `.concepts-grid` / `.concept-card` — key concepts
- `.portraits-grid` / `.portrait-card` — people, with `data-wiki="Wikipedia_Slug"` for auto-loaded images
- `.full-table` — large reference tables (artists, critics, etc.)
- `.movements-list` / `.movement-row` — timeline of periods
- `.quotes-list` / `.quote-item` — pull quotes
- `.book-card` — books with `data-isbn="..."` for auto-loaded covers
- `.section-label` — section headers with green rule

## Tools installed on this Mac

- `yt-dlp` — video downloader (via Homebrew)
- `faster-whisper` — local transcription (Python, no internet needed)
- Chrome with Patreon + Claude.ai already logged in
- No API keys required
