# Codex handoff — Partake image curation

You are a computer-use agent finishing the image coverage on a contemporary-art quiz site. This brief is **self-contained**; you have no memory of how the project got to this state.

## What Partake is

- A static HTML/CSS/JS site at `/Users/cicilan/Desktop/partake_notes/`, deployed to **https://partake-artverse.vercel.app**
- The relevant page is `artist_map.html`, which renders a "Test Yourself" quiz + knowledge cards for 857 artists across 13 blue-chip galleries (Gagosian, Hauser & Wirth, David Zwirner, Pace, White Cube, Marian Goodman, Sprüth Magers, Lisson, Thaddaeus Ropac, Galerie Perrotin, Galleria Continua, Massimo De Carlo, Sadie Coles HQ)
- Of those, 761 non-red-chip artists are in the quiz pool. Household-name red-chip artists (Hirst, Koons, Warhol, etc.) are deliberately excluded

## Your task

Close the image gaps for the **386 artists listed in `MANUAL_IMAGES_QUEUE.md`** (root of the repo). The queue has three categories:

| Category | Count | What's wrong | What you do |
|----------|------:|--------------|-------------|
| **A. Missing portrait** | 147 | Card renders only an initial-letter circle | Find a real portrait and add it |
| **B. Suspicious portrait** | 173 | Has a portrait URL but came from external-link og:image that is often a generic site hero, not the person | Visit the live card, eyeball it, replace if wrong, leave if right |
| **C. Thin works** | 66 | Portrait OK, but `<3` work images on the grid | Find more works |

Work the categories in order: A → B → C.

## How to source images

For each artist, in this priority order:

1. **The artist's own website** (often linked from their Wikipedia article's "External Links" section, or findable via "[Artist Name] artist website")
2. **The gallery's artist page** (search "[Artist Name] [Gallery]" — but note that **David Zwirner, Hauser & Wirth, Marian Goodman, Thaddaeus Ropac, Galerie Perrotin, Galleria Continua** are SPAs that render images client-side; you can still see them in the browser, just not in `view-source`)
3. **Instagram** (search "[Artist Name] artist" — log in only if you have credentials; otherwise grab images from anonymous-accessible profile/post pages)
4. **Press coverage** (Frieze, Artforum, Artnet, Hyperallergic, ARTnews, Brooklyn Rail, Apollo, Studio International)
5. **Museum collection pages** (Tate, MoMA, Whitney, Met, Walker, Guggenheim) — especially good for works

## How to verify visually

A portrait is correct if:
- It clearly shows a **human face** (not an artwork, not an installation shot)
- The person matches other photos of the same artist you can find via a quick image search
- Reject anything that looks like an artwork even if the filename has the artist's name

A work image is correct if:
- It's actually an artwork by the artist (not a portrait, not an installation shot of a different artist's show)
- The image is reasonable resolution (≥600px on the long side ideally; reject thumbnails)
- Captioning ideally identifies the work title and year

## How to update the data

Two JSON files. Both are arrays-of-objects keyed by artist ID (`a123`).

### To add or replace a portrait

Edit `quiz_portraits.json`:

```json
{
  "a123": {
    "url": "https://example.com/path/to/image.jpg",
    "source": "artist's website" 
  }
}
```

- The `url` must be a **directly hot-linkable** image URL (test it: opening it in a new tab should show ONLY the image, no HTML wrapper)
- The `source` is a short human-readable note for future reference (e.g., `"artist's website"`, `"Whitney bio page"`, `"Frieze interview"`, `"Instagram @handle"`)

### To remove a wrong portrait

Delete that artist's entire entry from `quiz_portraits.json`. The card will fall back to an initial-letter placeholder until something better is added.

### To add a work

Edit `quiz_images.json`, find the artist's ID, and append to the `candidates` array:

```json
{
  "source": "Tate",
  "title": "Untitled (Pad Thai)",
  "year": "1990",
  "image": "https://example.com/image.jpg",
  "credit": "Tate Collection",
  "url": "https://tate.org.uk/art/artworks/..."
}
```

Keep `candidates` ≤ 6 per artist. The UI shows up to 6.

## Validation against the live site

After each batch of ~10-20 artist updates:

1. Commit and push (see Git below)
2. Wait ~1 min for Vercel to deploy
3. Open `https://partake-artverse.vercel.app/artist_map.html` in a fresh browser tab
4. Take a quiz, answer questions to surface those specific artists' knowledge cards
5. Confirm the portrait + works render correctly
6. If anything looks wrong, fix and re-commit

## Git workflow

The repo is at `/Users/cicilan/Desktop/partake_notes/` with remote `origin/main` already configured.

After every batch of updates:

```bash
cd /Users/cicilan/Desktop/partake_notes
git add quiz_portraits.json quiz_images.json
git commit -m "images: added portraits + works for [batch description]"
git push
```

Vercel auto-deploys on push. **Don't skip the push** — partial progress on disk doesn't help if the session ends.

## Things to avoid

- **Do not** save Wikipedia/Wikimedia URLs that this project already exhausted — they're tried via Python scripts already (`complete_pass.py`, `portrait_pass2.py`, etc.). If you find a Wikipedia portrait that wasn't picked up, OK, but Wikimedia Commons file-name searches give too many false positives — be visual about it.
- **Do not** save Pinterest or Google Image thumbnail URLs (Google's `encrypted-tbn0.gstatic.com` will rate-limit and won't load reliably for end users)
- **Do not** save images behind authentication (gated Instagram posts, Facebook private profiles)
- **Do not** modify any Python script — they're done passes, not part of your job
- **Do not** modify `quiz_messages.js` or `quiz_facts.js` — the text content is locked
- **Do not** add new artists to the pool — the 857 is final

## Progress tracking

Every 25 artists you complete, post a one-line update:
> "Done 25/147 missing portraits. Sample: a206, a213, a484. Pushed."

When you reach a category boundary (finish A, start B), report:
> "Category A (missing portraits) complete — N/147 with new portraits, M skipped (couldn't find verifiable image). Moving to B."

## Stopping conditions

Stop when:
- All three categories are walked once
- OR you've spent ~4 hours of agent time
- OR you've made 100+ updates and want to checkpoint

Report final tallies in this format:
- Category A: N new portraits / 147 attempted
- Category B: N replaced / N kept / N removed / 173 reviewed
- Category C: N artists with new works / 66 attempted

## Key files & locations

| File | What |
|------|------|
| `MANUAL_IMAGES_QUEUE.md` | Your work list, three categorized tables |
| `quiz_portraits.json` | Portraits keyed by artist ID. **You edit this.** |
| `quiz_images.json` | Works keyed by artist ID. **You edit this.** |
| `quiz_facts.js` | Each artist's `name`, `born`, `based`, `wiki` slug. **Read-only.** |
| `artist_map.html` | The page that renders the cards. **Read-only.** |
| `FINAL_QUALITY_REPORT.md` | State at the start of your task |
| `quality_audit.py` | Re-run anytime to see tier counts |

Good luck.
