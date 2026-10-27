# -*- coding: utf-8 -*-
"""
SEPARER LES MONDES — l'inventaire avant le demenagement (lot 2).

    python scripts/migrations/separer_mondes.py            # a sec, le rapport
    python scripts/migrations/separer_mondes.py --bavard   # les listes entieres
    python scripts/migrations/separer_mondes.py --table personnages
    python scripts/migrations/separer_mondes.py --vraiment # ecrit la repartition

POURQUOI CE SCRIPT EXISTE. Le depot porte DEUX mondes fondus l'un dans l'autre,
et l'epreuve du chantier est de les separer (docs/refonte-plan.md § 1). Le
resolveur de monde existe depuis le lot 1 ; ce qui manque est la repartition des
DONNEES. Mesure du 9.9 : 154 fiches sur 280 touchent Venise, 76 dossiers de
`chambres/` sur 313, 49 aretes sur 193, une maison et ses 26 volumes. Ce script
en corrige une : ce ne sont pas 76 chambres mais 154 — le fichier marqueur
`serenissima` n'en couvre que la moitie, et c'est le plus faible des criteres.

Un `grep braavos` ne suffit pas, et c'est tout le sujet. Il compte 140 items de
flux quand 1 078 sont adresses au siege venitien ; il ne voit aucune fiche a la
Fosse aux Dragons quand 76 citoyens de Venise y sont poses. Ce qui decide n'est
pas le mot : ce sont des CRITERES, plusieurs, et surtout ce qu'ils disent quand
ils ne disent pas la meme chose.

CE QUE CE SCRIPT TRANCHE, ET POURQUOI DANS CE SENS.

1. **La topologie prime, mais elle ne dit pas le monde.** `chemins.json` a
   QUATRE composantes connexes, pas deux : Peyredragon (36 salles), Port-Real
   (52), Braavos (34) et Barralfond (6). Une composante est un SITE — un endroit
   d'ou l'on ne marche pas ailleurs — et trois de ces quatre sont Westeros. Le
   critere topologique se lit par temoins declares, jamais en comptant.
2. **L'etat declare deja un monde, a un seul endroit, et personne ne le sait.**
   `corps.json` porte `monde: "braavos"` sur 153 corps, qui sont exactement les
   153 fiches de `maison-serenissima` — accord parfait, verifie. C'est le
   critere le plus solide du depot, et il ne servait a rien.
3. **On ne suppose JAMAIS qu'une fiche appartient a exactement un monde.** Seule
   contrainte que `docs/traversee.md` impose au lot 2. D'ou quatre categories :
   `westeros`, `venise`, `traverse` (ce qui touche les deux parce qu'un
   traversant DECLARE l'explique) et `indecidable` (ce que les criteres se
   disputent sans traversant pour le justifier). Le script LISTE les deux
   dernieres, il ne les tranche pas. Une memoire ne se coupant pas en deux, une
   repartition qui proposerait de dupliquer une chambre, une fiche ou un cahier
   serait le signe d'une categorie manquante, pas d'une solution.
4. **Les references cassees sont la sortie la plus utile.** Une repartition
   juste qui coupe vingt-cinq relations en deux est une perte, pas une
   separation. Elles sont classees par gravite, et ce qui est DEJA rompu
   aujourd'hui est compte a part : on ne met pas sur le dos de la separation ce
   qui etait casse avant elle.
5. **A SEC PAR DEFAUT** (convention de `scripts/pousser_donnees.py`). Meme sous
   `--vraiment`, rien n'est ecrit dans `etat/` ni dans `chambres/` : la
   repartition est deposee sous `.agents-runtime/`. Un inventaire qui deplace ne
   peut plus se relancer pour verifier.

POURQUOI IL N'EST PAS COUPE EN TROIS, malgre le cliquet des 500 lignes. Ses
trois parties — les criteres, les tables, le rapport — n'ont aucun sens l'une
sans l'autre, et `scripts/migrations/` n'est pas sur le chemin des freres : un
module voisin ne s'importerait que sous appel direct, et faire descendre les
entrailles d'une migration a usage unique dans `noyau/` — le dossier des modules
PARTAGES et permanents — couterait plus cher que les lignes en trop.

CE QU'IL NE FAIT PAS. Il ne deplace aucun octet, ne cree aucun paquet de monde,
n'ecrit aucun manifeste, ne pose ni `monde_natal` ni amarre. Le raisonnement,
les chiffres commentes et la date d'amarre proposee vivent dans
`docs/separation-mondes.md`.
"""
import os as _os, sys as _sys  # le chemin des freres : scripts/ et scripts/noyau/
_d = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_d) != "scripts" and _os.path.dirname(_d) != _d:
    _d = _os.path.dirname(_d)
