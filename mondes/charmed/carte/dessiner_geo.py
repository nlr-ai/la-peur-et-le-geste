# -*- coding: utf-8 -*-
"""Dessine la table de Charmed : la baie de San Francisco a l'automne 2001.

    python mondes/charmed/carte/dessiner_geo.py   -> carte/geo.js (a cote)

Meme format que `ecrans/modules/geo.js` (Westeros, engendre du mod AGOT), mais
trace A LA MAIN : des longitudes et latitudes relevees de memoire, projetees a
plat. C'est un croquis juste a quelques centaines de metres pres, pas un releve
-- assez pour qu'une distance tranche (le P3 est a vingt minutes de voiture de
Prescott Street, Oakland est au bout d'un pont), pas assez pour un cadastre. On
retouche les points ici et on relance, jamais geo.js a la main.

LE RIVAGE EST CELUI DE 2001. Repris du generateur de 1906 (mondes/charmed-1906)
et modernise : la Marina remblayee pour l'Exposition de 1915 et Crissy Field au
pied du Presidio ; Fort Mason et ses jetees ; les quais du Wharf et
l'Embarcadero (sa voie rapide est tombee apres le seisme de 1989, il reste le
boulevard) ; Mission Bay et China Basin comblees jusqu'a Pier 70 ; Hunters
Point et Candlestick avances dans la baie. En face : l'ile au Tresor (remblayee
en 1937) collee a Yerba Buena, le port d'Oakland et Alameda Point. Les vraies
routes sont les deux ponts, les freeways et les grands boulevards ; il reste
deux ferrys depuis le Ferry Building.

Les lieux de `etat/lieux.json` qui sont AILLEURS (les Enfers, La-haut,
l'au-dela, les limbes, la terre desolee) n'ont pas de point ici : ils ne sont
sur aucune table, et c'est juste.
"""
import json
import os

ICI = os.path.dirname(os.path.abspath(__file__))

# La projection : 1 unite = 1/1000 de degre de latitude (~111 m). Les longitudes
# sont ecrasees par cos(37.8) pour que la ville ne s'etire pas en largeur.
O_LON, O_LAT, K = -122.56, 37.92, 790.0


def P(lon, lat):
    return [round((lon - O_LON) * K, 1), round((O_LAT - lat) * 1000, 1)]


def d(pts, ferme=True):
    q = [P(*p) for p in pts]
    s = "M" + " L".join("%s,%s" % (x, y) for x, y in q)
    return s + (" Z" if ferme else "")


def ovale(lon, lat, rx, ry):
    x, y = P(lon, lat)
    return "M%s,%s a%s,%s 0 1 0 %s,0 a%s,%s 0 1 0 %s,0 Z" % (
        round(x - rx, 1), y, rx, ry, 2 * rx, rx, ry, -2 * rx)


def centre(pts):
    q = [P(*p) for p in pts]
    return [round(sum(a for a, _ in q) / len(q), 1), round(sum(b for _, b in q) / len(q), 1)]


