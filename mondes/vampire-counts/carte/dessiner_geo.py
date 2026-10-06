# -*- coding: utf-8 -*-
"""Dessine la table de Vampire Counts : la Terre des Cinq, vue de haut.

    python mondes/vampire-counts/carte/dessiner_geo.py   -> carte/geo.js (a cote)

Meme format que `ecrans/modules/geo.js` (Westeros) et que la table de
Charmed 1906 : `window.Geo`, servi a la place de Westeros par
`serveur/routes/geo.js`. On retouche ICI et on relance, jamais geo.js a la main.

LA SOURCE : `canon/map.json` (copie du projet Vampire Kings) — 330 villes et
villages poses sur un plan de 2000 x 1400, et 269 lieux anciens types, chacun
avec son `terrain` (LivingForest | Plains). Rien d'autre : la carte d'origine
ne porte ni relief, ni routes, ni trace de riviere. Elle NOMME une riviere, la
Tarnava, sans lui donner un seul point.

L'ECHELLE. Une unite du canon ~ 80 m (manuel.md, canon/LISEZ-MOI.md). Le moteur
de la table est cale sur des cartes de 300 a 600 unites de large (corps de
texte, rayons des points, bannieres sont en unites du cadrage) : on divise donc
les coordonnees par S = 4. Dans geo.js, UNE UNITE = 4 unites canon ~ 320 m.
Rupea-Homorod ~ 19 unites (6 km), Rupea-Sighisoara ~ 160 unites (51 km).

CE QUI EST FONDE SUR LE CANON
  - la position de chaque ville et village (map.json, tel quel, a S pres) ;
  - les forets vivantes : un champ de vote des 269 sites selon leur `terrain`,
    noyau gaussien, puis le contour ou forets et plaines s'equilibrent. C'est
    une interpolation des donnees, pas un releve : la lisiere est juste a
    quelques kilometres pres, loin des sites elle est molle.

CE QUI EST INVENTE, ET DECLARE COMME TEL
  - LE TRACE DE LA TARNAVA. Le canon la nomme sans la tracer. On la fait passer
    par les villes que la Tarnava Mare traverse dans la toponymie reelle dont
    le pays est tire (Odorheiu Secuiesc, Cristuru Secuiesc, Sighisoara,
    Dumbraveni, Medias, Copsa Mica), d'est en ouest ; la source a l'est
    d'Odorheiu et la sortie a l'ouest sont posees a l'oeil. Entre deux villes,
    la courbe est une spline, pas un cours reel.
  - LE RELIEF, schematique : des montagnes au nord-est et a l'est, la ou le
    canon pose ses forteresses de col (Corund, Dealu, Liban, Ocna de Jos,
    Varsag) et au sud-est (Maierus) ; quelques collines entre les villes
    parce que le pays « tient entre des collines et des montagnes »
    (LORE_RECIT §1). Ce sont des ombres, sans valeur de mesure : aucun col,
    aucune ligne de crete n'en decoule.
  - Pas de routes : le canon n'en porte pas (les chemins vivent dans
    etat/chemins.json, hors de cette carte).

PAS DE MER. Tout est de la terre ; le rectangle `terre` deborde le plan de
toutes parts, pour qu'aucun cadrage ne decouvre la mer du moteur.
"""
import json
import math
import os
import re
import unicodedata

ICI = os.path.dirname(os.path.abspath(__file__))
MONDE = os.path.dirname(ICI)
SOURCE = os.path.join(MONDE, "canon", "map.json")
LIEUX_ETAT = os.path.join(MONDE, "etat", "lieux.json")

S = 4.0  # unites canon par unite de geo.js


def r1(v):
    return round(v, 1)


def P(x, y):
    """Canon (2000 x 1400) -> geo.js."""
    return [r1(x / S), r1(y / S)]


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def chemin(pts, ferme=True):
    s = "M" + " L".join("%s,%s" % (r1(x), r1(y)) for x, y in pts)
    return s + (" Z" if ferme else "")


def ovale(x, y, rx, ry):
    """Ovale en unites CANON, rendu en unites geo."""
    x, y, rx, ry = x / S, y / S, rx / S, ry / S
    return "M%s,%s a%s,%s 0 1 0 %s,0 a%s,%s 0 1 0 %s,0 Z" % (
        r1(x - rx), r1(y), r1(rx), r1(ry), r1(2 * rx), r1(rx), r1(ry), r1(-2 * rx))