for _p in (_d, _os.path.join(_d, "noyau")):
    if _p not in _sys.path:
        _sys.path.insert(0, _p)

import argparse
import collections
import io
import json
import os
import re
import sys

import racines
import tables

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

W, V = "westeros", "venise"
TRAVERSE, INDECIDABLE = "traverse", "indecidable"
GRAVITES = ("rupture", "pendante", "deja-rompu", "bruit")

# LES TEMOINS — le seul endroit ou ce script nomme un monde, et c'est legitime :
# une migration est datee, elle ne fait pas partie du moteur (refonte-plan, E4).
# Une salle temoin par SITE ; le site herite du monde, la composante du site.
TEMOINS = {
    "table-peinte": W,          # Peyredragon
    "salle-du-trone": W,        # Port-Real
    "la-souche": W,             # Barralfond, au-dela du Mur
    "braavos-table-peinte": V,  # Braavos
}
LIEUX_DE_VENISE = {"braavos"}
MAISONS_DE_VENISE = {"maison-serenissima"}
MARQUEURS_CHAMBRE = {"serenissima": V}
MONDE_DU_CORPS = {"braavos": V}

# LES TRAVERSANTS — declares, jamais devines. `docs/traversee.md` § 6 tranche que
# le monde natal de Nicolas est Venise ; `nicolas-reynolds` est l'ancien id du
# meme homme, encore porte par 49 actes et 203 items de flux.
TRAVERSANTS = {"nicolas-lester-reynolds": V, "nicolas-reynolds": V}

# LE LEXIQUE NE VOTE PAS : il contredit, ou il se tait. La moitie des mentions de
# decor sont justes (refonte-plan § 7.6) ; un mot n'a jamais decide d'un monde
# ici, il sert de controle contre les criteres qui, eux, decident.
LEX = {
    V: re.compile(u"braavos|serenissima|ducat|venise|rialto|cittadin", re.I),
    W: re.compile(u"peyredragon|targaryen|rhaenyra|port-réal|port-real"
                  u"|aegon|valyrien", re.I),
}
# Les mots westeriens qui survivent au retrait du prefixe `braavos-` : ce sont
# eux qui font tomber E3 (« Venise ne connait pas Westeros ») sur des salles.
WESTERIEN_NU = {"table-peinte", "porte-dragon", "jardin-aegon", "septuaire",
                "tour-dragon-mer", "appartements-reine", "guivre-des-vents",
                "roukerie", "chambre-enfants"}