# ---- la ville : le rivage de 2001, dans le sens des aiguilles -------------
# Les sommets partages avec les quartiers sont ecrits a l'identique : un
# quartier qui touche l'eau s'arrete sur le meme point que la cote.
VILLE = [
    (-122.502, 37.680), (-122.497, 37.700), (-122.5035, 37.720), (-122.508, 37.740),
    (-122.5105, 37.760), (-122.5108, 37.765), (-122.512, 37.771), (-122.5124, 37.774),
    (-122.513, 37.777), (-122.5115, 37.781), (-122.506, 37.788), (-122.494, 37.789),
    (-122.484, 37.7915), (-122.481, 37.800), (-122.478, 37.808), (-122.4775, 37.8105),
    # Crissy Field et la Marina
    (-122.470, 37.806), (-122.460, 37.8045), (-122.4485, 37.805), (-122.447, 37.8075),
    (-122.442, 37.8065), (-122.436, 37.8065),
    # Fort Mason, Aquatic Park, le Wharf, Pier 39
    (-122.432, 37.809), (-122.428, 37.8085), (-122.4235, 37.8075), (-122.419, 37.810),
    (-122.414, 37.8095), (-122.4095, 37.8105),
    # l'Embarcadero jusqu'au Ferry Building, puis l'ancrage du pont
    (-122.4045, 37.8075), (-122.400, 37.8045), (-122.396, 37.800), (-122.393, 37.7955),
    (-122.3895, 37.791), (-122.388, 37.786), (-122.3865, 37.781), (-122.3875, 37.776),
    # Mission Bay comblee, Pier 70, Islais Creek, Hunters Point, Candlestick
    (-122.386, 37.770), (-122.383, 37.764), (-122.380, 37.758), (-122.382, 37.752),
    (-122.384, 37.745), (-122.377, 37.741), (-122.366, 37.736), (-122.357, 37.729),
    (-122.363, 37.722), (-122.375, 37.716), (-122.379, 37.709), (-122.388, 37.705),
    (-122.392, 37.690), (-122.390, 37.680),
]
ILES = {
    "yerba-buena": (-122.366, 37.810, 5.2, 4.2),
    "ile-au-tresor": (-122.3705, 37.8235, 4.4, 7.0),
    "alcatraz": (-122.423, 37.827, 1.8, 1.2),
    "angel": (-122.432, 37.861, 8.5, 8.0),
}
# ---- le lointain : Marin au nord de la Porte d'Or, l'East Bay a l'est -------
MARIN = [
    (-122.560, 37.827), (-122.531, 37.816), (-122.510, 37.826), (-122.492, 37.825),
    (-122.478, 37.826), (-122.477, 37.838), (-122.484, 37.852), (-122.480, 37.862),
    (-122.466, 37.871), (-122.452, 37.873), (-122.447, 37.885), (-122.458, 37.900),
    (-122.478, 37.920), (-122.560, 37.920),
]
TIBURON = [
    (-122.478, 37.920), (-122.462, 37.905), (-122.452, 37.890), (-122.442, 37.878),
    (-122.450, 37.868), (-122.465, 37.872), (-122.470, 37.885), (-122.490, 37.905),
    (-122.500, 37.920),
]
# L'East Bay de 2001 : Emeryville, la place de peage du Bay Bridge sur son
# remblai, le port d'Oakland, l'estuaire, Alameda Point, l'aeroport.
EST = [
    (-122.335, 37.920), (-122.315, 37.895), (-122.310, 37.870), (-122.305, 37.845),
    (-122.310, 37.830), (-122.318, 37.824), (-122.322, 37.812), (-122.305, 37.802),
    (-122.330, 37.788), (-122.320, 37.775), (-122.290, 37.770), (-122.258, 37.755),
    (-122.240, 37.740), (-122.225, 37.718), (-122.200, 37.700), (-122.180, 37.680),
    (-122.180, 37.920),
]

