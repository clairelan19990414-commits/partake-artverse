#!/usr/bin/env python3
"""
Fetch one portrait per artist. Strategy:
  1. Try the artist's gallery profile page (og:image is usually a portrait/header).
  2. Try Wikipedia page summary thumbnail (professional press images via Wikidata).
Result is written to quiz_portraits.json: { aid: {url, source} }
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

OUT = Path(__file__).parent / "quiz_portraits.json"

# (aid, name, gallery_url_or_None, wiki_slug)
ARTISTS = [
    ("a146", "Lucas Arruda",            "https://www.davidzwirner.com/artists/lucas-arruda",            "Lucas_Arruda_(artist)"),
    ("a176", "Victor Man",              "https://www.davidzwirner.com/artists/victor-man",              "Victor_Man"),
    ("a188", "Yu Nishimura",            "https://www.davidzwirner.com/artists/yu-nishimura",            "Yu_Nishimura"),
    ("a206", "Amy Sillman",             "https://www.davidzwirner.com/artists/amy-sillman",             "Amy_Sillman"),
    ("a203", "Dana Schutz",             "https://www.davidzwirner.com/artists/dana-schutz",             "Dana_Schutz"),
    ("a221", "Lisa Yuskavage",          "https://www.davidzwirner.com/artists/lisa-yuskavage",          "Lisa_Yuskavage"),
    ("a313", "Marina Perez Simao",      "https://www.pacegallery.com/artists/marina-perez-simao/",      "Marina_Perez_Sim%C3%A3o"),
    ("a980", "Wilhelm Sasnal",          "https://www.sadiecoles.com/artists/wilhelm-sasnal",            "Wilhelm_Sasnal"),
    ("a291", "Mao Yan",                 "https://www.pacegallery.com/artists/mao-yan/",                 "Mao_Yan"),
    ("a929", "Matthew Wong",            None,                                                           "Matthew_Wong"),
    ("a996", "Co Westerik",             "https://www.sadiecoles.com/artists/co-westerik",               "Co_Westerik"),
    ("a356", "Etel Adnan",              None,                                                           "Etel_Adnan"),

    ("a149", "Huma Bhabha",             "https://www.davidzwirner.com/artists/huma-bhabha",             "Huma_Bhabha"),
    ("a57",  "Carol Bove",              "https://www.davidzwirner.com/artists/carol-bove",              "Carol_Bove"),
    ("a213", "Andra Ursuta",            "https://www.davidzwirner.com/artists/andra-ursuta",            "Andra_Ursu%C8%9Ba"),
    ("a501", "Adrian Villar Rojas",     "https://www.mariangoodman.com/artists/adrian-villar-rojas",    "Adri%C3%A1n_Villar_Rojas"),
    ("a794", "Berlinde De Bruyckere",   "https://www.galleriacontinua.com/artists/berlinde-de-bruyckere-21", "Berlinde_De_Bruyckere"),
    ("a458", "Cristina Iglesias",       None,                                                           "Cristina_Iglesias"),
    ("a963", "Tau Lewis",               "https://www.sadiecoles.com/artists/tau-lewis",                 "Tau_Lewis"),
    ("a803", "Eva Jospin",              "https://www.galleriacontinua.com/artists/eva-jospin-320",      "Eva_Jospin"),
    ("a853", "Sanford Biggers",         None,                                                           "Sanford_Biggers"),
    ("a384", "Klara Hosnedlova",        "https://whitecube.com/artists/artist/klara_hosnedlova",        "Kl%C3%A1ra_Hosnedlov%C3%A1"),

    ("a257", "Hai Bo",                  "https://www.pacegallery.com/artists/hai-bo/",                  "Hai_Bo"),
    ("a273", "Josef Koudelka",          None,                                                           "Josef_Koudelka"),
    ("a296", "Richard Misrach",         None,                                                           "Richard_Misrach"),
    ("a79",  "Roni Horn",               None,                                                           "Roni_Horn"),

    ("a396", "Christian Marclay",       "https://whitecube.com/artists/artist/christian_marclay",       "Christian_Marclay"),
    ("a446", "Tacita Dean",             None,                                                           "Tacita_Dean"),
    ("a649", "Wael Shawky",             "https://www.lissongallery.com/artists/wael-shawky",            "Wael_Shawky"),
    ("a490", "Tino Sehgal",             "https://www.mariangoodman.com/artists/tino-sehgal",            "Tino_Sehgal"),
    ("a583", "Ryan Trecartin",          "https://spruethmagers.com/artists/ryan-trecartin/",            "Ryan_Trecartin"),

    ("a414", "Doris Salcedo",           None,                                                           "Doris_Salcedo"),
    ("a795", "Leandro Erlich",          "https://www.galleriacontinua.com/artists/leandro-erlich-24",   "Leandro_Erlich"),
    ("a841", "Nari Ward",               "https://www.galleriacontinua.com/artists/nari-ward-76",        "Nari_Ward"),
    ("a20",  "Theaster Gates",          None,                                                           "Theaster_Gates"),
    ("a311", "Adam Pendleton",          "https://www.pacegallery.com/artists/adam-pendleton/",          "Adam_Pendleton"),

    ("a159", "Marcel Dzama",            "https://www.davidzwirner.com/artists/marcel-dzama",            "Marcel_Dzama"),
    ("a191", "Raymond Pettibon",        "https://www.davidzwirner.com/artists/raymond-pettibon",        "Raymond_Pettibon"),
    ("a735", "Sophie Calle",            None,                                                           "Sophie_Calle"),
    ("a83",  "Glenn Ligon",             None,                                                           "Glenn_Ligon"),

    # ── Batch 2 ──
    ("a596", "Allora & Calzadilla",     "https://www.lissongallery.com/artists/allora-calzadilla",      "Allora_and_Calzadilla"),
    ("a381", "Mona Hatoum",             "https://whitecube.com/artists/artist/mona_hatoum",             "Mona_Hatoum"),
    ("a584", "Rosemarie Trockel",       "https://spruethmagers.com/artists/rosemarie-trockel/",         "Rosemarie_Trockel"),
    ("a533", "Cyprien Gaillard",        "https://spruethmagers.com/artists/cyprien-gaillard/",          "Cyprien_Gaillard"),
    ("a821", "Hans Op de Beeck",        "https://www.galleriacontinua.com/artists/hans-op-de-beeck",    "Hans_Op_de_Beeck"),
    ("a545", "Karen Kilimnik",          "https://spruethmagers.com/artists/karen-kilimnik/",            "Karen_Kilimnik"),
    ("a364", "Miroslaw Balka",          "https://whitecube.com/artists/artist/miroslaw_balka",          "Miros%C5%82aw_Ba%C5%82ka"),
    ("a282", "Maya Lin",                "https://www.pacegallery.com/artists/maya-lin/",                "Maya_Lin"),
    ("a567", "Pamela Rosenkranz",       "https://spruethmagers.com/artists/pamela-rosenkranz/",         "Pamela_Rosenkranz"),
    ("a371", "Cerith Wyn Evans",        "https://whitecube.com/artists/artist/cerith_wyn_evans",        "Cerith_Wyn_Evans"),
]

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 Safari/605.1.15"

def _fetch_text(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout, context=_CTX) as r:
        return r.read().decode("utf-8", errors="ignore")


def _extract_og_image(html):
    m = re.search(
        r'<meta\s+[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']',
        html, re.I)
    if m:
        return m.group(1)
    m = re.search(
        r'<meta\s+[^>]*content=["\']([^"\']+)["\'][^>]*property=["\']og:image["\']',
        html, re.I)
    return m.group(1) if m else None


def from_gallery(url):
    if not url:
        return None
    try:
        html = _fetch_text(url, timeout=20)
    except Exception as e:
        return None
    og = _extract_og_image(html)
    if og and not re.search(r'logo|favicon|placeholder', og, re.I):
        return og
    return None


def from_wikipedia(slug):
    if not slug:
        return None
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{slug}"
        d = json.loads(_fetch_text(url, timeout=15))
    except Exception:
        return None
    thumb = (d.get("thumbnail") or {}).get("source")
    if thumb:
        # Prefer original size if available (larger)
        orig = (d.get("originalimage") or {}).get("source")
        return orig or thumb
    return None


def main():
    portraits = {}
    for aid, name, gurl, slug in ARTISTS:
        result = {"url": None, "source": None}
        # 1. Try gallery og:image
        url = from_gallery(gurl)
        if url:
            result["url"] = url
            result["source"] = gurl
            print(f"  [{aid}] {name} ← gallery og:image")
        else:
            # 2. Try Wikipedia
            url = from_wikipedia(slug)
            if url:
                result["url"] = url
                result["source"] = f"Wikipedia: {slug}"
                print(f"  [{aid}] {name} ← wikipedia")
            else:
                print(f"  [{aid}] {name} — NOT FOUND")
        portraits[aid] = result
        time.sleep(0.2)
    OUT.write_text(json.dumps(portraits, indent=2, ensure_ascii=False))
    hit = sum(1 for p in portraits.values() if p["url"])
    print(f"\nDone: {hit}/{len(ARTISTS)} portraits found.")
    print(f"Written to {OUT}")


if __name__ == "__main__":
    main()
