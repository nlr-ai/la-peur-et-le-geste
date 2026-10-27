# -*- coding: utf-8 -*-
"""Dessine la table de Lyon 1943 : la France occupee, vue de haut.

    python mondes/lyon-1943/carte/dessiner_geo.py   -> carte/geo.js (a cote)

Meme format que `ecrans/modules/geo.js` (Westeros) et que la table de Navarre
1572 : `window.Geo`, servi a la place de Westeros par `serveur/routes/geo.js`.
On retouche ICI et on relance, jamais geo.js a la main.

LA SOURCE : des longitudes et latitudes reelles, relevees a la main pour les
cotes, les frontieres, le Rhone et la Saone, et pour les villes. Projection
equirectangulaire corrigee du cosinus de 46,5 degres : juste a quelques
kilometres pres, ce qui suffit a une table de guerre.

CE QUI EST FONDE
  - la position des villes, des cotes, du Rhone et de la Saone ;
  - le sud de l'Angleterre (Londres dans le cadre, au bord nord) et la Corse ;
  - les quatre regions de mars 1943, a gros traits :
      zone-sud       la France entiere en fond : l'ancienne zone libre, occupee
                     par les Allemands depuis le 11 novembre 1942 ;
      zone-nord      la zone occupee depuis juin 1940, cote atlantique comprise ;
      zone-italienne a l'est du Rhone (Savoie, Dauphine, Provence orientale,
                     Corse), de novembre 1942 a septembre 1943 ; Lyon, la
                     vallee du Rhone et Marseille restent aux Allemands ;
      alsace-moselle annexee de fait au Reich.
  - l'ancienne ligne de demarcation, en trait (servie dans `routes`, seul
    format de trait que la page connait) : de la frontiere suisse pres de
    Geneve par Dole, Chalon, Paray, Moulins, Vierzon, Loches, l'est
    d'Angouleme, Libourne, Langon et Mont-de-Marsan jusqu'a Saint-Jean-Pied-de-Port.

CE QUI EST SCHEMATIQUE, ET DECLARE COMME TEL
  - le trace fin de toutes les frontieres et de la ligne entre ces points ;
  - la limite exacte de la zone italienne (qui a bouge plusieurs fois) ;
  - le relief (Alpes, Jura, Massif central, Pyrenees, Vosges) : des ombres
    sans valeur de mesure ;
  - pas de routes : les chemins de Lyon vivent dans etat/chemins.json.
"""
import json
import math
import os

ICI = os.path.dirname(os.path.abspath(__file__))

LON0, LON1, LAT0, LAT1 = -6.0, 10.0, 41.3, 51.8
COS = math.cos(math.radians(46.5))
W = 500.0
K = W / ((LON1 - LON0) * COS)
H = round((LAT1 - LAT0) * K, 1)


def r1(v):
    return round(v, 1)


def P(lon, lat):
    return (r1((lon - LON0) * COS * K), r1((LAT1 - lat) * K))


def chemin(pts, ferme=True):
    pts = [P(*p) for p in pts]
    d = "M%s,%s " % pts[0] + " ".join("L%s,%s" % p for p in pts[1:])
    return d + (" Z" if ferme else "")


def aire(pts):
    """Aire signee (en lon/lat) : son signe dit le sens du trace."""
    return sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(pts, pts[1:] + pts[:1])) / 2