carte = json.load(open(SOURCE, encoding="utf-8"))
LARG, HAUT = carte["width"], carte["height"]
W, H = r1(LARG / S), r1(HAUT / S)
VILLES = carte["towns"]
SITES = carte["sites"]

# ---- les lieux de l'etat : leur id est le nom de la ville, sans accents ------
# Un lieu de l'etat sans ville du meme nom n'est pas sur la table ; on peut le
# rattacher par `alias` dans etat/lieux.json (un des alias = un slug de ville).
PAR_SLUG = {}
for t in VILLES:
    PAR_SLUG.setdefault(slug(t["name"]), t)
lieux_etat = json.load(open(LIEUX_ETAT, encoding="utf-8"))
LIEUX, PRIS, MANQUE = {}, set(), []
for l in lieux_etat:
    cands = [l["id"]] + list(l.get("alias") or [])
    t = next((PAR_SLUG[c] for c in cands if c in PAR_SLUG), None)
    if t is None:
        MANQUE.append(l["id"])
        continue
    LIEUX[l["id"]] = P(t["x"], t["y"])
    PRIS.add(t["id"])

# ---- les bourgs : toutes les autres villes, eclaircies ----------------------
# A la loupe seulement (carte.js : SEUIL_BOURGS). On garde les bourgs (niveau 2)
# d'abord, puis les villages, et l'on saute un village trop pres d'un nom deja
# pose : 312 hameaux a quelques km les uns des autres feraient une bouillie.
ECART = 7.0  # unites geo (~2,2 km)
poses = [tuple(p) for p in LIEUX.values()]
BOURGS, vus = [], {}
for t in sorted(VILLES, key=lambda t: (t["level"], t["id"])):
    if t["id"] in PRIS:
        continue
    p = P(t["x"], t["y"])
    if t["level"] >= 3 and any(math.hypot(p[0] - a, p[1] - b) < ECART for a, b in poses):
        continue
    i = slug(t["name"])
    if i in vus or i in LIEUX:
        i = "%s-%d" % (i, t["id"])
    vus[i] = 1
    BOURGS.append({"id": i, "nom": t["name"], "p": p})
    poses.append(tuple(p))

# ---- les forets vivantes : vote des sites, contour du champ ------------------
PAS = 20.0     # pas de la grille, canon
SIGMA = 75.0   # portee d'un site, canon (~6 km)
BIAIS = 0.04   # loin de tout site, la plaine l'emporte (le pays laboure)
M = 12         # cellules de marge (> 3 sigma) : la foret s'eteint d'elle-meme hors du plan
nx, ny = int(LARG / PAS) + 1 + 2 * M, int(HAUT / PAS) + 1 + 2 * M


def gx(i):
    return (i - M) * PAS


def gy(j):
    return (j - M) * PAS


champ = [[0.0] * nx for _ in range(ny)]
for j in range(ny):
    for i in range(nx):
        if i == 0 or j == 0 or i == nx - 1 or j == ny - 1:
            champ[j][i] = -1.0            # bordure : ferme les contours
            continue
        x, y = gx(i), gy(j)
        f = 0.0
        for s in SITES:
            d2 = (s["x"] - x) ** 2 + (s["y"] - y) ** 2
            if d2 > 9 * SIGMA * SIGMA:
                continue
            w = math.exp(-d2 / (2 * SIGMA * SIGMA))
            f += w if s["terrain"] == "LivingForest" else -w
        champ[j][i] = f - BIAIS


def marcher(champ):
    """Carres marchants, niveau 0 : segments non orientes (voir `orienter`)."""
    segs = []

    def pt(a, b, va, vb):
        t = va / (va - vb)
        return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

    for j in range(ny - 1):
        for i in range(nx - 1):
            c = [(gx(i), gy(j)), (gx(i + 1), gy(j)), (gx(i + 1), gy(j + 1)), (gx(i), gy(j + 1))]
            v = [champ[j][i], champ[j][i + 1], champ[j + 1][i + 1], champ[j + 1][i]]
            # aretes du carre, dans le sens c0->c1->c2->c3
            croise = []
            for k in range(4):
                a, b = k, (k + 1) % 4
                if (v[a] > 0) != (v[b] > 0):
                    croise.append((k, pt(c[a], c[b], v[a], v[b])))
            if not croise:
                continue
            if len(croise) == 2:
                segs.append((croise[0][1], croise[1][1]))
            else:  # point-selle : on tranche par la valeur au centre
                pts = dict(croise)
                centre = sum(v) / 4
                paires = [(0, 1), (2, 3)] if (centre > 0) == (v[0] > 0) else [(3, 0), (1, 2)]
                for p, q in paires:
                    segs.append((pts[p], pts[q]))
    return segs