def _normal(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _texte(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as f:
        return f.read()


class Monde(object):
    """Ce que l'etat sait de lui-meme, lu une fois et partage par les criteres."""

    def __init__(self):
        self.personnages = {f["id"]: f for f in tables.lire("personnages")}
        self.lieux = {l["id"]: l for l in tables.lire("lieux")}
        self.maisons = {m["id"]: m for m in tables.lire("maisons")}
        self.chemins = tables.lire("chemins")
        self.joueurs = tables.lire("joueurs")
        self.horloges = tables.lire("horloges", {})
        self.chambres = racines.chambres()
        self.site = self._composantes()
        self.corps = {c["personnage_id"]: MONDE_DU_CORPS[c["monde"]]
                      for c in tables.lire("corps", {}).get("corps", [])
                      if c.get("monde") in MONDE_DU_CORPS}

    def _composantes(self):
        """salle -> monde, par la composante connexe et le temoin qu'elle porte."""
        voisins = collections.defaultdict(set)
        for a in self.chemins.get("aretes", []):
            voisins[a[0]].add(a[1])
            voisins[a[1]].add(a[0])
        site, vus = {}, set()
        for depart in voisins:
            if depart in vus:
                continue
            pile, bloc = [depart], set()
            while pile:
                u = pile.pop()
                if u not in bloc:
                    bloc.add(u)
                    pile.extend(voisins[u] - bloc)
            vus |= bloc
            monde = ([TEMOINS[s] for s in sorted(bloc) if s in TEMOINS] or [None])[-1]
            site.update({s: monde for s in bloc})
        for faux, vrai in (self.chemins.get("alias") or {}).items():
            site.setdefault(faux, site.get(vrai))
        return site

    # --- LES CRITERES. Chacun rend (monde, motif) ou None : « je ne sais pas »
    # n'est pas « westeros ». Un critere muet ne vote pas.

    def par_salle(self, salle):
        m = self.site.get(salle)
        return (m, u"salle %s" % salle) if m else None

    def par_lieu(self, lieu):
        if not lieu:
            return None
        if lieu in LIEUX_DE_VENISE:
            return (V, u"lieu %s" % lieu)
        return (W, u"lieu %s" % lieu) if lieu in self.lieux else self.par_salle(lieu)

    def par_maison(self, maison):
        if not maison:
            return None
        if maison in MAISONS_DE_VENISE:
            return (V, u"maison %s" % maison)
        return (W, u"maison %s" % maison) if maison in self.maisons else None

    def par_corps(self, pid):
        return (self.corps[pid], u"corps.monde") if pid in self.corps else None

    def par_chambre(self, dossier):
        for marque, monde in MARQUEURS_CHAMBRE.items():
            if os.path.exists(os.path.join(self.chambres, dossier, marque)):
                return (monde, u"marqueur %s" % marque)
        return None

    def par_homme(self, pid):
        """Le monde d'un homme. Le traversant declare passe avant sa fiche."""
        if pid in TRAVERSANTS:
            return (TRAVERSANTS[pid], u"traversant declare")
        f = self.personnages.get(pid)
        if not f:
            return None
        for c in (self.par_maison(f.get("maison_id")), self.par_corps(pid),
                  self.par_lieu(f.get("lieu_id"))):
            if c:
                return c
        return None

    def par_lexique(self, texte):
        trouve = [m for m, rx in LEX.items() if rx.search(texte)]
        return trouve[0] if len(trouve) == 1 else None


def verdict(votes):
    """Des votes {monde: [motifs]} vers (categorie, motifs, desaccord).

    Un desaccord explique par un traversant declare est une TRAVERSEE ; le meme
    desaccord sans traversant est indecidable, et le script ne tranche pas.
    """
    mondes = sorted(m for m in votes if m in (W, V))
    motifs = sorted(set(m for liste in votes.values() for m in liste))
    if not mondes:
        return (INDECIDABLE, motifs, u"aucun critere ne parle")
    if len(mondes) == 1:
        return (mondes[0], motifs, None)
    desaccord = u" / ".join(u"%s: %s" % (m, u", ".join(sorted(set(votes[m]))))
                            for m in mondes)
    quoi = TRAVERSE if u"traversant declare" in motifs else INDECIDABLE
    return (quoi, motifs, desaccord)


def vote(*criteres):
    votes = collections.defaultdict(list)
    for c in criteres:
        if c and c[0]:
            votes[c[0]].append(c[1])
    return verdict(votes)


class Rapport(object):
    def __init__(self):
        self.tables = collections.OrderedDict()
        self.liens = []

    def poser(self, nom, lignes):
        self.tables[nom] = lignes          # [(cle, categorie, motifs, desaccord)]

    def casse(self, gravite, table, quoi, pourquoi):
        self.liens.append((gravite, table, quoi, pourquoi))

    def comptes(self, nom):
        return collections.Counter(l[1] for l in self.tables[nom])

    def ruptures(self):
        return sum(1 for g, _t, _q, _p in self.liens if g == "rupture")


def _coupe(ligne):
    """Vrai si la ligne est un vrai partage entre deux mondes, non explique."""
    return ligne[1] == INDECIDABLE and ligne[3] and u"aucun" not in ligne[3]


# ---------------------------------------------------------------------------
# LES TABLES — chacune dit par quels criteres se lisent ses lignes.
# ---------------------------------------------------------------------------

def t_lieux(m, r):
    r.poser("lieux", [(i,) + vote(m.par_lieu(i)) for i in sorted(m.lieux)])


def t_maisons(m, r):
    r.poser("maisons", [(i,) + vote(m.par_maison(i), m.par_lieu(h.get("siege_id")))
                        for i, h in sorted(m.maisons.items())])


def t_personnages(m, r):
    lignes = []
    for pid, f in sorted(m.personnages.items()):
        declare = (TRAVERSANTS.get(pid), u"traversant declare") if pid in TRAVERSANTS else None
        l = (pid,) + vote(declare, m.par_maison(f.get("maison_id")),
                          m.par_corps(pid), m.par_lieu(f.get("lieu_id")))
        lignes.append(l)
        if _coupe(l):
            r.casse("pendante", "personnages", pid,
                    u"sa fiche part d'un cote, son `lieu_id` de l'autre : il "
                    u"pointera vers un lieu que son paquet ne contient pas")
    r.poser("personnages", lignes)


def t_chambres(m, r):
    lignes, doublons = [], collections.defaultdict(list)
    fiches = collections.defaultdict(list)
    for pid in m.personnages:
        fiches[_normal(pid)].append(pid)
    for d in sorted(os.listdir(m.chambres)):
        if not os.path.isdir(os.path.join(m.chambres, d)):
            continue
        doublons[_normal(d)].append(d)
        pids = fiches.get(_normal(d)) or []
        l = (d,) + vote(m.par_chambre(d), *[m.par_homme(p) for p in pids])
        lignes.append(l)
        if not pids:
            r.casse("deja-rompu", "chambres", d,
                    u"aucune fiche de personnage ne porte ce nom")
        if _coupe(l):
            r.casse("rupture", "chambres", d,
                    u"son marqueur et sa fiche ne disent pas le meme monde")
    for noms in (n for n in doublons.values() if len(n) > 1):
        r.casse("rupture", "chambres", u" + ".join(noms),
                u"deux chambres pour un seul homme : une memoire ne se coupe pas "
                u"en deux")
    r.poser("chambres", lignes)


def t_chemins(m, r):
    lignes = []
    for a in m.chemins.get("aretes", []):
        l = (u"%s — %s" % (a[0], a[1]),) + vote(m.par_salle(a[0]), m.par_salle(a[1]))
        lignes.append(l)
        if _coupe(l):
            r.casse("rupture", "chemins", l[0], u"arete coupee par la separation")
    for salle, monde in sorted(m.site.items()):
        if monde == V and salle.replace("braavos-", "") in WESTERIEN_NU:
            r.casse("bruit", "chemins", salle,
                    u"salle de Venise nommee en westerien : E3 tombe dessus")
    r.poser("chemins", lignes)


def t_livres(m, r):
    base = os.path.join(racines.etat(), "maisons")
    lignes = []
    for maison in sorted(os.listdir(base) if os.path.isdir(base) else []):
        d = os.path.join(base, maison, "documents", "books")
        for nom in sorted(os.listdir(d) if os.path.isdir(d) else []):
            if nom == "_ordre.json" or not nom.endswith(".json"):
                continue
            try:
                with io.open(os.path.join(d, nom), encoding="utf-8") as fh:
                    v = json.load(fh)
            except ValueError:
                r.casse("deja-rompu", "livres", u"%s/%s" % (maison, nom),
                        u"volume illisible")
                continue
            salle, cle = v.get("salle_id"), u"%s/%s" % (maison, v.get("id") or nom)
            l = (cle,) + vote(m.par_maison(maison), m.par_lieu(v.get("lieu_id")),
                              m.par_salle(salle) if salle else None)
            lignes.append(l)
            if salle and not m.site.get(salle):
                r.casse("pendante", "livres", cle,
                        u"pose dans la salle « %s », absente de la topologie" % salle)
            if _coupe(l):
                r.casse("rupture", "livres", cle,
                        u"le tenant s'en va : sa maison et sa salle sont de deux mondes")
    r.poser("livres", lignes)


def t_sieges(m, r):
    lignes = []
    for s in m.joueurs:
        pid = s.get("personnage_id")
        # Corneille n'incarne personne : elle regarde. Faute de fiche a
        # interroger, c'est son poste d'observation qui decide.
        propre = m.par_salle(s.get("salle") or "")
        l = (pid,) + (vote(propre) if s.get("regie")
                      else vote(m.par_homme(pid), propre))
        lignes.append(l)
        etrangers = sorted(p for p in (s.get("pnj") or [])
                           if m.par_homme(p) and l[1] in (W, V)
                           and m.par_homme(p)[0] != l[1])
        if etrangers:
            r.casse("pendante", "joueurs.json", pid,
                    u"tient %d compagnon(s) de l'autre monde : %s"
                    % (len(etrangers), u", ".join(etrangers[:4])))
    r.poser("sieges", lignes)
    mondes = set((m.par_homme(k) or (None,))[0] for k in m.horloges)
    if len(mondes) > 1:
        r.casse("rupture", "horloges",
                u"etat/horloges.json (%d sieges)" % len(m.horloges),
                u"un seul fichier d'horloge pour des sieges de deux mondes : "
                u"Venise est calee sur le calendrier des Targaryen")


def t_flux(m, r):
    monde_du_siege = dict(TRAVERSANTS)
    for l in r.tables.get("sieges", []):
        if l[1] in (W, V):
            monde_du_siege.setdefault(l[0], l[1])
    lignes = []
    for n, brut in enumerate(io.open(os.path.join(racines.etat(), "flux.jsonl"),
                                     encoding="utf-8"), 1):
        brut, cle = brut.strip(), u"ligne %d" % n
        if not brut:
            continue
        try:
            item = json.loads(brut)
        except ValueError:
            r.casse("deja-rompu", "flux", cle, u"JSON illisible")
            continue
        pour = item.get("pour")
        pour = pour if isinstance(pour, list) else ([pour] if pour else [])
        oreilles = [x.strip() for y in pour for x in str(y).split(",")
                    if x.strip() and x.strip() != "tous"]
        l = (cle,) + vote(*[(monde_du_siege.get(o), u"adresse a %s" % o)
                            for o in oreilles])
        if l[1] == INDECIDABLE and not oreilles:
            lex = m.par_lexique(brut)
            l = (cle, lex, [u"lexique"], None) if lex else (
                cle, INDECIDABLE, [], u"aucun `pour`, aucun mot des deux mondes")
        lignes.append(l)
        if _coupe(l) and oreilles:
            r.casse("rupture", "flux", u"%s (%s)" % (cle, item.get("type")),
                    u"servie a des sieges de deux mondes : %s" % u", ".join(oreilles))
        elif l[1] == INDECIDABLE:
            r.casse("bruit", "flux", cle,
                    u"aucun `pour` : personne ne sait de quel monde elle est")
    r.poser("flux", lignes)


def _ids(entree, champs):
    vus = set()
    for ch in champs:
        v = entree.get(ch)
        if isinstance(v, str):
            vus.add(v)
        elif isinstance(v, list):
            vus.update(x for x in v if isinstance(x, str))
    return vus - {"tous"}


# nom, table, sous-clef, champs d'identite, gravite du partage, ce qu'il coute
TABLES_PAR_IDS = (
    ("relations", "relations", None, ("source_id", "cible_id"), "rupture",
     u"une relation dont les deux bouts partent dans deux mondes"),
    ("actes", "actes", None, ("acteur_id", "cible_id", "temoins", "connu_de"),
     "rupture", u"un acte dont l'acteur et les temoins se separent"),
    ("paroles", "paroles", None,
     ("locuteur_id", "destinataire_id", "destinataires", "temoins", "connu_de"),
     "rupture", u"une parole dont le locuteur et les temoins se separent"),
    ("info", "info", None, ("destinataire_id", "connu_de"), "pendante",
     u"une nouvelle servie de part et d'autre"),
    ("intentions", "intentions", None, ("personnage_id",), "rupture",
     u"une tete partagee"),
    ("pensees", "pensees", "pensees", ("qui",), "rupture", u"une pensee partagee"),
    ("conclusions", "conclusions", "conclusions", ("qui",), "rupture",
     u"une conclusion partagee"),
    ("evenements", "evenements", None, ("acteurs",), "rupture",
     u"un evenement dont les acteurs se separent"),
)


def t_par_ids(m, r):
    for nom, table, sous, champs, gravite, pourquoi in TABLES_PAR_IDS:
        d = tables.lire(table, [])
        if isinstance(d, dict):
            d = d.get(sous, []) if sous else list(d.values())
        lignes = []
        for i, e in enumerate(x for x in d if isinstance(x, dict)):
            gens = sorted(_ids(e, champs))
            # Une relation n'a pas d'`id` : on la nomme par ses bouts, sinon le
            # rapport rend « relations[76] » et personne ne sait de qui il parle.
            cle = e.get("id") or u" + ".join(gens[:3]) or u"%s[%d]" % (nom, i)
            l = (cle,) + vote(*[m.par_homme(g) for g in gens])
            lignes.append(l)
            if _coupe(l):
                r.casse(gravite, nom, cle, pourquoi)
            for g in gens:
                if g not in m.personnages and g not in TRAVERSANTS:
                    r.casse("deja-rompu", nom, cle,
                            u"cite « %s », qui n'a pas de fiche" % g)
        r.poser(nom, lignes)


def t_dossiers_de_siege(m, r):
    """Ce qu'un siege CROIT du monde : jetons, vues, objectifs, journal."""
    base = os.path.join(racines.etat(), "joueurs")
    lignes = []
    for siege in sorted(os.listdir(base) if os.path.isdir(base) else []):
        d = os.path.join(base, siege)
        if not os.path.isdir(d):
            continue
        sien = m.par_homme(siege)
        lignes.append((siege,) + vote(sien))
        if not sien:
            r.casse("deja-rompu", "joueurs/<siege>", siege,
                    u"dossier de siege sans fiche ni entree dans joueurs.json")
            continue
        etranger = sorted(f for f in os.listdir(d)
                          if f.endswith(".json") and not f.startswith("partie-")
                          and m.par_lexique(_texte(os.path.join(d, f)))
                          not in (None, sien[0]))
        if etranger:
            r.casse("pendante", "joueurs/<siege>", siege,
                    u"son dossier (%s) croit des choses de l'autre monde ; la "
                    u"memoire suit l'homme, les ids qu'elle nomme ne le suivent pas"
                    % u", ".join(etranger))
    r.poser("joueurs/<siege>", lignes)


def t_dossiers_dates(m, r):
    """`depeches/` et `activations/` : une journee d'homme par fichier."""
    for nom in ("depeches", "activations"):
        base = os.path.join(racines.etat(), nom)
        r.poser(nom, [(f,) + vote(m.par_homme(
            re.sub(r"^\d{8}-\d{6}-\d+-(?:[0-9a-f]{6}-)?", "",
                   f.rsplit(".", 1)[0])))
            for f in sorted(os.listdir(base) if os.path.isdir(base) else [])])


def repartir():
    m, r = Monde(), Rapport()
    for etape in (t_lieux, t_maisons, t_personnages, t_chambres, t_chemins,
                  t_livres, t_sieges, t_flux, t_par_ids, t_dossiers_de_siege,
                  t_dossiers_dates):
        etape(m, r)
    return m, r


# ---------------------------------------------------------------------------
# LE RAPPORT
# ---------------------------------------------------------------------------

def _grouper(titre, entrees, marge, bavard, plafond):
    """Un seul imprimeur : les deux listes du rapport groupent par (ou, motif),
    comptent, et donnent des exemples. `entrees` : [(ou, quoi, motif)].
    """
    print(u"%s (%d)" % (titre, len(entrees)))
    groupes = collections.Counter((o, m) for o, _q, m in entrees)
    for (ou, motif), n in groupes.most_common(None if bavard else plafond):
        ex = [q for o, q, m in entrees if o == ou and m == motif]
        print(u"%s%-16s %5d  %s" % (marge, ou, n, motif[:90]))
        print(u"%s    ex. %s" % (marge, u", ".join(ex[:8 if bavard else 3])))
    if not bavard and len(groupes) > plafond:
        print(u"%s... et %d motif(s) de plus — `--bavard`"
              % (marge, len(groupes) - plafond))


def rendre(r, bavard=False, seule=None):
    print(u"SEPARER LES MONDES — a sec. Rien n'a ete deplace.")
    print(u"racine lue : %s\n" % racines.etat())
    print(u"%-18s %8s %8s %9s %12s" % (u"table", u"westeros", u"venise",
                                       u"traverse", u"indecidable"))
    print(u"-" * 60)
    for nom in r.tables:
        if not seule or nom == seule:
            c = r.comptes(nom)
            print(u"%-18s %8d %8d %9d %12d" % (nom, c[W], c[V], c[TRAVERSE],
                                               c[INDECIDABLE]))
    muet = sum(1 for lignes in r.tables.values() for l in lignes
               if l[1] == INDECIDABLE and (not l[3] or u"aucun" in l[3]))
    dispute = sum(r.comptes(n)[INDECIDABLE] for n in r.tables) - muet
    print(u"\nSur les indecidables : %d sont un DESACCORD de criteres — ceux-la "
          u"demandent une\ndecision — et %d un SILENCE : aucun critere ne parle.\n"
          % (dispute, muet))
    for categorie, titre in ((TRAVERSE, u"CE QUI TRAVERSE — a poser, pas a couper"),
                             (INDECIDABLE, u"CE QUI RESTE INDECIDABLE")):
        _grouper(titre, [(n, l[0], l[3] or u"?")
                         for n, lignes in r.tables.items() for l in lignes
                         if l[1] == categorie and (not seule or n == seule)],
                 u"    ", bavard, 12)
        print(u"")
    print(u"CE QUE LA SEPARATION CASSERAIT, par gravite")
    for g in GRAVITES:
        _grouper(u"  [%s]" % g, [(t, q, p) for gg, t, q, p in r.liens
                                 if gg == g and (not seule or t == seule)],
                 u"      ", bavard, 8)
    print(u"")
    return r.ruptures()


def amarre(m):
    """L'AMARRE — le script ne la pose pas, il dit ou les deux calendriers se
    touchent aujourd'hui. Une seule correspondance datee suffit, le reste est de
    l'arithmetique (docs/traversee.md § 3) ; tant que les sieges des deux mondes
    lisent la MEME date, ce jour-la est le dernier point de contact honnete.
    """
    par_monde = collections.defaultdict(set)
    for siege, h in sorted(m.horloges.items()):
        homme = m.par_homme(siege)
        par_monde[homme[0] if homme else u"?"].add(
            (h.get("annee"), h.get("lune"), h.get("jour")))
    print(u"L'AMARRE — ou les deux calendriers se touchent encore")
    for monde in sorted(par_monde):
        for annee, lune, jour in sorted(par_monde[monde]):
            print(u"    %-10s an %s, %se lune, %se jour" % (monde, annee, lune, jour))
    if len(set().union(*par_monde.values())) == 1:
        print(u"    Les deux mondes lisent la MEME date. C'est elle qu'il faut "
              u"figer en amarre\n    avant de separer : apres, plus rien ne les "
              u"raccorde.")
    print(u"")


def ecrire_repartition(r, vers):
    """Le seul geste de `--vraiment` : deposer la repartition HORS de `etat/`."""
    os.makedirs(vers, exist_ok=True)
    for nom, lignes in r.tables.items():
        cible = os.path.join(vers, re.sub(r"[/<>]", "-", nom) + ".json")
        with io.open(cible, "w", encoding="utf-8") as fh:
            fh.write(json.dumps([{"cle": a, "monde": b, "motifs": c, "desaccord": d}
                                 for a, b, c, d in lignes],
                                ensure_ascii=False, indent=1))
    with io.open(os.path.join(vers, "_liens-casses.json"), "w",
                 encoding="utf-8") as fh:
        fh.write(json.dumps([{"gravite": g, "table": t, "quoi": q, "pourquoi": p}
                             for g, t, q, p in r.liens],
                            ensure_ascii=False, indent=1))
    print(u"repartition ecrite sous %s" % vers)
    print(u"Aucun octet de `etat/` ni de `chambres/` n'a bouge : le demenagement "
          u"proprement dit est un autre script, et il lira ces fichiers.")


def main(argv=None):
    p = argparse.ArgumentParser(
        description=u"Inventaire de la separation des mondes (lot 2).")
    p.add_argument("--vraiment", action="store_true",
                   help=u"ecrit la repartition (jamais dans etat/ ni chambres/)")
    p.add_argument("--vers", default=os.path.join(racines.DEPOT, ".agents-runtime",
                                                  "separation"),
                   help=u"ou deposer la repartition sous --vraiment")
    p.add_argument("--table", default=None, help=u"n'afficher qu'une table")
    p.add_argument("--bavard", action="store_true", help=u"les listes entieres")
    a = p.parse_args(argv)

    m, r = repartir()
    ruptures = rendre(r, a.bavard, a.table)
    amarre(m)
    if not a.vraiment:
        print(u"APERCU SEUL — relancez avec --vraiment pour ecrire la repartition")
        return 0
    if ruptures:
        raise SystemExit(
            u"REFUS : %d rupture(s) non tranchee(s). Une separation qui coupe une "
            u"relation en deux n'est pas une separation, c'est une perte. "
            u"Tranchez-les d'abord — docs/separation-mondes.md dit lesquelles."
            % ruptures)
    ecrire_repartition(r, a.vers)
    return 0


if __name__ == "__main__":
    sys.exit(main())