def ruban(pts, l0, l1):
    """Un fleuve en ruban ferme, de la source (l0) a l'embouchure (l1)."""
    q = [P(*p) for p in pts]
    g, d = [], []
    n = len(q)
    for i, (x, y) in enumerate(q):
        a, b = q[max(i - 1, 0)], q[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        m = math.hypot(dx, dy) or 1
        w = (l0 + (l1 - l0) * i / (n - 1)) / 2
        g.append((r1(x - dy / m * w), r1(y + dx / m * w)))
        d.append((r1(x + dy / m * w), r1(y - dx / m * w)))
    tout = g + d[::-1]
    return "M%s,%s " % tout[0] + " ".join("L%s,%s" % p for p in tout[1:]) + " Z"


def ovale(lon, lat, rx, ry):
    x, y = P(lon, lat)
    return "M%s,%s a%s,%s 0 1 0 %s,0 a%s,%s 0 1 0 %s,0 Z" % (
        r1(x - rx), y, rx, ry, r1(2 * rx), rx, ry, r1(-2 * rx))


# ---- les cotes francaises, de Bray-Dunes a Hendaye ---------------------------
COTE_OUEST = [
    (2.55, 51.09), (2.37, 51.04), (1.86, 50.95), (1.6, 50.73), (1.6, 50.2),
    (1.08, 49.93), (0.37, 49.76), (0.1, 49.49), (0.23, 49.42), (-0.3, 49.32),
    (-1.26, 49.67), (-1.62, 49.65), (-1.94, 49.72), (-1.6, 48.84), (-1.5, 48.64),
    (-2.0, 48.65), (-2.76, 48.52), (-3.44, 48.82), (-3.98, 48.73), (-4.77, 48.36),
    (-4.73, 48.04), (-4.37, 47.8), (-3.37, 47.75), (-3.12, 47.48), (-2.5, 47.3),
    (-2.2, 47.27), (-2.25, 47.0), (-1.78, 46.5), (-1.15, 46.16), (-1.0, 45.95),
    (-1.03, 45.62), (-1.07, 45.57), (-1.2, 44.65), (-1.43, 43.65), (-1.56, 43.48),
    (-1.78, 43.37),
]
# les Pyrenees, d'Hendaye a Cerbere
PYRENEES = [
    (-1.78, 43.37), (-1.4, 43.05), (-0.75, 42.95), (0.0, 42.7), (0.7, 42.75),
    (1.45, 42.6), (1.75, 42.5), (2.5, 42.35), (3.17, 42.43),
]
# la Mediterranee, de Cerbere a Menton
COTE_MIDI = [
    (3.17, 42.43), (3.03, 42.53), (3.05, 42.9), (3.47, 43.28), (3.7, 43.4),
    (4.19, 43.53), (4.6, 43.4), (5.0, 43.35), (5.37, 43.3), (5.6, 43.17),
    (5.93, 43.1), (6.4, 43.15), (6.64, 43.27), (6.95, 43.55), (7.27, 43.7),
    (7.53, 43.78),
]
# les Alpes, de Menton a Geneve (frontiere italienne puis suisse)
ALPES = [
    (7.53, 43.78), (7.7, 44.15), (6.95, 44.4), (6.85, 44.85), (6.65, 45.0),
    (7.15, 45.25), (6.8, 45.65), (7.04, 45.92), (6.8, 46.4), (6.2, 46.25),
    (5.97, 46.2),
]
# de Geneve a Bray-Dunes : Jura, Rhin, Lorraine, Luxembourg, Belgique
EST_NORD = [
    (5.97, 46.2), (6.1, 46.45), (6.45, 46.95), (7.0, 47.45), (7.55, 47.58),
    (7.6, 48.1), (7.8, 48.6), (8.2, 48.97), (7.6, 49.08), (7.0, 49.15),
    (6.37, 49.47), (6.13, 49.47), (5.8, 49.55), (5.4, 49.6), (4.85, 49.9),
    (4.83, 50.14), (4.15, 50.3), (3.2, 50.75), (2.55, 51.09),
]

FRANCE = COTE_OUEST[:-1] + PYRENEES[:-1] + COTE_MIDI[:-1] + ALPES[:-1] + EST_NORD[:-1]

# ---- l'ancienne ligne de demarcation (juin 1940 - novembre 1942) ------------
# de Saint-Jean-Pied-de-Port a la frontiere suisse ; schematique entre ces points
LIGNE = [
    (-1.25, 43.08), (-1.0, 43.35), (-0.6, 43.65), (-0.45, 43.95), (-0.25, 44.5),
    (-0.15, 44.95), (0.3, 45.6), (0.7, 46.05), (0.95, 46.6), (1.0, 47.13),
    (2.07, 47.22), (2.6, 46.85), (3.33, 46.57), (4.12, 46.45), (4.85, 46.78),
    (5.25, 46.95), (5.49, 47.09), (5.75, 46.75), (5.85, 46.4), (5.97, 46.2),
]
# la zone nord : la cote de Bray-Dunes a Hendaye, un bout de Pyrenees, la
# ligne, puis la frontiere de Geneve a la mer du Nord
ZONE_NORD = COTE_OUEST + [(-1.4, 43.05)] + LIGNE + EST_NORD[1:-1]

# ---- l'Alsace-Moselle annexee de fait --------------------------------------
ALSACE_MOSELLE = [
    (7.55, 47.58), (7.6, 48.1), (7.8, 48.6), (8.2, 48.97), (7.6, 49.08),
    (7.0, 49.15), (6.37, 49.47), (6.13, 49.47), (5.95, 49.35), (5.95, 49.05),
    (6.3, 48.85), (6.75, 48.55), (7.1, 48.45), (7.05, 48.05), (6.85, 47.82),
    (7.0, 47.6), (7.15, 47.48),
]

# ---- la zone italienne (novembre 1942 - septembre 1943) ---------------------
# a l'est du Rhone : Lyon, la vallee et Marseille restent hors d'elle ; la
# limite occidentale suit le Rhone a quelques lieues a l'est, schematiquement
ZONE_ITALIENNE = (
    [(5.82, 46.12), (5.75, 45.65), (5.4, 45.6), (5.1, 45.45), (5.0, 45.1),
     (4.95, 44.75), (5.0, 44.3), (5.05, 43.9), (5.3, 43.6), (5.6, 43.17)]
    + COTE_MIDI[COTE_MIDI.index((5.93, 43.1)):]
    + ALPES[1:-1] + [(5.97, 46.2)]
)
CORSE = [
    (9.45, 43.0), (9.35, 42.7), (9.55, 42.4), (9.4, 41.95), (9.25, 41.45),
    (9.1, 41.38), (8.8, 41.55), (8.65, 41.85), (8.6, 42.1), (8.7, 42.4),
    (9.0, 42.65), (9.3, 42.7),
]

FOND = [(LON0 - 2, LAT1 + 2), (LON1 + 2, LAT1 + 2), (LON1 + 2, LAT0 - 2), (LON0 - 2, LAT0 - 2)]

REGIONS = [
    {"id": "etranger", "nom": "Les pays d'alentour", "court": "Ailleurs",
     "d": chemin(FOND), "etiquette": None},
    {"id": "zone-sud", "nom": "La zone sud, occupee depuis le 11 novembre 1942",
     "court": "Zone sud", "d": chemin(FRANCE), "etiquette": list(P(2.2, 44.6))},
    {"id": "zone-nord", "nom": "La zone nord, occupee depuis 1940",
     "court": "Zone nord", "d": chemin(ZONE_NORD), "etiquette": list(P(0.4, 47.9))},
    {"id": "alsace-moselle", "nom": "L'Alsace-Moselle, annexee de fait au Reich",
     "court": "Alsace-Moselle", "d": chemin(ALSACE_MOSELLE), "etiquette": list(P(7.25, 48.9))},
    {"id": "zone-italienne", "nom": "La zone d'occupation italienne",
     "court": "Zone italienne", "d": chemin(ZONE_ITALIENNE) + " " + chemin(CORSE),
     "etiquette": list(P(6.3, 44.3))},
]

# ---- les eaux ---------------------------------------------------------------
# la mer de l'ouest : de la Cornouailles a la Flandre, puis la cote francaise
# vers le sud, la cote cantabrique, et le bord de la table
MER_OUEST = (
    [(-6.2, 50.06), (-5.7, 50.06), (-5.2, 49.96), (-4.14, 50.37), (-3.64, 50.22),
     (-2.45, 50.6), (-1.1, 50.78), (-0.14, 50.82), (1.3, 51.13), (1.45, 51.38),
     (0.9, 51.45), (0.7, 51.55), (1.1, 51.78), (1.6, 52.0), (4.2, 52.0),
     (3.6, 51.4), (2.92, 51.23)]
    + COTE_OUEST
    + [(-1.98, 43.32), (-2.93, 43.26), (-3.8, 43.46), (-5.66, 43.54), (-6.2, 43.54)]
)
MER_MIDI = (
    [(0.8, 41.1), (1.25, 41.12), (2.17, 41.38), (2.8, 41.65), (3.2, 41.9), (3.32, 42.32)]
    + COTE_MIDI[1:]
    + [(7.8, 43.82), (8.25, 43.95), (8.8, 44.4), (9.5, 44.1), (10.0, 44.0),
       (10.2, 43.9), (10.2, 41.1)]
)
# la Corse, trou dans la mer : trace en sens contraire de la mer
CORSE_TROU = CORSE if aire(CORSE) * aire(MER_MIDI) < 0 else CORSE[::-1]
LEMAN = ovale(6.5, 46.43, 9, 2.2)

EAUX = " ".join([chemin(MER_OUEST), chemin(MER_MIDI), chemin(CORSE_TROU), LEMAN])

SAONE = [(5.9, 47.95), (5.6, 47.6), (5.3, 47.2), (5.0, 47.0), (4.85, 46.78),
         (4.9, 46.55), (4.83, 46.31), (4.8, 46.0), (4.83, 45.76)]
RHONE = [(5.97, 46.2), (5.82, 46.1), (5.75, 45.8), (5.55, 45.8), (5.2, 45.82),
         (4.98, 45.8), (4.83, 45.76), (4.82, 45.5), (4.85, 45.2), (4.89, 44.93),
         (4.75, 44.4), (4.81, 43.95), (4.63, 43.68), (4.7, 43.42)]
SEINE = [(4.57, 47.86), (4.07, 48.3), (2.95, 48.38), (2.66, 48.54), (2.35, 48.86),
         (1.95, 48.98), (1.5, 49.1), (1.1, 49.44), (0.6, 49.42), (0.2, 49.45)]
LOIRE = [(4.0, 45.0), (4.07, 46.04), (3.16, 46.99), (2.63, 47.69), (1.91, 47.9),
         (1.33, 47.59), (0.69, 47.39), (-0.55, 47.42), (-1.55, 47.22), (-2.2, 47.27)]
ALLIER = [(3.6, 44.7), (3.4, 45.4), (3.43, 46.13), (3.33, 46.57), (3.1, 46.97)]
GARONNE = [(1.44, 43.6), (0.62, 44.2), (-0.58, 44.84), (-0.7, 45.25), (-1.07, 45.57)]
ISERE = [(6.6, 45.6), (6.0, 45.5), (5.72, 45.19), (5.3, 45.1), (4.89, 44.98)]
TAMISE = [(-1.0, 51.6), (-0.13, 51.5), (0.7, 51.48)]

RIVIERES = " ".join([
    ruban(SAONE, .9, 2.6), ruban(RHONE, 1.0, 3.2),
    ruban(SEINE, .7, 2.2), ruban(LOIRE, .7, 2.6), ruban(ALLIER, .5, 1.2),
    ruban(GARONNE, .9, 3.6), ruban(ISERE, .5, 1.3), ruban(TAMISE, .6, 1.6),
])

# ---- les lieux de etat/lieux.json, et les bourgs ----------------------------
LIEUX = {i: list(P(*c)) for i, c in {
    "lyon": (4.835, 45.76), "vichy": (3.43, 46.13), "macon": (4.83, 46.31),
    "chalon-sur-saone": (4.85, 46.78), "dijon": (5.04, 47.32),
    "oyonnax": (5.66, 46.26), "vercors": (5.45, 45.02),
    "marseille": (5.37, 43.3), "paris": (2.35, 48.86), "londres": (-0.13, 51.5),
}.items()}

BOURGS_LL = [
    ("grenoble", "Grenoble", 5.72, 45.19), ("saint-etienne", "Saint-Étienne", 4.39, 45.44),
    ("valence", "Valence", 4.89, 44.93), ("avignon", "Avignon", 4.81, 43.95),
    ("bourg-en-bresse", "Bourg-en-Bresse", 5.23, 46.2), ("nantua", "Nantua", 5.61, 46.15),
    ("annecy", "Annecy", 6.13, 45.9), ("chambery", "Chambéry", 5.92, 45.57),
    ("geneve", "Genève", 6.14, 46.2), ("romans", "Romans", 5.05, 45.04),
    ("clermont-ferrand", "Clermont-Ferrand", 3.08, 45.78), ("moulins", "Moulins", 3.33, 46.57),
    ("roanne", "Roanne", 4.07, 46.04), ("besancon", "Besançon", 6.02, 47.24),
    ("toulouse", "Toulouse", 1.44, 43.6), ("bordeaux", "Bordeaux", -0.58, 44.84),
    ("limoges", "Limoges", 1.26, 45.83), ("montpellier", "Montpellier", 3.88, 43.61),
    ("toulon", "Toulon", 5.93, 43.12), ("nice", "Nice", 7.27, 43.7),
    ("strasbourg", "Strasbourg", 7.75, 48.58), ("metz", "Metz", 6.18, 49.12),
    ("lille", "Lille", 3.06, 50.63), ("rouen", "Rouen", 1.1, 49.44),
    ("nantes", "Nantes", -1.55, 47.22), ("tours", "Tours", 0.69, 47.39),
    ("bourges", "Bourges", 2.4, 47.08), ("turin", "Turin", 7.68, 45.07),
    ("ajaccio", "Ajaccio", 8.74, 41.93), ("douvres", "Douvres", 1.31, 51.13),
]
BOURGS = [{"id": i, "nom": n, "p": list(P(lo, la))} for i, n, lo, la in BOURGS_LL]

MONTAGNES = " ".join([
    ovale(6.6, 45.3, 14, 34), ovale(7.0, 44.3, 12, 14),            # Alpes
    ovale(-0.6, 42.85, 30, 7), ovale(1.4, 42.7, 26, 6),            # Pyrenees
    ovale(9.05, 42.2, 5, 14),                                      # Corse
])
COLLINES = " ".join([
    ovale(2.9, 45.3, 24, 22),                                      # Massif central
    ovale(5.9, 46.6, 8, 20),                                       # Jura
    ovale(5.45, 45.0, 6, 9),                                       # le Vercors
    ovale(6.95, 48.2, 7, 18),                                      # Vosges
])

geo = {
    "viewBox": "0 0 %s %s" % (W, H), "largeur": W, "hauteur": H,
    "regions": REGIONS,
    "fonds": {},
    "lieux": LIEUX,
    "terre": chemin(FOND),
    "eaux": EAUX,
    "relief": {"collines": COLLINES, "montagnes": MONTAGNES},
    "rivieres": RIVIERES,
    "bourgs": BOURGS,
    "routes": [
        {"id": "ligne-de-demarcation",
         "nom": "L'ancienne ligne de demarcation (1940-1942)",
         "d": chemin(LIGNE, ferme=False)},
    ],
}

RATIO = 1.2


def boite(ids, marge):
    xs = [LIEUX[i][0] for i in ids]
    ys = [LIEUX[i][1] for i in ids]
    x0, x1, y0, y1 = min(xs) - marge, max(xs) + marge, min(ys) - marge, max(ys) + marge
    l, h = x1 - x0, y1 - y0
    if l / h < RATIO:
        n = h * RATIO
        x0 -= (n - l) / 2
        l = n
    else:
        n = l / RATIO
        y0 -= (n - h) / 2
        h = n
    return "%s %s %s %s" % (r1(x0), r1(y0), r1(l), r1(h))


geo["cadres"] = {
    "france": "0 0 %s %s" % (W, H),
    "region-lyonnaise": boite(["lyon", "macon", "chalon-sur-saone", "oyonnax",
                               "vercors", "vichy"], 14),
}

with open(os.path.join(ICI, "geo.js"), "w", encoding="utf-8") as f:
    f.write("// geo.js — la France occupee en mars 1943, ENGENDRE par dessiner_geo.py\n"
            "// Ne pas editer a la main : retoucher le generateur et relancer.\n"
            "// Projection equirectangulaire (cos 46,5). Frontieres, zones et relief : schematiques.\n"
            '"use strict";\nwindow.Geo = ' + json.dumps(geo, ensure_ascii=False) + ";\n")
print("geo.js : %d lieux, %d bourgs, table %sx%s, region-lyonnaise %s" % (
    len(LIEUX), len(BOURGS), W, H, geo["cadres"]["region-lyonnaise"]))
for nom, ll in [("Manche", (-2.6, 49.95)), ("Ocean", (-4.5, 46.0)),
                ("Mediterranee", (6.0, 42.4)), ("Mer du Nord", (2.6, 51.6))]:
    print("mer", nom, P(*ll))