# ---- les quartiers de 2001 ---------------------------------------------------
QUARTIERS = [
    ("presidio", "Le Presidio", "Presidio", [
        (-122.484, 37.7915), (-122.481, 37.800), (-122.478, 37.808), (-122.4775, 37.8105),
        (-122.470, 37.806), (-122.460, 37.8045), (-122.4485, 37.805), (-122.447, 37.799),
        (-122.447, 37.788), (-122.459, 37.786), (-122.478, 37.786)]),
    ("marina", "La Marina et Cow Hollow", "Marina", [
        (-122.4485, 37.805), (-122.447, 37.8075), (-122.442, 37.8065), (-122.436, 37.8065),
        (-122.432, 37.809), (-122.428, 37.8085), (-122.4235, 37.8075), (-122.4235, 37.800),
        (-122.447, 37.799)]),
    ("pacific-heights", "Pacific Heights", "Pacific Heights", [
        (-122.447, 37.799), (-122.4235, 37.800), (-122.4229, 37.7925), (-122.4225, 37.787),
        (-122.447, 37.788)]),
    ("richmond", "Le Richmond", "Richmond", [
        (-122.5124, 37.774), (-122.513, 37.777), (-122.5115, 37.781), (-122.506, 37.788),
        (-122.494, 37.789), (-122.484, 37.7915), (-122.478, 37.786), (-122.459, 37.786),
        (-122.447, 37.788), (-122.447, 37.774)]),
    ("parc", "Le parc du Golden Gate", "Golden Gate Park", [
        (-122.5124, 37.774), (-122.453, 37.774), (-122.453, 37.766), (-122.5108, 37.765),
        (-122.512, 37.771)]),
    ("sunset", "Le Sunset", "Sunset", [
        (-122.5108, 37.765), (-122.470, 37.766), (-122.462, 37.745), (-122.470, 37.720),
        (-122.5035, 37.720), (-122.508, 37.740), (-122.5105, 37.760)]),
    ("western-addition", "Western Addition et Hayes Valley", "Western Addition", [
        (-122.447, 37.788), (-122.4225, 37.787), (-122.421, 37.779), (-122.4195, 37.7752),
        (-122.447, 37.771)]),
    ("nord", "North Beach, Russian Hill et Chinatown", "North Beach", [
        (-122.4235, 37.8075), (-122.419, 37.810), (-122.414, 37.8095), (-122.4095, 37.8105),
        (-122.4045, 37.8075), (-122.400, 37.8045), (-122.396, 37.800), (-122.401, 37.7955),
        (-122.407, 37.792), (-122.4229, 37.7925), (-122.4235, 37.800)]),
    ("centre", "Le centre, Nob Hill et le Tenderloin", "Nob Hill", [
        (-122.396, 37.800), (-122.393, 37.7955), (-122.405, 37.7865), (-122.4195, 37.7752),
        (-122.421, 37.779), (-122.4225, 37.787), (-122.4229, 37.7925), (-122.407, 37.792),
        (-122.401, 37.7955)]),
    ("som", "South of Market", "SoMa", [
        (-122.393, 37.7955), (-122.3895, 37.791), (-122.388, 37.786), (-122.3865, 37.781),
        (-122.3875, 37.776), (-122.398, 37.7715), (-122.4065, 37.7685), (-122.4195, 37.7700),
        (-122.4195, 37.7752), (-122.405, 37.7865)]),
    ("mission", "La Mission, le Castro et Noe Valley", "Mission", [
        (-122.4065, 37.7685), (-122.4195, 37.7700), (-122.4195, 37.7752), (-122.447, 37.771),
        (-122.440, 37.745), (-122.425, 37.735), (-122.405, 37.745), (-122.4045, 37.760)]),
    ("potrero", "Mission Bay, Potrero et Bayview", "Potrero", [
        (-122.3875, 37.776), (-122.398, 37.7715), (-122.4065, 37.7685), (-122.4045, 37.760),
        (-122.405, 37.745), (-122.425, 37.735), (-122.420, 37.715), (-122.388, 37.705),
        (-122.379, 37.709), (-122.375, 37.716), (-122.363, 37.722), (-122.357, 37.729),
        (-122.366, 37.736), (-122.377, 37.741), (-122.384, 37.745), (-122.382, 37.752),
        (-122.380, 37.758), (-122.383, 37.764), (-122.386, 37.770)]),
]

# ---- le relief : les collines de la ville, les cretes d'en face ------------
COLLINES = [
    (-122.4475, 37.7535, 7, 5), (-122.453, 37.739, 5, 4), (-122.4135, 37.7925, 3.2, 2.4),
    (-122.418, 37.801, 3, 2.4), (-122.4055, 37.8025, 2.2, 1.8), (-122.3935, 37.786, 1.8, 1.4),
    (-122.401, 37.758, 3.6, 2.4), (-122.415, 37.743, 3, 2.4), (-122.458, 37.763, 3, 2),
    (-122.437, 37.784, 2.6, 1.8), (-122.4365, 37.7925, 2.4, 1.6),
]
MONTAGNES = [
    (-122.245, 37.880, 9, 18), (-122.215, 37.835, 8, 16), (-122.195, 37.795, 7, 14),
    (-122.540, 37.860, 12, 10), (-122.505, 37.875, 8, 8), (-122.425, 37.862, 5, 5),
]

