# Project memory · Partake notes / transcript + creator-page cleanup

This note is for future Codex sessions returning to the `partake_notes` / Instagram synthesis work.

## User standard

The user does **not** want shallow AI-summary pages, fake visual placeholders, or generic robot-facing markdown dumps. The work should feel like a careful editorial/archive project:

- Re-read original transcripts/captions before enriching a creator page.
- Prefer fewer pages done thoroughly over many thin pages.
- Make creator pages human-readable, guided, and visually integrated.
- Images must clarify actual references mentioned by the creator, not random influencer portraits or generated text-card filler.
- Use real, sourceable references: artworks, books, films, brands, institutions, interfaces, places, objects, and primary visual materials.
- Captions should explain why the image matters to the argument.
- Keep synthesis pages rich but coherent: update the related theme page when a creator page is improved.
- Verify locally and, when requested, deploy to Vercel and verify live URLs.

## Transcript repair status

A detailed transcript layer was created because the original `_transcript.txt` files were too thin. New tooling:

- `transcribe_instagram_detailed.py`
- `transcribe_local_instagram_batch.sh`
- `download_instagram_fuller.sh`
- `download_instagram_ids.py`
- `full_instagram_transcript.sh`

Detailed transcript outputs live in `transcripts/*_transcript_detailed.txt` and `transcripts/*_transcript_detailed.json`.

Important correction from 2026-06-04:

- Do not treat `*_curation.txt`, `*_curation.json`, captions, or Claude summaries as the source of truth for creator pages.
- The source of truth is downloaded video plus `transcripts/<handle>_transcript_detailed.txt/json`.
- `download_instagram_ids.py` now defaults to `--source captions` so it downloads the broad caption-ID inventory instead of silently collapsing to an 8-post curation.
- Use `./full_instagram_transcript.sh <handle> 40` or `./full_instagram_transcript.sh <handle> 60` for the real workflow: caption inventory, video download, full local transcription, and coverage reporting.
- Use `PARTAKE_SKIP_TRANSCRIBE=1 ./full_instagram_transcript.sh <handle> 40` when you only want to check/download coverage without starting a long Whisper pass.
- For each creator page, make the coverage explicit: caption IDs found, local mp4s, transcribed clips, transcript word count, and missing IDs.

Current full-corpus rebuild status:

- `davidkylechoe`: rebuilt from 38 detailed video transcripts / 17,512 words. Caption inventory had 40 IDs; two IDs did not land as usable local mp4s after retry: `DVj5LuRCX1n`, `DVTY-QMDqK0`.

As of 2026-05-25, 23 creators had detailed transcripts. Remaining no-video / mostly visual cases included:

- `etymologynerd`: visual/image posts; no mp4 from selected IDs.
- `kai_rehagen`: visual-first, sparse captions; no mp4 from selected IDs.
- `g.a.works`: visual/object/process posts; no mp4 from selected IDs.
- `maalivikabhat`, `sihaam`, `fastfoodledgendofficial`, `art_lust`: no local mp4/captions/notes found at that time.

Known transcript exceptions:

- `kaburbank`: one 1h44m video (`DVzShFyj5Ox.mp4`) was queued for separate long-video transcription rather than blocking the reel batch.
- `eyes_of_apoorva`: one failed clip had no audio stream.
- `andreyazizov`: two failed clips were video-only/silent.

## Page-enrichment workflow

For each creator/theme, do this slowly:

1. Re-read `transcripts/<handle>_transcript_detailed.txt`, captions, notes, curation, and existing page.
2. Identify real concepts and references from the source material.
3. Add/replace visuals only when they are real and useful.
4. Rebuild or enrich the creator page with a guided argument, not scattered facts.
5. Update the relevant synthesis page.
6. Check image paths and browser rendering locally.
7. Deploy only after verification if the user asks.

## Visual rules

Avoid:

- fake/generated placeholder SVGs
- gray or black text-card images pretending to be references
- random influencer portraits
- tiny thumbnails
- Google/Pinterest thumbnail URLs
- unsourced decorative images

Prefer:

- direct image files from artist/museum/gallery/brand/institution pages
- Wikimedia only when visually verified and appropriate
- official book covers, artworks, film stills, product/reference objects, buildings/institutions, maps, archival photos
- source metadata saved in `content/reference_sources/<handle>.json` when adding a major creator reference set

## Tone of future work

The user wants dedication, not speed theater. Be explicit about what is complete, what is partial, and what still needs user help. If something is too thin, say so and improve the source base rather than beautifying weak material.
