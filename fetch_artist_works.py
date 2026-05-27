#!/usr/bin/env python3
"""
Fetch multiple distinct artworks per artist from gallery websites.
Each gallery has a different image-URL pattern; we curl the artist's
profile page and extract all matching work URLs, dedupe by base
filename, cap at 5 per artist.

Result merges with rebuild_quiz_images.py output.
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

OUT = Path(__file__).parent / "quiz_artist_works.json"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 Safari/605.1.15"

# (aid, name, gallery_label, gallery_url)
ARTISTS = [
    ("a146", "Lucas Arruda",            "David Zwirner",          "https://www.davidzwirner.com/artists/lucas-arruda"),
    ("a176", "Victor Man",              "David Zwirner",          "https://www.davidzwirner.com/artists/victor-man"),
    ("a188", "Yu Nishimura",            "David Zwirner",          "https://www.davidzwirner.com/artists/yu-nishimura"),
    ("a206", "Amy Sillman",             "David Zwirner",          "https://www.davidzwirner.com/artists/amy-sillman"),
    ("a203", "Dana Schutz",             "David Zwirner",          "https://www.davidzwirner.com/artists/dana-schutz"),
    ("a221", "Lisa Yuskavage",          "David Zwirner",          "https://www.davidzwirner.com/artists/lisa-yuskavage"),
    ("a313", "Marina Perez Simao",      "Pace Gallery",           "https://www.pacegallery.com/artists/marina-perez-simao/"),
    ("a980", "Wilhelm Sasnal",          "Sadie Coles HQ",         "https://www.sadiecoles.com/artists/wilhelm-sasnal"),
    ("a291", "Mao Yan",                 "Pace Gallery",           "https://www.pacegallery.com/artists/mao-yan/"),
    ("a929", "Matthew Wong",            "Massimo De Carlo",       "https://www.massimodecarlo.com/artist/matthew-wong"),
    ("a996", "Co Westerik",             "Sadie Coles HQ",         "https://www.sadiecoles.com/artists/co-westerik"),
    ("a356", "Etel Adnan",              "Galleria Continua",      "https://www.galleriacontinua.com/artists/etel-adnan-32"),
    ("a149", "Huma Bhabha",             "David Zwirner",          "https://www.davidzwirner.com/artists/huma-bhabha"),
    ("a57",  "Carol Bove",              "David Zwirner",          "https://www.davidzwirner.com/artists/carol-bove"),
    ("a213", "Andra Ursuta",            "David Zwirner",          "https://www.davidzwirner.com/artists/andra-ursuta"),
    ("a501", "Adrian Villar Rojas",     "Marian Goodman",         "https://www.mariangoodman.com/artists/adrian-villar-rojas"),
    ("a794", "Berlinde De Bruyckere",   "Galleria Continua",      "https://www.galleriacontinua.com/artists/berlinde-de-bruyckere-21"),
    ("a458", "Cristina Iglesias",       "Marian Goodman",         "https://www.mariangoodman.com/artists/cristina-iglesias"),
    ("a963", "Tau Lewis",               "Sadie Coles HQ",         "https://www.sadiecoles.com/artists/tau-lewis"),
    ("a803", "Eva Jospin",              "Galleria Continua",      "https://www.galleriacontinua.com/artists/eva-jospin-320"),
    ("a853", "Sanford Biggers",         "Massimo De Carlo",       "https://www.massimodecarlo.com/artist/sanford-biggers"),
    ("a384", "Klara Hosnedlova",        "White Cube",             "https://whitecube.com/artists/artist/klara_hosnedlova"),
    ("a257", "Hai Bo",                  "Pace Gallery",           "https://www.pacegallery.com/artists/hai-bo/"),
    ("a273", "Josef Koudelka",          "Pace Gallery",           "https://www.pacegallery.com/artists/josef-koudelka/"),
    ("a296", "Richard Misrach",         "Pace Gallery",           "https://www.pacegallery.com/artists/richard-misrach/"),
    ("a79",  "Roni Horn",               "Hauser & Wirth",         "https://www.hauserwirth.com/artists/2849-roni-horn/"),
    ("a396", "Christian Marclay",       "White Cube",             "https://whitecube.com/artists/artist/christian_marclay"),
    ("a446", "Tacita Dean",             "Marian Goodman",         "https://www.mariangoodman.com/artists/tacita-dean"),
    ("a649", "Wael Shawky",             "Lisson Gallery",         "https://www.lissongallery.com/artists/wael-shawky"),
    ("a490", "Tino Sehgal",             "Marian Goodman",         "https://www.mariangoodman.com/artists/tino-sehgal"),
    ("a583", "Ryan Trecartin",          "Sprüth Magers",          "https://spruethmagers.com/artists/ryan-trecartin/"),
    ("a414", "Doris Salcedo",           "White Cube",             "https://whitecube.com/artists/artist/doris_salcedo"),
    ("a795", "Leandro Erlich",          "Galleria Continua",      "https://www.galleriacontinua.com/artists/leandro-erlich-24"),
    ("a841", "Nari Ward",               "Galleria Continua",      "https://www.galleriacontinua.com/artists/nari-ward-76"),
    ("a20",  "Theaster Gates",          "White Cube",             "https://whitecube.com/artists/artist/theaster_gates"),
    ("a311", "Adam Pendleton",          "Pace Gallery",           "https://www.pacegallery.com/artists/adam-pendleton/"),
    ("a159", "Marcel Dzama",            "David Zwirner",          "https://www.davidzwirner.com/artists/marcel-dzama"),
    ("a191", "Raymond Pettibon",        "David Zwirner",          "https://www.davidzwirner.com/artists/raymond-pettibon"),
    ("a735", "Sophie Calle",            "Galerie Perrotin",       "https://www.perrotin.com/artists/Sophie_Calle/14"),
    ("a83",  "Glenn Ligon",             "Hauser & Wirth",         "https://www.hauserwirth.com/artists/2842-glenn-ligon/"),
    # Batch 2
    ("a596", "Allora Calzadilla",       "Lisson Gallery",         "https://www.lissongallery.com/artists/allora-calzadilla"),
    ("a381", "Mona Hatoum",             "White Cube",             "https://whitecube.com/artists/artist/mona_hatoum"),
    ("a584", "Rosemarie Trockel",       "Sprüth Magers",          "https://spruethmagers.com/artists/rosemarie-trockel/"),
    ("a533", "Cyprien Gaillard",        "Sprüth Magers",          "https://spruethmagers.com/artists/cyprien-gaillard/"),
    ("a821", "Hans Op de Beeck",        "Galleria Continua",      "https://www.galleriacontinua.com/artists/hans-op-de-beeck-53"),
    ("a545", "Karen Kilimnik",          "Sprüth Magers",          "https://spruethmagers.com/artists/karen-kilimnik/"),
    ("a364", "Miroslaw Balka",          "White Cube",             "https://whitecube.com/artists/artist/miroslaw_balka"),
    ("a282", "Maya Lin",                "Pace Gallery",           "https://www.pacegallery.com/artists/maya-lin/"),
    ("a567", "Pamela Rosenkranz",       "Sprüth Magers",          "https://spruethmagers.com/artists/pamela-rosenkranz/"),
    ("a371", "Cerith Wyn Evans",        "White Cube",             "https://whitecube.com/artists/artist/cerith_wyn_evans"),
]


def fetch_html(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20, context=_CTX) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"    fetch failed: {e}")
        return ""


def _norm_for_dedupe(url):
    """Strip size suffixes, query args, and cache keys to detect dupes."""
    u = url.split("?")[0]
    u = re.sub(r"\.width-\d+", "", u)
    u = re.sub(r"\.original\b", "", u)
    u = re.sub(r"/_jpg\d+/", "/", u)
    u = re.sub(r"/_webp\d+/", "/", u)
    # Sanity/imgix have stable hashes — strip everything after hash if needed
    return u


def _title_from_filename(url):
    # last path segment minus extension
    name = url.split("?")[0].rsplit("/", 1)[-1]
    name = re.sub(r"\.\w+$", "", name)
    name = re.sub(r"^\d+-", "", name)
    name = re.sub(r"_+\d+x\d+$", "", name)
    name = re.sub(r"-\d+x\d+$", "", name)
    name = name.replace("_", " ").replace("-", " ").strip()
    return name[:80] or "Untitled"


def extract_zwirner(html, name):
    """Sanity CDN, format release-adp/[hash]-WxH.jpg"""
    pat = r'https://cdn\.sanity\.io/images/juzvn5an/release-adp/[0-9a-f]+-\d+x\d+\.(?:jpg|jpeg|png|webp)'
    urls = list(dict.fromkeys(re.findall(pat, html)))
    return [{"image": u + "?w=1600&q=85&auto=format", "title": "Untitled work", "year": ""} for u in urls[:6]]


def extract_pace(html, name):
    pat = r'https://www\.pacegallery\.com/media/images/[\w./-]+?\.(?:jpg|jpeg|png|webp)'
    raw = re.findall(pat, html)
    # Use the largest size variant for each base image
    by_base = {}
    for u in raw:
        base = _norm_for_dedupe(u)
        # Prefer original or width-2000
        if "original" in u or "width-2000" in u:
            by_base[base] = u
        elif base not in by_base:
            by_base[base] = u
    urls = list(by_base.values())
    # Filter out static favicons etc.
    urls = [u for u in urls if "/static/" not in u and "favicon" not in u]
    return [{"image": u, "title": "Untitled work", "year": ""} for u in urls[:6]]


def extract_sadiecoles(html, name):
    pat = r'https://sadie-coles\.transforms\.svdcdn\.com/production/images/Artists/[^"\s]+?\.(?:jpg|jpeg|png|webp)(?:\?[^"\s]*)?'
    raw = re.findall(pat, html)
    # Dedupe by filename ignoring query
    by_base = {}
    for u in raw:
        base = u.split("?")[0]
        if base not in by_base:
            by_base[base] = u
    urls = [u for u in by_base.values() if "Artworks" in u or "Selected-Works" in u or "Exhibitions" in u]
    if not urls:  # fall back to any artist image
        urls = list(by_base.values())
    return [{"image": u.replace("&amp;", "&"), "title": _title_from_filename(u), "year": ""} for u in urls[:6]]


def extract_whitecube(html, name):
    pat = r'https://white-cube\.transforms\.svdcdn\.com/production/[^"\s]+?\.(?:jpg|jpeg|png|webp)(?:\?[^"\s]*)?'
    raw = re.findall(pat, html)
    by_base = {}
    for u in raw:
        base = u.split("?")[0]
        if base not in by_base:
            by_base[base] = u
    urls = [u for u in by_base.values() if "imported-artworks" in u or "Artworks" in u or "Selected" in u]
    if not urls:
        urls = list(by_base.values())
    return [{"image": u.replace("&amp;", "&"), "title": _title_from_filename(u), "year": ""} for u in urls[:6]]


def extract_continua(html, name):
    pat = r'https://www\.galleriacontinua\.com/assets/artists_images/[^"\s]+?\.(?:jpg|jpeg|png|webp)'
    raw = re.findall(pat, html)
    by_base = {}
    for u in raw:
        base = re.sub(r'/\d+x\d+/', '/', u)
        if base not in by_base:
            by_base[base] = u
    urls = [u for u in by_base.values() if "logo" not in u.lower()]
    return [{"image": u, "title": _title_from_filename(u), "year": ""} for u in urls[:6]]


def extract_mariangoodman(html, name):
    pat = r'https://static-assets\.artlogic\.net/[^"\s]+?/ws-mariangoodman/[^"\s]+?\.(?:jpg|jpeg|png|webp)'
    raw = re.findall(pat, html)
    by_base = {}
    for u in raw:
        # Strip the artlogic size segment from the dedupe key
        base = re.sub(r'/w_\d+(?:,h_\d+)?(?:,[^/]+)?/', '/', u)
        if base not in by_base:
            by_base[base] = u
    urls = [u for u in by_base.values() if "light-grey" not in u and "placeholder" not in u]
    return [{"image": u, "title": _title_from_filename(u), "year": ""} for u in urls[:6]]


def extract_lisson(html, name):
    pat = r'https://lisson-art\.s3\.amazonaws\.com/uploads/attachment/image/body/\d+/[^"\s]+?\.(?:jpg|jpeg|png|webp)'
    raw = list(dict.fromkeys(re.findall(pat, html)))
    return [{"image": u, "title": _title_from_filename(u), "year": ""} for u in raw[:6]]


def extract_spruethmagers(html, name):
    pat1 = r'https://spruethmagers\.com/files/[^"\s]+?\.(?:jpg|jpeg|png|webp)'
    pat2 = r'https://res\.cloudinary\.com/smimagebank/image/upload/[^"\s]+?/sprueth_magers_[^"\s]+?\.(?:jpg|jpeg|png|webp)'
    raw = list(dict.fromkeys(re.findall(pat1, html))) + list(dict.fromkeys(re.findall(pat2, html)))
    raw = [u for u in raw if "logo" not in u.lower() and "favicon" not in u.lower() and "spm_logo" not in u]
    return [{"image": u, "title": _title_from_filename(u), "year": ""} for u in raw[:6]]


def extract_perrotin(html, name):
    pat = r'https://www\.perrotin\.com/[^"\s]+?artworks/[^"\s]+?\.(?:jpg|jpeg|png|webp)'
    raw = list(dict.fromkeys(re.findall(pat, html)))
    if not raw:
        pat = r'https://cdn\.perrotin\.com/[^"\s]+?\.(?:jpg|jpeg|png|webp)'
        raw = list(dict.fromkeys(re.findall(pat, html)))
    return [{"image": u, "title": _title_from_filename(u), "year": ""} for u in raw[:6]]


def extract_mdc(html, name):
    pat = r'https://mdc-space\.fra1\.cdn\.digitaloceanspaces\.com/[^"\s]+?\.(?:jpg|jpeg|png|webp)'
    raw = re.findall(pat, html)
    by_base = {}
    for u in raw:
        base = re.sub(r'/_jpg\d+/', '/', u)
        base = re.sub(r'/_webp\d+/', '/', base)
        if base not in by_base or "_jpg3000" in u:
            by_base[base] = u
    urls = list(by_base.values())
    return [{"image": u, "title": _title_from_filename(u), "year": ""} for u in urls[:6]]


def extract_hauserwirth(html, name):
    # HW uses lazy-loading, og:image is the artist's portrait. Page rarely
    # has work URLs inline. Try og:image at minimum.
    m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html)
    if m:
        return [{"image": m.group(1), "title": "Selected work", "year": ""}]
    return []


EXTRACTORS = {
    "David Zwirner":      extract_zwirner,
    "Pace Gallery":       extract_pace,
    "Sadie Coles HQ":     extract_sadiecoles,
    "White Cube":         extract_whitecube,
    "Galleria Continua":  extract_continua,
    "Marian Goodman":     extract_mariangoodman,
    "Lisson Gallery":     extract_lisson,
    "Sprüth Magers":      extract_spruethmagers,
    "Galerie Perrotin":   extract_perrotin,
    "Massimo De Carlo":   extract_mdc,
    "Hauser & Wirth":     extract_hauserwirth,
}


def dedupe(cands):
    seen, out = set(), []
    for c in cands:
        base = _norm_for_dedupe(c["image"])
        if base in seen:
            continue
        seen.add(base)
        out.append(c)
    return out


def main():
    results = {}
    for aid, name, gallery, url in ARTISTS:
        html = fetch_html(url)
        if not html:
            results[aid] = []
            print(f"  [{aid}] {name:<30} ({gallery}): fetch failed")
            continue
        ext = EXTRACTORS.get(gallery)
        if not ext:
            print(f"  [{aid}] {name}: no extractor for {gallery}")
            results[aid] = []
            continue
        cands = ext(html, name)
        cands = dedupe(cands)
        # Stamp source on all
        for c in cands:
            c["source"] = gallery
            c["credit"] = f"Courtesy {gallery}"
        results[aid] = cands
        print(f"  [{aid}] {name:<30} ({gallery}): {len(cands)} works")
        time.sleep(0.3)
    OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    total = sum(len(v) for v in results.values())
    nonzero = sum(1 for v in results.values() if v)
    print(f"\nWritten {total} works across {nonzero}/{len(ARTISTS)} artists.")


if __name__ == "__main__":
    main()
