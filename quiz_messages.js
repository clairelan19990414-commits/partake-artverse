// Quiz pool messages — 3 sentences per artist:
//   1. Whereabouts (where based, training, geographic locus)
//   2. Experience / relativity (what shaped the practice — lineage, biography, historical moment)
//   3. Relevance + artist statement (why the work matters now, the thesis)
// Used by the embedded quiz on artist_map.html.

const QUIZ_MESSAGES = {

  // ── Painting ────────────────────────────────────────────────────

  a146: { // Lucas Arruda
    message: "Arruda lives and works in São Paulo, where he was trained at the Fundação Armando Álvares Penteado in a Brazilian painterly tradition shaped by both modernist abstraction and Romantic landscape. His small-format Deserto-Modelo paintings are built from memory rather than observation, distilling sky and horizon into atmospheric thresholds that hover between geography and inner state. He treats landscape as a verb — an event of perception — and insists that what counts is not what is depicted but the time the painting holds inside it."
  },

  a176: { // Victor Man
    message: "Romanian-born and based between Cluj and Berlin, Man emerged from the Cluj School alongside Adrian Ghenie and Mircea Cantor in the early 2000s. His paintings draw on Northern Renaissance portraiture, esoteric symbolism, and Eastern Orthodox iconography, filtered through a deliberate slowness that resists art-world tempo. He uses figuration as a way to hold ambiguity in place — bodies and objects in his work are vessels for hermetic, art-historical, and erotic readings that never fully resolve."
  },

  a188: { // Yu Nishimura
    message: "Based in Kanagawa, Japan, Nishimura paints in a register pulled equally from anime backgrounds and Édouard Vuillard's domestic interiors. Working with thin glazes and visible weave, he renders figures as if seen through a soft veil — half-formed, half-receding — refusing the hard outline contemporary painting habitually demands. His message is one of attention without grasping: a quiet plea for the looseness and porosity that figurative painting has largely traded away for legibility."
  },

  a206: { // Amy Sillman
    message: "Sillman lives in Brooklyn and Berlin and trained at SVA before becoming a central figure in the post-postmodern revival of gestural painting in New York from the late 1990s. Her practice braids drawing, painting, and writing — she edits the zine The O-G and writes extensively on color and process — and her paintings are full of revision and self-argument. The work insists that abstraction can carry feeling and politics at once: that a yellow next to a green can hold an uncertainty about gender, mood, or the very question of whether to keep painting."
  },

  a203: { // Dana Schutz
    message: "Schutz lives in Brooklyn and trained at CalArts and Columbia; she emerged in the early 2000s with the Frank from Observation series, in which she painted the world's last man. Her practice operates by invented constraint — imagined subjects, scenarios that could never have been witnessed — making narrative painting a way of testing what the form can still believe in. After Open Casket (2016) and the controversy that followed, her work has continued to ask whether painting can host group catastrophe, panic, and gallows comedy without flattening them into kitsch."
  },

  a221: { // Lisa Yuskavage
    message: "Yuskavage lives in New York and trained at Tyler and Yale, where she studied alongside John Currin and Sean Landers. Her pin-up-derived nudes mobilize the language of soft-core figuration, kitsch, and 19th-century landscape pastoral to court vulgarity head-on rather than ironize it. The message is that the eroticized female body can be a serious site for color theory, light, and shame — that taste itself, including the viewer's discomfort, belongs inside the frame of the painting."
  },

  a313: { // Marina Perez Simão
    message: "Perez Simão lives and works in São Paulo and came to painting after curatorial work, including with the Cildo Meireles estate. Her paintings flatten Brazilian modernist landscape — Tarsila, Volpi, Burle Marx — into rippling colour-field bands that move between geometry and sensation. She frames her work as a contemporary continuation of antropofagia: digesting European abstraction through a tropical formal vocabulary that is neither nostalgic nor postcolonial-corrective but unapologetically pleasurable."
  },

  a980: { // Wilhelm Sasnal
    message: "Sasnal is based in Tarnów and Kraków, Poland, and was a founding member of the Ładnie Group in the late 1990s, which broke from Polish historical painting toward pop and the everyday. He paints from photographs — family snapshots, news images, film stills, Holocaust documentation — translating each into a flat, deskilled mark that interrogates what a photograph can no longer do. The work argues that painting in post-1989 Eastern Europe is a way of slowing down history: each image becomes a small act of refusing to scroll past."
  },

  a291: { // Mao Yan
    message: "Mao Yan lives and teaches in Nanjing, where he is one of the central figures of the post-Cultural Revolution generation of Chinese realist painters. His portraits — typically of a single sitter, Thomas, his German friend, painted over many years — strip down representation to a pale, near-monochrome surface in which the face barely emerges. He treats portraiture as a slow exposure of presence, refusing both Socialist Realism's heroic legibility and the Cynical Realism boom of the 1990s."
  },

  a929: { // Matthew Wong
    message: "Wong was born in Toronto, lived between Canada and Hong Kong, and was self-taught — he turned to painting in his late 20s after photography and writing, learning publicly through Facebook conversations with John Yau, Peter Doig, and others. His landscapes braid Van Gogh, Shitao, and Bonnard into solitary, dreamlike interiors and forests rendered in dotted, jewel-toned facture. After his death in 2019 at thirty-five, the work has become a touchstone for the question of whether figurative painting can still be made from solitude rather than from market demand."
  },

  a996: { // Co Westerik
    message: "Westerik lived and worked in The Hague for nearly all of his life and trained at the Royal Academy of Art there in the immediate post-war period. His small, hyper-detailed paintings of bodies, hands, and intimate encounters owe nothing to the Cobra moment that surrounded him, opting instead for a deeply slow, psychologically charged realism. The work asks for a contemplation of skin, contact, and the weight of small gestures at a scale and speed contemporary painting has largely abandoned."
  },

  a356: { // Etel Adnan
    message: "Adnan was born in Beirut to a Greek mother and a Syrian Ottoman father, lived through the Lebanese Civil War in exile in Paris and Sausalito, and was a poet before she was a painter. Her small landscapes — most famously of Mount Tamalpais, seen from her California kitchen — are built from straight palette-knife strokes laid down quickly and without correction. She insisted that painting was where she could be silent, that color was a way of saying what her Arabic, French, and English could not — and the late market discovery of her work, after age eighty, did not change that."
  },

  // ── Sculpture ────────────────────────────────────────────────────

  a149: { // Huma Bhabha
    message: "Bhabha was born in Karachi and is based in Poughkeepsie, New York; she trained at RISD and Columbia and built her early sculptures from junkyard finds while working as an assistant to artists in Manhattan. Her totemic figures — assembled from cork, styrofoam, clay, and burnt wood — invoke Gandharan Buddha statuary, sci-fi prophecy, and post-conflict ruin in a single body. The work insists that figuration can carry catastrophe without illustrating it: each piece is a witness left standing after something we are not shown."
  },

  a57: { // Carol Bove
    message: "Bove lives and works in Red Hook, Brooklyn, and emerged in the early 2000s with sculptural arrangements that drew explicitly on the 1960s — Playboy magazines, peacock feathers, Donald Judd. Her current 'collage sculpture' bends thick steel I-beams into floppy ribbon-like forms that read as both monumental modernist sculpture and the parody of it. The work argues that the postwar formal vocabulary is still good for something, but only if you treat it as malleable rather than canonical."
  },

  a213: { // Andra Ursuța
    message: "Ursuța grew up in Salonta, Romania, under Ceaușescu and moved to New York in the 1990s; she now lives and works in Brooklyn. Her recent Vandal Lust sculptures are cast in lead crystal and glass from forms she shapes around her own body, producing translucent ghosts that read as armor, fetish, and devotional object at once. She uses sculpture as a way to embody Eastern European post-Communist abjection without explaining it — the body becomes a site of contaminated glamour."
  },

  a501: { // Adrián Villar Rojas
    message: "Villar Rojas was born in Rosario, Argentina, and works site-specifically across a nomadic, team-based studio practice that has installed at the Met rooftop, Athens, the Geffen, and the Istanbul Biennial. His monumental unfired-clay sculptures — including a full-scale Michelangelo's David reduced to debris — are made to crack and decay across the run of the exhibition. He treats geology and extinction as raw material, asking what a sculpture is when its medium is the future viewer's absence."
  },

  a794: { // Berlinde De Bruyckere
    message: "De Bruyckere lives and works in Ghent, raised in a Catholic boarding school whose imagery of suffering bodies haunts her practice. She casts wax over wax to make horse hides, human limbs, and tree forms that look both freshly dead and slowly transforming, often shown under blankets or inside vitrines. Her work proposes the wounded body as a contemporary site of the sacred — neither religious nor secular, but stubbornly material."
  },

  a458: { // Cristina Iglesias
    message: "Iglesias lives in Madrid and trained as a ceramicist before studying sculpture in London under Tony Cragg; she emerged in the late 1980s as part of a new Spanish sculptural generation. Her work — vegetal screens of bronze, suspended pavilions, and water installations carved into public ground — places the viewer inside architecture that is also landscape. She frames her practice as a feminist re-routing of public sculpture: rather than the standing male monument, an enterable, ambiguous space."
  },

  a963: { // Tau Lewis
    message: "Lewis is Black Canadian, born in Toronto and based in Brooklyn, and is self-taught — she began making work after the 2016 election from textile scraps gathered in her family's home. Her quilted masks and figures stitch together leather, fur, sequins, and found cloth into beings she describes as ancestors, healers, or scouts from a Black aquatic future. The work proposes diaspora as a form of repair: that craft, intuition, and material salvage can compose a worldview the gallery system did not author."
  },

  a803: { // Eva Jospin
    message: "Jospin lives in Paris and trained at the Beaux-Arts there in the early 2000s; she works almost exclusively in cardboard, layering and cutting it to build dense forest interiors and grotto walls. Her source material is the romantic European garden — Versailles, the picturesque ruin, the cabinet of curiosities — recast in a humble, recyclable material. She argues that the forest, as a Western imaginative space, is still available for sculpture if you are willing to make it out of trash."
  },

  a853: { // Sanford Biggers
    message: "Biggers lives in New York and studied in Atlanta, Philadelphia, and Japan, where his interest in Buddhism and the African diaspora collided. He paints, sews, and overlays on antique American quilts — many possibly used as signals on the Underground Railroad — embedding African masks, mandalas, and bullet holes into the cloth. The work insists that American material history is already a Black history, and that the role of the artist is to make it readable again."
  },

  a384: { // Klára Hosnedlová
    message: "Hosnedlová was born in Uherské Hradiště and lives in Berlin, trained at UMPRUM in Prague in a Czech tradition of disciplined craft labour. She works in silk-thread embroidery, building tonal gradations stitch by surgical stitch, often staged inside immersive sand-and-glass environments. Her practice argues that the slow technical knowledge of textile labour — Eastern European, gendered, undervalued — is a contemporary medium, not a heritage."
  },

  // ── Photography ─────────────────────────────────────────────────

  a257: { // Hai Bo
    message: "Hai Bo lives in Beijing, was born in Changchun in the year of the Cultural Revolution, and trained as a painter before moving to photography in the 1990s. His best-known series re-stages old family group portraits with the same sitters decades later — and with the missing absent — exposing the temporal violence of late-twentieth-century China without comment. He uses photography as a slow elegy rather than a record, treating the medium's claim on the real as an act of mourning."
  },

  a273: { // Josef Koudelka
    message: "Koudelka was born in Moravia in 1938, photographed the 1968 Soviet invasion of Prague clandestinely, and lived as a stateless exile in Europe through the Magnum cooperative for the next four decades. His Gypsies and Exiles series document Roma communities, war landscapes, and the European post-war condition in dense, off-balance black-and-white compositions. He treats documentary photography as a form of geological time: each frame holds dispossession at landscape scale."
  },

  a296: { // Richard Misrach
    message: "Misrach lives in Berkeley and has spent more than four decades photographing the American desert in large-format colour, from Death Valley to the Salton Sea to the petrochemical corridor of Louisiana's Cancer Alley. His Desert Cantos cycle is built as a long-form essay: bombing ranges, dead animals, burning palms, all rendered in painterly colour at sublime scale. The work argues that environmental destruction in the United States is not a future warning but a long-running record, and that beauty is one of the few tools left to make people look at it."
  },

  a79: { // Roni Horn
    message: "Horn lives in New York and has spent forty years travelling to Iceland, where she made the long-running Library of Water archive in a former library in Stykkishólmur. Her practice moves between photography (the Cabinet of, Bird, and You Are the Weather series), cast-glass sculpture, drawing, and written text on identity and androgyny. She insists that identity — of a self, a place, a piece of glass — is unstable, mirrored, never closed, and that the role of art is to keep that instability visible rather than resolve it."
  },

  // ── Video / Film / Performance ──────────────────────────────────

  a396: { // Christian Marclay
    message: "Marclay was born in San Rafael, California, raised in Geneva, and trained in Boston; he began in the 1980s as one of the first turntablist musicians, treating LPs as sculptural material. His twenty-four-hour montage The Clock (2010) splices thousands of film clips that show or mention the current real-world time, so the work and the viewer's watch run together. The piece argues that cinema's century-long fragmentation of time is now the medium of everyday attention — and that editing, as a practice, is the contemporary form of composition."
  },

  a446: { // Tacita Dean
    message: "Dean was born in Canterbury, trained at the Slade, and lives in Berlin and Los Angeles; she has campaigned publicly to keep 16mm and 35mm film stock in production. Her films — Disappearance at Sea, FILM (Tate Turbine Hall), and the Bubble House — let the camera sit on landscape, weather, and absence at a duration the medium can barely sustain. She frames analog film not as nostalgia but as a different cognitive technology: a way of attending to time that digital capture has efficiently erased."
  },

  a649: { // Wael Shawky
    message: "Shawky was born in Alexandria, lives between Alexandria and Philadelphia, and founded MASS Alexandria as an independent space for young Egyptian artists. His Cabaret Crusades trilogy is a feature-length narration of the Crusades performed by 200-year-old Murano-glass marionettes, drawn from Arab historian Amin Maalouf's source material. Shawky's argument is that the historical record is itself a performance — that the way the West narrates its own history depends entirely on which body, and whose hand, is doing the speaking."
  },

  a490: { // Tino Sehgal
    message: "Sehgal was born in London, raised in Düsseldorf and Paris, studied political economy and dance, and lives in Berlin. His 'constructed situations' — choreographed encounters in museums between trained interpreters and visitors — exist only in spoken contracts; no documentation, photographs, or installation views are permitted. He argues that the contemporary economy's main product is the immaterial — speech, encounter, attention — and that art's task is to take that production seriously as form."
  },

  a583: { // Ryan Trecartin
    message: "Trecartin was born in Texas, trained at RISD with Lizzie Fitch (his ongoing collaborator), and lives in Athens, Ohio, where the pair built a rural compound for production. His feature-length videos — I-Be Area, Re'Search Wait'S, Comma Boat — are hyperkinetic family-and-friends performances in heavy digital makeup, scripted as if a teenage internet swallowed itself. Trecartin treats the post-2007 social-web subject as a real subject for art, and his videos remain one of the few honest attempts to render what online attention does to identity."
  },

  // ── Installation / Conceptual ───────────────────────────────────

  a414: { // Doris Salcedo
    message: "Salcedo lives in Bogotá and has, since the 1980s, built a practice entirely from the testimony of victims of Colombia's long civil violence — paramilitary, FARC, and state. Her sculptures embed household furniture, women's clothing, and human hair in concrete; her interventions — like Shibboleth, a 167-metre crack in the Tate Modern floor — are public acts of mourning at architectural scale. The work argues that contemporary sculpture's first responsibility is to the named, specific, unburied dead; abstraction is allowed only on those terms."
  },

  a795: { // Leandro Erlich
    message: "Erlich lives in Buenos Aires and is the son of an architect; his early career was built around precisely engineered perceptual illusions — a swimming pool seen from below by viewers walking through it, an elevator shaft that drops into infinity. His work has migrated from a Surrealist-aligned 1990s vocabulary into civic-scale public sculpture (Maison Fond, the Pulled by the Roots house). He argues that the contemporary urban subject is now so habituated to the perceptual interface that a moment of disorientation is a political event, however brief."
  },

  a841: { // Nari Ward
    message: "Ward was born in St Andrew, Jamaica, moved to Brooklyn as a child, and trained at City College and Brooklyn College in the early 1990s. He builds installations from the materials of the post-industrial Black diaspora — shopping carts, fire hoses, baby strollers, copper nails — found in his Harlem neighborhood. His message, articulated through works like Amazing Grace and We the People, is that the readymade is not Duchamp's joke: it is the assembled archive of who and what a city throws away."
  },

  a20: { // Theaster Gates
    message: "Gates was raised in Chicago by a roofer father and trained as an urban planner and a ceramicist in Iowa, Cape Town, and Tokoname. His Rebuild Foundation has bought, restored, and reactivated abandoned buildings across Chicago's South Side, housing collections (the Johnson Publishing archive, Frankie Knuckles's records) inside ceramic-and-tar architectural propositions. He argues that the Black artist's most consequential medium in the 21st century is real estate — the literal, undertaxed, racialized ground itself — and that ceramics teaches you how to handle that ground."
  },

  a311: { // Adam Pendleton
    message: "Pendleton is based in New York and developed his concept of 'Black Dada' in the mid-2000s, riffing on Amiri Baraka's poem and Dada's anti-syntax. His silkscreen paintings, video portraits (of Lorraine O'Grady, David Hammons, Adrienne Kennedy), and book-objects assemble a Black avant-garde lineage that did not previously sit together. He argues that contemporary art's formalist languages are not race-neutral, and that grammar — typographic, painterly, archival — is itself a place where Black political life can take place."
  },

  // ── Drawing / Mixed ─────────────────────────────────────────────

  a159: { // Marcel Dzama
    message: "Dzama was born in Winnipeg, studied at the University of Manitoba, and was a founding member of the Royal Art Lodge collective; he now lives in Brooklyn. His drawings — root beer-tinted from his early Winnipeg practice — populate a folk-cinematic world of bear-soldiers, ballerinas, witches, and chess armies, drawn equally from Dadaist puppet theatre and prairie folk art. The work argues that contemporary drawing can carry a coherent fictional cosmology — not as illustration of a story, but as the story's primary mode of existence."
  },

  a191: { // Raymond Pettibon
    message: "Pettibon was born Raymond Ginn in Tucson, raised in Hermosa Beach, and is the younger brother of Black Flag's Greg Ginn; he made flyers, album covers, and zines for SST and the Minutemen across the 1980s. His ink-and-text drawings braid Henry James, William Blake, surf, baseball, and dropouts in a flat punk graphic style that was for a long time unsellable. He argues that text is a visual medium, and that the proper site of American literary thinking is not the novel but the wall."
  },

  a735: { // Sophie Calle
    message: "Calle was born in Paris, lives there still, and began her practice in the late 1970s by following strangers in the street and photographing them — a working method she has used continually since. Her project-as-life works (Suite Vénitienne, The Hotel, Take Care of Yourself, Exquisite Pain) braid autobiography, surveillance, and contractual game-playing with the people in her own romantic and family life. The work argues that the self is a public artifact, and that the rules under which we agree to be observed are themselves the medium."
  },

  a83: { // Glenn Ligon
    message: "Ligon was born and raised in the Bronx, trained at Wesleyan and the Whitney Independent Study Program, and lives in New York. His text-based painting practice — Stranger in the Village, Untitled (I Am a Man), Warm Broad Glow — borrows phrases from James Baldwin, Zora Neale Hurston, Richard Pryor, and Civil Rights placards and lets them degrade into illegibility as the surface accumulates. He argues that race is not legible by sight but by language, and that the painting can stage exactly the moment where the language stops working."
  },

  // ── Batch 2 additions ──

  a596: { // Allora & Calzadilla
    message: "Jennifer Allora (b. 1974, Philadelphia) and Guillermo Calzadilla (b. 1971, Havana) have worked as a single artist since 1995 and live in San Juan, Puerto Rico, the island whose colonial and military history their practice has tracked since their first projects on the US Navy's Vieques bombing range. Their works pull a tuba through Bach for the Venice Biennale, drag a stuffed military hippopotamus across an opera stage, and stage piano recitals in which the instrument is the floor. Their argument is that geopolitics enters art most precisely as sound and choreography — the body of a singer, a soldier, an animal — not as illustration or slogan."
  },

  a381: { // Mona Hatoum
    message: "Hatoum was born in Beirut to a Palestinian family already in exile and was stranded in London by the outbreak of the Lebanese Civil War in 1975; she still lives in London and Berlin. Her practice moves between household objects scaled to weaponry (a cheese grater the size of a sliding door), surveillance-and-body video (Corps étranger sends an endoscope through her own body), and rubber-and-metal installations of barbed wire as domestic furniture. She insists that the domestic and the geopolitical share the same materials — that exile is not a metaphor but a measurable property of a kitchen object."
  },

  a584: { // Rosemarie Trockel
    message: "Trockel lives in Cologne and emerged in the early 1980s from the male-dominated German painting scene with knitted-wool 'paintings' bearing Playboy logos, hammer-and-sickles, and corporate marks woven by industrial machine. She has since produced ceramics, video, schematic 'book drafts,' and stovetop assemblages that refuse to settle into a single signature style. The argument across forty years is that femininity, taste, and category are themselves the material — that an artist who refuses to be legible is doing political labour, not branding it."
  },

  a533: { // Cyprien Gaillard
    message: "Gaillard was born in Paris in 1980, lives between Paris and Berlin, and works in landscape photography, sculpture, and 35mm and 3D video. His best-known films — Cities of Gold and Mirrors (Cancun), Nightlife (Cleveland), Ocean II Ocean (Athens to Bangkok) — track the decay of modernist architecture, ancient monuments, and post-industrial ruins as a single continuous geological event. He argues that contemporary destruction is too slow to be an event and too fast to be ruin — and that the artist's job is to find the camera angle at which time becomes visible."
  },

  a821: { // Hans Op de Beeck
    message: "Op de Beeck lives in Brussels and works in monochrome — every sculpture, drawing, film, and life-size environment he makes is rendered in a single dust-grey palette so that material distinctions collapse into mood. His Sanctuary and The Collector's House installations are full-scale grey rooms inhabited by grey figures eating grey food, photographed by visitors in colour. He treats grey as the contemporary condition's true colour: the screen-flattened, decision-suspended, mass-anesthetised tone in which Western private life now takes place."
  },

  a545: { // Karen Kilimnik
    message: "Kilimnik lives in Philadelphia, trained at Temple, and emerged in the 1990s with small fast paintings of teenage pop idols (Kate Moss, Leonardo DiCaprio, ballet stars) rendered in the loose hand of an obsessive fan. Her installations stage Marie-Antoinette boudoirs, ballet stage sets, and witch-girl bedrooms as if a 13-year-old had been given gallery walls. The argument — refined over thirty years — is that fan culture, romance, and femininity are serious painterly subjects, and that the polished MFA hand is one historical option among many."
  },

  a364: { // Mirosław Bałka
    message: "Bałka lives in Otwock outside Warsaw, the small town where he was born in 1958 and where he has used his family home and the local railway as the dimensional and material basis for his sculpture for forty years. His works — How It Is (Tate Turbine Hall 2009, a 30-metre dark steel box visitors walk into), salt-and-steel floors, soap-and-felt geometries — return obsessively to the Polish Jewish absence in the post-war landscape. He insists on sculpture's responsibility to specific historical sites; the dimensions of his works are often his own body's, or his childhood house's, measured in centimetres."
  },

  a282: { // Maya Lin
    message: "Lin is American-born to Chinese parents who arrived after the 1949 revolution; she designed the Vietnam Veterans Memorial in Washington at age 21 as a Yale undergraduate, and has since divided her practice between architecture and sculpture. Her sculptural work — Wave Field, Storm King's Wavefield, Pin River — translates topography and hydrography into earthworks and pin-and-glass installations. She argues that landscape is the still-uncatalogued American memorial subject — and that the artist's job is to map what is being lost while it is still here to be mapped."
  },

  a567: { // Pamela Rosenkranz
    message: "Rosenkranz lives in Zürich and Switzerland, and trained at Bern and the Università IUAV di Venezia in philosophy and visual culture. Her practice mobilises industrial colour, perfume, biotech materials, and engineered environments — pools of synthetic skin tone, scented LED-lit interiors, AI-generated dog avatars — to test where the human ends and the chemical environment begins. She argues that the body of the contemporary subject is already a corporate object, and that sculpture's task is to make this legible at the level of pigment, scent, and serotonin."
  },

  a371: { // Cerith Wyn Evans
    message: "Wyn Evans was born in Llanelli, Wales, in 1958, lives in London, and began his career as a film-maker working with Derek Jarman in the 1980s before turning to sculpture, neon, and text in the 1990s. His best-known works are large flown neon armatures of handwritten phrases, chandeliers that flicker Morse-code transcripts of literary texts, and quotations rerouted through optical glass. He treats light as a medium with a grammar — capable of speaking, citing, and refusing to be read — and argues that the work of art is a sentence the viewer has to finish."
  },

  // ── Batch 3 (cycle 1 of automation) ──

  a270: { // Acaye Kerunen
    message: "Kerunen lives between Kampala and New York and trained as an actor and curator before her woven sculpture practice; she co-represented Uganda at the 2022 Venice Biennale alongside Collin Sekajugo. Her work is hand-woven from raffia, banana fibre, palm leaf, and other indigenous Ugandan materials that she sources directly from rural women's craft cooperatives whose labour she names in the wall text. She insists that contemporary sculpture is a labour relation — that the work is unfinished without the visible economy of who made it and from what."
  },
  a981: { // Agnes Scherer
    message: "Scherer lives in Berlin and Salzburg and trained at HBK Braunschweig; she works at the unstable seam between visual art, opera, and stage design. Her immersive installations — The Salesman (2019), Cupid and the Animals (2021) — paint sets, write libretti, build puppets, and stage live performances inside the same gallery walls. She treats the exhibition as a coherent theatrical event rather than a display of discrete objects, and argues that contemporary art's atomised media categories obscure the much older form to which all the parts already belong."
  },
  a815: { // Ahmed Mater
    message: "Mater was born in Tabuk, trained as a physician at King Khalid University, and works between Abu Arish, Mecca, and London; he co-founded Edge of Arabia in 2003 with Stephen Stapleton. His photography and video project Desert of Pharan (2011–2016) documents the rapid redevelopment of Mecca for the Hajj at industrial scale, and his magnet-and-iron-filings Magnetism (2012) restages the Kaaba as a field experiment. He argues that the most consequential transformation of Islamic sacred space in a century is not a religious event but a construction one, and that the artist's job is to keep that visible."
  },
  a784: { // Alejandro Campins
    message: "Campins was born in Manzanillo, lives in Havana, and trained at the Instituto Superior de Arte; he emerged from a strong Cuban painting tradition shaped by both Eastern European Socialist Realism and Caribbean light. His large canvases — Patria (2014), Lethargy (2013) — depict abandoned modernist architecture, rural ruin, and revolutionary monuments slowly being reabsorbed by tropical landscape. The argument is that the Cuban Revolution's built environment is now a sublime subject for painting in exactly the romantic sense Constable would have recognised — heroic, weathered, ungovernable."
  },
  a315: { // Alejandro Piñeiro Bello
    message: "Piñeiro Bello was born in Pinar del Río, Cuba, in 1990 and lives in Miami; he is self-taught and openly cites Wifredo Lam and José Bedia as primary lineage. His large canvases — Tierra de Promisión (2022), Bahia Honda (2023) — render Caribbean landscape, Afro-Cuban Santería iconography, and mythological hybridity in dense layered colour. He argues that Cuban-American painting need not narrate exile as a closed story — that the Caribbean imaginary is still being painted, by people who left, into the present."
  },
  a946: { // Alex Da Corte
    message: "Da Corte was born in Camden, NJ to Venezuelan-Italian parents, trained at Yale and the University of the Arts, and lives in Philadelphia. His video installations — Rubber Pencil Devil (2018), the Met rooftop commission As Long as the Sun Lasts (2021) — assemble pop culture, midcentury advertising, Wizard of Oz iconography, and stage-set sculpture into hyper-saturated, candy-coloured emotional environments. He argues that the language of American consumer surrealism is its own folk vernacular, and that taking it seriously as form is not the same as celebrating it."
  },
  a837: { // Ana Maria Tavares
    message: "Tavares lives in São Paulo and trained at the city's Escola de Comunicações e Artes; she has worked in the long shadow of Brazilian modernist architecture since the 1980s. Her sculptural installations — Atlântico (2007), Desvios (2010) — re-stage the materials of airport interiors, hotel lobbies, and Lúcio Costa transit corridors as mirror, steel, and water environments inside the museum. She treats the seductive surfaces of modernist transit space as the contemporary Brazilian sublime — political, beautiful, and ambivalent at once."
  },
  a591: { // Andrea Zittel
    message: "Zittel lives in the high desert outside Joshua Tree, California, and trained at RISD; she founded the A-Z Enterprise in 1991 as the brand name for her own life-as-art. Her A-Z Living Units, Escape Vehicles, Wagon Stations, and Smockshop clothing are tested by her, by friends, and by paying visitors — and her annual High Desert Test Sites brings the practice into landscape and community. She argues that the structures of daily life — what you wear, what you sleep in, how you eat — are art's first and most consequential material."
  },
  a809: { // André Komatsu
    message: "Komatsu lives and works in São Paulo, where he trained at FAAP; his Japanese-Brazilian lineage and the city's brutalist architecture are equally present in his practice. His sculptural installations — Estado Provisório (2012), Reverso (2015) — disassemble construction debris, reinforcing bar, and salvaged drywall into precariously balanced compositions that re-stage the means of urban building. He argues that Latin American architectural power is most legible in its rubble — and that sculpture is one of the few mediums that can read it without flattering it."
  },
  a471: { // Annette Messager
    message: "Messager lives in Paris and Malakoff and was a central figure of the post-1968 French feminist art scene from the 1970s onward. Her installations — Mes voeux (1989), the Venice Golden Lion-winning Casino (2005), Articulés-Désarticulés — assemble stuffed animals, photo fragments, hand-written texts, coloured pencils, and net-sewn body parts into theatres of unsettled girlhood and grief. She treats the categories of woman, child, witch, and collector as ungovernable bodies that the gallery cannot organise, and argues that the unfinished private archive is a feminist sculptural form."
  },
  a904: { // Ariana Papademetropoulos
    message: "Papademetropoulos lives in Los Angeles, trained at CalArts, and is the daughter of a Greek-American family with roots in the city's visual-effects industry. Her photorealist canvases — The Emerald Tablet (2022) — paint decaying 1970s domestic interiors that bloom mid-frame into mushrooms, portals, and fairytale apparitions, all rendered with the smoothness of a film still. The argument is that the suburban American interior is already a haunted, hallucinogenic space — that painting need only stop pretending otherwise."
  },
  a839: { // Armando Testa
    message: "Testa was born in Turin in 1917, founded Studio Armando Testa in 1946, and worked across advertising, graphic design, and animation until his death in 1992. His campaigns for Punt e Mes, Pirelli, Lavazza, and Papalla collapsed Surrealist visual logic into mass commercial communication and shaped the postwar Italian visual environment as completely as any single designer. The estate-managed argument is that the line between graphic design and fine art was a postwar accident — and that the most legible Italian visual modernism of the 20th century is on billboards, not on canvas."
  },
  a927: { // Austyn Weiner
    message: "Weiner lives in Miami and trained at Tulane and Parsons; she emerged in the late 2010s as part of a generation of women painters working at the unstable seam between abstraction and confessional figuration. Her canvases — Just Above My Head (2022) — layer fast, vibrating colour, scribbled text, and figurative passages into surfaces that read at autobiographical pitch. The work argues that the diaristic intensity of post-internet female interiority is a serious painterly subject, and that legibility need not be sacrificed to it."
  },
  a781: { // Barbana Bojadzi
    message: "Bojadzi was born in 1990 and is among the youngest artists on the Galleria Continua roster; her practice moves between painting and small-scale installation. Her early work, including untitled 2020 paintings, engages memory, place, and Balkan domestic ritual in muted, layered surfaces. The argument is that landscape and family interior remain available to painting as long as the artist is willing to slow down — that what the contemporary attention economy cannot reward, painting can still hold."
  },
  a295: { // Beatriz Milhazes
    message: "Milhazes lives and works in Rio de Janeiro, where she still uses the same Lapa studio she opened in the early 1990s after studying at Parque Lage. Her layered, decal-transferred paintings — Maresias (2002), Succulent Eggplants (1996) — collapse Brazilian Baroque ornament, modernist colour theory, Carnaval, and tropical pattern into surfaces of extraordinary chromatic density. She argues that decoration, ornament, and the so-called feminine surface are not lesser than abstraction — they are abstraction's most under-read tradition."
  },
  a890: { // Bertrand Lavier
    message: "Lavier lives in Paris and Aignay-le-Duc, trained as a horticulturist, and emerged in the late 1970s with sculptural assemblages that overpaint, stack, or weld together pairs of brand-name domestic appliances. His Brandt/Haffner and Walt Disney Productions series interrogate authorship, the readymade, and the legal status of corporate logos. The argument extends Duchamp: that the readymade is not a one-time gesture but a still-operative grammar — and that the categories of art and commodity are governed by trademark law more than by aesthetic decision."
  },
  a979: { // Borna Sammak
    message: "Sammak lives in New York and trained at Tyler School of Art; his practice braids video, painting, and digital collage in a register that treats commercial software the way an earlier generation treated oil paint. Works like Not Yet Titled (2014) and Just Beachy (2018) mine stock-footage libraries, screensavers, and Adobe artefacts for visual excess that registers as both junk and luxury. The argument is that contemporary commercial imagery is the only widely shared visual language left — and that painting's task is to take its glitches seriously."
  },
  a460: { // Brennan Gerard & Ryan Kelly
    message: "Gerard and Kelly are an American collaborative duo who met at the Whitney Independent Study Program and have worked together since 2003; both trained as dancers before crossing into video and installation. Their projects — Timelining (2014), Modern Living (2016), Lazarus (2022) — stage live choreographies of queer intimacy inside the houses of midcentury modernism (Schindler, Eames), where private domestic ritual collides with surveillance and the politics of looking. The argument is that the modernist house was always a stage; the duo simply restores the bodies that the documentary photograph cropped out."
  },
  a911: { // Brian Rochefort
    message: "Rochefort lives in Los Angeles and trained at the Rhode Island School of Design; his vessels and sculptures sit between the lineage of Peter Voulkos and a younger generation of ceramicists working with deliberate ruin. His Crater series builds the vessel up through dozens of glaze firings until the surface bubbles, encrusts, and slumps into something that reads as a geological event rather than a pot. The argument is that ceramic, the oldest sculptural medium, is also the only one that visibly records every accident of its own making."
  },
  a845: { // Carla Accardi
    message: "Accardi was born in Trapani, Sicily in 1924, lived and worked in Rome, and co-founded the Forma 1 group in 1947 alongside Pietro Consagra and Antonio Sanfilippo. Her Sicofoil paintings (1965 onward) replaced canvas with transparent industrial plastic, allowing painted sign-and-symbol marks to float in literal space rather than on opaque ground. The estate-managed argument is that Italian abstraction's most radical move was material, not stylistic — Accardi made painting transparent before the Americans declared painting dead."
  },
  a792: { // Carlos Cruz-Diez
    message: "Cruz-Diez was born in Caracas in 1923, lived in Paris from 1960 until his death in 2019, and is, with Soto and Otero, one of the three central Venezuelan kinetic artists. His Physichromies (1959–) and Chromosaturations (1965 onward) make colour autonomous from form — fields of light visible only when the viewer moves, with no inherent image to memorise. The estate argues that colour is not a property of objects but an event in time, and that Latin American modernism's contribution to perception is still under-credited in the Northern art-historical record."
  },
  a617: { // Carmen Herrera
    message: "Herrera was born in Havana in 1915, moved to New York in 1939, and worked as an unknown painter for fifty years before her first solo show at age 89 in 2004; she died in Manhattan in 2022. Her hard-edge geometric abstractions — Blanco y Verde (1959), Iberic (1949) — anticipate Ellsworth Kelly and the New York minimalist generation that ignored her for a half-century on grounds of gender and Cuban exile. The estate-managed argument is that the canon of geometric abstraction is wrong in its dates — the work was always there, the institutions chose not to look."
  },
  a27: { // Carsten Höller
    message: "Höller lives in Stockholm and Biriwa, Ghana, and trained as an agricultural entomologist (PhD in olfactory insect communication) before he became an artist. His installations — Test Site (2006 Tate Turbine Hall slides), Decision (2015), Mushroom Suite (2000 onward, with Amanita muscaria) — restage the gallery as a behavioural laboratory in which the visitor's own perception is the experimental subject. The argument is that art's claim on perception is empirical and falsifiable — and that uncertainty is not a defect of the experience but the experience itself."
  },
  a425: { // Cecile Abish
    message: "Abish was born in New York in 1931, lived between New York and Cologne with her husband Walter Abish, and trained in the post-war American sculpture milieu before turning to ephemeral floor-based installation in the 1970s. Her works — 4 Into 3 (1973), Equal Quantities (1975), Crossings (1978) — laid sand, gravel, plywood, and tape grids onto gallery floors in temporary configurations documented only photographically. The argument is that sculpture's permanence was always a curatorial assumption rather than a formal requirement — and that the photograph is the work's primary site."
  },
  a439: { // Christian Boltanski
    message: "Boltanski was born in Paris in 1944 — the day of the city's liberation — to a Russian-Jewish father who had spent the war hidden under the floorboards of the family's apartment, and he lived and worked in Malakoff until his death in 2021. His installations — Personnes (Paris Monumenta 2010), The Reserves (1989), the Inventory of the Children of Dijon — accumulate clothing, photographs, and recorded heartbeats into civic-scale monuments to absent specific persons. The estate argues that contemporary sculpture's responsibility is not to evoke the dead but to count them, one by one, even when no name remains."
  },
  a881: { // Christian Holstad
    message: "Holstad lives in Brooklyn, trained at Pratt, and emerged in the early 2000s as part of a generation of queer artists working between drawing, textile, and ephemeral performance. His Newspaper Erasure Drawings (2005 onward) systematically rub out images and words from the front pages of the New York Times, leaving residual figures, intimate gestures, and ghosts of the news. The argument is that the daily newspaper is a queer archive in disguise — that erasure can be a reading practice, not a destruction."
  },
  a984: { // Christiana Soulou
    message: "Soulou was born in Athens in 1961, lives there still, and trained at the Athens School of Fine Arts in a tradition that links Greek modernism to French illustration. Her pencil and coloured-pencil drawings — the Characters of Balzac (2012), Animal Kingdom (2015) — render literary characters and zoological subjects in a precise, slow line that owes equally to medieval manuscript and to Cocteau. She argues that drawing is a reading medium — that the body of a Balzac character can be made visible only by someone who has read the novel slowly enough to draw it."
  },
  a218: { // Christopher Williams
    message: "Williams lives in Los Angeles, trained at CalArts under John Baldessari, and has worked since the 1980s in a strict conceptual photography that re-stages the protocols of commercial product photography, industrial catalogue images, and Cold War darkroom technique. His series — Angola to Vietnam* (1989), For Example (2003 onward) — produce images that look correct in every commercial sense and refuse to deliver the documentary content their formal vocabulary promises. The argument is that the conventions of photography are themselves the subject — and that the obedient image is the most political one available."
  },
  a957: { // Dada Khanyisa
    message: "Khanyisa lives in Cape Town and Johannesburg, was born in 1991, and trained at the Michaelis School of Fine Art in the post-Marlene-Dumas South African painting generation. Their wall-mounted reliefs — Good Feelings (2020), Moments of Joy (2021) — combine carved and painted wood with mixed-media collage to depict Black queer social life with sharp stylised geometry and intimate humour. The argument is that South African contemporary art has been written too long around the apartheid trauma frame, and that Black queer joy is itself a sufficient and political painterly subject."
  },
  a284: { // Damian Loeb
    message: "Loeb lives and works in New York, is self-taught, and emerged in the late 1990s alongside other photorealist painters (Currin, Yuskavage) but with a specifically cinematic source vocabulary. His paintings — Sora (2009), Lunaris (2014) — render film stills, satellite imagery, and astronomical photography in seamless hyperreal oil, in which the viewer cannot determine whether the source was film or sky. The argument is that photorealism's job in the 21st century is no longer to imitate photography but to imitate the screen — and that the painting has to know which one it is."
  },
  a602: { // Daniel Buren
    message: "Buren was born in Boulogne-Billancourt in 1938, has lived and worked in Paris for sixty years, and is, with Toroni, Mosset, and Parmentier, a co-founder of BMPT — the 1960s group that declared painting could be reduced to a single repeated gesture. Since 1965 his entire output has consisted of 8.7-centimetre alternating stripes deployed in situ — including Les Deux Plateaux at the Palais Royal (1985–86) and the Grand Palais Excentrique(s) (2012). The argument is that the stripe is not a style but a tool — a visible measuring instrument by which any architectural site reveals its own politics."
  },
  a958: { // David Korty
    message: "Korty lives in Los Angeles and trained at UCLA; he emerged in the early 2000s alongside other West Coast painters working between watercolour landscape and post-pop graphic abstraction. His mixed-media works on paper and canvas — Blue Figure (2017), Yellow Grid (2019) — combine printed and silkscreened patterns with handpainted gestural marks in a slow accumulation that resembles both city plan and weather report. The argument is that the contemporary painter need not choose between observational drawing and abstraction — that the LA atmospheric register holds both at once."
  },
  a886: { // Dennis Kardon
    message: "Kardon lives in New York and trained at Yale; he has worked since the 1980s as a figurative painter and a critic, with the latter activity quietly informing the former. His Jewish Noses (1993) installed 54 oil-painted ceramic noses of friends and acquaintances on a single wall, turning a phenotypic anti-Semitic trope back on itself as material evidence. The argument is that figuration's contract with the viewer is governed by perception's social conditioning — and that the painter who refuses to confront that is not a neutral observer but an accomplice."
  },
  a864: { // Diane Dal-Pra
    message: "Dal-Pra was born in Bordeaux in 1991, lives in Paris, and trained at the École nationale supérieure des Beaux-Arts; she emerged in the late 2010s with a small, slow figurative practice. Her paintings — Devotional Objects (2022) — render women's hands, household textiles, ceramics, and ritual gestures in muted brown-grey palettes that recall both 17th-century Dutch genre painting and contemporary editorial photography. The argument is that domestic ritual is still under-painted, and that the supposedly minor categories of still life and genre scene remain serious territory for women's painting."
  },
  a968: { // Diego Marcon
    message: "Marcon was born in Busto Arsizio in 1985, lives and works in Milan, and trained at the Brera Academy. His short films — Ludwig (2018), The Parents' Room (2021) — combine prosthetic-faced live actors with looping musical structure and uncanny CGI to produce small horror narratives that the viewer cannot exit. The argument is that the cinematic short, the medium least at home in either the gallery or the cinema, is the form in which contemporary dread and pathos can be held without softening — and that loop, not narrative arc, is its grammar."
  },
  a868: { // Dominique Fung
    message: "Fung was born in Ottawa in 1987, lives in Brooklyn, and trained at Capilano College in Vancouver; she is of Hong Kong Chinese descent. Her lush figurative canvases — It's Not Polite to Stare (2021) — paint Asian women, museum vitrines, antiquities, and decorative interiors in a register that simultaneously inhabits and dismantles the European orientalist tradition. The argument is that the museum's catalogue is not a neutral record — the Asian female body has been a decorative subject of Western painting for three centuries, and the painter who refuses to flinch from that history changes what figuration can do now."
  },
  a889: { // Elad Lassry
    message: "Lassry was born in Tel Aviv in 1977, lives in Los Angeles, and trained at CalArts; his practice operates inside the conventions of commercial still-life and product photography that he refuses to either celebrate or critique. His photographs — Untitled (Red Cabbage) (2009) — appear in custom-coloured editorial frames that are physically continuous with the image; sculptures and films extend the same enquiry into other media. The argument is that the photographic object's frame is part of the image, that the image is part of the institutional decision to call it one, and that contemporary photography's subject is its own conditions of display."
  },
  a788: { // Elizabet Cerviño
    message: "Cerviño was born in Manzanillo, Cuba in 1986, trained at ISA in Havana, and lives between Havana and Madrid. Her elemental sculptures and installations — Llanto (2014), Marabú (2016) — work with earth, sea-salt, candle-wax, plant material, and her own body in a contemplative register at the seam of Caribbean Catholicism and Yoruba ritual. The argument is that the post-revolutionary Cuban artist's most reliable subject is the natural elements themselves — and that material, used with care, can carry a spirituality that explicit imagery would coarsen."
  },
  a180: { // Emma McIntyre
    message: "McIntyre was born in Auckland in 1990, lives in Los Angeles, and trained at the Auckland-based Elam School of Fine Arts followed by an MFA at ArtCenter College of Design. Her paintings — Rose in a glass (2023), A Wild Note of Longing (2023) — build saturated colour through oxidation, stain, and pour, refusing the hard-edge contemporary preference and returning to the lineage of Helen Frankenthaler and Pat Steir. The argument is that abstraction's chromatic, atmospheric register — once treated as the lyric problem of mid-century American women painters — is still unfinished, and the form is large enough to hold another generation's grief."
  },
  a254: { // Emmet Gowin
    message: "Gowin was born in Danville, Virginia in 1941, lives in New Jersey, and taught at Princeton for thirty-five years; he studied under Harry Callahan at RISD. His earliest series, the intimate portraits of his wife Edith and her extended family (1969 onward), gave way after 1980 to large-format aerial photography of US nuclear test sites, Hanford Reach, and mountaintop-removed Appalachia. The argument is that the photographer's responsibility extends in both directions — to the kitchen table and to the cratered Earth visible from a plane — and that the same person can hold both at the same level of care."
  },
  a437: { // Eric Orr
    message: "Orr was born in Covington, Kentucky in 1939, lived in Los Angeles, and died there in 1998; he was a central but quieter figure of the Light and Space generation alongside Robert Irwin, James Turrell, and Doug Wheeler. His immersive rooms — Zero Mass (1972), Sunrise (1985), Prime Matter (1989) — used fire, water, blood, lead, and gold leaf to make environments that were not paintings, not sculptures, and not light installations in the strict sense. The estate's argument is that California perception art was never a single Turrell school — that Orr's elemental, alchemical strand of it remains under-credited."
  },
  a732: { // Erwin Wurm
    message: "Wurm was born in Bruck an der Mur, Austria in 1954, lives in Vienna and Limberg, and trained in Salzburg and Vienna; he taught at the Universität für angewandte Kunst Wien for many years. His ongoing One Minute Sculptures (1996 onward) instruct the visitor to perform a brief physical absurdity with everyday objects — sit on a pencil, balance an orange on the forehead — making the visitor's own body the temporary sculpture; his Fat Cars (2001 onward) physically swell consumer goods into bulging forms. The argument is that sculpture's medium in the post-industrial age is the body's relation to commodity — and that the absurd instruction is its declaration of independence."
  },
  a915: { // Ferrari Sheppard
    message: "Sheppard was born in Chicago in 1983, lives in Los Angeles, and is largely self-taught after a journalistic career that included writing on global politics and a long stint in Beijing. His paintings — In My Mind (2021) — combine charcoal-drawn Black figures with gold-leaf passages and gestural acrylic on raw linen, producing portraits whose figures appear both contemporary and historically iconic. The argument is that the African American figurative painting tradition that runs from Charles White through Kerry James Marshall has a place for an explicitly devotional register — gold-leaf gravitas as a contemporary, not nostalgic, claim."
  },
  a897: { // France-Lise McGurn
    message: "McGurn was born in Glasgow in 1983 and lives there; she trained at the Glasgow School of Art and the Royal College of Art. Her paintings — Sleepless (2019) — extend beyond the canvas onto gallery walls and floors in fluid contour-line figures of women, lovers, dancers, and nightlife bodies, painted at the tempo of nightclub late-night looseness. The argument is that the wall painting — fresco's contemporary descendant — is a feminist sculptural format, because it refuses the discrete commodity object and treats the room itself as a body."
  },
  a959: { // Gabriel Kuri
    message: "Kuri was born in Mexico City in 1970, lives in Brussels and LA, and trained at the Universidad Iberoamericana before joining the seminal Gabriel Orozco taller in 1990s Mexico City. His sculptures — Donation Box (2010), Spent (2014) — combine printed receipts, ATM stubs, cigarette butts, marble, and concrete in arrangements that quietly diagram the economic micro-transactions that pass through every body in a day. The argument is that sculpture's subject in the late-capitalist period is the receipt — the smallest, most disposable, most truthful record of how an economy actually behaves."
  },
  a873: { // Gelitin
    message: "Gelitin is an Austrian collaborative of four — Ali Janka, Wolfgang Gantner, Florian Reither, and Tobias Urban — who have worked together as a single artistic body since 1993 and live across Vienna. Their projects — The B-Thing (an unauthorised balcony built off the World Trade Center, 2000), Hase (a 200-foot pink stuffed rabbit knitted by villagers on an Italian hillside, 2005) — are large-scale, absurd, and often physically risky public interventions performed half-naked. The argument is that contemporary sculpture's residual seriousness is itself the problem — that the collective body, drunk and exhibitionist, is the only honest material left."
  },

};

// Expose for the quiz UI
if (typeof window !== 'undefined') window.QUIZ_MESSAGES = QUIZ_MESSAGES;