# ---- les grandes voies de 2001 : deux ponts, des freeways, des boulevards --
ROUTES = [
    ("golden-gate-bridge", "Le pont du Golden Gate",
     [(-122.4775, 37.8105), (-122.4782, 37.8185), (-122.4790, 37.8265), (-122.4800, 37.8330)]),
    ("bay-bridge", "Le Bay Bridge",
     [(-122.3885, 37.7875), (-122.3745, 37.8000), (-122.3665, 37.8085), (-122.3550, 37.8135),
      (-122.3300, 37.8195), (-122.3120, 37.8235)]),
    ("us-101-marin", "La 101 vers Marin",
     [(-122.4800, 37.8330), (-122.4870, 37.8450), (-122.4980, 37.8620), (-122.5080, 37.8800),
      (-122.5200, 37.9000)]),
    ("i-80-est", "La 80 vers Oakland et Berkeley",
     [(-122.3120, 37.8235), (-122.2990, 37.8290), (-122.2960, 37.8500), (-122.3000, 37.8800),
      (-122.3150, 37.9050)]),
    ("lombard", "Lombard Street et Doyle Drive",
     [(-122.4235, 37.8000), (-122.4470, 37.7990), (-122.4650, 37.8020), (-122.4775, 37.8105)]),
    ("market", "Market Street", [(-122.3935, 37.7955), (-122.405, 37.7865),
                                 (-122.4195, 37.7752), (-122.4285, 37.768), (-122.435, 37.7625)]),
    ("van-ness", "Van Ness Avenue",
     [(-122.4235, 37.8065), (-122.4235, 37.8000), (-122.4225, 37.787), (-122.421, 37.779),
      (-122.4195, 37.7752)]),
    ("geary", "Geary Boulevard",
     [(-122.4223, 37.7855), (-122.447, 37.7825), (-122.480, 37.7805), (-122.5105, 37.7795)]),
    ("park-presidio", "Park Presidio et la 19e avenue",
     [(-122.4700, 37.8030), (-122.4720, 37.7860), (-122.4725, 37.7740), (-122.4755, 37.7650),
      (-122.4755, 37.7350), (-122.4740, 37.7200), (-122.4725, 37.7060)]),
    ("i-80-ville", "La 80 et la Central Freeway",
     [(-122.3885, 37.7875), (-122.3980, 37.7800), (-122.4050, 37.7725), (-122.4080, 37.7680),
      (-122.4195, 37.7700)]),
    ("us-101-bayshore", "La 101, Bayshore Freeway",
     [(-122.4080, 37.7680), (-122.4065, 37.7620), (-122.4050, 37.7450), (-122.4035, 37.7300),
      (-122.4000, 37.7150), (-122.3950, 37.7000), (-122.3930, 37.6850)]),
    ("i-280", "La 280",
     [(-122.3935, 37.7745), (-122.3980, 37.7660), (-122.4035, 37.7500), (-122.4130, 37.7370),
      (-122.4360, 37.7300), (-122.4500, 37.7180), (-122.4620, 37.7050), (-122.4700, 37.6900)]),
    ("embarcadero", "L'Embarcadero",
     [(-122.4095, 37.8085), (-122.4045, 37.8060), (-122.4000, 37.8030), (-122.3945, 37.7955),
      (-122.3900, 37.7905), (-122.3880, 37.7815), (-122.3890, 37.7765)]),
    ("ferry-oakland", "Le ferry d'Alameda et d'Oakland",
     [(-122.3935, 37.7955), (-122.360, 37.801), (-122.330, 37.799), (-122.312, 37.800)]),
    ("ferry-sausalito", "Le ferry de Sausalito et de Larkspur",
     [(-122.3935, 37.7955), (-122.420, 37.818), (-122.455, 37.838), (-122.480, 37.855)]),
]

# Les LIEUX de l'etat (etat/lieux.json) : un point, un nom, cliquable. Un lieu
# de l'etat sans coordonnee ici n'existe pas sur la table — rien n'echoue, il
# manque, c'est tout. Les bourgs ne sont que des reperes, sans fiche.
# CANON = l'adresse ou le quartier est dit dans la serie ; sinon INVENTE.
LIEUX = {
    "san-francisco": (-122.4190, 37.7850),
    "prescott-street": (-122.4365, 37.7900),   # canon : 1329 Prescott Street (rue fictive)
    "p3": (-122.4010, 37.7790),                # invente : SoMa
    "appartement-cole": (-122.3995, 37.7935),  # invente : le quartier des affaires
    "appartement-paige": (-122.4200, 37.7600), # invente : la Mission
    "services-sociaux": (-122.4080, 37.7765),  # invente : SoMa, Howard Street
    "commissariat": (-122.4040, 37.7752),      # le Hall of Justice, 850 Bryant (le vrai QG de 2001)
    "maison-darryl": (-122.4820, 37.7560),     # invente : une maison du Sunset
    "bay-mirror": (-122.4055, 37.7835),        # invente : Mission Street, pres de la 5e rue
    "hopital": (-122.4050, 37.7555),           # invente : Potrero Avenue
    "golden-gate": (-122.4787, 37.8255),       # canon : le sommet d'un pilier du pont
    "cimetiere": (-122.4560, 37.6830),         # invente : Colma, ou San Francisco enterre ses morts
    "salon-de-la-glaneuse": (-122.4185, 37.8010),  # invente : Russian Hill
    "planque-ezra": (-122.4330, 37.7505),      # invente : Noe Valley
    "domicile-cowan": (-122.4150, 37.7410),    # invente : Bernal Heights
    "domicile-gil": (-122.4310, 37.7720),      # invente : Lower Haight
}

