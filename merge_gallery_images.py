#!/usr/bin/env python3
"""
Merge gallery-scraped images into quiz_images.json.
The museum-API hits are already there from fetch_quiz_images.py.
This script adds the gallery candidates we collected via WebFetch + curl.
"""

import json
from pathlib import Path

DATA = Path(__file__).parent / "quiz_images.json"

# (artist_id, source-gallery, title, year, image_url)
GALLERY = [
    ("a149", "David Zwirner", "Remembering Things", "2025",
     "https://cdn.sanity.io/images/juzvn5an/release-adp/504c6cfa218810c2965fa9d9668c9231a9290b3b-3000x2250.jpg?w=3840"),

    ("a396", "White Cube", "Christian Marclay (exhibition view), Centre Pompidou", "2022",
     "https://white-cube.transforms.svdcdn.com/production/imported-artworks/Christian-Marclay/Christian-Marclay-Centre-Pompidou/a194352.jpg?w=720&q=80&auto=format&fit=crop&crop=focalpoint&fp-x=0.5&fp-y=0.5&dm=1688002798&s=c508ee5a5a03f2027045030b63c8f35f"),

    ("a176", "David Zwirner", "Maternity with Legend", "2024",
     "https://cdn.sanity.io/images/juzvn5an/release-adp/c44f465cead30c92c224a0e2bd51906fb72a8cb0-2447x3000.jpg?w=3840"),

    ("a188", "David Zwirner", "Permeation", "2025",
     "https://cdn.sanity.io/images/juzvn5an/release-adp/acda9d843ec7011d0be03a9cf7f4b52c56f7405f-3000x2562.jpg?w=3840"),

    ("a213", "David Zwirner", "Untitled (bronze, copper, antique glass, stone)", "2025",
     "https://cdn.sanity.io/images/juzvn5an/release-adp/cd06d019832d859af297de3a52126dbf179d98f1-3000x2249.jpg?w=3840"),

    ("a291", "Pace Gallery", "Madam", "2022",
     "https://www.pacegallery.com/media/images/971559keyKM11VJ82_GUFq6QEYIyJAg.width-2000.webp"),

    ("a257", "Pace Gallery", "The Southern Series No. 24", "2012",
     "https://www.pacegallery.com/media/images/68802.01.width-2000.jpg"),

    ("a311", "Pace Gallery", "Untitled (WE ARE NOT)", "2019",
     "https://www.pacegallery.com/media/images/19-148_AP_JPG_LR.original.jpg"),

    ("a996", "Sadie Coles HQ", "Grasses and Hand (Grassen en Hand)", None,
     "https://sadie-coles.transforms.svdcdn.com/production/images/Artists/Co-Westerik/Selected-Works/HQ22-CW15542P.jpeg?w=1200&auto=compress%2Cformat&fit=crop"),

    ("a963", "Sadie Coles HQ", "Lunar infants and trembling reeds", "2025",
     "https://sadie-coles.transforms.svdcdn.com/production/images/Artists/Tau-Lewis/Exhibitions/2025-Bury-Street/Artworks/Tau-Lewis_Lunar_infants_and_trembling_reeds_2025.jpeg"),

    ("a501", "Marian Goodman Gallery", "Two Suns", "2015",
     "https://static-assets.artlogic.net/w_2400,h_1800,c_limit,f_auto,fl_lossy,q_auto/ws-mariangoodman/usr/artists/images/67/avr-2015-two-suns.png"),

    ("a583", "Sprüth Magers", "Please Knock Before Going Outside (Flood Season)", "2023",
     "https://res.cloudinary.com/smimagebank/image/upload/w_2560,c_limit,f_auto,fl_progressive/v1700473268/RYT_54406_Please_Knock_Before_Going_Outside_Flood_Season_2023_01_gm_ivmt5c.jpg"),

    ("a794", "Galleria Continua", "Same Old, Same Old (installation view)", "2025",
     "https://www.galleriacontinua.com/assets/artists_images/786x430/BERLINDE-DE-BRUYCKERE-Same_Old_Same_Old-04-DSB04593.jpg"),

    ("a803", "Galleria Continua", "Trompe l'œil", "2024",
     "https://www.galleriacontinua.com/assets/artists_images/786x430/Eva_Jospin_Trompe_l_oeil_1.jpg"),

    ("a795", "Galleria Continua", "Hybrids", "2026",
     "https://www.galleriacontinua.com/assets/artists_images/786x430/Hybrids_Leandro_Erlich_2026_HYdh.jpg"),

    ("a841", "Galleria Continua", "Spring Note", "2025",
     "https://www.galleriacontinua.com/assets/artists_images/786x430/NARI_WARD_SPRING_NOTE_01.jpg"),

    ("a384", "White Cube", "Klára Hosnedlová (artist page header — embroidery)", None,
     "https://white-cube.transforms.svdcdn.com/production/uploads/Headers/Artist-Pages/JJ77776-1.jpg?w=1200&h=630&q=82&auto=format&fit=crop&dm=1722510806"),

    ("a649", "Lisson Gallery", "Drama 1882 (Venice 2024 installation)", "2024",
     "https://lisson-art.s3.amazonaws.com/uploads/attachment/image/body/29221/WSHA240001_Install-Venice-2024_001.3.jpeg"),

    ("a490", "Marian Goodman Gallery", "Tino Sehgal (Oxfordshire 2021 exhibition view)", "2021",
     "https://static-assets.artlogic.net/w_800,h_800,c_limit,f_auto,fl_lossy,q_auto/ws-mariangoodman/usr/images/exhibitions/main_image_override/items/93/93ea3db85ef440a9a85f12c81b0bcd5a/sehgal-2021-exhibition-oxfordshire-01.jpeg"),

    ("a929", "Massimo De Carlo", "Matthew Wong (selected work)", None,
     "https://mdc-space.fra1.cdn.digitaloceanspaces.com/prod/_jpg3000/Social_Share_img_2023-03-29-142746_xmxa.jpg"),

    ("a313", "Pace Gallery", "Marina Perez Simão (selected work)", None,
     "https://www.pacegallery.com/media/images/49378.width-1100.jpg"),

    ("a57", "David Zwirner", "Frieze 2022 Presentation (installation view of new sculptures)", "2022",
     "https://cdn.sanity.io/images/juzvn5an/release-adp/f0f70812f6702e7f2d51854064719f27e4fd2396-3000x1765.jpg?w=3840"),

    ("a980", "Sadie Coles HQ", "Anka", "2023",
     "https://sadie-coles.transforms.svdcdn.com/production/images/Artists/Wilhelm-Sasnal/Artworks/HQ27-WS20348P_Anka_2023_4.jpeg?w=1200&h=630&q=82&auto=format&fit=crop"),
]


def main():
    data = json.loads(DATA.read_text())
    added = 0
    for aid, source, title, year, image in GALLERY:
        if aid not in data:
            print(f"  WARN: {aid} not in quiz_images.json — skipping")
            continue
        entry = {
            "source": source,
            "title": title,
            "year": year or "",
            "image": image,
            "credit": f"Courtesy {source}, image accessed from gallery website",
            "url": None,
        }
        data[aid]["candidates"].insert(0, entry)
        added += 1
    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    have_image = sum(1 for v in data.values() if v["candidates"])
    print(f"Added {added} gallery candidates")
    print(f"Total artists with at least one image: {have_image}/{len(data)}")
    no_img = [v["name"] for v in data.values() if not v["candidates"]]
    if no_img:
        print(f"Still without images: {no_img}")


if __name__ == "__main__":
    main()
