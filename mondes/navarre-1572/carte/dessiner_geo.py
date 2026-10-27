# -*- coding: utf-8 -*-
"""Dessine la table de Navarre 1572 : le royaume de France, vu de haut.

    python mondes/navarre-1572/carte/dessiner_geo.py   -> carte/geo.js (a cote)

Meme format que `ecrans/modules/geo.js` (Westeros) et que les tables de
Charmed 1906 et de Vampire Counts : `window.Geo`, servi a la place de Westeros
par `serveur/routes/geo.js`. On retouche ICI et on relance, jamais geo.js a la
main.

LA SOURCE : des longitudes et latitudes reelles, relevees a la main pour une
soixantaine de points de cote, de frontiere et de cours d'eau, et pour les
villes. Projection equirectangulaire corrigee du cosinus de 46,5 degres :
juste a quelques lieues pres, ce qui suffit a une table de conseil.

CE QUI EST FONDE
  - la position des villes, des cotes et des grands fleuves (Seine, Loire,
    Garonne, Rhone et Saone) ;
  - la frontiere du royaume EN 1572, a gros traits : Calais francais, Gravelines
    et l'Artois espagnols ; Metz, Toul et Verdun sous protection francaise
    depuis 1552 ; la Franche-Comte espagnole ; la Bresse et Nice savoyardes ; le
    Roussillon espagnol. Le Bearn et la Basse-Navarre, souverains, a part.

CE QUI EST SCHEMATIQUE, ET DECLARE COMME TEL
  - le trace fin de la frontiere entre ces points ;
  - le relief (Pyrenees, Alpes, Massif central, Vosges) : des ombres sans
    valeur de mesure ;
  - pas de routes : les chemins de Paris vivent dans etat/chemins.json.
"""
import json
import math
import os

ICI = os.path.dirname(os.path.abspath(__file__))

LON0, LON1, LAT0, LAT1 = -6.0, 8.6, 41.0, 51.6
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


# ---- les cotes francaises, de Gravelines a Hendaye ---------------------------
COTE_OUEST = [
    (2.12, 51.0), (1.86, 50.95), (1.6, 50.73), (1.6, 50.2), (1.08, 49.93),
    (0.37, 49.76), (0.1, 49.49), (0.23, 49.42), (-0.3, 49.32), (-1.26, 49.67),
    (-1.62, 49.65), (-1.94, 49.72), (-1.6, 48.84), (-1.5, 48.64), (-2.0, 48.65),
    (-2.76, 48.52), (-3.44, 48.82), (-3.98, 48.73), (-4.77, 48.36), (-4.73, 48.04),
    (-4.37, 47.8), (-3.37, 47.75), (-3.12, 47.48), (-2.5, 47.3), (-2.2, 47.27),
    (-2.25, 47.0), (-1.78, 46.5), (-1.15, 46.16), (-1.0, 45.95), (-1.03, 45.62),
    (-1.07, 45.57), (-1.2, 44.65), (-1.43, 43.65), (-1.56, 43.48), (-1.78, 43.37),
]
# la mer de l'ouest : de la Cornouailles anglaise a la Flandre, puis la cote
# francaise vers le sud, la cote cantabrique, et le bord de la table
MER_OUEST = (
    [(-6.2, 50.06), (-5.7, 50.06), (-5.2, 49.96), (-4.14, 50.37), (-3.64, 50.22),
     (-2.45, 50.6), (-1.1, 50.78), (-0.14, 50.82), (1.3, 51.13), (1.45, 51.38),
     (1.45, 51.8), (3.8, 51.8), (3.6, 51.4), (2.92, 51.23), (2.37, 51.04)]
    + COTE_OUEST
    + [(-1.98, 43.32), (-2.93, 43.26), (-3.8, 43.46), (-5.66, 43.54), (-6.2, 43.54)]
)
MER_MIDI = [
    (0.8, 40.8), (1.25, 41.1), (2.17, 41.38), (2.8, 41.65), (3.2, 41.9), (3.32, 42.32),
    (3.08, 42.53), (3.05, 42.9), (3.47, 43.28), (3.7, 43.4), (4.19, 43.53), (4.6, 43.4),
    (5.0, 43.35), (5.37, 43.3), (5.93, 43.1), (6.64, 43.27), (7.27, 43.7), (7.8, 43.8),
    (8.8, 44.1), (8.8, 40.8),
]

