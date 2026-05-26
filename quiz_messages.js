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

  // ── Chunk 2 (still session, before first cron) ──

  a953: { // Georg Herold
    message: "Herold was born in Jena in 1947 in East Germany, escaped to West Berlin in his twenties, and trained at the Hochschule für bildende Künste Hamburg under Sigmar Polke; he lives in Cologne. His work uses humble or absurd materials — roof battens, bricks, caviar, dry potato — assembled into figures that openly mock the heroic German sculpture lineage he inherited. The argument is that cultural value is a joke history plays on its materials, and the sculptor who pretends otherwise is participating in the lie."
  },
  a951: { // Georgia Gardner Gray
    message: "Gardner Gray was born in Washington, DC in 1988 and lives in Berlin; she trained at Cooper Union and at the Städelschule under Amy Sillman. Her figurative paintings — Commuters (2018), Terrace (2020) — stage social tableaux of contemporary Western life with the theatricality of a stage set and the cruelty of a satirist. She argues that the contemporary group portrait is still a serious painterly subject — provided the painter is willing to render social humiliation with the same precision as classical religious painting once rendered grace."
  },
  a876: { // Giorgio Griffa
    message: "Griffa was born in Turin in 1936, trained as a lawyer, and has worked in his Turin studio since the late 1960s — when he began making the rhythmic, unstretched-canvas paintings he is still making at almost ninety. Loosely associated with Arte Povera and Italian analytical painting, his work consists of repeated marks — dashes, horizontals, ideograms — that stop when the canvas is no longer 'curious about itself.' The argument is that painting is a practice of attention, not of production — and that the unfinished canvas, folded and stored when not exhibited, is the truer object."
  },
  a859: { // Giulia Cenci
    message: "Cenci was born in Cortona, Italy in 1988 and lives between Cortona and Amsterdam, where she trained at the Rijksakademie after the Brera Academy in Milan. Her installations — dry salvages (2022), secondary forest (2021) — assemble cast aluminium, industrial detritus, animal-derived molds, and hybrid creature-forms into landscape-scale environments that read as both archaeological and post-apocalyptic. She argues that contemporary sculpture's true subject is the agricultural-industrial ruin of Italy's countryside — and that the human figure is no longer the most legible body in that landscape."
  },
  a268: { // Glenn Kaino
    message: "Kaino was born in Los Angeles in 1972, lives there still, and trained at UC Irvine and UCSD; he has worked at the seam of conceptual sculpture and explicit political collaboration since the early 2000s. His project Bridge (2014) cast the raised gloved arm of Olympic athlete Tommie Smith into 200 suspended gold-plated sculptures (an act made in direct collaboration with Smith), and In the Light of a Shadow (2021) recast the bullets of Bloody Sunday as a chandelier. He argues that political memory needs material vessels at the right scale — and that contemporary sculpture's most useful task is to be the steady collaborator."
  },
  a799: { // Gu Dexin
    message: "Gu Dexin was born in Beijing in 1962, was largely self-taught, and was one of the foundational figures of the 1985 New Wave Chinese avant-garde alongside Huang Yong Ping and Xu Bing. His installations of rotting fruit, melted plastic, raw meat, and pressed flesh — Plastic Pieces (1983–89), 2009-05-02 (2009) — confronted Chinese state ideology with materials that explicitly refused permanence. He announced his retirement from art on the date that titles his last work — May 2nd 2009 — and has not made art since, an act that itself argues that the artist's most powerful gesture can be to stop."
  },
  a869: { // Günther Förg
    message: "Förg was born in Füssen in 1952, lived between Munich and Areuse, Switzerland, and died in 2013; he trained at the Akademie der Bildenden Künste München under Karl Fred Dahmen. His Grey Paintings (1973 onward), large lead-and-aluminium wall works, architecture photographs of fascist-era Italian buildings, and Spot Paintings (2007) collapse the language of postwar abstract painting into a deliberately uneven, almost careless gesture. He treats the inheritance of European modernist abstraction not as a faith but as a found language — useable, exhaustible, and worth refusing to perfect."
  },
  a230: { // Harry Callahan
    message: "Callahan was born in Detroit in 1912, taught himself photography in the late 1930s, and was hired by László Moholy-Nagy at Chicago's Institute of Design in 1946; he later led the photography department at RISD. His three lifelong subjects — his wife Eleanor (photographed for nearly forty years), Chicago and Cape Cod street scenes, and dense natural-form abstractions — built a body of work that quietly redefined American mid-century photography. He argued that photography's discipline was attention rather than novelty — that the same subject, returned to over decades, was the longest education a photographer could give themselves."
  },
  a856: { // Hejum Bä
    message: "Hejum Bä was born in South Korea in 1987 and trained at Seoul National University before moving to a contemporary international practice. Her abstract canvases work with line, gesture, and the body's relationship to surface in a register that draws equally on East Asian calligraphic tradition and post-painterly Western abstraction. She argues that the line — drawn, painted, or breathed onto a surface — is the most under-credited unit of painting, and that contemporary abstraction's preoccupation with field has obscured what a single mark can still do."
  },
  a969: { // Helen Marten
    message: "Marten was born in Macclesfield, England in 1985 and lives in London; she trained at Central Saint Martins and the Ruskin School at Oxford. Her dense, hybrid installations — Lunar Nibs (2016), Eucalyptus, Let Us In (2016) — combine welded steel, ceramic, screen-printed textile, found object, and dense written text into compositions that refuse to settle into a single interpretive frame. The argument, which won her both the 2016 Turner Prize and the inaugural Hepworth Sculpture Prize in the same year, is that contemporary sculpture's task is to overwhelm the viewer's pattern-matching ability — to be more dense than the museum label can be."
  },

  // ── Chunk 3 (50-batch) ──

  a261: { // Hong Hao
    message: "Hong Hao was born in Beijing in 1965 and lives there still; he trained at the Central Academy of Fine Arts in the early years of China's economic opening. His My Things (2001 onward) is built by scanning every object that passes through his hands over the course of a year — receipts, packaging, coins, takeout — and arraying them at flat scale into a single image; his Selected Scriptures (1992) reworked classical-style maps as documents of geopolitical absurdity. The argument is that the post-1980s Chinese subject can be inventoried only at the level of the consumer object — and that the scan-bed, not the camera, is its honest portrait."
  },
  a238: { // Huong Dodinh
    message: "Dodinh was born in Vietnam in 1945 and arrived in Paris as a young child in the early 1950s; she has worked from a single Paris studio for over sixty years. Her near-white, near-grey monochromatic paintings (T-126 and the long Untitled series) build slow tonal fields with a quietness that owes equally to Buddhist meditation and to Yves Klein. The argument is that monochrome can be an act of devotion rather than reduction — that silence in painting is not the absence of subject but its most concentrated form."
  },
  a947: { // Isabella Ducrot
    message: "Ducrot was born in Naples in 1931, lives in Rome, and came to art-making only in her sixties after a long life in Italian publishing and Asian-textile collecting. Her practice — Big Aubergines (2021), Tendernesses (2022) — works on antique fabric, sewn paper, and large-scale painted cloth with patterns drawn from the Silk Road textiles she spent decades studying. The argument is that the late-life entry into art is not a footnote but a position — that pattern, ornament, and care for the made object are subjects painting cannot reach by youth alone."
  },
  a785: { // Iván Capote
    message: "Capote was born in Pinar del Río, Cuba in 1973, lives in Havana, and trained at the Instituto Superior de Arte (ISA); his twin brother Yoan Capote is also a sculptor. His sculptures — Dyslexia (2010), Reflexión (2014) — work through visual puns, anagrams, and typographic paradoxes carved into stone, neon, and steel. The argument is that the contemporary Cuban condition is itself a linguistic paradox — and that the most efficient sculptural medium for it is the visual joke that, once read, refuses to stop meaning."
  },
  a810: { // Jannis Kounellis
    message: "Kounellis was born in Piraeus, Greece in 1936, moved to Rome in 1956, and died there in 2017; he trained at the Accademia di Belle Arti di Roma and married into Italy's curatorial avant-garde. His 12 Horses (Galleria L'Attico, Rome, 1969) tethered live horses inside a gallery space, and his decades-long use of coal, wool, raw steel, fire, and lead made him a central figure of Arte Povera alongside Pistoletto, Anselmo, and Pascali. He argued that materials carry history before the artist arrives — coal is the Industrial Revolution, wool is rural labour — and that sculpture's job is to let them speak rather than to compose them."
  },
  a848: { // Jean-Marie Appriou
    message: "Appriou was born in Brest, France in 1986 and lives in Paris; he trained at the École européenne supérieure d'art de Bretagne in Lorient. His cast-aluminium, bronze, and glass figures — The Horses and Les Cavaliers (2019, installed in Central Park) — are made by deliberately preserving the marks of the foundry process, so casting accidents and seams remain legible. The argument is that contemporary sculpture's romance with the polished finished surface obscures the medium's actual subject — fire, mold, gravity — and that the half-finished cast tells the truth the finished bronze conceals."
  },
  a737: { // Jean-Michel Othoniel
    message: "Othoniel was born in Saint-Étienne, France in 1964, lives in Paris, and trained at the École nationale supérieure d'arts de Cergy. His Murano-glass-bead sculptures — Le Kiosque des Noctambules (2000, the Palais Royal Métro entrance), The Big Wave (2017), the Versailles fountains — translate jewelry's intimate scale into architecture and landscape. The argument is that public sculpture has a permission to be beautiful that contemporary practice has largely refused — and that the glass bead, an object of explicit decoration, is the medium most honest about that permission."
  },
  a875: { // Jenna Gribbon
    message: "Gribbon was born in Knoxville, Tennessee in 1978 and lives in Brooklyn; she trained at the University of Tennessee and Hunter College. Her paintings — M Lit by Phone (2021) is typical — depict her partner Mackenzie Scott (the musician Torres) in the intimate domestic settings of contemporary lesbian life, painted with the brushy, fast figurative hand of mid-century American painting. The argument is that queer domesticity is a sufficient and serious painterly subject, and that the lover-as-model tradition (from Bonnard's Marthe to Hammershøi's Ida) was never closed — it was simply waiting for the painters with the standing to enter it."
  },
  a882: { // Jessie Homer French
    message: "Homer French was born in New York in 1940 and has lived in California's Mojave Desert for forty years; she is self-taught and only began exhibiting widely in her seventies. Her Fire Maps (2010 onward) and rural-California narrative paintings show wildfires, fishermen, cemeteries, and ranch animals in a flattened folk-modernist register. The argument is that the western American landscape's contemporary subject is fire — and that the painter who has lived through twenty years of seasonal evacuation can paint it with a directness no urban observer can match."
  },
  a880: { // Jim Hodges
    message: "Hodges was born in Spokane, Washington in 1957, trained at Fort Wright College and Pratt Institute, and lives in New York. His sculptures and installations — Every Touch (1995, silk flowers sewn into a curtain), Untitled (Gate) (1991), spider-web stitching, and the long Movements series of mirrored stones — treat fragility itself as a structural material rather than a defect. He argues that the materials American sculpture inherited from minimalism (steel, concrete, fluorescent tube) were chosen as much for emotional refusal as for industrial honesty, and that an alternative inheritance — paper, silk, mirror, breath — is available."
  },
  a341: { // JoAnn Verburg
    message: "Verburg was born in Summit, New Jersey in 1950, lives between Minneapolis and Spoleto, Italy, and trained at Rochester Institute of Technology under Nathan Lyons. Her multi-panel large-format colour photographs — Present Tense (2007), After Lunch (1999), the long Olive Trees series — slow Italian domestic and arboreal subjects to a tempo that registers as durational, not single-frame. The argument is that the photograph need not be a punctum — that the multi-panel composite can give photography the slow, conversational time that painting has historically claimed for itself."
  },
  a885: { // Johannes Kahrs
    message: "Kahrs was born in Bremen in 1965 and lives in Berlin; he trained at the Hochschule der Künste Berlin under Karl Horst Hödicke. His oil paintings — Untitled (man bending over) (2007) is characteristic — extract single frames from cinema, news media, and pornography and render them at the deliberate blur of a paused video tape on a 1990s television. The argument is that the photographic source image is not transcended by painting but slowed down by it — and that the slow surface registers exactly what the cinematic frame, in motion, refused to show."
  },
  a849: { // John Armleder
    message: "Armleder was born in Geneva in 1948, lives there still, and co-founded the Ecart group in 1969 — a Swiss outpost of the Fluxus international that briefly hosted Beuys, Filliou, and Brecht. His Furniture Sculptures (1979 onward, combining found furniture with modernist abstract painting) and Pour Paintings (1990s onward, large dot and pour canvases) treat the readymade and the abstract painting as parallel exhausted lineages he can deploy interchangeably. The argument is that postwar European art's twin inheritances — Duchamp and Mondrian — are no longer in dialectical tension but in flat juxtaposition, and that taking that flatness seriously is a curatorial discipline."
  },
  a248: { // John Gerrard
    message: "Gerrard was born in Dublin in 1974 and lives in Dublin and Vienna; he trained at the Ruskin School at Oxford and the Städelschule in Frankfurt. His Solar Reserve (2014) and Western Flag (2017) are real-time computer simulations — running continuously on dedicated hardware in the gallery — that depict, respectively, the Crescent Dunes solar plant in Nevada and the historical site of the Spindletop oil gusher in Texas. The argument is that the computer simulation is now sculpture's most honest medium for energy and ecology — because it can run for the lifetime of a viewer and never repeat."
  },
  a896: { // John McAllister
    message: "McAllister lives and works in Provincetown, Massachusetts, and trained at the University of New Mexico; he emerged in the 2000s with a distinctly West-Coast-influenced painterly practice. His landscapes and interiors — Sumptuous Sun Sets Sweltering (2014) — drench the Fauvist-Bonnard chromatic tradition in late-summer Californian saturation, with title-as-alliteration as part of the painting. The argument is that pleasure and decoration are still under-credited as painterly subjects — that the Bonnard interior is not a closed historical chapter but a viable contemporary register."
  },
  a871: { // Jonathan Gardner
    message: "Gardner was born in Lexington, Kentucky in 1982 and lives in Brooklyn; he trained at the Maryland Institute College of Art and at the School of the Art Institute of Chicago. His paintings — The Reader (2018) — collage Picasso, Magritte, Léger, and mid-century Italian magazine illustration into flat, deadpan figurative compositions of women in domestic interiors. The argument is that the early-modernist visual language is now available as a vernacular — quoting Picasso and Léger is no different from quoting an advertisement — and that the contemporary painter can use them without piety."
  },
  a814: { // Jorge Macchi
    message: "Macchi was born in Buenos Aires in 1963, lives there still, and trained at the Universidad Nacional de las Artes. His drawings, collages, and installations — Buenos Aires Tour (2003, in which a broken pane of glass is read as a city map), Music Stands Still (2006) — turn everyday materials (atlases, sheet music, newspapers) into melancholic small constructions. The argument is that the poetic image is still available to conceptual art if the artist is willing to slow down — that a single broken windowpane, attended to long enough, becomes a sufficient subject."
  },
  a207: { // Josh Smith
    message: "Smith was born in Okinawa, Japan in 1976 to American military parents and lives in New York; he is largely self-taught and worked for years as Christopher Wool's studio assistant. He paints continuously, often producing several canvases a day, organised into long signature motifs — his own name, fish, leaves, palm trees, skeletons, devils, plates — at every scale from postcard to wall. The argument is that the singular masterpiece is a fiction of the secondary market — and that the painter's truer unit of production is the studio-day, the wall-of-paintings, the unstoppable serial output."
  },
  a834: { // José Antonio Suárez Londoño
    message: "Suárez Londoño was born in Medellín, Colombia in 1955, lives there still, and trained as a microbiologist before turning fully to art. Since 1996 he has kept an annual notebook — the Yearbooks — in which he completes one small drawing or etching per day on a literary, scientific, or art-historical theme decided at the start of each January. The argument is that drawing is a daily discipline, not an event — and that the slow accumulation of small marks across a lifetime is the truest form a visual practice can take."
  },
  a817: { // José Mesías
    message: "Mesías was born in Havana in 1989, lives there still, and trained at ISA (Instituto Superior de Arte) in Havana. His paintings and drawings work in a figurative register grounded in Cuban personal and national narrative, often with rural and family subjects. The argument is that the next generation of Cuban painting still has serious figurative work to do — that the figure has not been exhausted by the country's earlier conceptual and performance generations."
  },
  a779: { // Juan Araujo
    message: "Araujo was born in Caracas in 1971 and lives between Lisbon and Caracas; he trained at the Instituto Universitario de Estudios Superiores de Artes Plásticas Armando Reverón. His paintings — Casa de Vidro (2010, after Lina Bo Bardi), the Niemeyer Studies (2013), small reproductions of Burle Marx photographs — meticulously copy book-page reproductions of Latin American modernist architecture in oil at the size of the source photograph. The argument is that the canonical buildings of Brazilian and Venezuelan modernism are known to most viewers only as printed reproductions — and that painting that reproduction is more honest than painting the building."
  },
  a812: { // Julio Le Parc
    message: "Le Parc was born in Mendoza, Argentina in 1928, moved to Paris in 1958, and was a founding member in 1960 of the Groupe de recherche d'art visuel (GRAV) with François Morellet, Horacio García Rossi, and others. His Continuel-Lumière (1963), Modulation (1976), and Cellule projection rooms use moving light, motorised steel, and mirror to produce kinetic perceptual environments that activate the viewer's body. The argument — which won him the Venice Biennale Grand Prize in 1966 — is that art's social emancipation requires removing the singular master-author and replacing them with a participatory perceptual situation."
  },
  a936: { // Karimah Ashadu
    message: "Ashadu was born in London in 1985 to a Nigerian family and lives in Hamburg and Lagos; she trained at the Slade and the Royal College of Art. Her films — Machine Boys (2024, Silver Lion at Venice), Plateau (2021), Lagos Sand Merchants (2013) — document informal labour in Nigerian okada drivers, mineworkers, and sand-harvesters with a long-take, ambient-sound discipline. The argument is that West African informal economies are an underseen contemporary subject — and that the film camera is the only medium that can hold their duration without exoticising them."
  },
  a879: { // Karin Gulbran
    message: "Gulbran lives and works in Los Angeles and trained at the California Institute of the Arts (CalArts); she emerged in the late 1990s alongside Laura Owens and Sue Williams in a generation that took pleasure-and-decoration seriously. Her ceramic landscape vessels and paintings render trees, deer, mushrooms, and pastoral scenes in a deliberately naive folk hand. The argument is that the Californian decorative-and-folk register — long dismissed as light — is in fact a serious philosophical position about how much pleasure painting is allowed to give."
  },
  a952: { // Kati Heck
    message: "Heck was born in Düsseldorf in 1979, trained at the Royal Academy of Fine Arts Antwerp under Karel Dierickx, and lives between Antwerp and the Belgian-Dutch border. Her paintings — Hasenherz (2017), Schnaps Idee (2014) — combine virtuoso figurative oil technique with surreal humour, prosthetic costumes, and family-and-friends models in compositions that read as both portrait and slapstick. The argument is that European figurative oil-painting tradition has been treated too solemnly — and that humour, when grounded in genuine craft, is not lighter than gravity but its more honest companion."
  },
  a982: { // Katja Seib
    message: "Seib was born in Düsseldorf in 1989, trained at the Kunstakademie Düsseldorf and the Royal College of Art, and lives in Los Angeles. Her figurative oil paintings on coarse hessian — The Confidants (2020), Fortune Teller (2021) — depict women in moody, theatrical interiors with a palette closer to early Italian Renaissance fresco than to contemporary LA painting. The argument is that the coarse-canvas substrate is part of the image's subject — that the texture beneath the figure is the painter's most undervalued formal decision."
  },
  a235: { // Keith Coventry
    message: "Coventry was born in Burnley, England in 1958, trained at Brighton Polytechnic and Chelsea College of Art, and lives in London; he is loosely associated with the YBA generation. His Estate Paintings (1991 onward) depict the layouts of London council-housing estates in pure Suprematist white-on-white style; his White Abstract (Junk) series (2012) presses fast-food trash into pristine cast-plaster reliefs. The argument — which won him the John Moores Painting Prize in 2010 — is that British social housing's geometry is, on paper, the most rigorous abstract painting the postwar period produced, and that painting that geometry honestly is also painting the politics."
  },
  a307: { // Kenjiro Okazaki
    message: "Okazaki was born in Tokyo in 1955 and works there as an artist, theorist, art historian, and landscape designer; he represented Japan at the 2002 Venice Architecture Biennale. His Topica Pictus (2020) paintings and Zerstreut liegen Steine (2002) sculptures work alongside dense theoretical writing on aesthetics, the Japanese garden, and contemporary critical theory. The argument is that the artist's work and the theorist's writing are not separate professional lives but a single body of thought — and that Japanese contemporary art's most distinctive contribution is the artist-theorist as integrated figure."
  },
  a256: { // Kevin Francis Gray
    message: "Gray was born in County Armagh, Northern Ireland in 1972, trained at the National College of Art and Design Dublin and Goldsmiths, and works between London and Pietrasanta in the Italian Carrara marble district. His marble and bronze figures — Ballerina (2011), Reclining Nude (2017), the Veiled series — use classical Italian carving technique to make veiled bodies, hooded street kids, and beaded subjects that sit at the seam of classical and contemporary. The argument is that classical figurative carving is not an exhausted tradition — its contemporary subject is simply who gets sculpted, and at what scale of dignity."
  },
  a327: { // Kiki Smith
    message: "Smith was born in Nuremberg in 1954, the daughter of sculptor Tony Smith, and was raised in New Jersey; she trained at the Hartford Art School and worked as an EMT before her art career began in earnest in the early 1980s. Her bronze, glass, ceramic, and tapestry figures — Born (2002), Lilith (1994), Pyre Woman, the body-fluid series — return obsessively to the female body in mystical, Catholic-iconographic, and natural registers. The argument is that the body is a sacred and porous object — leaking, gestating, transforming — and that sculpture's traditional treatment of it as closed marble was a violence the medium can now correct."
  },
  a964: { // Klara Liden
    message: "Liden was born in Stockholm in 1979, lives between Stockholm and Berlin, and trained as an architect at the Royal Institute of Technology before crossing into art at Konstfack. Her videos, sculptures, and interventions — Bodies of Society (2006, in which she destroys a bicycle with a hammer in a tiled bathroom), Pretty Vacant (2010), the trash-can totems she installs in public space — confront the body against urban infrastructure with deliberate physical violence. The argument is that contemporary public space's quiet hostility to bodies is only legible when it is met with returning bodily force — that politeness is the city's most effective form of erasure."
  },
  a290: { // Kylie Manning
    message: "Manning was born in Alaska in 1983, raised between Alaska and Mexico, and lives in Brooklyn; she trained at Cooper Union and the New York Studio School. Her paintings — Sea Change (2023), In Bloom (2022) — combine fluid, atmospheric figuration with chromatic abstraction in a register that draws on both Inuit visual tradition and Mexican muralism. The argument is that contemporary American painting need not choose between figuration and abstraction — and that the artist raised between two opposed visual cultures is uniquely positioned to refuse the choice."
  },
  a962: { // Lawrence Lek
    message: "Lek was born in Frankfurt in 1982 to a Malaysian-Chinese family, was raised between Hong Kong, Singapore, and London, and lives in London; he trained as an architect at the Architectural Association before moving into video and games. His CGI films and playable game-works — Geomancer (2017), AIDOL (2019), Black Cloud (2021) — construct speculative worlds in which AI characters develop consciousness, sing pop songs, and act out post-human dramas inside hyperreal architectural environments. The argument is that the video game engine is contemporary sculpture's most consequential new medium — and that the AI protagonist is the dramatic figure best suited to the present moment."
  },
  a887: { // Lee Kit
    message: "Lee Kit was born in Hong Kong in 1978, lives in Taipei, and trained at the Chinese University of Hong Kong; he represented Hong Kong at the 2013 Venice Biennale. His hand-painted cloth panels, projection-light installations, and gentle still-life paintings — Hold your breath, dance slowly (2016) — work in a register of quiet domesticity that takes shampoo bottles, T-shirts, and Cantopop lyrics as legitimate subjects. The argument is that contemporary art's pursuit of intensity has obscured a humbler available subject — the texture of an ordinary day — and that Cantonese popular culture is its proper material vocabulary."
  },
  a277: { // Lee Kun-Yong
    message: "Lee Kun-Yong was born in Hwanghae Province (now North Korea) in 1942, fled south during the Korean War, and trained at Hongik University in Seoul; he founded the Avant-Garde Association (AG) in 1969. His performance-and-drawing works — The Method of Drawing (1976, in which he draws on a wall using only his body's range of motion), Logic of Place (1975) — established a Korean conceptual vocabulary distinct from Japanese Mono-ha and Western performance. The argument is that the body's joint and reach are the painter's first measuring instrument, and that the Korean avant-garde of the 1970s was solving a different problem than its Japanese and American contemporaries — one that took the political body of post-war Korea as starting point."
  },
  a778: { // Leila Alaoui
    message: "Alaoui was born in Paris in 1982 to a Moroccan family and was killed in the 2016 al-Qaeda attack on the Splendid Hotel in Ouagadougou while photographing for an Amnesty International women's-rights commission. Her Les Marocains (2010–2014) project documented the diversity of Moroccan dress, ethnicity, and labour in formal large-format portraiture; her Crossings (2013) video installation documented sub-Saharan migrants in transit through Morocco toward Europe. The estate-managed argument is that documentary photography's responsibility is to the named, specific person in front of the lens — and that the photographer's own life can be the cost of taking that responsibility seriously."
  },
  a872: { // Lenz Geerk
    message: "Geerk was born in Basel, Switzerland in 1988, trained at the Düsseldorf Kunstakademie, and lives in Düsseldorf. His paintings — the Table Trilogy (2019) — depict single figures alone at a table or in domestic interiors in muted brown-grey palettes that recall Vilhelm Hammershøi and Lucian Freud's quietest works. The argument is that solitary contemporary interiority is a serious painterly subject — that the painting of a single person, slowly looking at nothing, holds the present moment more accurately than most narrative figuration."
  },
  a280: { // Li Songsong
    message: "Li Songsong was born in Beijing in 1973, trained at the Central Academy of Fine Arts, and lives in Beijing. His thickly impastoed oil paintings — A Dream of Power (2010), Spring of 1959 (2007) — work directly from photographs documenting twentieth-century Chinese political history, with paint laid on so heavily that the photographic source becomes visible only when one steps back. The argument is that Chinese political memory is mediated almost entirely through black-and-white press photography — and that painting's task is to slow that mediation down to the speed at which a viewer is forced to look."
  },
  a919: { // Lily Stockman
    message: "Stockman was born in New Jersey in 1982, lives in Los Angeles, and trained at Harvard and NYU; she also co-founded Block Shop Textiles, a workshop in Bagru, Rajasthan that produces hand-block-printed cottons with traditional Indian artisans. Her hard-edge oil-on-linen abstractions — the Garden Paintings (2019) — derive their shapes from botany, Mughal miniature, and the textile patterns of her parallel printing practice. The argument is that contemporary American hard-edge abstraction has been written as a Northern minimalist tradition — and that recasting it as derived from Indian textile pattern is a chromatic and political correction."
  },
  a283: { // Liu Jianhua
    message: "Liu Jianhua was born in Jiangxi province in 1962, trained at the Jingdezhen Ceramic Institute (the historic centre of Chinese porcelain), and lives in Shanghai. His porcelain installations — Trace (2011), Square (2014) — translate ceramic, China's most historically over-determined craft material, into contemporary minimalist forms whose engagement with consumer culture and global trade routes is read only at the level of material. The argument is that Chinese contemporary sculpture's most under-credited medium is the one Westerners associate with souvenir — and that working through the actual kilns of Jingdezhen is a political position about what counts as serious sculpture."
  },
  a393: { // Liu Wei
    message: "Liu Wei was born in Beijing in 1972, trained at the China Academy of Art in Hangzhou, and lives in Beijing; he is part of a Post-Sense Sensibility generation that emerged in the late 1990s. His sculptures and installations — Library (2012, dense compressed-book towers), Purple Air (2003, urban-rubble photo prints) — engage the rapid demolition and rebuilding of Chinese cities and the politics of public cultural display. The argument is that the post-1990s Chinese urban condition is too fast to be painted — its true sculptural material is the demolition rubble itself, packed into geometric volumes that read as both library and bunker."
  },
  a174: { // Liu Ye
    message: "Liu Ye was born in Beijing in 1964, trained at the Central Academy of Fine Arts and at the Hochschule der Künste Berlin (1990s), and lives in Beijing. His paintings — Bamboo Bamboo Broadway (2011), the long Book Painting series (2013 onward) — depict small childlike figures, books, Miffy the rabbit, and Mondrian-derived geometry in jewel-like, slow, deliberately tender compositions. The argument is that childhood, the book, and the Western-modernist primary colour are not naïve subjects — and that the contemporary Chinese painter can claim them precisely because Western painting has, by exhaustion, conceded them."
  },
  a917: { // Lu Song
    message: "Lu Song was born in Beijing in 1982, trained at Wimbledon College of Art in London, and lives in Beijing. His paintings — Wanderer in the Mist (2018) — work in a moody, cinematic atmospheric register that draws on European Romantic landscape, contemporary film stills, and personal memory. The argument is that the figure-in-landscape, a tradition that Chinese ink painting and German Romanticism share more than either school admits, is still the most consequential subject available to a painter formed between both."
  },
  a960: { // Lucia Laguna
    message: "Laguna was born in São Fidélis, Brazil in 1941, did not begin painting until her fifties, and lives in the working-class Lins neighborhood of Rio de Janeiro. Her paintings — Estudo (2010), Paisagem (2015) — layer views from her studio window, fragments of Brazilian landscape painting tradition, and the daily sounds of the favela into compositions made collaboratively with younger assistants she has trained. The argument is that painting is not a solo practice and the late-life artist not a footnote — that the studio is a small social form whose visible labour relations belong inside the painting."
  },
  a901: { // Ludovic Nkoth
    message: "Nkoth was born in Cameroon in 1994 and emigrated to South Carolina at age thirteen; he lives in New York and trained at the New York Academy of Art. His paintings — Mother and Son (2021) — depict Black figures in expressive, gesturally painted scenes of African and African-American family life, with the open paint of an oil-painter who has thoroughly absorbed late-twentieth-century Black figurative painting. The argument is that the contemporary diasporic African painter's responsibility is to the named family — the mother, son, brother — rendered with the same painterly seriousness Renaissance painting reserved for sacred subjects."
  },
  a902: { // Luigi Ontani
    message: "Ontani was born in Vergato, Italy in 1943 and lives in Rome; he emerged in the 1960s with the Arte Povera generation but worked at its eccentric, theatrical edge. His tableaux vivants (1970 onward), in which he poses as a saint, mythological figure, or hybrid divinity, alongside ceramic sculpture, photography, and Balinese-craft collaborations, build a single mythological-autobiographical universe. The argument is that Italian Catholic, classical, and pagan iconographies are still the contemporary Italian artist's deepest available vocabulary — and that the self-portrait as god, hero, or hermaphrodite is its honest contemporary form."
  },
  a813: { // Luis López-Chávez
    message: "López-Chávez was born in Cuba in 1983 and trained at ISA (Instituto Superior de Arte) in Havana. His paintings layer fragmented imagery and abstract gesture in compositions that work between Cuban history, image-mediation, and perceptual interruption. The argument is that the contemporary Cuban painting subject is itself fragmented — that the visual culture of the post-Special-Period generation is collaged, not whole, and that painting must honour that condition rather than smooth it over."
  },
  a424: { // Léon Wuidar
    message: "Wuidar was born in Liège, Belgium in 1938 and has worked from a single studio there for over six decades; he trained at the Académie des beaux-arts de Liège. His paintings — Sans titre (1975), the long Journal series (2015 onward) — combine warm-toned, hand-drawn geometric abstraction with a daily-diaristic dimension where each work is a single date's composition. The argument is that geometric abstraction is not an austere or chilly tradition — that hand-drawn line and warm colour are part of geometry's available vocabulary, and that the daily painting record is its most honest format."
  },
  a829: { // Manuela Sedmach
    message: "Sedmach was born in Trieste, Italy in 1953 and lives there; her work is shaped by Trieste's specific geography — the Adriatic light, the limestone karst, the long border between Italy and Slovenia. Her atmospheric near-abstract canvases — Paesaggio (2010), Orizzonte (2015) — render sea, fog, and horizon at the threshold where landscape becomes pure tonal field. The argument is that Trieste's specific light is itself a painting subject — neither Italian luminism nor Slovene mysticism, but the meteorological condition particular to a bordered city the European art map has long underweighted."
  },
  a791: { // Marcelo Cidade
    message: "Cidade was born in São Paulo in 1979 and lives there; he emerged in the early 2000s alongside other São Paulo artists working at the seam of skateboard culture, urban intervention, and conceptual sculpture. His works — Transestatal (2010), Tempo Suspenso de um Estado Provisório (2011) — repurpose materials lifted directly from public space (broken bus shelters, surveillance-camera housings, found concrete) into gallery sculptures that diagram urban surveillance and the legacies of Brazilian modernist architecture. The argument is that the city is a found-object archive and that the artist's most precise tool is the small, almost unnoticed displacement of one of its parts."
  },

  // ── Chunk 4 (50-batch) ──

  a467: { // Marisol
    message: "Marisol Escobar was born in Paris in 1930 to wealthy Venezuelan parents, moved to New York in 1950, and worked there until her death in 2016; her mother died when she was eleven and she chose, in protest of silence, to use only her first name for the rest of her life. Her wooden-block figures — The Family (1962), Women and Dog (1964), The Party (1965) — combine carving, painting, photo-transfer, and found object to make life-sized satirical portraits of public figures and family groups. She was briefly the most famous female Pop artist in the United States, then was systematically written out of the Pop canon — and her estate argument is that the historical record is being corrected, slowly, work by work."
  },
  a833: { // Marta Spagnoli
    message: "Spagnoli was born in Verona, Italy in 1994 and lives in Venice; she trained at the Accademia di Belle Arti di Venezia. Her gestural paintings — Creature (2020), Paesaggio (2022) — work in the unstable territory between figure and abstraction, drawing on Venetian colour tradition, animal forms, and a kind of mythological half-figuration that refuses to fully resolve. The argument is that the youngest generation of Italian painters still has a usable claim on the Venetian colour heritage — provided they enter it through abstraction rather than imitation."
  },
  a900: { // Matt Mullican
    message: "Mullican was born in Santa Monica in 1951, trained at CalArts under John Baldessari, and lives in New York and Berlin. Since the late 1970s he has built a single life-long cosmology — Five into One (1991) and the ongoing That Person's Workbook (2007) — a system of colour-coded zones (Subjective, Signs, Arts, World Framed, World Unframed) that he charts in posters, banners, drawings, and hypnotically induced 'That Person' performances. He argues that contemporary conceptual art has been too embarrassed to claim cosmology — and that a system of meaning, sustained over fifty years by one artist, is itself the work."
  },
  a940: { // Meriem Bennani
    message: "Bennani was born in Rabat, Morocco in 1988 and lives in Brooklyn; she trained at Cooper Union and at the École nationale supérieure des Arts Décoratifs in Paris. Her video installations — Party on the CAPS (2018–19), Mission Teens (2019), Fardaous Funjab (2015) — combine documentary footage, hand-drawn animation, talking-head interview, and meme humour into multichannel pieces that document Moroccan and diasporic life with the speed of a phone screen. The argument is that diasporic identity is now lived as a multichannel feed — and that the gallery's task is to give it a room rather than a single screen."
  },
  a214: { // Merrill Wagner
    message: "Wagner was born in Tacoma, Washington in 1935, lived in New York until her death in 2024, and was married to the painter Robert Ryman for over fifty years; she trained at Sarah Lawrence College. Her paintings — the long Rust series of the 1980s on weathered steel, the Seasonal stone works, the slate paintings — applied paint to surfaces that already had material history, letting weather, rust, and mineral grain become part of the composition. The argument is that the contemporary abstract painting's surface — stretched white cotton — was a convention, not a neutral ground, and that any material the world has already inscribed can be the painter's substrate."
  },
  a825: { // Michelangelo Pistoletto
    message: "Pistoletto was born in Biella, Italy in 1933 and still lives and works there at age 92; he is one of the founding figures of Arte Povera. His Mirror Paintings (1962 onward) screen-print figures onto polished stainless-steel surfaces so that the gallery viewer is inscribed inside the work; Venus of the Rags (1967) places a classical Venus before a heap of used clothing; and Cittadellarte (founded 1998 in Biella) extends the practice into a working model for socially engaged art education. The argument, sustained over six decades, is that the mirror is the most honest medium of post-war art — and that the viewer's own body inside the frame is the contemporary subject."
  },
  a903: { // Mimmo Paladino
    message: "Paladino was born in Paduli, Italy in 1948, lives in Rome and Paduli, and is a central figure of the Italian Transavanguardia movement theorised by Achille Bonito Oliva in the late 1970s. His Montagna di sale (1990, a 60-tonne salt-and-horses sculpture installed in Naples and later Milan) and his decades of painting, etching, and bronze figure draw on Etruscan, Egyptian, early Christian, and archaic Mediterranean visual vocabularies. The argument is that the post-Conceptual moment of the late 1970s did not require a clean break — that the painter could return to ancient image traditions without nostalgia, treating them as still-operative."
  },
  a861: { // Monster Chetwynd
    message: "Chetwynd was born in London in 1973 (and has worked under the names Spartacus and Marvin Gaye before settling on Monster), trained at the Slade and the Royal College of Art, and lives in Glasgow. Her costumed performance works — Hermitos Children (2008), Bat Opera (2003 onward) — restage Pasolini, Rabelais, fairy tale, sci-fi, and political iconography with sewn cardboard costumes, recruited performers, and deliberately rough production values. The argument is that contemporary performance's most undervalued tool is amateur cardboard — and that the polished art-fair production is a confession of unseriousness, not its opposite."
  },
  a971: { // Nabuqi
    message: "Nabuqi was born in Inner Mongolia in 1984 and lives in Beijing; she trained at the Central Academy of Fine Arts (CAFA). Her installations — Do real things happen in moments of rationality? (2018), A View Beyond Space (2015) — stage uncanny scenes in which fabricated foliage, mass-produced consumer objects, and fragments of generic architecture inhabit the gallery as if a stage set abandoned mid-performance. The argument is that the contemporary Chinese urban interior is itself a stage — and that sculpture's job is to render the gap between the consumer object and the human life it was sold to host."
  },
  a988: { // Nicola Tyson
    message: "Tyson was born in London in 1960 and has lived in New York since 1989; she helped found the influential Trial Balloon women's project space in early-1990s downtown New York. Her paintings — Self-Portrait (1996), Dancing Figure (2010) — depict distorted, slumped, swollen, or proboscis-like female figures in flat unmodulated colour that owes equally to Philip Guston and to a private cartoonish vocabulary. The argument is that the female body, in painting, need not be either beautiful or critically deconstructed — that it can be ungainly, comic, and psychologically charged on its own terms."
  },
  a928: { // Nicole Wittenberg
    message: "Wittenberg was born in New York in 1979, trained at the New York Studio School and the Royal Academy in London, and lives between Brooklyn and Maine. Her landscape and figurative pastels — Maine Coast (2020) and ongoing nude series — channel Fauvist colour and the gestural intimacy of pre-1914 European painting into a contemporary American practice that openly embraces decorative pleasure. The argument is that the Bonnard-Vuillard line is not closed history — that contemporary American painting can still inhabit Fauvist colour without irony, provided it has earned the right through observational rigour."
  },
  a233: { // Nigel Cooke
    message: "Cooke was born in Manchester, England in 1973 and lives in rural Kent; he trained at Nottingham Trent and the Royal College of Art before completing a PhD at Goldsmiths. His paintings — Black Mimosa (2009), Spring in Fialta (2018, after Nabokov) — combine landscape, figuration, and literary reference in densely layered surfaces that move from photorealism to abstract gesture within a single canvas. The argument is that contemporary British painting need not choose between figuration and abstraction, between landscape and conceptual armature — that the single painting can hold all of them at once if the painter is patient enough to layer."
  },
  a308: { // Oldenburg / van Bruggen
    message: "Claes Oldenburg (born Stockholm 1929, d. 2022) and Coosje van Bruggen (born Groningen 1942, d. 2009) collaborated as a single artistic body from 1976 until her death; he had previously been a central figure of American Pop, and she was an art historian and curator. Their joint monumental public sculptures — Spoonbridge and Cherry (1985, Walker Art Center), Cupid's Span (2002, San Francisco), the dozens of giant clothespins, badminton birdies, and trowel forms placed in plazas worldwide — argue that the public-art commission is best taken as joint authorship rather than as the heroic single sculptor's gesture. The estate-managed continuation insists that the monumental object can be both consumer-cliché and tender — that the absurd scale is a love-letter."
  },
  a899: { // Olivier Mosset
    message: "Mosset was born in Bern, Switzerland in 1944 and lives in Tucson, Arizona, where he has worked for the last three decades; he co-founded the BMPT group in 1966 in Paris with Daniel Buren, Michel Parmentier, and Niele Toroni. His paintings from that period reduced painting to a single Black Circle (1966) repeated identically across years, and his subsequent work has continued to interrogate authorship through monochromes, copies, and serial geometric abstraction made by him or by his assistants. The argument is that the painter's individual touch — the so-called signature — is an ideological construction, and that the painting's authority comes from elsewhere: from the decision, the protocol, the rule."
  },
  a822: { // Ornaghi & Prestinari
    message: "Valentina Ornaghi and Claudio Prestinari were both born in 1986 in northern Italy and trained at Brera and at the Politecnico di Milano; they have collaborated since 2011 and live in Milan. Their sculptures — Tela (2015), Sutura (2017) — combine traditional Italian craft technique (stone-cutting, embroidery, ceramics) with contemporary minimalist composition, often built around small acts of repair, stitch, or material splice. The argument is that Italian craft tradition is still operative as a contemporary medium — that the visible mend or sutured seam is a serious sculptural form, and that two-person collaboration is the relation in which craft can survive an art market trained to celebrate the single signature."
  },
  a797: { // Osvaldo González
    message: "González was born in Sancti Spíritus, Cuba in 1979, lives in Havana, and trained at the Instituto Superior de Arte (ISA). His sculptures — Coliseo (2014), Lágrimas Negras (2016) — are made from adhesive tape, fishing line, and light, producing ghostly architectural and natural forms whose materiality almost disappears under exhibition lighting. The argument is that the Cuban Special Period taught a generation of artists that scarcity is a working condition, not a defect — and that an entire sculptural vocabulary can be built from packing tape if the alternative is silence."
  },
  a923: { // Paloma Varga Weisz
    message: "Varga Weisz was born in Mannheim, Germany in 1966 to a Hungarian-German family, trained in traditional woodcarving in Bavaria before studying at the Düsseldorf Kunstakademie under Gerhard Merz and Tony Cragg, and lives in Düsseldorf. Her carved-wood figures — Bumped Body (2002), Root of a Dream (2017) — evoke European folklore, Catholic saint sculpture, and the medieval workshop, but the bodies are subtly hybridised, swollen, or interrupted. The argument is that German woodcarving is not a closed historical medium — and that the uncanny female figure, in the lineage of the medieval Virgin and the dark fairy tale, is still its proper subject."
  },
  a320: { // Paolo Roversi
    message: "Roversi was born in Ravenna, Italy in 1947 and has lived and worked in Paris since 1973; he is one of the central fashion photographers of the late twentieth century, with long-standing collaborations at Vogue Italia, Comme des Garçons, Yohji Yamamoto, and Christian Dior. His large-format Polaroid portraits — Nudi (1999), Studio (2005), the long Natalia Vodianova series — work in slow exposures with dust-grey backgrounds and a painterly chiaroscuro that owes more to Velázquez than to fashion. The argument is that fashion photography is not a lower medium than fine art — that its working tradition, when treated with the slowness of large-format Polaroid, produces images on the same continuum as the Renaissance portrait."
  },
  a838: { // Pascale Marthine Tayou
    message: "Tayou was born in Yaoundé, Cameroon in 1966 and lives in Ghent, Belgium; he changed the spelling of his name to add the feminine '-e' as an early refusal of inherited identity categories. His riotous installations — the Plastic Bags series (2008 onward), Colonial Erection (2009), the Crystal Tree, Falling Houses — assemble cheap commodity objects from West African markets, Murano glass, ceramic, and salvaged building material into compositions about globalisation's circulation of bodies and goods. The argument is that the contemporary African artist's medium cannot be confined to a single material tradition — global trash is the global condition, and sculpture's task is to make its scale legible."
  },
  a994: { // Paul Anthony Harford
    message: "Harford was born in Southend-on-Sea, England in 1943 and worked there in obscurity until his death in 2016; he had a single solo gallery exhibition in his lifetime. His finely observed pencil and ink drawings depict pubs, post-war working-class streets, lone figures, and bedsit interiors with a precision that owes more to Edward Hopper and Eric Ravilious than to anyone working in the contemporary British art scene. The estate-managed argument is that the working-class British provincial draughtsman, working alone for decades without market relationship, has produced a body of work that the art-historical record was not equipped to register — and the gallery system is, slowly, learning how to."
  },
  a255: { // Paul Graham
    message: "Graham was born in Stafford, England in 1956 and lives in New York; he taught himself photography and emerged in the 1980s alongside Martin Parr as a central figure of British color documentary. His series — A1: The Great North Road (1981–82, the first British color documentary book), Beyond Caring (waiting rooms in the Thatcher-era social-security system), and a shimmer of possibility (2004, twelve volumes of small American street observations) — refused the black-and-white humanist tradition. The argument — which won him the Hasselblad Award in 2012 — is that color photography is not a softer documentary medium but a more honest one, because it does not pretend that the world is morally legible at a glance."
  },
  a337: { // Paul Thek
    message: "Thek was born in Brooklyn in 1933, died of AIDS in 1988, and lived between New York and Europe; his Technological Reliquaries (1964) — wax casts of meat in minimalist plexiglas vitrines — confronted the cool surface of 1960s American minimalism with raw human flesh-quality. His later immersive installations — The Tomb (1967), the long Processions series of the 1970s — used candle, drift, and procession to make works that prefigured installation art before that category had been institutionalised. The estate-managed argument is that the American 1960s avant-garde had a hidden second wing — sacred, queer, mortal — and that Thek's reinstatement as a central figure of the period is still incomplete."
  },
  a913: { // Peter Schuyff
    message: "Schuyff was born in Baarn, Netherlands in 1958, moved to Vancouver and then to New York, and is loosely associated with the Neo-Geo generation of the early 1980s alongside Peter Halley, Sherrie Levine, and Jeff Koons. His paintings — the Untitled hard-edge geometric abstractions of 1986 onward — replicate Op-art-derived patterns with a cool, hand-painted precision that uses the language of Vasarely and Bridget Riley as already-historical material. The argument is that the 1980s painter could no longer make a 'new' abstraction, only quote a previous one — and that the deliberately deadpan re-painting of Op art is a position about painting's historical condition, not a nostalgia for it."
  },
  a910: { // Pietro Roccasalva
    message: "Roccasalva was born in Modica, Sicily in 1970 and lives in Milan; he trained at the Accademia di Belle Arti di Brera and emerged in the early 2000s with a multi-media practice that operates as a single ongoing allegorical drama. His paintings, sculptures, drawings, and tableaux — Il Traviatore (2010) — recur to a small set of figures (the juicer, the harlequin, the singer) layered with operatic, religious, and Sicilian-Baroque references, in compositions that read as both painting and stage design. The argument is that the Sicilian-Baroque visual tradition is still operative — and that the contemporary artist who returns to allegory and theatre is not retreating but advancing into a tradition that conceptual art's twentieth century had quietly suspended."
  },
  a920: { // Piotr Uklański
    message: "Uklański was born in Warsaw in 1968, lives in New York and Warsaw, and trained at the Cooper Union after emigrating from communist Poland. His Nazis (1998) installed 164 publicity photographs of actors playing Nazis in films — Brando, Olivier, Bowie, Caine — as a single immersive grid; his Dance Floor (1996) installed a colour-flashing illuminated nightclub floor in galleries from Gavin Brown to the Whitney. The argument is that popular culture's dirty visual archive — Nazis-played-by-handsome-actors, nightclub flooring, soft-core pin-up calendars — is not a lower register for art to slum in but a central one, where contemporary politics actually circulates."
  },
  a82: { // Rashid Johnson
    message: "Johnson was born in Chicago in 1977, trained at Columbia College Chicago and the School of the Art Institute, and lives in New York. His painting, sculpture, film, writing, and performance practice — the Anxious Men (2015) painted-soap heads, The Hikers (2019, a feature-length film), the long Cosmic Slop tar-and-shea-butter painting series — works through a stable vocabulary of Black domestic, intellectual, and bodily reference (soap, shea butter, plant, mirror, books) layered with deliberate emotional intensity. The argument is that the American Black male interior life has been chronically underrepresented as a painterly subject — and that the painting can render anxiety, grief, and inherited cultural weight at the same scale as historical religious painting."
  },
  a202: { // Raymond Saunders
    message: "Saunders was born in Pittsburgh in 1934, lives in Oakland, California, and is now (in his nineties) finally recognised as one of the central American postwar painters; he taught for decades at California College of the Arts. His blackboard-like paintings — Marie's Bill (1970), Jack Johnson (1972) — layer painted figures, chalk-drawn text, photo-transfer, and pinned ephemera onto matte black grounds, building dense fields of vernacular Black American visual material. His 1967 essay 'Black Is a Color' refused both Greenbergian abstraction's politics-blindness and the Black Arts Movement's demand for political legibility — and the work, sustained over fifty years, argues that Black painting need not choose between the two."
  },
  a276: { // Richard Learoyd
    message: "Learoyd was born in Nelson, Lancashire in 1966, lives in London, and works inside a single room-sized camera obscura he has built into his studio — exposures are taken on Ilfochrome positive paper directly through the camera's lens, with no intermediate negative. His portraits and still lifes — Agnes (2008), Man with Octopus Tattoo (2011) — produce a single physical print per sitting, unique and at the scale of the sitter's body. The argument is that the photograph as multiple, infinitely reproducible image is a historical accident of the medium — and that the singular print, made through a Victorian apparatus, is photography's other available tradition."
  },
  a211: { // Rirkrit Tiravanija
    message: "Tiravanija was born in Buenos Aires in 1961 to Thai diplomatic parents, grew up between Thailand, Ethiopia, and Canada, and lives between New York, Berlin, and Chiang Mai. His Untitled (Pad Thai) (1990) and Untitled (Free) (1992) at 303 Gallery transformed the gallery into a Thai kitchen in which he cooked and served free meals to visitors — a foundational work of what Nicolas Bourriaud later codified as relational aesthetics. His Land Foundation in Chiang Mai (founded 1998 with Kamin Lertchaiprasert) extends the practice into a working agricultural-and-art community. The argument is that hospitality is a serious sculptural medium — and that the meal shared with the stranger is contemporary art's most under-credited form."
  },
  a94: { // Rita Ackermann
    message: "Ackermann was born in Budapest in 1968, arrived in New York in 1992, and has worked there since. Her semi-figurative paintings — Fire by Days (2010), the Mama series (2017 onward) — work through a process of building up female figures in compressed-charcoal, oil, and pastel, then deliberately erasing, scraping, and washing the surface so that figure and ground become indistinguishable. The argument is that the female figure in painting is most truthful when partly erased — that the cleanly rendered woman is a lie about how women are actually perceived, and that the painting's surface needs to register that mid-perceptual incompleteness."
  },
  a867: { // Roland Flexner
    message: "Flexner was born in Nice, France in 1944 and has lived in New York since 1990. His best-known works are the Liquid Drawings (2009 onward), produced by blowing soap bubbles loaded with ink onto small sheets of paper and arresting the bubble at the moment its surface tension records a brief landscape, vortex, or galactic pattern. The argument is that drawing's contemporary subject can be the ephemeral physical event itself — that an artist whose entire output consists of capturing brief surface-tension accidents is not gimmicky but disciplined: each drawing is unrepeatable, and that unrepeatability is the work."
  },
  a820: { // Rudi Ninov
    message: "Ninov was born in Sofia, Bulgaria in 1991 and lives between Sofia and Vienna; he trained at the National Academy of Art in Sofia and at the Academy of Fine Arts Vienna. His paintings and works on paper — Untitled (2021) — examine language, abstraction, and the gesture of writing as primary subject, working with text-fragments, written marks, and the abstract field as if they were the same operation. The argument is that the painter's mark and the writer's letter are the same gesture historically separated by institutional categories — and that contemporary Eastern European abstraction can productively dissolve that boundary."
  },
  a250: { // Sam Gilliam
    message: "Gilliam was born in Tupelo, Mississippi in 1933, lived in Washington DC for over fifty years, and died in 2022; he was the first Black American artist to represent the United States at the Venice Biennale, in 1972. His Drape Paintings (1968 onward) and beveled-edge canvases stained colour into raw cotton and then suspended the canvas off the stretcher, draped across walls, ceilings, and rooms, in a move that — three years before Olitski or Frankenthaler — extended Color Field painting into three dimensions. The estate-managed argument is that the canonical narrative of American Color Field abstraction has the chronology and the authorship wrong, and that Gilliam's draped canvas was the medium's most consequential single innovation."
  },
  a181: { // Sarah Michelson
    message: "Michelson was born in Manchester, England in 1964 and lives in New York; she trained as a dancer at the London Contemporary Dance School and crossed into the gallery and Whitney circuit in the early 2000s. Her site-specific dance pieces — Devotion Study #1 (2012 Whitney Biennial, for which she received the Bucksbaum Award), Dover Beach (2009) — work with extreme physical endurance, intricate floor diagrams painted directly onto the institution's surfaces, and exhausting duration. The argument is that contemporary dance in the gallery context is not theatre's poor cousin — and that the dancer's body, sustained at the threshold of collapse, is a sculptural condition the museum has only recently learned how to host."
  },
  a167: { // Scott Kahn
    message: "Kahn was born in Trenton, New Jersey in 1946, trained at the University of Pennsylvania and at the Indiana University MFA, and lived for decades in relative obscurity in New York and Lyme, Connecticut before his late-career re-discovery in the 2020s. His paintings — My House at Night (1995), The Dream (1989) — render meticulous, dreamlike landscapes, interiors, and autobiographical scenes in a slow folk-modernist register that recalls Florine Stettheimer and Henri Rousseau more than any post-1960 American painter. The argument is that the art-historical record has a late-discovery problem — that work made carefully and consistently over forty years is not less serious for having been ignored, and that the slow domestic painter is a real contemporary category."
  },
  a648: { // Sean Scully
    message: "Scully was born in Dublin in 1945, raised in working-class south London, and lives between New York, Munich, and Tappan; he trained at Croydon College of Art and Newcastle. His stripe paintings — initially hard-edged minimalist grids in the 1970s, then increasingly painterly horizontal-and-vertical bands from the mid-1980s onward, culminating in the long Wall of Light series — sit between European geometric abstraction (Mondrian, Klee) and American post-Rothko colour-field painting. The argument is that the stripe is not an exhausted modernist motif but a flexible vessel for emotional content — provided the painter is willing to admit that emotion, light, and weight are still valid painterly subjects."
  },
  a830: { // Serse
    message: "Serse Roma was born in San Polo di Piave, Italy in 1952 and lives in Trieste; he works exclusively in graphite on paper at sizes that approach painting. His hyperrealist drawings — Acque (2000 onward), Paesaggio (2008) — depict water, fog, rock, and sky at near-photographic precision, but the medium (pencil) is so fundamentally insufficient to the subject (light, wetness) that the gap between rendering and reality becomes the actual content. The argument is that hyperrealism's contemporary value lies in choosing the wrong medium for the right subject — graphite can never become water, and the visible failure of the attempt is what the drawing is about."
  },
  a976: { // Seth Price
    message: "Price was born in East Jerusalem in 1973 to American parents and lives in New York; he trained at Brown and is also a noted writer and theorist. His artist's essay Dispersion (2002) — written before social media — anticipated the gallery's loss of authority over how images circulate; his Vintage Bomber (2006) sculptural series, video, painting, and fashion-line collaborations test where the work's edge actually is. The argument is that contemporary art's hidden medium is distribution — and that the artist's task in a post-2000 networked condition is to make work that already knows how it will be reproduced, screen-captured, and re-sold, and that uses that anticipation as a formal device."
  },
  a857: { // Shannon Cartier Lucy
    message: "Cartier Lucy was born in Nashville, Tennessee in 1977 and lives there; she trained at NYU's Tisch School and worked in New York before moving back to Tennessee. Her figurative paintings — The Strawberry (2019), Woman with Cake (2020) — depict women in domestic interiors performing small absurd or unsettled acts (squeezing a strawberry against a wall, sitting before a cake) in a flat narrative register that recalls Eric Fischl and Balthus without their voyeurism. The argument is that the women-alone-in-a-room subject is not a closed historical category — that the contemporary woman's private moments, when painted without explanation, are themselves the painting's psychological content."
  },
  a948: { // Shannon Ebner
    message: "Ebner was born in Englewood, New Jersey in 1971 and lives in Los Angeles; she trained at Bard MFA. Her photographs — The Electric Comma (2009), A Public Character (2012), STRIKE — photograph letters, signs, and language fragments in the American landscape as if they were sculptural form, then construct them into longer poetic sequences. The argument is that contemporary photography's most under-explored subject is the written word as physical object — that the highway sign, the storefront letter, and the dropped roadside placard constitute an American vernacular sculpture that photography is uniquely positioned to read."
  },
  a974: { // Simon Periton
    message: "Periton was born in Kent, England in 1964, trained at Saint Martin's School of Art, and lives in London; he was one of the artists associated with the Cabinet gallery generation of mid-1990s London. His intricate cut-paper doilies — Anarchy Doily (1996) substitutes anarchist symbols, skulls, and political graffiti for the traditional doily's floral motif — and his later Black Iris (2008) cut-metal sculptures translate the doily's lacework into permanent architectural scale. The argument is that the decorative paper doily — pure feminine craft, dismissed by every modernism — is in fact a vessel of considerable formal sophistication, and that smuggling punk content inside it is a critique of both ornamental tradition and anti-ornamental modernism."
  },
  a860: { // Skyler Chen
    message: "Chen was born in Tainan, Taiwan in 1991 and lives in New York; he trained at the School of Visual Arts. His dreamlike figurative paintings — Bathers (2022) — depict queer Asian-diasporic figures in lush interiors, bathhouses, and natural settings rendered in saturated colour with a delicacy that recalls early Italian fresco. The argument is that contemporary queer Asian-diasporic painting need not stage trauma as its constitutive subject — that pleasure, memory, and the bathhouse as classical genre scene are sufficient and seriously available."
  },
  a893: { // Spencer Lewis
    message: "Lewis was born in Hartford, Connecticut in 1979, trained at the University of Hartford and Yale MFA, and lives in Los Angeles. His paintings on jute — the long Untitled jute series (2018 onward) — combine aggressive gestural mark-making (acrylic, ink, enamel, spray) with collage-like compositional structure on raw rough textile, in a register that returns deliberately to the post-Abstract-Expressionist American painting moment. The argument is that the raw, unsized jute support is not an aesthetic affectation but a working condition — its tooth, weight, and aggressive surface refuse the painter's options in ways that produce truer paintings than cotton ever can."
  },
  a862: { // Steven Claydon
    message: "Claydon was born in London in 1969, lives there, and trained at the Royal College of Art; he has worked as both an artist and a curator since the early 2000s. His sculptures and installations — Analogues, Methods, Hosts and Mascots (2014) — examine how museum display, ethnographic vitrine, and modernist cabinet have framed objects into the meaning categories the institution required them to occupy. The argument is that the contemporary sculpture is not a discrete object but a display proposition — and that the artist's medium includes the case, the pedestal, the wall-label, and the lighting decision that the museum normally treats as neutral."
  },
  a990: { // TJ Wilcox
    message: "Wilcox was born in Seattle in 1965, trained at the School of Visual Arts and CalArts, and lives in New York. His film collages — Garlands (2005), In the Air (2013, a 360-degree panoramic video installation of a single day's sky over Union Square) — splice archival footage of figures including Marie Antoinette, Stephen Tennant, and Garbo with personal narration and 16mm-feeling colour treatments. The argument is that the contemporary artist's archive is now indistinguishable from the personal photo album — and that the film essay, which the museum has been slow to host, is the medium for that dissolved boundary."
  },
  a877: { // Thomas Grünfeld
    message: "Grünfeld was born in Opladen, Germany in 1956 and lives in Cologne; he trained at the Hochschule für bildende Künste Hamburg under Sigmar Polke alongside Georg Herold and Albert Oehlen. His Misfits series (1990 onward) commissions traditional taxidermists to combine the bodies of different animals — a St Bernard's head onto a sheep's body, a peacock onto a pig — into hybrid creatures that look entirely convincing as natural specimens. The argument is that the taxidermy display, the museum's quietest form, has been hiding a deeply uncomfortable epistemology — and that the obvious fake animal is more honest about what the natural history museum has always been doing."
  },
  a306: { // Thomas Nozkowski
    message: "Nozkowski was born in Teaneck, New Jersey in 1944 and died in 2019; he trained at Cooper Union and lived for most of his career in the Hudson Valley and the New York downtown scene. His small canvases — typically 16 by 20 inches, all titled Untitled with a numbered identifier — were built slowly through scraping, overpainting, and revision, with each work drawing on a specific personal memory, observation, or art-historical reference that he refused to disclose. The argument is that the intimate-scale abstract painting is not a lesser format than the large gestural canvas — that the small painting, built through patient memory work, is one of the great American post-war painterly traditions still being underwritten."
  },
  a827: { // Tobias Rehberger
    message: "Rehberger was born in Esslingen, Germany in 1966, trained at the Städelschule under Thomas Bayrle and Martin Kippenberger, and is now a professor there. His practice — the Venice Biennale cafeteria (2009, for which he received the Golden Lion for Was du liebst, bringt dich auch zum Weinen), 81 Years (2002), dazzle-painted interiors — works at the deliberately ambiguous seam of art, design, and architecture, producing functional environments that operate as immersive sculpture. The argument is that the design-versus-art boundary is an art-historical convenience — and that the most useful contemporary sculptures are also chairs, lamps, cafés, or façades."
  },
  a444: { // Tony Cragg
    message: "Cragg was born in Liverpool in 1949, trained at the Royal College of Art in London, and has lived in Wuppertal, Germany since 1977, where he served as rector of the Kunstakademie Düsseldorf from 2009 to 2013. His early works — Stack (1975, layered domestic debris), Britain Seen from the North (1981, a wall map made of found plastic) — were assemblages of urban-industrial waste; his later computer-modeled bronze and wood forms (Rational Beings, Early Forms) are smooth swept-surface volumes that emerge from layered cross-sections. The argument, sustained over fifty years, is that contemporary sculpture's medium is material science — and that the British tradition of object-as-subject (from Henry Moore through Cragg) can be extended through computation without losing its physical seriousness."
  },
  a265: { // Virginia Jaramillo
    message: "Jaramillo was born in El Paso, Texas in 1939 to Mexican parents, lived in Los Angeles in the 1960s where she was part of the African-American Watts Tower visual community, and has lived in upstate New York since 1971. Her hard-edge and curvilinear abstractions — Green Dawn (1971), the long Curvilinear Paintings of the 1970s, and the recent linen-paper-and-pigment works — were largely written out of the American Color Field canon until her inclusion in the 2017 Tate Modern exhibition Soul of a Nation. The argument is that the canonical narrative of post-war American abstraction systematically excluded Latina and Black women practitioners — and that the corrective is not symbolic inclusion but a re-reading of the period itself, work by work."
  },

};

// Expose for the quiz UI
if (typeof window !== 'undefined') window.QUIZ_MESSAGES = QUIZ_MESSAGES;
