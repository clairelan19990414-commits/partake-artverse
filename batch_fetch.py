#!/usr/bin/env python3
"""
Fetch portraits + works for newly-completed artists.
Idempotent: only processes IDs in state.completed that are missing
from quiz_images.json or quiz_portraits.json.

Pipeline per artist:
  1. Wikipedia portrait (infobox image, if any)
  2. Art Institute of Chicago search
  3. Wikimedia Commons category (best-effort)
  4. Gallery scrape (where URL pattern is predictable)
"""

import json
import re
import ssl
import time
import urllib.parse
import urllib.request
from pathlib import Path

try:
    import certifi
    _CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _CTX = ssl.create_default_context()

DIR = Path(__file__).parent
STATE = DIR / "quiz_scale_state.json"
IMGS = DIR / "quiz_images.json"
PORTRAITS = DIR / "quiz_portraits.json"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 Safari/605.1.15"
WIKI_UA = "partake-quiz/1.0 (educational)"


def _get_text(url, ua=UA, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=timeout, context=_CTX) as r:
        return r.read().decode("utf-8", errors="ignore")


def _get_json(url, ua=UA, timeout=20):
    return json.loads(_get_text(url, ua=ua, timeout=timeout))


def _slug(name):
    # Plain kebab-case slug — strip accents for some galleries
    s = name.lower()
    s = re.sub(r"[àáâãä]", "a", s); s = re.sub(r"[èéêë]", "e", s)
    s = re.sub(r"[ìíîï]", "i", s); s = re.sub(r"[òóôõö]", "o", s)
    s = re.sub(r"[ùúûü]", "u", s); s = re.sub(r"[ñ]", "n", s)
    s = re.sub(r"[ł]", "l", s); s = re.sub(r"[ý]", "y", s)
    s = re.sub(r"[ć]", "c", s); s = re.sub(r"[ş]", "s", s)
    s = re.sub(r"[ț]", "t", s); s = re.sub(r"[á]", "a", s)
    s = re.sub(r"[&]", "and", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def _wiki_slug(name):
    return urllib.parse.quote(name.replace(" ", "_"))


def wiki_portrait(name):
    slug = _wiki_slug(name)
    try:
        d = _get_json(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{slug}",
            ua=WIKI_UA,
        )
    except Exception:
        return None
    if d.get("type") == "disambiguation":
        return None
    orig = (d.get("originalimage") or {}).get("source")
    thumb = (d.get("thumbnail") or {}).get("source")
    return orig or thumb


def _norm_name(s):
    return re.sub(r"[^a-z]", "", (s or "").lower())


def _name_match(query, candidate):
    if not candidate:
        return False
    q = _norm_name(query)
    c = _norm_name(candidate)
    last = _norm_name(query.split()[-1])
    if last not in c:
        return False
    return all(_norm_name(t) in c for t in query.split() if len(t) > 1)


def aic_works(name, n=4):
    q = urllib.parse.quote(name)
    fields = "id,title,artist_title,image_id,date_display,credit_line"
    try:
        d = _get_json(f"https://api.artic.edu/api/v1/artworks/search?q={q}&fields={fields}&limit=25")
    except Exception:
        return []
    out, seen = [], set()
    for x in d.get("data", []):
        if not x.get("image_id") or not _name_match(name, x.get("artist_title")):
            continue
        t = (x.get("title") or "").strip()
        if t.lower() in seen:
            continue
        seen.add(t.lower())
        out.append({
            "source": "Art Institute of Chicago",
            "title": t,
            "year": x.get("date_display") or "",
            "image": f"https://www.artic.edu/iiif/2/{x['image_id']}/full/1200,/0/default.jpg",
            "credit": x.get("credit_line") or "",
            "url": f"https://www.artic.edu/artworks/{x['id']}",
        })
        if len(out) >= n:
            break
    return out


def commons_works(name, n=4):
    cat = name.replace(" ", "_")
    q = urllib.parse.quote(f"Category:{cat}")
    try:
        d = _get_json(
            f"https://commons.wikimedia.org/w/api.php?action=query&format=json"
            f"&list=categorymembers&cmtype=file&cmlimit=15&cmtitle={q}&origin=*",
            ua=WIKI_UA,
        )
    except Exception:
        return []
    members = (d.get("query") or {}).get("categorymembers") or []
    out = []
    for m in members:
        title = m.get("title", "")
        if not title.startswith("File:"):
            continue
        if not re.search(r"\.(jpe?g|png|tif?f)$", title, re.I):
            continue
        if re.search(r"signature|portrait|headshot|selfie|signature$", title, re.I):
            continue
        try:
            ii = _get_json(
                f"https://commons.wikimedia.org/w/api.php?action=query&format=json"
                f"&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=1200"
                f"&titles={urllib.parse.quote(title)}&origin=*",
                ua=WIKI_UA,
            )
        except Exception:
            continue
        for _, page in ((ii.get("query") or {}).get("pages") or {}).items():
            for info in (page.get("imageinfo") or []):
                img = info.get("thumburl") or info.get("url")
                if not img:
                    continue
                meta = info.get("extmetadata") or {}
                artist_meta = re.sub(r"<[^>]+>", "",
                                     (meta.get("Artist") or {}).get("value", ""))
                if artist_meta and not _name_match(name, artist_meta):
                    continue
                pretty = title.replace("File:", "").rsplit(".", 1)[0].replace("_", " ")
                pretty = re.sub(r"\s*\(\d{6,}\)$", "", pretty)
                out.append({
                    "source": "Wikimedia Commons",
                    "title": pretty,
                    "year": (meta.get("DateTimeOriginal") or {}).get("value", "") or "",
                    "image": img,
                    "credit": artist_meta or "Wikimedia Commons",
                    "url": f"https://commons.wikimedia.org/wiki/{title.replace(' ', '_')}",
                })
        if len(out) >= n:
            break
        time.sleep(0.1)
    return out


# Predictable gallery URL patterns (only those we know work)
GALLERY_URL = {
    "Gagosian":          lambda name: None,  # blocks bots, skip
    "Hauser & Wirth":    lambda name: None,  # SPA, no inline images
    "David Zwirner":     lambda name: f"https://www.davidzwirner.com/artists/{_slug(name)}",
    "Pace Gallery":      lambda name: f"https://www.pacegallery.com/artists/{_slug(name)}/",
    "White Cube":        lambda name: f"https://whitecube.com/artists/artist/{name.lower().replace(' ', '_').replace('-', '_')}",
    "Marian Goodman":    lambda name: f"https://www.mariangoodman.com/artists/{_slug(name)}",
    "Sprüth Magers":     lambda name: f"https://spruethmagers.com/artists/{_slug(name)}/",
    "Lisson Gallery":    lambda name: f"https://www.lissongallery.com/artists/{_slug(name)}",
    "Thaddaeus Ropac":   lambda name: f"https://ropac.net/artists/{_slug(name)}",
    "Galerie Perrotin":  lambda name: None,  # title-case + numeric suffix, unpredictable
    "Galleria Continua": lambda name: None,  # has unpredictable numeric suffix
    "Massimo De Carlo":  lambda name: f"https://www.massimodecarlo.com/artist/{_slug(name)}",
    "Sadie Coles HQ":    lambda name: f"https://www.sadiecoles.com/artists/{_slug(name)}",
}

# Each gallery's image-URL regex on its artist page
GALLERY_PATTERNS = {
    "David Zwirner":     r"https://cdn\.sanity\.io/images/juzvn5an/release-adp/[0-9a-f]+-\d+x\d+\.(?:jpg|jpeg|png|webp)",
    "Pace Gallery":      r"https://www\.pacegallery\.com/media/images/[\w./-]+?\.(?:jpg|jpeg|png|webp)",
    "Sadie Coles HQ":    r"https://sadie-coles\.transforms\.svdcdn\.com/production/images/Artists/[^\"\s]+?\.(?:jpg|jpeg|png|webp)(?:\?[^\"\s]*)?",
    "White Cube":        r"https://white-cube\.transforms\.svdcdn\.com/production/[^\"\s]+?\.(?:jpg|jpeg|png|webp)(?:\?[^\"\s]*)?",
    "Marian Goodman":    r"https://static-assets\.artlogic\.net/[^\"\s]+?/ws-mariangoodman/[^\"\s]+?\.(?:jpg|jpeg|png|webp)",
    "Lisson Gallery":    r"https://lisson-art\.s3\.amazonaws\.com/uploads/attachment/image/body/\d+/[^\"\s]+?\.(?:jpg|jpeg|png|webp)",
    "Sprüth Magers":     r"https://(?:spruethmagers\.com/files|res\.cloudinary\.com/smimagebank/image/upload/[^\"\s]+?/sprueth_magers)[^\"\s]+?\.(?:jpg|jpeg|png|webp)",
    "Massimo De Carlo":  r"https://mdc-space\.fra1\.cdn\.digitaloceanspaces\.com/[^\"\s]+?\.(?:jpg|jpeg|png|webp)",
}


def gallery_works(name, gallery, n=5):
    url_fn = GALLERY_URL.get(gallery)
    pat = GALLERY_PATTERNS.get(gallery)
    if not url_fn or not pat:
        return []
    url = url_fn(name)
    if not url:
        return []
    try:
        html = _get_text(url, timeout=15)
    except Exception:
        return []
    raw = re.findall(pat, html)
    seen, urls = set(), []
    for u in raw:
        base = re.sub(r"\.width-\d+|\.original|/_jpg\d+/|/_webp\d+/|-\d+x\d+(?=\.\w+$)", "", u.split("?")[0])
        if base in seen or "logo" in u.lower() or "favicon" in u.lower():
            continue
        seen.add(base)
        # Filter out gallery-template noise
        if "spm_logo" in u or "social-" in u:
            continue
        urls.append(u.replace("&amp;", "&"))
        if len(urls) >= n:
            break
    return [{
        "source": gallery, "title": "Untitled work", "year": "",
        "image": u, "credit": f"Courtesy {gallery}", "url": None,
    } for u in urls]


def _dedupe(cands):
    seen, out = set(), []
    for c in cands:
        u = c["image"]
        base = re.sub(r"\.width-\d+|\.original|/_jpg\d+/|/_webp\d+/|-\d+x\d+(?=\.\w+$)", "", u.split("?")[0])
        if base in seen:
            continue
        seen.add(base)
        out.append(c)
    return out[:6]


def main():
    state = json.loads(STATE.read_text())
    images = json.loads(IMGS.read_text())
    portraits = json.loads(PORTRAITS.read_text())

    # Read source-of-truth ARTISTS data via batch_pick._parse_artists
    sys_path_added = str(DIR) not in __import__("sys").path
    if sys_path_added:
        __import__("sys").path.insert(0, str(DIR))
    from batch_pick import _parse_artists
    all_artists = _parse_artists()

    # Process any artist that has a facts entry but no image record yet
    # (i.e., Claude wrote content but fetch hasn't run yet)
    import re
    facts_src = (DIR / "quiz_facts.js").read_text()
    facts_ids = set(re.findall(r"^  (a\d+):\s*\{", facts_src, re.M))
    new_ids = [aid for aid in facts_ids if aid not in images]
    print(f"Processing {len(new_ids)} new IDs (no existing image record)")

    for aid in new_ids:
        a = all_artists.get(aid)
        if not a:
            print(f"  [{aid}] not found in source — skip")
            continue
        name = a["name"]
        gallery = a["gallery"]
        print(f"  [{aid}] {name} ({gallery})")

        # Portrait
        p = wiki_portrait(name)
        if p:
            portraits[aid] = {"url": p, "source": f"Wikipedia: {_wiki_slug(name)}"}
            print(f"     portrait ← wikipedia")
        else:
            portraits[aid] = {"url": None, "source": None}

        # Works
        cands = []
        gallery_c = gallery_works(name, gallery, n=5)
        if gallery_c:
            cands.extend(gallery_c)
            print(f"     gallery: {len(gallery_c)} works")
        aic_c = aic_works(name, n=3)
        if aic_c:
            cands.extend(aic_c)
            print(f"     AIC: {len(aic_c)} works")
        if len(cands) < 3:
            commons_c = commons_works(name, n=3)
            if commons_c:
                cands.extend(commons_c)
                print(f"     Commons: {len(commons_c)} works")
        cands = _dedupe(cands)
        images[aid] = {
            "name": name,
            "dates": a.get("dates", ""),
            "gallery": gallery,
            "candidates": cands,
        }
        if not cands:
            print(f"     NO WORKS FOUND")
        time.sleep(0.4)

    IMGS.write_text(json.dumps(images, indent=2, ensure_ascii=False))
    PORTRAITS.write_text(json.dumps(portraits, indent=2, ensure_ascii=False))

    have_p = sum(1 for v in portraits.values() if v.get("url"))
    have_w = sum(1 for v in images.values() if v.get("candidates"))
    print(f"\nDone. Portraits {have_p}/{len(portraits)}. Works {have_w}/{len(images)}.")


if __name__ == "__main__":
    main()