# ---- le royaume en 1572 -----------------------------------------------------
ROYAUME = (
    COTE_OUEST[:-1]
    + [(-1.6, 43.25), (-1.4, 43.5), (-0.4, 43.6), (0.0, 43.3),   # contourne le Bearn
       (0.0, 42.85), (0.7, 42.7), (1.45, 42.6), (1.75, 42.62), (2.2, 42.85),
       (3.0, 42.88), (3.05, 42.9), (3.47, 43.28), (3.7, 43.4), (4.19, 43.53),
       (4.6, 43.4), (5.37, 43.3), (5.93, 43.1), (6.64, 43.27), (7.2, 43.7),
       (6.9, 44.4), (6.6, 45.0), (5.8, 45.3), (5.2, 45.7), (4.9, 46.3), (4.9, 46.6),
       (5.3, 47.0), (5.5, 47.6), (5.7, 48.0), (6.4, 48.6), (6.5, 49.2), (5.8, 49.5),
       (5.0, 49.8), (4.2, 49.95), (3.3, 50.05), (2.4, 50.15), (1.95, 50.45),
       (2.1, 50.85)]
)
BEARN = [(-1.78, 43.37), (-1.4, 43.5), (-0.4, 43.6), (0.0, 43.3), (0.0, 42.85),
         (-0.7, 42.85), (-1.4, 43.05), (-1.6, 43.25)]

REGIONS = [
    {"id": "etranger", "nom": "Les terres d'ailleurs", "court": "Ailleurs",
     "d": chemin([(LON0 - 2, LAT1 + 2), (LON1 + 2, LAT1 + 2), (LON1 + 2, LAT0 - 2), (LON0 - 2, LAT0 - 2)]),
     "etiquette": None},
    {"id": "royaume", "nom": "Le royaume de France", "court": "France",
     "d": chemin(ROYAUME), "etiquette": list(P(2.6, 46.6))},
    {"id": "bearn", "nom": "Le Bearn et la Basse-Navarre", "court": "Bearn",
     "d": chemin(BEARN), "etiquette": list(P(-0.9, 43.15))},
]

# ---- les fleuves -------------------------------------------------------------
SEINE = [(4.57, 47.86), (4.07, 48.3), (2.95, 48.38), (2.66, 48.54), (2.35, 48.86),
         (1.95, 48.98), (1.5, 49.1), (1.1, 49.44), (0.6, 49.42), (0.2, 49.45)]
LOIRE = [(4.0, 45.0), (4.07, 46.04), (3.16, 46.99), (2.63, 47.69), (1.91, 47.9),
         (1.33, 47.59), (0.69, 47.39), (-0.55, 47.42), (-1.55, 47.22), (-2.2, 47.27)]
GARONNE = [(1.44, 43.6), (0.62, 44.2), (-0.58, 44.84), (-0.7, 45.25), (-1.07, 45.57)]
RHONE = [(5.5, 47.6), (4.85, 46.78), (4.84, 45.76), (4.89, 44.93), (4.81, 43.95),
         (4.63, 43.68), (4.7, 43.42)]

EAUX = " ".join([chemin(MER_OUEST), chemin(MER_MIDI)])
RIVIERES = " ".join([ruban(SEINE, .8, 2.4), ruban(LOIRE, .8, 3.0),
                     ruban(GARONNE, 1.0, 4.5), ruban(RHONE, .8, 2.6)])

# ---- les lieux de etat/lieux.json, et les bourgs ----------------------------
LIEUX = {i: list(P(*c)) for i, c in {
    "paris": (2.35, 48.86), "meaux": (2.88, 48.96), "senlis": (2.59, 49.21),
    "chatillon-sur-loing": (2.85, 47.82), "orleans": (1.91, 47.9),
    "joinville": (5.14, 48.44), "la-rochelle": (-1.15, 46.16),
    "nerac": (0.34, 44.14), "pau": (-0.37, 43.3),
}.items()}

