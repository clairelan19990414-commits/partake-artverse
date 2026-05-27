# Batch Instructions — Partake Quiz Pool Scaling

> **For the cron-fired Claude session.** You have no memory of prior sessions.
> Read this carefully and execute the steps in order. Do not skip steps.

## Mission

Add ~46 more artists to the Partake quiz pool. Each artist needs:
1. A 3-sentence `message` in `quiz_messages.js`
2. A structured `facts` entry in `quiz_facts.js`
3. Portrait + works images (fetched by script)
4. Inclusion in `QUIZ_POOL_IDS` if non-red-chip (handled by script)
5. Git commit + push (handled by script)

Target: **376 enriched artists total**, ≈46/cycle, ~7 cycles total.

## Step 1 — See the batch

```bash
cd /Users/cicilan/Desktop/partake_notes
python3 batch_pick.py 46
```

This prints the next 46 artists with full context: name, dates, gallery, museums, school, collectors, works, and existing bio. Output is also written to `/tmp/quiz_batch_current.json`.

## Step 2 — Write content for each artist

For each of the 46 artists in the batch:

### 2a. Write a 3-sentence message → append to `quiz_messages.js`

**Style** (read `quiz_messages.js` for examples before writing):
- **Sentence 1** — whereabouts: birthplace, where they live and work, where they trained.
- **Sentence 2** — experience/relativity: what lineage, biographical incident, historical moment, or peer cohort shaped the practice.
- **Sentence 3** — relevance + thesis: what their work argues now, in one declarative claim.

Length: ~80–100 words. Voice: editorial, art-historical, specific. Do **not** name the artist's name inside the message body — the test depends on this (the quiz uses message-attribution questions where the reader has to guess who).

Append before the closing `};` of `QUIZ_MESSAGES`. Use the existing 50 entries as your formal template — match the exact comment style (` // Artist Name`).

### 2b. Write a structured facts entry → append to `quiz_facts.js`

Required fields (same shape as existing 50 entries):
- `born`: "City, Country, YEAR" or "City, Country, YEAR (d. YEAR)" if deceased
- `based`: where they live/work
- `training`: school + city, or "Self-taught" if applicable
- `signature`: named series, named work, or named institution they built
- `method`: one-clause description of their distinctive process
- `thesis`: one-sentence paraphrase of their argument (slight rephrase of Sentence 3 of the message)
- `cohort`: historical scene, movement, or peer cluster
- `pron`: `{ written: "phonetic English-friendly guide", ipa: "/IPA/", lang: "BCP-47 language tag" }`
  - Examples of `lang`: `en-US`, `pt-BR`, `de-DE`, `fr-FR`, `pl-PL`, `cs-CZ`, `zh-CN`, `ja-JP`, `ar`, `es-MX`, `it-IT`, `nl-NL`
  - For names whose pronunciation is non-obvious, the written guide should be unmistakable to an English speaker
- `wiki`: Wikipedia slug (URL-encoded; usually `Firstname_Lastname`)

Append before the trailing `};` of `QUIZ_FACTS`.

## Step 3 — Fetch images for new IDs

```bash
python3 batch_fetch.py
```

This is idempotent: it only fetches portraits and works for IDs that don't yet have entries in `quiz_images.json`. Uses Wikipedia (portraits), Art Institute of Chicago (works), Wikimedia Commons (works), and gallery scrape (where URL pattern is predictable).

Some artists will end up with no portrait and only 1–2 works. That's fine — the card degrades gracefully.

## Step 4 — Finalize: update pool, commit, push

```bash
python3 batch_finalize.py
```

This:
- Moves the new IDs from `queue` → `completed` in `quiz_scale_state.json`
- Updates `QUIZ_POOL_IDS` in `artist_map.html` with all non-red-chip completed IDs
- `git add` the data files, commits with cycle number + count, pushes to origin
- Vercel deploys automatically within ~1 minute

## Step 5 — Confirm

Print one summary line to the user:
> Cycle N complete. Now at X/376 artists. Y new this cycle. Pushed to GitHub.

Then stop. Wait for the next cron fire.

## Quality guardrail — placeholder-bio artists (Phase 2)

After cycle 1, many artists arrive with **only a one-line placeholder bio** like *"British artist, represented by Gagosian"* or *"American artist, represented by Pace."* For these:

**Use your training knowledge if you have it.** Many gallery-roster artists (even less-famous ones) appear in your training data — exhibition catalogues, art press, museum bios. You can write a substantive entry from that knowledge.

**Do not fabricate.** If you don't recognize the artist at all and the placeholder bio gives almost no clues:
- Write a conservative entry that sticks strictly to verifiable facts (gallery affiliation, work titles + years if available, nationality if stated).
- For the `message`, keep it shorter and more guarded (e.g., open with "Represented by [Gallery] since [year if known]...") rather than inventing biography, exhibitions, or theses.
- For the `facts`, leave fields you can't fill with `''` (empty string) — do not invent training schools, signature projects, or theses.
- Add a `// LOW-CONTEXT` comment above the entry so it can be flagged for later hand-curation.

**Never invent:**
- Specific dates, schools, exhibitions, or galleries that aren't given in the source data or your reliable knowledge
- Thesis statements you can't ground in the artist's actual practice
- IPA pronunciations you're not confident about (write the `pron.written` guide only; leave `ipa: ''`)
- Wikipedia slugs you haven't verified exist (write your best guess but flag it)

A short honest entry is always better than a long invented one. The quiz is meant to test real knowledge; fabrication breaks the contract.

## If something goes wrong

- **Queue empty**: the goal is reached. Tell the user and stop.
- **`git push` fails**: tell the user; don't re-run finalize.
- **Hitting usage limits mid-chunk**: stop cleanly. If you haven't yet run `batch_finalize.py` for the current chunk, don't run it — the next cron fire can resume by re-running `batch_pick.py`. If finalize already ran, you're safe; the next fire just continues.