def orienter(segs):
    """Oriente chaque segment pour que la foret soit a gauche (verification
    au point milieu, par le champ interpole), puis chaine les segments."""
    def val(x, y):
        i = min(max(x / PAS + M, 0), nx - 1.001)
        j = min(max(y / PAS + M, 0), ny - 1.001)
        i0, j0 = int(i), int(j)
        fx, fy = i - i0, j - j0
        return (champ[j0][i0] * (1 - fx) * (1 - fy) + champ[j0][i0 + 1] * fx * (1 - fy) +
                champ[j0 + 1][i0] * (1 - fx) * fy + champ[j0 + 1][i0 + 1] * fx * fy)

    out = []
    for a, b in segs:
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy) or 1
        # gauche en repere ecran (y vers le bas) : (dy, -dx)
        gxv, gyv = mx + dy / n * 2, my - dx / n * 2
        out.append((a, b) if val(gxv, gyv) > val(mx - dy / n * 2, my + dx / n * 2) else (b, a))
    return out


def chainer(segs):
    cle = lambda p: (round(p[0], 3), round(p[1], 3))
    suivant = {}
    for a, b in segs:
        suivant.setdefault(cle(a), []).append(b)
    boucles = []
    while suivant:
        k0 = next(iter(suivant))
        boucle = [k0]
        k = k0
        while True:
            lst = suivant.get(k)
            if not lst:
                break
            b = lst.pop()
            if not lst:
                del suivant[k]
            k = cle(b)
            if k == k0:
                break
            boucle.append(k)
        if len(boucle) > 3:
            boucles.append(boucle)
    return boucles


def chaikin(pts, n=2):
    for _ in range(n):
        q = []
        for i in range(len(pts)):
            a, b = pts[i], pts[(i + 1) % len(pts)]
            q.append((a[0] * .75 + b[0] * .25, a[1] * .75 + b[1] * .25))
            q.append((a[0] * .25 + b[0] * .75, a[1] * .25 + b[1] * .75))
        pts = q
    return pts


def aire(pts):
    return sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1]
               for i in range(len(pts))) / 2


boucles = [chaikin(b) for b in chainer(orienter(marcher(champ)))]
boucles = [b for b in boucles if abs(aire(b)) > (PAS * 3) ** 2]   # pas de confettis
geo_b = [[(x / S, y / S) for x, y in b] for b in boucles]
# les massifs (contours exterieurs) ont tous le meme signe d'aire ; les
# clairieres (plaine enclose dans la foret) le signe oppose. Remplissage
# `nonzero` : la foret se dessine telle quelle.
signe_foret = 1 if sum(aire(b) for b in geo_b) > 0 else -1