BOURGS_LL = [
    ("rouen", "Rouen", 1.1, 49.44), ("lyon", "Lyon", 4.84, 45.76),
    ("bordeaux", "Bordeaux", -0.58, 44.84), ("toulouse", "Toulouse", 1.44, 43.6),
    ("marseille", "Marseille", 5.37, 43.3), ("nantes", "Nantes", -1.55, 47.22),
    ("tours", "Tours", 0.69, 47.39), ("blois", "Blois", 1.33, 47.59),
    ("reims", "Reims", 4.03, 49.26), ("dijon", "Dijon", 5.04, 47.32),
    ("calais", "Calais", 1.86, 50.95), ("montauban", "Montauban", 1.35, 44.02),
    ("poitiers", "Poitiers", 0.34, 46.58), ("angers", "Angers", -0.55, 47.47),
    ("metz", "Metz", 6.18, 49.12), ("rennes", "Rennes", -1.68, 48.11),
    ("bayonne", "Bayonne", -1.47, 43.49), ("nimes", "Nîmes", 4.36, 43.84),
    ("grenoble", "Grenoble", 5.72, 45.19), ("limoges", "Limoges", 1.26, 45.83),
    ("amiens", "Amiens", 2.3, 49.89), ("saint-jean-d-angely", "Saint-Jean-d'Angély", -0.52, 45.95),
    ("jarnac", "Jarnac", -0.17, 45.68), ("montpellier", "Montpellier", 3.88, 43.61),
    ("mons", "Mons", 3.95, 50.45), ("besancon", "Besançon", 6.02, 47.24),
    ("londres", "Londres", -0.13, 51.5),
]
BOURGS = [{"id": i, "nom": n, "p": list(P(lo, la))} for i, n, lo, la in BOURGS_LL]

MONTAGNES = " ".join([
    ovale(-0.6, 42.75, 34, 9), ovale(1.4, 42.65, 30, 8),           # Pyrenees
    ovale(6.6, 45.2, 14, 34), ovale(7.3, 44.3, 12, 16),            # Alpes
    ovale(2.9, 45.3, 26, 22),                                      # Massif central
])
COLLINES = " ".join([ovale(6.9, 48.2, 9, 22), ovale(4.6, 47.5, 16, 8), ovale(-3.3, 48.2, 18, 8)])

geo = {
    "viewBox": "0 0 %s %s" % (W, H), "largeur": W, "hauteur": H,
    "regions": REGIONS,
    "fonds": {},
    "lieux": LIEUX,
    "terre": chemin([(LON0 - 2, LAT1 + 2), (LON1 + 2, LAT1 + 2), (LON1 + 2, LAT0 - 2), (LON0 - 2, LAT0 - 2)]),
    "eaux": EAUX,
    "relief": {"collines": COLLINES, "montagnes": MONTAGNES},
    "rivieres": RIVIERES,
    "bourgs": BOURGS,
    "routes": [],
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
    "royaume": "0 0 %s %s" % (W, H),
    "ile-de-france": boite(["paris", "meaux", "senlis", "chatillon-sur-loing", "orleans"], 20),
}

with open(os.path.join(ICI, "geo.js"), "w", encoding="utf-8") as f:
    f.write("// geo.js — le royaume de France en 1572, ENGENDRE par dessiner_geo.py\n"
            "// Ne pas editer a la main : retoucher le generateur et relancer.\n"
            "// Projection equirectangulaire (cos 46,5). Frontieres et relief : schematiques.\n"
            '"use strict";\nwindow.Geo = ' + json.dumps(geo, ensure_ascii=False) + ";\n")
print("geo.js : %d lieux, %d bourgs, table %sx%s, ile-de-france %s" % (
    len(LIEUX), len(BOURGS), W, H, geo["cadres"]["ile-de-france"]))
