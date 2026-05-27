#!/usr/bin/env python3
"""
Fetch museum-API images for the 40 pilot quiz artists.

Sources queried in order:
  1. Metropolitan Museum of Art (no key)
  2. Art Institute of Chicago (no key)
  3. Cleveland Museum of Art (no key)
  4. Smithsonian Open Access (no key, free tier)
  5. Rijksmuseum (no key for low volume)

Each artist gets up to 5 candidate works with metadata. Output is
written to quiz_images.json for review before bundling into the page.
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
    _SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CTX = ssl.create_default_context()

OUT = Path(__file__).parent / "quiz_images.json"
PILOT = [
    # (id, name, dates, gallery, medium-summary)
    ("a146", "Lucas Arruda", "b. 1983", "Zwirner", "painting"),
    ("a176", "Victor Man", "b. 1974", "Zwirner", "painting"),
    ("a188", "Yu Nishimura", "b. 1982", "Zwirner / Sadie Coles", "painting"),
    ("a206", "Amy Sillman", "b. 1955", "Zwirner", "painting"),
    ("a203", "Dana Schutz", "b. 1976", "Zwirner", "painting"),
    ("a221", "Lisa Yuskavage", "b. 1962", "Zwirner", "painting"),
    ("a313", "Marina Perez Simão", "b. 1980", "Pace", "painting"),
    ("a980", "Wilhelm Sasnal", "b. 1972", "Sadie Coles", "painting"),
    ("a291", "Mao Yan", "b. 1968", "Pace", "painting"),
    ("a929", "Matthew Wong", "1984–2019", "De Carlo", "painting"),
    ("a996", "Co Westerik", "1924–2018", "Sadie Coles", "painting"),
    ("a356", "Etel Adnan", "1925–2021", "Continua / White Cube", "painting"),

    ("a149", "Huma Bhabha", "b. 1962", "Zwirner", "sculpture"),
    ("a57",  "Carol Bove", "b. 1971", "Gagosian", "sculpture"),
    ("a213", "Andra Ursuţa", "b. 1979", "Zwirner / De Carlo", "sculpture"),
    ("a501", "Adrián Villar Rojas", "b. 1980", "Marian Goodman", "sculpture"),
    ("a794", "Berlinde De Bruyckere", "b. 1964", "Continua", "sculpture"),
    ("a458", "Cristina Iglesias", "b. 1956", "Marian Goodman", "sculpture"),
    ("a963", "Tau Lewis", "b. 1993", "Sadie Coles", "sculpture"),
    ("a803", "Eva Jospin", "b. 1975", "Continua", "sculpture"),
    ("a853", "Sanford Biggers", "b. 1970", "De Carlo", "sculpture"),
    ("a384", "Klára Hosnedlová", "b. 1990", "White Cube", "sculpture"),

    ("a257", "Hai Bo", "b. 1962", "Pace", "photography"),
    ("a273", "Josef Koudelka", "b. 1938", "Pace", "photography"),
    ("a296", "Richard Misrach", "b. 1949", "Pace", "photography"),
    ("a79",  "Roni Horn", "b. 1955", "Hauser & Wirth", "photography"),

    ("a396", "Christian Marclay", "b. 1955", "White Cube", "video"),
    ("a446", "Tacita Dean", "b. 1965", "Marian Goodman", "video"),
    ("a649", "Wael Shawky", "b. 1971", "Lisson", "video"),
    ("a490", "Tino Sehgal", "b. 1976", "Marian Goodman", "performance"),
    ("a583", "Ryan Trecartin", "b. 1981", "Sprüth Magers", "video"),

    ("a414", "Doris Salcedo", "b. 1958", "White Cube", "installation"),
    ("a795", "Leandro Erlich", "b. 1973", "Continua", "installation"),
    ("a841", "Nari Ward", "b. 1963", "Continua", "installation"),
    ("a20",  "Theaster Gates", "b. 1973", "Gagosian / White Cube", "installation"),
    ("a311", "Adam Pendleton", "b. 1984", "Pace", "conceptual"),

    ("a159", "Marcel Dzama", "b. 1974", "Zwirner", "drawing"),
    ("a191", "Raymond Pettibon", "b. 1957", "Zwirner / Sadie Coles", "drawing"),
    ("a735", "Sophie Calle", "b. 1953", "Perrotin", "conceptual"),
    ("a83",  "Glenn Ligon", "b. 1960", "Hauser & Wirth", "conceptual"),
]


def _get(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "partake-quiz/1.0"})
    with urllib.request.urlopen(req, timeout=timeout, context=_SSL_CTX) as r:
        return json.loads(r.read())


def _norm(s):
    return re.sub(r"[^a-z]", "", (s or "").lower())


def _name_match(query, artist_field):
    if not artist_field:
        return False
    q = _norm(query)
    a = _norm(artist_field)
    # Require last name (last whitespace-separated token of query) to appear
    last = _norm(query.split()[-1])
    return last in a and (q in a or all(_norm(tok) in a for tok in query.split()))


def from_met(name):
    """Met Museum API. Returns list of candidate works."""
    q = urllib.parse.quote(name)
    try:
        idx = _get(f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={q}&hasImages=true")
    except Exception:
        return []
    ids = (idx.get("objectIDs") or [])[:25]
    out = []
    for oid in ids:
        try:
            obj = _get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{oid}")
        except Exception:
            continue
        if not _name_match(name, obj.get("artistDisplayName")):
            continue
        img = obj.get("primaryImage") or obj.get("primaryImageSmall")
        if not img:
            continue
        out.append({
            "source": "Met",
            "title": obj.get("title"),
            "year": obj.get("objectDate"),
            "image": img,
            "credit": obj.get("creditLine"),
            "url": obj.get("objectURL"),
        })
        if len(out) >= 5:
            break
        time.sleep(0.1)
    return out


def from_aic(name):
    """Art Institute of Chicago."""
    q = urllib.parse.quote(name)
    fields = "id,title,artist_title,image_id,date_display,credit_line"
    try:
        d = _get(
            f"https://api.artic.edu/api/v1/artworks/search?q={q}"
            f"&fields={fields}&limit=20"
        )
    except Exception:
        return []
    out = []
    for x in d.get("data", []):
        if not x.get("image_id"):
            continue
        if not _name_match(name, x.get("artist_title")):
            continue
        out.append({
            "source": "Art Institute of Chicago",
            "title": x.get("title"),
            "year": x.get("date_display"),
            "image": f"https://www.artic.edu/iiif/2/{x['image_id']}/full/843,/0/default.jpg",
            "credit": x.get("credit_line"),
            "url": f"https://www.artic.edu/artworks/{x['id']}",
        })
        if len(out) >= 5:
            break
    return out


def from_cleveland(name):
    """Cleveland Museum of Art."""
    q = urllib.parse.quote(name)
    try:
        d = _get(
            f"https://openaccess-api.clevelandart.org/api/artworks/?q={q}&has_image=1&limit=20"
        )
    except Exception:
        return []
    out = []
    for x in d.get("data", []):
        creator = (x.get("creators") or [{}])[0].get("description", "")
        if not _name_match(name, creator):
            continue
        web = (x.get("images") or {}).get("web", {}).get("url")
        if not web:
            continue
        out.append({
            "source": "Cleveland Museum of Art",
            "title": x.get("title"),
            "year": x.get("creation_date"),
            "image": web,
            "credit": x.get("creditline"),
            "url": x.get("url"),
        })
        if len(out) >= 5:
            break
    return out


def from_smithsonian(name):
    """Smithsonian Open Access — name-field scoped query."""
    # Use name-field query for precision
    q = urllib.parse.quote(f'name:"{name}" AND online_media_type:"Images"')
    try:
        d = _get(
            f"https://api.si.edu/openaccess/api/v1.0/search?q={q}&rows=20&api_key=DEMO_KEY"
        )
    except Exception:
        return []
    out = []
    rows = (d.get("response") or {}).get("rows") or []
    for x in rows:
        content = x.get("content", {})
        descNote = content.get("descriptiveNonRepeating") or {}
        idx = content.get("indexedStructured") or {}
        names = idx.get("name") or []
        name_strs = [n if isinstance(n, str) else n.get("content", "") for n in names]
        if not any(_name_match(name, s) for s in name_strs):
            continue
        media = (descNote.get("online_media") or {}).get("media", []) or []
        if not media:
            continue
        img = media[0].get("content") or media[0].get("thumbnail")
        if not img:
            continue
        title = (descNote.get("title") or {}).get("content") if isinstance(descNote.get("title"), dict) else descNote.get("title")
        date = idx.get("date") or []
        out.append({
            "source": "Smithsonian",
            "title": title,
            "year": date[0] if isinstance(date, list) and date else "",
            "image": img,
            "credit": descNote.get("data_source"),
            "url": (descNote.get("record_link") or descNote.get("guid")),
        })
        if len(out) >= 5:
            break
    return out


def from_wikimedia_commons(name):
    """Wikimedia Commons — professional image archive used by museums and presses.
    Distinct from Wikipedia article thumbnails. First tries 'Category:<name>'
    (curated), then falls back to a file-search by name.
    """
    members = []
    # 1. Try category direct
    cat = name.replace(" ", "_")
    q = urllib.parse.quote(f"Category:{cat}")
    url = (
        f"https://commons.wikimedia.org/w/api.php?action=query&format=json"
        f"&list=categorymembers&cmtype=file&cmlimit=20"
        f"&cmtitle={q}&origin=*"
    )
    try:
        d = _get(url)
        members = (d.get("query") or {}).get("categorymembers") or []
    except Exception:
        pass

    # 2. Fallback: file search
    if not members:
        sq = urllib.parse.quote(f'"{name}"')
        search_url = (
            f"https://commons.wikimedia.org/w/api.php?action=query&format=json"
            f"&list=search&srnamespace=6&srlimit=15&srsearch={sq}&origin=*"
        )
        try:
            d = _get(search_url)
            members = (d.get("query") or {}).get("search") or []
        except Exception:
            pass
    out = []
    for m in members:
        title = m.get("title", "")
        if not title.startswith("File:"):
            continue
        # Filter to image extensions
        if not re.search(r"\.(jpe?g|png|tif?f)$", title, re.I):
            continue
        # Skip obvious portraits/signatures
        if re.search(r"signature|portrait|headshot|selfie", title, re.I):
            continue
        # Get image URL via imageinfo
        fname = urllib.parse.quote(title)
        info_url = (
            f"https://commons.wikimedia.org/w/api.php?action=query&format=json"
            f"&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=900"
            f"&titles={fname}&origin=*"
        )
        try:
            ii = _get(info_url)
        except Exception:
            continue
        pages = (ii.get("query") or {}).get("pages") or {}
        for _, page in pages.items():
            infos = page.get("imageinfo") or []
            if not infos:
                continue
            info = infos[0]
            img = info.get("thumburl") or info.get("url")
            meta = info.get("extmetadata") or {}
            artist_meta = (meta.get("Artist") or {}).get("value", "")
            # Clean HTML
            artist_clean = re.sub(r"<[^>]+>", "", artist_meta)
            out.append({
                "source": "Wikimedia Commons",
                "title": title.replace("File:", "").rsplit(".", 1)[0].replace("_", " "),
                "year": (meta.get("DateTimeOriginal") or {}).get("value", "") or "",
                "image": img,
                "credit": artist_clean or (meta.get("Credit") or {}).get("value", ""),
                "url": f"https://commons.wikimedia.org/wiki/{title.replace(' ', '_')}",
            })
        if len(out) >= 5:
            break
        time.sleep(0.1)
    return out


def fetch_all():
    results = {}
    for aid, name, dates, gallery, medium in PILOT:
        print(f"\n[{aid}] {name} ({dates})")
        candidates = []
        for fn, label in [
            (from_aic, "AIC"),
            (from_met, "Met"),
            (from_cleveland, "Cleveland"),
            (from_smithsonian, "Smithsonian"),
            (from_wikimedia_commons, "Commons"),
        ]:
            try:
                hits = fn(name)
            except Exception as e:
                print(f"  {label}: error {e}")
                continue
            if hits:
                print(f"  {label}: {len(hits)} match(es)")
                candidates.extend(hits)
        results[aid] = {
            "name": name,
            "dates": dates,
            "gallery": gallery,
            "medium": medium,
            "candidates": candidates,
        }
        time.sleep(0.2)
    OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    hit = sum(1 for r in results.values() if r["candidates"])
    print(f"\n=== Done ===")
    print(f"Artists with at least one image: {hit}/{len(PILOT)}")
    print(f"Written to: {OUT}")


if __name__ == "__main__":
    fetch_all()
