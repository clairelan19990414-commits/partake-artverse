#!/usr/bin/env python3
"""
Rebuild quiz_images.json from scratch with deduplication and verification.
Sources:
  1. Manually curated gallery images (verified by artist name) — highest priority
  2. Art Institute of Chicago (verified artist_title match)
  3. Wikimedia Commons category (curated; skip noise titles)
Caps each artist at 4 distinct works.
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

OUT = Path(__file__).parent / "quiz_images.json"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 Safari/605.1.15"

# Each artist in the pilot. (id, name, gallery_label).
# Curated gallery candidates inline (already collected). AIC fetched live.
PILOT = [
    ("a146", "Lucas Arruda", "Zwirner"),
    ("a176", "Victor Man", "Zwirner"),
    ("a188", "Yu Nishimura", "Zwirner / Sadie Coles"),
    ("a206", "Amy Sillman", "Zwirner"),
    ("a203", "Dana Schutz", "Zwirner"),
    ("a221", "Lisa Yuskavage", "Zwirner"),
    ("a313", "Marina Perez Simão", "Pace"),
    ("a980", "Wilhelm Sasnal", "Sadie Coles"),
    ("a291", "Mao Yan", "Pace"),
    ("a929", "Matthew Wong", "De Carlo"),
    ("a996", "Co Westerik", "Sadie Coles"),
    ("a356", "Etel Adnan", "Continua / White Cube"),
    ("a149", "Huma Bhabha", "Zwirner"),
    ("a57",  "Carol Bove", "Gagosian / Zwirner"),
    ("a213", "Andra Ursuţa", "Zwirner / De Carlo"),
    ("a501", "Adrián Villar Rojas", "Marian Goodman"),
    ("a794", "Berlinde De Bruyckere", "Continua"),
    ("a458", "Cristina Iglesias", "Marian Goodman"),
    ("a963", "Tau Lewis", "Sadie Coles"),
    ("a803", "Eva Jospin", "Continua"),
    ("a853", "Sanford Biggers", "De Carlo"),
    ("a384", "Klára Hosnedlová", "White Cube"),
    ("a257", "Hai Bo", "Pace"),
    ("a273", "Josef Koudelka", "Pace"),
    ("a296", "Richard Misrach", "Pace"),
    ("a79",  "Roni Horn", "Hauser & Wirth"),
    ("a396", "Christian Marclay", "White Cube"),
    ("a446", "Tacita Dean", "Marian Goodman"),
    ("a649", "Wael Shawky", "Lisson"),
    ("a490", "Tino Sehgal", "Marian Goodman"),
    ("a583", "Ryan Trecartin", "Sprüth Magers"),
    ("a414", "Doris Salcedo", "White Cube"),
    ("a795", "Leandro Erlich", "Continua"),
    ("a841", "Nari Ward", "Continua"),
    ("a20",  "Theaster Gates", "Gagosian / White Cube"),
    ("a311", "Adam Pendleton", "Pace"),
    ("a159", "Marcel Dzama", "Zwirner"),
    ("a191", "Raymond Pettibon", "Zwirner / Sadie Coles"),
    ("a735", "Sophie Calle", "Perrotin"),
    ("a83",  "Glenn Ligon", "Hauser & Wirth"),

    # ── Batch 2 ──
    ("a596", "Allora & Calzadilla", "Lisson"),
    ("a381", "Mona Hatoum", "White Cube"),
    ("a584", "Rosemarie Trockel", "Sprüth Magers"),
    ("a533", "Cyprien Gaillard", "Sprüth Magers"),
    ("a821", "Hans Op de Beeck", "Continua"),
    ("a545", "Karen Kilimnik", "Sprüth Magers"),
    ("a364", "Mirosław Bałka", "White Cube"),
    ("a282", "Maya Lin", "Pace"),
    ("a567", "Pamela Rosenkranz", "Sprüth Magers"),
    ("a371", "Cerith Wyn Evans", "White Cube"),
]

# Gallery-scraped images — one per artist, verified during prior fetch
GALLERY = {
    "a149": ("David Zwirner", "Remembering Things", "2025",
        "https://cdn.sanity.io/images/juzvn5an/release-adp/504c6cfa218810c2965fa9d9668c9231a9290b3b-3000x2250.jpg?w=2000"),
    "a396": ("White Cube", "Christian Marclay (exhibition view), Centre Pompidou", "2022",
        "https://white-cube.transforms.svdcdn.com/production/imported-artworks/Christian-Marclay/Christian-Marclay-Centre-Pompidou/a194352.jpg?w=1200&q=85&auto=format"),
    "a176": ("David Zwirner", "Maternity with Legend", "2024",
        "https://cdn.sanity.io/images/juzvn5an/release-adp/c44f465cead30c92c224a0e2bd51906fb72a8cb0-2447x3000.jpg?w=2000"),
    "a188": ("David Zwirner", "Permeation", "2025",
        "https://cdn.sanity.io/images/juzvn5an/release-adp/acda9d843ec7011d0be03a9cf7f4b52c56f7405f-3000x2562.jpg?w=2000"),
    "a213": ("David Zwirner", "Untitled (bronze, copper, antique glass, stone)", "2025",
        "https://cdn.sanity.io/images/juzvn5an/release-adp/cd06d019832d859af297de3a52126dbf179d98f1-3000x2249.jpg?w=2000"),
    "a291": ("Pace Gallery", "Madam", "2022",
        "https://www.pacegallery.com/media/images/971559keyKM11VJ82_GUFq6QEYIyJAg.width-2000.webp"),
    "a257": ("Pace Gallery", "The Southern Series No. 24", "2012",
        "https://www.pacegallery.com/media/images/68802.01.width-2000.jpg"),
    "a311": ("Pace Gallery", "Untitled (WE ARE NOT)", "2019",
        "https://www.pacegallery.com/media/images/19-148_AP_JPG_LR.original.jpg"),
    "a996": ("Sadie Coles HQ", "Grasses and Hand", None,
        "https://sadie-coles.transforms.svdcdn.com/production/images/Artists/Co-Westerik/Selected-Works/HQ22-CW15542P.jpeg?w=1200&auto=format&fit=crop"),
    "a963": ("Sadie Coles HQ", "Lunar infants and trembling reeds", "2025",
        "https://sadie-coles.transforms.svdcdn.com/production/images/Artists/Tau-Lewis/Exhibitions/2025-Bury-Street/Artworks/Tau-Lewis_Lunar_infants_and_trembling_reeds_2025.jpeg"),
    "a501": ("Marian Goodman", "Two Suns", "2015",
        "https://static-assets.artlogic.net/w_2400,h_1800,c_limit,f_auto,fl_lossy,q_auto/ws-mariangoodman/usr/artists/images/67/avr-2015-two-suns.png"),
    "a583": ("Sprüth Magers", "Please Knock Before Going Outside (Flood Season)", "2023",
        "https://res.cloudinary.com/smimagebank/image/upload/w_2560,c_limit,f_auto,fl_progressive/v1700473268/RYT_54406_Please_Knock_Before_Going_Outside_Flood_Season_2023_01_gm_ivmt5c.jpg"),
    "a794": ("Galleria Continua", "Same Old, Same Old (installation view)", "2025",
        "https://www.galleriacontinua.com/assets/artists_images/786x430/BERLINDE-DE-BRUYCKERE-Same_Old_Same_Old-04-DSB04593.jpg"),
    "a803": ("Galleria Continua", "Trompe l'œil", "2024",
        "https://www.galleriacontinua.com/assets/artists_images/786x430/Eva_Jospin_Trompe_l_oeil_1.jpg"),
    "a795": ("Galleria Continua", "Hybrids", "2026",
        "https://www.galleriacontinua.com/assets/artists_images/786x430/Hybrids_Leandro_Erlich_2026_HYdh.jpg"),
    "a841": ("Galleria Continua", "Spring Note", "2025",
        "https://www.galleriacontinua.com/assets/artists_images/786x430/NARI_WARD_SPRING_NOTE_01.jpg"),
    "a384": ("White Cube", "Untitled (from the series GROWTH)", "2024",
        "https://white-cube.transforms.svdcdn.com/production/uploads/Headers/Artist-Pages/JJ77776-1.jpg?w=1200&h=900&q=85&auto=format&fit=crop"),
    "a649": ("Lisson Gallery", "Drama 1882 (Venice 2024 installation)", "2024",
        "https://lisson-art.s3.amazonaws.com/uploads/attachment/image/body/29221/WSHA240001_Install-Venice-2024_001.3.jpeg"),
    "a490": ("Marian Goodman", "Tino Sehgal (Oxfordshire exhibition view)", "2021",
        "https://static-assets.artlogic.net/w_800,h_800,c_limit,f_auto,fl_lossy,q_auto/ws-mariangoodman/usr/images/exhibitions/main_image_override/items/93/93ea3db85ef440a9a85f12c81b0bcd5a/sehgal-2021-exhibition-oxfordshire-01.jpeg"),
    "a929": ("Massimo De Carlo", "Matthew Wong (selected work)", None,
        "https://mdc-space.fra1.cdn.digitaloceanspaces.com/prod/_jpg3000/Social_Share_img_2023-03-29-142746_xmxa.jpg"),
    "a313": ("Pace Gallery", "Marina Perez Simão (selected work)", None,
        "https://www.pacegallery.com/media/images/49378.width-2000.jpg"),
    "a57":  ("David Zwirner", "Frieze 2022 Presentation (installation view)", "2022",
        "https://cdn.sanity.io/images/juzvn5an/release-adp/f0f70812f6702e7f2d51854064719f27e4fd2396-3000x1765.jpg?w=2000"),
    "a980": ("Sadie Coles HQ", "Anka", "2023",
        "https://sadie-coles.transforms.svdcdn.com/production/images/Artists/Wilhelm-Sasnal/Artworks/HQ27-WS20348P_Anka_2023_4.jpeg?w=1200&h=900&q=85&auto=format&fit=crop"),

    # Batch 2
    "a381": ("White Cube", "Cappello per due II", "2013",
        "https://white-cube.transforms.svdcdn.com/production/uploads/Artist-Pages/Thumbnails/Mona-Hatoum-Cappello-per-due-II-2013-square-crop.jpg?w=1200&q=85&auto=format&fit=crop"),
    "a584": ("Sprüth Magers", "Cogito Ergo Sum", None,
        "https://spruethmagers.com/files/rtr-0194-cogito-ergo-sum-e1587113005123.jpg"),
    "a533": ("Sprüth Magers", "Ocean II Ocean (installation view)", "2020",
        "https://res.cloudinary.com/smimagebank/image/upload/w_2560,c_limit,f_auto,fl_progressive/v1588168393/sprueth_magers_Cyprien_Gaillard_Ocean_II_Ocean_11566.jpg"),
    "a821": ("Galleria Continua", "Hans Op de Beeck (selected work)", "2023",
        "https://www.galleriacontinua.com/assets/artists_images/786x430/Hans_Op_de_Beeck_2023_17da.jpg"),
    "a545": ("Sprüth Magers", "Degas painting hair ornament accessories bag world", "2004",
        "https://res.cloudinary.com/smimagebank/image/upload/w_2560,c_limit,f_auto,fl_progressive/v1653326862/sprueth_magers_Karen_Kilimnik_Degas_painting_hair_4683.jpg"),
    "a364": ("White Cube", "260 x 9 x 9", None,
        "https://white-cube.transforms.svdcdn.com/production/imported-artworks/Miroslaw-Balka/260-x-9-x-9/a151792.jpg?w=1200&q=85&auto=format&fit=crop"),
    "a282": ("Pace Gallery", "Maya Lin (selected work)", None,
        "https://www.pacegallery.com/media/images/66846.AP1.width-2000.jpg"),
    "a567": ("Sprüth Magers", "Pamela Rosenkranz (selected work)", None,
        "https://spruethmagers.com/files/pro-27296-gm.jpg"),
    "a371": ("White Cube", "Witness (after Iannis Xenakis)", None,
        "https://white-cube.transforms.svdcdn.com/production/imported-artworks/Cerith-Wyn-Evans/Witness-after-Iannis-Xenakis/a41804.jpg?w=1200&q=85&auto=format&fit=crop"),
}


def _get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout, context=_CTX) as r:
        return json.loads(r.read())


def _norm(s):
    return re.sub(r"[^a-z]", "", (s or "").lower())


def _name_match(query, artist_field):
    if not artist_field:
        return False
    last = _norm(query.split()[-1])
    a = _norm(artist_field)
    if last not in a:
        return False
    # Require all multi-char tokens of the name to appear
    toks = [_norm(t) for t in query.split() if len(t) > 1]
    return all(t in a for t in toks)


def from_aic(name, n=4):
    q = urllib.parse.quote(name)
    fields = "id,title,artist_title,image_id,date_display,credit_line"
    try:
        d = _get(f"https://api.artic.edu/api/v1/artworks/search?q={q}&fields={fields}&limit=25")
    except Exception:
        return []
    out, seen_titles = [], set()
    for x in d.get("data", []):
        if not x.get("image_id"):
            continue
        if not _name_match(name, x.get("artist_title")):
            continue
        title = (x.get("title") or "").strip()
        if title.lower() in seen_titles:
            continue
        seen_titles.add(title.lower())
        out.append({
            "source": "Art Institute of Chicago",
            "title": title,
            "year": x.get("date_display") or "",
            "image": f"https://www.artic.edu/iiif/2/{x['image_id']}/full/1200,/0/default.jpg",
            "credit": x.get("credit_line") or "",
            "url": f"https://www.artic.edu/artworks/{x['id']}",
        })
        if len(out) >= n:
            break
    return out


def from_commons(name, n=3):
    """Wikimedia Commons category direct (more reliable than fuzzy search)."""
    cat = name.replace(" ", "_")
    q = urllib.parse.quote(f"Category:{cat}")
    url = (f"https://commons.wikimedia.org/w/api.php?action=query&format=json"
           f"&list=categorymembers&cmtype=file&cmlimit=25&cmtitle={q}&origin=*")
    try:
        d = _get(url)
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
        if re.search(r"signature|portrait|headshot|selfie|signature\b|^File:\s*[A-Z]\w+_signature", title, re.I):
            continue
        # Skip exhibition/installation duplicates (panorama, detail of same exhibition)
        clean = re.sub(r"\s+", "_", title.replace("File:", "").rsplit(".", 1)[0])
        # Get image URL
        fname = urllib.parse.quote(title)
        info_url = (f"https://commons.wikimedia.org/w/api.php?action=query&format=json"
                    f"&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=1200"
                    f"&titles={fname}&origin=*")
        try:
            ii = _get(info_url)
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
                # Reject if artist meta clearly mentions someone else (sanity check)
                if artist_meta and not _name_match(name, artist_meta):
                    continue
                pretty_title = title.replace("File:", "").rsplit(".", 1)[0].replace("_", " ")
                # Trim parens with photo IDs like "(26283979293)"
                pretty_title = re.sub(r"\s*\(\d{6,}\)$", "", pretty_title)
                out.append({
                    "source": "Wikimedia Commons",
                    "title": pretty_title,
                    "year": (meta.get("DateTimeOriginal") or {}).get("value", "") or "",
                    "image": img,
                    "credit": artist_meta or "Wikimedia Commons",
                    "url": f"https://commons.wikimedia.org/wiki/{title.replace(' ', '_')}",
                })
        if len(out) >= n:
            break
        time.sleep(0.1)
    return out


def dedupe_candidates(cands):
    """Strip same-image-different-size and same-title duplicates."""
    def norm_url(u):
        if not u:
            return ""
        u = u.split("?")[0]
        u = re.sub(r"\.width-\d+", "", u)
        u = re.sub(r"/_jpg\d+/", "/", u)
        u = re.sub(r"/_webp\d+/", "/", u)
        return u

    seen_urls, seen_titles, out = set(), set(), []
    for c in cands:
        nu = norm_url(c["image"])
        nt = (c.get("title") or "").strip().lower()
        if nu in seen_urls:
            continue
        if nt and nt in seen_titles:
            continue
        seen_urls.add(nu)
        if nt:
            seen_titles.add(nt)
        out.append(c)
    return out


def main():
    results = {}
    for aid, name, gallery in PILOT:
        print(f"[{aid}] {name}")
        cands = []
        # 1. Curated gallery candidate (highest priority)
        if aid in GALLERY:
            src, title, year, img = GALLERY[aid]
            cands.append({
                "source": src,
                "title": title,
                "year": year or "",
                "image": img,
                "credit": f"Courtesy {src}",
                "url": None,
            })
            print(f"  + gallery: {title}")
        # 2. AIC
        aic = from_aic(name, n=4)
        if aic:
            cands.extend(aic)
            print(f"  + AIC: {len(aic)} works")
        # 3. Commons (only if we still need more)
        if len(cands) < 3:
            cm = from_commons(name, n=4)
            if cm:
                cands.extend(cm)
                print(f"  + Commons: {len(cm)} candidates")
        # Dedupe + cap at 4
        cands = dedupe_candidates(cands)[:4]
        results[aid] = {
            "name": name,
            "dates": "",
            "gallery": gallery,
            "candidates": cands,
        }
        time.sleep(0.15)

    OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    hit = sum(1 for v in results.values() if v["candidates"])
    avg = sum(len(v["candidates"]) for v in results.values()) / max(1, len(results))
    print(f"\nDone. {hit}/{len(PILOT)} artists with images. Avg {avg:.1f} works/artist.")
    print(f"Written: {OUT}")


if __name__ == "__main__":
    main()
