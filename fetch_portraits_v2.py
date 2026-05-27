#!/usr/bin/env python3
"""
Re-fetch portraits — Wikipedia thumbnails ONLY. Gallery og:image is
almost always the lead artwork, not a photo of the artist, so we drop
that source entirely. For artists with no Wikipedia portrait, leave the
record empty so the card falls back to an initial-letter placeholder.
"""

import json
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
UA = "partake-quiz/1.0 (educational; portrait re-fetch)"

# (id, name, wikipedia_slug)
ARTISTS = [
    ("a146", "Lucas Arruda", "Lucas_Arruda_(artist)"),
    ("a176", "Victor Man", "Victor_Man"),
    ("a188", "Yu Nishimura", "Yu_Nishimura"),
    ("a206", "Amy Sillman", "Amy_Sillman"),
    ("a203", "Dana Schutz", "Dana_Schutz"),
    ("a221", "Lisa Yuskavage", "Lisa_Yuskavage"),
    ("a313", "Marina Perez Simao", "Marina_Perez_Sim%C3%A3o"),
    ("a980", "Wilhelm Sasnal", "Wilhelm_Sasnal"),
    ("a291", "Mao Yan", "Mao_Yan"),
    ("a929", "Matthew Wong", "Matthew_Wong"),
    ("a996", "Co Westerik", "Co_Westerik"),
    ("a356", "Etel Adnan", "Etel_Adnan"),
    ("a149", "Huma Bhabha", "Huma_Bhabha"),
    ("a57",  "Carol Bove", "Carol_Bove"),
    ("a213", "Andra Ursuta", "Andra_Ursu%C8%9Ba"),
    ("a501", "Adrian Villar Rojas", "Adri%C3%A1n_Villar_Rojas"),
    ("a794", "Berlinde De Bruyckere", "Berlinde_De_Bruyckere"),
    ("a458", "Cristina Iglesias", "Cristina_Iglesias"),
    ("a963", "Tau Lewis", "Tau_Lewis"),
    ("a803", "Eva Jospin", "Eva_Jospin"),
    ("a853", "Sanford Biggers", "Sanford_Biggers"),
    ("a384", "Klara Hosnedlova", "Kl%C3%A1ra_Hosnedlov%C3%A1"),
    ("a257", "Hai Bo", "Hai_Bo"),
    ("a273", "Josef Koudelka", "Josef_Koudelka"),
    ("a296", "Richard Misrach", "Richard_Misrach"),
    ("a79",  "Roni Horn", "Roni_Horn"),
    ("a396", "Christian Marclay", "Christian_Marclay"),
    ("a446", "Tacita Dean", "Tacita_Dean"),
    ("a649", "Wael Shawky", "Wael_Shawky"),
    ("a490", "Tino Sehgal", "Tino_Sehgal"),
    ("a583", "Ryan Trecartin", "Ryan_Trecartin"),
    ("a414", "Doris Salcedo", "Doris_Salcedo"),
    ("a795", "Leandro Erlich", "Leandro_Erlich"),
    ("a841", "Nari Ward", "Nari_Ward"),
    ("a20",  "Theaster Gates", "Theaster_Gates"),
    ("a311", "Adam Pendleton", "Adam_Pendleton"),
    ("a159", "Marcel Dzama", "Marcel_Dzama"),
    ("a191", "Raymond Pettibon", "Raymond_Pettibon"),
    ("a735", "Sophie Calle", "Sophie_Calle"),
    ("a83",  "Glenn Ligon", "Glenn_Ligon"),
    # Batch 2
    ("a596", "Allora & Calzadilla", "Allora_and_Calzadilla"),
    ("a381", "Mona Hatoum", "Mona_Hatoum"),
    ("a584", "Rosemarie Trockel", "Rosemarie_Trockel"),
    ("a533", "Cyprien Gaillard", "Cyprien_Gaillard"),
    ("a821", "Hans Op de Beeck", "Hans_Op_de_Beeck"),
    ("a545", "Karen Kilimnik", "Karen_Kilimnik"),
    ("a364", "Miroslaw Balka", "Miros%C5%82aw_Ba%C5%82ka"),
    ("a282", "Maya Lin", "Maya_Lin"),
    ("a567", "Pamela Rosenkranz", "Pamela_Rosenkranz"),
    ("a371", "Cerith Wyn Evans", "Cerith_Wyn_Evans"),
]


def get_portrait(slug):
    """Wikipedia summary endpoint — returns the infobox image, which is
    almost always a portrait of the subject."""
    try:
        req = urllib.request.Request(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{slug}",
            headers={"User-Agent": UA},
        )
        with urllib.request.urlopen(req, timeout=15, context=_CTX) as r:
            d = json.loads(r.read())
        # Prefer originalimage (full-size); fall back to thumbnail
        orig = (d.get("originalimage") or {}).get("source")
        thumb = (d.get("thumbnail") or {}).get("source")
        return orig or thumb
    except Exception:
        return None


def main():
    results = {}
    for aid, name, slug in ARTISTS:
        url = get_portrait(slug)
        if url:
            results[aid] = {"url": url, "source": f"Wikipedia: {slug}"}
            print(f"  [{aid}] {name} ← wikipedia")
        else:
            results[aid] = {"url": None, "source": None}
            print(f"  [{aid}] {name} — none")
        time.sleep(2.5)  # respect Wikipedia rate limits

    OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    hit = sum(1 for v in results.values() if v["url"])
    print(f"\nDone: {hit}/{len(ARTISTS)} portraits found.")


if __name__ == "__main__":
    main()