BOURGS = [
    ("cliff-house", "Cliff House", (-122.5137, 37.7785)),
    ("fort-point", "Fort Point", (-122.4770, 37.8105)),
    ("crissy-field", "Crissy Field", (-122.4620, 37.8040)),
    ("fort-mason", "Fort Mason", (-122.4300, 37.8060)),
    ("wharf", "Fisherman's Wharf", (-122.4165, 37.8080)),
    ("coit-tower", "Coit Tower", (-122.4058, 37.8024)),
    ("ferry-building", "Ferry Building", (-122.3940, 37.7955)),
    ("chinatown", "Chinatown", (-122.4065, 37.7940)),
    ("union-square", "Union Square", (-122.4075, 37.7880)),
    ("civic-center", "Civic Center", (-122.4180, 37.7790)),
    ("pac-bell-park", "Pac Bell Park", (-122.3893, 37.7786)),
    ("haight", "Haight-Ashbury", (-122.4470, 37.7700)),
    ("castro", "Le Castro", (-122.4350, 37.7620)),
    ("twin-peaks", "Twin Peaks", (-122.4475, 37.7535)),
    ("candlestick", "Candlestick Park", (-122.3860, 37.7135)),
    ("lake-merced", "Lac Merced", (-122.4850, 37.7255)),
    ("yerba-buena", "Île Yerba Buena", (-122.3660, 37.8100)),
    ("ile-au-tresor", "Île au Trésor", (-122.3705, 37.8240)),
    ("alcatraz", "Alcatraz", (-122.4230, 37.8270)),
    ("angel", "Île aux Anges", (-122.4320, 37.8610)),
    ("sausalito", "Sausalito", (-122.4850, 37.8580)),
    ("berkeley", "Berkeley", (-122.2700, 37.8700)),
    ("oakland", "Oakland", (-122.2700, 37.8050)),
    ("alameda", "Alameda", (-122.2600, 37.7650)),
]

W, H = P(-122.18, 37.68)
geo = {
    "viewBox": "0 0 %s %s" % (W, H), "largeur": W, "hauteur": H,
    "regions": [{"id": i, "nom": n, "court": c, "d": d(p), "etiquette": centre(p)}
                for i, n, c, p in QUARTIERS],
    # Marin et l'East Bay sont de la TERRE : en `fonds` (le lointain), carte.js
    # les peint presque de la teinte de l'eau et la baie n'a plus de rives.
    # Ce qui les distingue de la ville, c'est de n'avoir aucun quartier.
    "fonds": {},
    "lieux": {k: P(*v) for k, v in LIEUX.items()},
    "terre": " ".join([d(VILLE), d(MARIN), d(TIBURON), d(EST)] + [ovale(*v) for v in ILES.values()]),
    "eaux": ovale(-122.485, 37.7255, 3.2, 2.2),
    "relief": {"collines": " ".join(ovale(*c) for c in COLLINES),
               "montagnes": " ".join(ovale(*c) for c in MONTAGNES)},
    "rivieres": "",
    "bourgs": [{"id": i, "nom": n, "p": P(*p)} for i, n, p in BOURGS],
    "routes": [{"id": i, "nom": n, "d": d(p, False)} for i, n, p in ROUTES],
    "cadres": {"baie": "0 0 %s %s" % (W, H),
               "ville": "%s %s 138 115" % tuple(P(-122.522, 37.817))},
}
with open(os.path.join(ICI, "geo.js"), "w", encoding="utf-8") as f:
    f.write("// geo.js — la baie de San Francisco (Charmed, automne 2001), ENGENDRE par dessiner_geo.py\n"
            "// Ne pas editer a la main : retoucher les points du generateur et relancer.\n"
            '"use strict";\nwindow.Geo = ' + json.dumps(geo, ensure_ascii=False) + ";\n")
print("geo.js : %d regions, %d bourgs, %d routes, cadre %sx%s" % (
    len(geo["regions"]), len(geo["bourgs"]), len(geo["routes"]), W, H))
