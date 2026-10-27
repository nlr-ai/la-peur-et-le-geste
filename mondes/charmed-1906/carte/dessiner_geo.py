# -*- coding: utf-8 -*-
"""Dessine la table de Charmed 1906 : la baie de San Francisco, avant le seisme.

    python mondes/charmed-1906/carte/dessiner_geo.py   -> carte/geo.js (a cote)

Meme format que `ecrans/modules/geo.js` (Westeros, engendre du mod AGOT), mais
trace A LA MAIN : des longitudes et latitudes relevees de memoire, projetees a
plat. C'est un croquis juste a quelques centaines de metres pres, pas un releve
— assez pour qu'une distance tranche (la Mission est a une heure de marche de
Prescott Street, Oakland a vingt-cinq minutes de ferry), pas assez pour un
cadastre. On retouche les points ici et on relance, jamais geo.js a la main.

LE RIVAGE EST CELUI DE 1906. Mission Bay est encore une vasiere qui entre
jusqu'a la 7e rue, la Marina n'existe pas (elle sera remblayee pour l'Exposition
de 1915), et les decombres du seisme n'ont pas encore pousse le front de mer
vers l'est. Tout est de la terre ; seule la ville a des quartiers.
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


# ---- la ville : le rivage de 1906, dans le sens des aiguilles ---------------
VILLE = [
    (-122.505, 37.680), (-122.500, 37.705), (-122.503, 37.720), (-122.508, 37.745),
    (-122.511, 37.765), (-122.513, 37.776), (-122.514, 37.781), (-122.507, 37.788),
    (-122.494, 37.789), (-122.484, 37.794), (-122.479, 37.804), (-122.477, 37.811),
    (-122.466, 37.806), (-122.450, 37.804), (-122.437, 37.806), (-122.430, 37.809),
    (-122.422, 37.808), (-122.413, 37.809), (-122.404, 37.807), (-122.399, 37.804),
    (-122.395, 37.798), (-122.393, 37.795), (-122.389, 37.790), (-122.388, 37.786),
    (-122.392, 37.781), (-122.400, 37.776), (-122.404, 37.772), (-122.397, 37.769),
    (-122.389, 37.766), (-122.383, 37.761), (-122.384, 37.751), (-122.388, 37.745),
    (-122.395, 37.742), (-122.386, 37.737), (-122.372, 37.733), (-122.362, 37.729),
    (-122.369, 37.720), (-122.379, 37.713), (-122.380, 37.706), (-122.388, 37.696),
    (-122.392, 37.680),
]
ILES = {
    "yerba-buena": (-122.366, 37.810, 5.2, 4.2),
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
EST = [
    (-122.335, 37.920), (-122.315, 37.895), (-122.305, 37.870), (-122.298, 37.845),
    (-122.302, 37.826), (-122.296, 37.812), (-122.280, 37.800), (-122.300, 37.787),
    (-122.285, 37.772), (-122.258, 37.763), (-122.240, 37.748), (-122.215, 37.742),
    (-122.200, 37.728), (-122.192, 37.705), (-122.180, 37.680), (-122.180, 37.920),
]

# ---- les quartiers ---------------------------------------------------------
QUARTIERS = [
    ("presidio", "Le Presidio", "Presidio", [
        (-122.484, 37.794), (-122.479, 37.804), (-122.477, 37.811), (-122.466, 37.806),
        (-122.447, 37.804), (-122.447, 37.791), (-122.459, 37.786), (-122.478, 37.786)]),
    ("richmond", "Les dunes du Richmond", "Richmond", [
        (-122.514, 37.781), (-122.507, 37.788), (-122.494, 37.789), (-122.484, 37.794),
        (-122.478, 37.786), (-122.459, 37.786), (-122.447, 37.791), (-122.447, 37.774),
        (-122.511, 37.774)]),
    ("parc", "Le parc du Golden Gate", "Golden Gate Park", [
        (-122.511, 37.774), (-122.453, 37.774), (-122.453, 37.766), (-122.510, 37.765)]),
    ("sunset", "Les dunes du Sunset", "Sunset", [
        (-122.510, 37.765), (-122.470, 37.766), (-122.462, 37.745), (-122.470, 37.720),
        (-122.503, 37.720), (-122.508, 37.745)]),
    ("western-addition", "Western Addition", "Western Addition", [
        (-122.447, 37.804), (-122.430, 37.809), (-122.422, 37.808), (-122.424, 37.790),
        (-122.421, 37.772), (-122.447, 37.771), (-122.447, 37.791)]),
    ("nord", "North Beach et Chinatown", "North Beach", [
        (-122.422, 37.808), (-122.413, 37.809), (-122.404, 37.807), (-122.399, 37.804),
        (-122.395, 37.798), (-122.400, 37.793), (-122.407, 37.790), (-122.424, 37.790)]),
    ("centre", "Le centre et Nob Hill", "Nob Hill", [
        (-122.395, 37.798), (-122.393, 37.795), (-122.400, 37.793), (-122.407, 37.790),
        (-122.424, 37.790), (-122.421, 37.779), (-122.405, 37.782), (-122.398, 37.789)]),
    ("som", "South of Market", "South of Market", [
        (-122.393, 37.795), (-122.389, 37.790), (-122.388, 37.786), (-122.392, 37.781),
        (-122.400, 37.776), (-122.404, 37.772), (-122.412, 37.768), (-122.421, 37.772),
        (-122.421, 37.779), (-122.405, 37.782), (-122.398, 37.789)]),
    ("mission", "La Mission", "Mission", [
        (-122.404, 37.772), (-122.412, 37.768), (-122.421, 37.772), (-122.447, 37.771),
        (-122.440, 37.745), (-122.425, 37.735), (-122.405, 37.745), (-122.400, 37.760)]),
    ("potrero", "Potrero et Bayview", "Potrero", [
        (-122.404, 37.772), (-122.400, 37.760), (-122.405, 37.745), (-122.425, 37.735),
        (-122.420, 37.715), (-122.380, 37.706), (-122.379, 37.713), (-122.369, 37.720),
        (-122.362, 37.729), (-122.372, 37.733), (-122.386, 37.737), (-122.395, 37.742),
        (-122.388, 37.745), (-122.384, 37.751), (-122.383, 37.761), (-122.389, 37.766),
        (-122.397, 37.769)]),
]

# ---- le relief : les collines de la ville, les crêtes d'en face ------------
COLLINES = [
    (-122.4475, 37.7535, 7, 5), (-122.453, 37.739, 5, 4), (-122.4135, 37.7925, 3.2, 2.4),
    (-122.418, 37.801, 3, 2.4), (-122.4055, 37.8025, 2.2, 1.8), (-122.3935, 37.786, 1.8, 1.4),
    (-122.401, 37.758, 3.6, 2.4), (-122.415, 37.743, 3, 2.4), (-122.458, 37.763, 3, 2),
    (-122.437, 37.784, 2.6, 1.8),
]
MONTAGNES = [
    (-122.245, 37.880, 9, 18), (-122.215, 37.835, 8, 16), (-122.195, 37.795, 7, 14),
    (-122.540, 37.860, 12, 10), (-122.505, 37.875, 8, 8), (-122.425, 37.862, 5, 5),
]

# ---- les grandes voies, et les ferries qui sont les vraies routes -----------
ROUTES = [
    ("market", "Market Street", [(-122.3935, 37.7955), (-122.405, 37.7865),
                                 (-122.419, 37.7755), (-122.4285, 37.768), (-122.435, 37.7625)]),
    ("van-ness", "Van Ness Avenue", [(-122.4235, 37.8065), (-122.4205, 37.7795), (-122.419, 37.7725)]),
    ("mission-road", "Mission Street et la route de San José",
     [(-122.419, 37.7725), (-122.4195, 37.760), (-122.4225, 37.738), (-122.433, 37.718), (-122.440, 37.690)]),
    ("point-lobos", "Point Lobos Avenue", [(-122.4205, 37.7855), (-122.447, 37.782),
                                           (-122.480, 37.7805), (-122.510, 37.780)]),
    ("ferry-oakland", "Le ferry d'Oakland", [(-122.3935, 37.7955), (-122.360, 37.803), (-122.320, 37.812)]),
    ("ferry-sausalito", "Le ferry de Sausalito", [(-122.3935, 37.7955), (-122.420, 37.818),
                                                  (-122.455, 37.838), (-122.480, 37.855)]),
]

# Les LIEUX de l'etat (etat/lieux.json) : un point, un nom, cliquable. Un lieu
# de l'etat sans coordonnee ici n'existe pas sur la table — rien n'echoue, il
# manque, c'est tout. Les bourgs ne sont que des reperes, sans fiche.
LIEUX = {
    "san-francisco": (-122.4190, 37.7850),
    "prescott-street": (-122.4365, 37.7900),
    "van-ness": (-122.4225, 37.7950),
    "chinatown": (-122.4065, 37.7950),
    "barbary-coast": (-122.4025, 37.7985),
    "call-building": (-122.4035, 37.7870),
    "ferry-building": (-122.3935, 37.7955),
    "city-hall": (-122.4175, 37.7795),
    "nob-hill": (-122.4135, 37.7925),
    "mission-dolores": (-122.4269, 37.7644),
    "presidio": (-122.4600, 37.7980),
    "golden-gate-park": (-122.4700, 37.7695),
    "oakland": (-122.2700, 37.8050),
    "howard-street": (-122.4050, 37.7810),
    # les bonnes adresses
    "pharmacie-keane": (-122.4330, 37.7885),
    "laurel-hill": (-122.4520, 37.7860),
    "serre-golden-gate": (-122.4600, 37.7720),
    "california-market": (-122.4030, 37.7925),
    "old-st-mary": (-122.4058, 37.7930),
    "st-patrick": (-122.4025, 37.7855),
    "librairie-pell": (-122.4040, 37.7900),
    "epicerie-lucchesi": (-122.4085, 37.7995),
    "chandlerie-olsen": (-122.3975, 37.7990),
}

BOURGS = [
    ("cliff-house", "Cliff House", (-122.5137, 37.7785)),
    ("fort-point", "Fort Point", (-122.4770, 37.8105)),
    ("twin-peaks", "Twin Peaks", (-122.4475, 37.7535)),
    ("lake-merced", "Lac Merced", (-122.4850, 37.7255)),
    ("yerba-buena", "Île Yerba Buena", (-122.3660, 37.8100)),
    ("alcatraz", "Alcatraz", (-122.4230, 37.8270)),
    ("angel", "Île aux Anges", (-122.4320, 37.8610)),
    ("sausalito", "Sausalito", (-122.4850, 37.8580)),
    ("berkeley", "Berkeley", (-122.2700, 37.8700)),
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
    f.write("// geo.js — la baie de San Francisco en 1906, ENGENDRE par dessiner_geo.py\n"
            "// Ne pas editer a la main : retoucher les points du generateur et relancer.\n"
            '"use strict";\nwindow.Geo = ' + json.dumps(geo, ensure_ascii=False) + ";\n")
print("geo.js : %d regions, %d bourgs, %d routes, cadre %sx%s" % (
    len(geo["regions"]), len(geo["bourgs"]), len(geo["routes"]), W, H))
