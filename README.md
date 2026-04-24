# partake · notes

A video-to-notes pipeline. Each video or Instagram account becomes a structured HTML report page.

## Folder structure

```
partake_notes/
├── index.html                  ← home page, all reports as cards
├── master.html                 ← synthesis page, cross-report connections
├── vocabulary.html             ← personal English vocabulary notebook + test mode
├── shared.css                  ← all shared component styles
├── download_video.sh           ← single video downloader (Patreon, YouTube, Vimeo)
├── download_instagram.sh       ← batch Reels downloader for an Instagram handle
├── transcribe_instagram.sh     ← transcribes all mp4s in a handle folder → one merged txt
├── transcripts/                ← all transcript .txt files live here
└── README.md
```

Videos download to: `~/Desktop/partake_videos/`
Instagram reels download to: `~/Desktop/partake_videos/<handle>/`

---

## Workflow A: single video (Patreon / YouTube)

1. **Download** — run `download_video.sh`, paste URL when prompted
2. **Transcribe** — run faster-whisper on the mp4:
   ```bash
   python3 -c "
   from faster_whisper import WhisperModel
   model = WhisperModel('small', device='cpu')
   segments, _ = model.transcribe('PATH_TO_VIDEO.mp4', language='en')
   with open('transcripts/new_transcript.txt', 'w') as f:
       for s in segments: f.write(s.text + ' ')
   "
   ```
3. **Extract notes** — paste transcript into Claude.ai with:
   > "Extract structured notes from this video transcript. Return: key concepts with definitions, people mentioned with roles and Wikipedia name slugs, books/works referenced with ISBNs if possible, historical movements or periods with date ranges, and memorable direct quotes."
4. **Generate HTML** — build a new report page using the same CSS classes from `shared.css`, matching `post_internet.html` structure
5. **Update index.html** — add a new report card, auto-numbered

---

## Workflow B: Instagram creator (batch Reels)

1. **Download all Reels** — run in Terminal:
   ```bash
   bash download_instagram.sh
   # enter handle without @, e.g.: didoriot
   # saves to ~/Desktop/partake_videos/didoriot/
   ```
2. **Transcribe all clips** — run:
   ```bash
   bash transcribe_instagram.sh didoriot
   # processes every mp4 in the folder
   # outputs: transcripts/didoriot_transcript.txt
   ```
3. **Extract notes** — paste the merged transcript into Claude.ai with:
   > "This is a merged transcript of ~30-60 short Instagram Reels by a single creator. Extract structured notes: their main thesis or worldview, recurring concepts or frameworks they use (with definitions), people or works they reference, and 5-8 memorable direct quotes. Format as structured notes."
4. **Generate HTML** — build `<handle>.html` using same CSS classes, same structure
5. **Update index.html** — add card tagged `[instagram]`

---

## Instagram author queue (30 handles)

| # | Handle | Status |
|---|--------|--------|
| 01 | didoriot | pending |
| 02 | h_miller76 | pending |
| 03 | etymologynerd | pending |
| 04 | vinny_creative | pending |
| 05 | codebynordveritas | pending |
| 06 | stylebykvn | pending |
| 07 | thewaronbeauty | pending |
| 08 | bjornd.al | pending |
| 09 | willfrancis | pending |
| 10 | fastfoodledgendofficial | pending |
| 11 | eyes_of_apoorva | pending |
| 12 | lhuijuni.ldn | pending |
| 13 | fakeplasticbrands | pending |
| 14 | eugbrandstrat | pending |
| 15 | maryisalien | pending |
| 16 | maalivikabhat | pending |
| 17 | kai_rehagen | pending |
| 18 | bubsonline | pending |
| 19 | musingsofacrouton | pending |
| 20 | andreyazizov | pending |
| 21 | g.a.works | pending |
| 22 | itsvicchang | pending |
| 23 | davidkylechoe | pending |
| 24 | culturalfingerprints | pending |
| 25 | art_lust | pending |
| 26 | noteswnat | pending |
| 27 | sihaam | pending |
| 28 | dan_dug_ | pending |
| 29 | kaburbank | pending |
| 30 | aidanetcetera | pending |

---

## CSS components available in shared.css

- `.concepts-grid` / `.concept-card` — key concepts
- `.portraits-grid` / `.portrait-card` — people, with `data-wiki="Wikipedia_Slug"` for auto-loaded images
- `.full-table` — large reference tables
- `.movements-list` / `.movement-row` — timeline of periods
- `.quotes-list` / `.quote-item` — pull quotes
- `.book-card` — books with `data-isbn="..."` for auto-loaded covers
- `.section-label` — section headers with green rule

---

## Tools installed on this Mac

- `yt-dlp` — video downloader (via Homebrew); supports Instagram, YouTube, Patreon, Vimeo
- `faster-whisper` — local transcription (Python, no internet needed)
- Chrome with Instagram, Patreon, and Claude.ai already logged in
- No API keys required

## Codex prompt (to automate the full pipeline)

Tell Codex:
> "Read the README.md in this folder. Use Workflow B to process the Instagram handle `<handle>`. Run download_instagram.sh, then transcribe_instagram.sh, then open the merged transcript in Claude.ai to extract structured notes, then generate a new HTML report page matching the structure of post_internet.html using the same CSS classes. Finally update index.html with a new card for this creator tagged [instagram]."