def etiquette_foret():
    """Un point bien dans la foret, DANS le plan, loin des noms (pour le nom)."""
    reperes = list(LIEUX.values()) + [b["p"] for b in BOURGS]
    meilleur, score = None, -1
    for k in range(40 * 28):
        x = 40 + (W - 140) * ((k % 40) + .5) / 40      # le nom part vers la droite
        y = 20 + (H - 40) * ((k // 40) + .5) / 28
        if champ_geo(x, y) <= 0.3:
            continue
        d = min(math.hypot(x - a, y - c) for a, c in reperes)
        if d > score:
            meilleur, score = [r1(x), r1(y)], d
    return meilleur


def champ_geo(x, y):
    i = int(round(x * S / PAS + M))
    j = int(round(y * S / PAS + M))
    if 0 <= i < nx and 0 <= j < ny:
        return champ[j][i]
    return -1


foret_d = " ".join(chemin(b) for b in geo_b)
# Le cadre de la page n'a pas le ratio du plan : un cadrage peut deborder le
# plan, et sous la terre il y a la « mer » du moteur. La terre (et la plaine)
# deborde donc largement le plan — un pays sans mer n'a pas de rivage.
rect = [(-W, -H), (2 * W, -H), (2 * W, 2 * H), (-W, 2 * H)]
if aire(rect) * signe_foret > 0:
    rect = rect[::-1]
plaine_d = chemin(rect) + " " + foret_d
REGIONS = [
    {"id": "plaines", "nom": "Les plaines et les coteaux", "court": "Plaines",
     "d": plaine_d, "etiquette": None},
    {"id": "forets-vivantes", "nom": "Les forêts vivantes", "court": "Forêts vivantes",
     "d": foret_d, "etiquette": etiquette_foret()},
]

# ---- la Tarnava : INVENTEE (voir l'en-tete) -----------------------------------
def ville(nom):
    t = PAR_SLUG[slug(nom)]
    return (t["x"], t["y"])


TARNAVA = [(1880, 430), (1770, 505), ville("Odorheiu Secuiesc"), (1480, 600),
           ville("Cristuru Secuiesc"), (1160, 640), ville("Sighișoara"), (860, 735),
           ville("Dumbrăveni"), (580, 760), ville("Mediaș"), ville("Copșa Mică"),
           (120, 960), (-20, 990)]


def spline(pts, n=8):
    out = []
    q = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(q) - 2):
        p0, p1, p2, p3 = q[i - 1], q[i], q[i + 1], q[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * (2 * p1[c] + (-p0[c] + p2[c]) * t +
                                   (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2 +
                                   (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3) for c in (0, 1)))
    out.append(pts[-1])
    return out


def ruban(pts, l0, l1):
    """Un cours d'eau en ruban ferme (les couches d'eau sont remplies)."""
    g, d = [], []
    n = len(pts)
    for i, (x, y) in enumerate(pts):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        m = math.hypot(dx, dy) or 1
        w = (l0 + (l1 - l0) * i / (n - 1)) / 2
        g.append((x - dy / m * w, y + dx / m * w))
        d.append((x + dy / m * w, y - dx / m * w))
    return chemin([(x / S, y / S) for x, y in g + d[::-1]])


EAUX = ruban(spline(TARNAVA), 2.5, 7.0)

# ---- le relief : SCHEMATIQUE, invente (voir l'en-tete) ------------------------
MONTAGNES = [  # canon : x, y, rx, ry
    (1600, 70, 170, 80), (1830, 120, 190, 110), (1960, 320, 110, 170),
    (1985, 640, 80, 150), (1730, 260, 90, 60), (1890, 1330, 170, 90),
    (1990, 1150, 70, 140),
]
COLLINES = [
    (1250, 900, 120, 60), (1150, 1080, 110, 55), (650, 1000, 120, 55),
    (560, 420, 110, 55), (1200, 420, 130, 60), (870, 520, 100, 50),
    (1750, 900, 110, 70), (300, 1150, 120, 60), (1400, 250, 110, 50),
    (900, 300, 110, 50),
]

geo = {
    "viewBox": "0 0 %s %s" % (W, H), "largeur": W, "hauteur": H,
    "regions": REGIONS,
    "fonds": {},
    "lieux": LIEUX,
    "terre": chemin(rect),
    "eaux": EAUX,
    "relief": {"collines": " ".join(ovale(*c) for c in COLLINES),
               "montagnes": " ".join(ovale(*c) for c in MONTAGNES)},
    "rivieres": "",
    "bourgs": BOURGS,
    "routes": [],
}

# ---- les cadres -------------------------------------------------------------
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
    x0 = min(max(x0, 0), W - l) if l <= W else x0
    y0 = min(max(y0, 0), H - h) if h <= H else y0
    return "%s %s %s %s" % (r1(x0), r1(y0), r1(l), r1(h))


SUD_EST = ["rupea", "homorod", "comana-de-jos", "ticusu-vechi", "odorheiu-secuiesc", "cincu"]
geo["cadres"] = {
    "pays": "0 0 %s %s" % (W, H),
    "sud-est": boite([i for i in SUD_EST if i in LIEUX], 22),
}

with open(os.path.join(ICI, "geo.js"), "w", encoding="utf-8") as f:
    f.write("// geo.js — la Terre des Cinq, ENGENDRE par dessiner_geo.py depuis canon/map.json\n"
            "// Ne pas editer a la main : retoucher le generateur et relancer.\n"
            "// 1 unite = 4 unites du canon ~ 320 m. Trace de la Tarnava et relief : inventes.\n"
            '"use strict";\nwindow.Geo = ' + json.dumps(geo, ensure_ascii=False) + ";\n")
print("geo.js : %d lieux, %d bourgs, %d contours de foret, cadre %sx%s, sud-est %s" % (
    len(LIEUX), len(BOURGS), len(geo_b), W, H, geo["cadres"]["sud-est"]))
if MANQUE:
    print("SANS VILLE SUR LA CARTE (ajouter un `alias`) :", ", ".join(MANQUE))
