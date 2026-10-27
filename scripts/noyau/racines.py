# -*- coding: utf-8 -*-
"""
RACINES — ou vit l'etat, et de quel monde il est.

    import racines
    racines.etat()                  # .../etat  (ou .../mondes/venise/etat)
    racines.chambres()              # les chambres du monde courant
    racines.courant()               # "venise", ou None en disposition heritee
    racines.manifeste()             # calendrier, monnaie, titres, unites, canaux

POURQUOI CE MODULE EXISTE.

Le depot porte DEUX mondes depuis des lunes — Westeros et Venise — et rien ne
le declare. Ils partagent `personnages.json` (154 fiches veniciennes sur 280),
`chambres/` (76 dossiers sur 313), `chemins.json` (49 aretes sur 193), une
maison, un fil. Un siege joueur vit a Braavos et son horloge est dans le meme
fichier que celle de la reine, calee sur le 12e jour de la 5e lune de l'an 129 :
Venise tourne a l'heure des Targaryen.

Ce n'etait pas un choix. C'etait l'absence d'un concept : **un monde est un
paquet**, et le moteur n'en connait aucun — il en recoit un. Faute de ce
module, chaque fichier Python calculait sa racine depuis son propre chemin
(110 le font) et y collait `etat` en dur (80 le font). Une racine calculee
depuis `__file__` est une racine qu'on ne peut pas deplacer : elle designe
toujours le dossier ou le CODE se trouve, jamais celui ou les DONNEES sont.

CE QUE CE MODULE TRANCHE, ET POURQUOI DANS CE SENS.

1. **La racine du DEPOT se calcule depuis `__file__`, et c'est legitime.**
   Le code est bien la ou le code est. C'est la seule chose que ce module
   deduise de sa propre position.
2. **La racine du MONDE se declare, jamais ne se deduit.** Trois sources, dans
   cet ordre : `CONSEIL_RACINE` (un chemin absolu, ce que les tests du serveur
   emploient deja), puis `CONSEIL_MONDE` (un id sous `mondes/`), puis la
   disposition heritee — `etat/` a la racine du depot.
3. **La disposition heritee est le defaut, et elle est identique a l'octet
   pres.** Sans variable, `etat()` rend exactement ce que `tables.py` rendait
   avant ce module. C'est ce qui rend ce lot ADDITIF : rien ne bouge tant que
   personne ne nomme un monde. Le jour ou `mondes/westeros/` existera, le
   defaut se deplacera dans le manifeste, en une ligne et une fois.
4. **Le meme contrat que le serveur, aux memes mots.** `serveur/contexte.js`
   lit deja `CONSEIL_RACINE` et en fait un dossier qui CONTIENT `etat/`. Ce
   module en fait exactement la meme chose : les deux langues doivent tomber
   sur le meme dossier, sinon le brouillard d'un monde s'ouvre dans l'autre.
5. **Un monde inconnu PLANTE.** Meme raison que la porte des tables devant un
   JSON abime : servir silencieusement l'etat du monde precedent parce qu'on a
   mal tape son nom est la faute la plus couteuse possible, et la plus
   invisible.

POURQUOI PAS `monde.py`, LE NOM QUE LE SUJET APPELLE.
Meme piege que celui documente dans `tables.py`, et il a failli se refermer :
`scripts/monde/` est deja un dossier — la generation du monde en 3D, 21 585
lignes — et `pyproject.toml` declare `monde` comme paquet du projet. Aujourd'hui
un `scripts/noyau/monde.py` gagnerait, parce que ce dossier n'a pas d'`__init__`
et n'est donc qu'un paquet-espace-de-noms, qu'un vrai module bat. Le jour ou
quelqu'un y poserait un `__init__.py`, `scripts/` passant devant `scripts/noyau/`
dans `sys.path`, le paquet gagnerait et ce module serait masque SANS ERREUR :
tout le monde lirait l'etat du monde precedent. Livrer sous un nom pris la piece
qui decide OU l'on ecrit aurait ete la faute que ce module existe pour fermer.

CE QU'IL NE FAIT PAS. Il ne lit aucune table, ne connait aucun nom de lieu, de
maison ni de personnage, et n'a aucun avis sur le contenu d'un monde. Il dit ou
c'est. Ce qu'il y a dedans est l'affaire de `tables.py` et du manifeste.
"""
import io
import json
import os
import re

# La racine du DEPOT — la seule deduction legitime depuis `__file__` : le code
# est la ou le code est. scripts/noyau/racines.py -> scripts/noyau -> scripts -> .
DEPOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Le dossier des paquets de monde. Absent tant que le lot 2 n'a pas eu lieu.
MONDES = os.path.join(DEPOT, "mondes")

_VAR_RACINE = "CONSEIL_RACINE"   # un chemin absolu qui CONTIENT etat/
_VAR_MONDE = "CONSEIL_MONDE"     # un id de paquet sous mondes/


class MondeInconnu(Exception):
    """On a nomme un monde qui n'existe pas. On ne sert jamais celui d'a cote."""


def courant():
    """L'id du monde courant, ou None en disposition heritee.

    None n'est pas une panne : c'est l'etat du depot tant que `mondes/` n'a pas
    ete peuple. Un appelant qui veut un nom pour l'afficher dit « le monde »,
    pas « None ».
    """
    m = (os.environ.get(_VAR_MONDE) or "").strip()
    return m or None


def mondes(tous=False):
    """Les paquets disponibles, tries. Vide tant que `mondes/` n'existe pas.

    Un nom qui commence par `_` est un monde de SERVICE — `_epreuve` en est un :
    il existe pour que les tests aient un monde a exercer qui ne soit aucun des
    monde joues. Il est cache du menu du joueur, jamais de la machine : `tous`
    le rend, et un diagnostic qui ne le dirait pas mentirait sur ce qui est la.
    """
    try:
        noms = os.listdir(MONDES)
    except OSError:
        return []
    d = []
    for n in noms:
        if n.startswith("."):
            continue
        if not tous and n.startswith("_"):
            continue
        if os.path.isdir(os.path.join(MONDES, n)):
            d.append(n)
    return sorted(d)


def racine(monde=_VAR_MONDE):
    """Le dossier qui CONTIENT `etat/` — la racine du monde, pas celle du depot.

    `monde` non fourni : celui de l'environnement. `monde=None` : la disposition
    heritee, quoi que dise l'environnement — ce dont les migrations ont besoin
    pour lire l'ancien monde pendant qu'elles ecrivent le neuf.
    """
    force = os.environ.get(_VAR_RACINE)
    if force and monde is _VAR_MONDE:
        return os.path.abspath(force)
    m = courant() if monde is _VAR_MONDE else monde
    if not m:
        return DEPOT
    p = os.path.join(MONDES, m)
    if not os.path.isdir(p):
        raise MondeInconnu(
            "monde %r : %s n'existe pas.\n"
            "Mondes disponibles : %s" % (m, p, ", ".join(mondes(tous=True)) or "aucun"))
    return p


def etat(monde=_VAR_MONDE):
    """Le dossier `etat/` du monde. Le seul chemin que la porte des tables lit."""
    return os.path.join(racine(monde), "etat")


def chambres(monde=_VAR_MONDE):
    """Les chambres du monde — les domiciles de ses habitants."""
    return os.path.join(racine(monde), "chambres")


def manifeste(monde=_VAR_MONDE, defaut=None):
    """Ce que le monde declare de lui-meme : calendrier, monnaie, titres,
    genres d'unites, canaux, offices, signes, lieu de depart.

    Absent : le defaut fourni, ou un manifeste vide. C'est le cas de la
    disposition heritee, ou ces valeurs sont encore en dur dans le code — le
    lot 4 les fait descendre ici, une famille a la fois.
    """
    p = os.path.join(racine(monde), "manifeste.json")
    try:
        with io.open(p, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {} if defaut is None else defaut
    except ValueError as e:
        raise MondeInconnu("%s ne se lit pas : %s" % (p, e))


def dit(cle, defaut=None, monde=_VAR_MONDE):
    """Une valeur du manifeste, avec son defaut.

    C'est par ici que le moteur demande au monde ce qu'il ne doit pas savoir :
    `racines.dit("monnaie")`, `racines.dit("titres")`. Un defaut fourni ici est un
    aveu — il dit qu'une valeur de decor vit encore dans le code, et il rend
    la dette COMPTABLE au lieu de la rendre invisible.
    """
    return manifeste(monde).get(cle, defaut)


# ---------------------------------------------------------------------------
# LA MESURE — combien de fichiers decident encore seuls ou vit l'etat
# ---------------------------------------------------------------------------
# Meme discipline que `tables.py --verifier`, pour la meme raison : le compteur
# qui n'existe pas est celui qui derive. Une regle ecrite dans un en-tete est un
# souhait ; un chiffre affiche a cote des gardes est une regle, parce qu'on voit
# quand il monte.
#
# Ce qu'on compte : un fichier qui calcule sa racine depuis `__file__` PUIS y
# colle `etat` est un fichier qui ne pourra jamais changer de monde. Les deux
# ensemble, pas l'un ou l'autre — calculer la racine du DEPOT depuis `__file__`
# est legitime (c'est ce que fait ce module), et joindre `etat` a une racine
# recue ne l'est pas moins. C'est la CONJONCTION qui grave le monde dans le code.
#
# Ce chiffre ne doit que descendre. Il se migre un fichier par commit :
# `RACINE = os.path.dirname(...)` + `ETAT = os.path.join(RACINE, "etat")`
# devient `import racines` + `ETAT = racines.etat()`.

# LA MESURE A MENTI, ET VOICI COMMENT (corrige le 9.9, le soir).
# La premiere version ne cherchait que `RACINE`, en majuscules. Elle annoncait
# 74 puis 19 fichiers, et elle ne voyait pas `scripts/scene/flux_scribe.py` —
# qui nomme sa racine `racine`, en minuscules, et qui est LE fichier qui tient
# l'horloge du monde et la seule plume du flux. Consequence mesuree : une
# poussee lancee sous `CONSEIL_MONDE=cities-of-light` a ecrit dans le fil de
# WESTEROS, en le validant contre les horloges de Westeros, et il a fallu
# retirer la ligne a la main.
# Un compteur qui ne compte qu'une convention de nommage est pire qu'aucun
# compteur : il donne l'air d'avoir fini. On capture donc le NOM, quel qu'il
# soit, puis on regarde si c'est bien LUI qu'on colle a `etat`.
_CALCULE = re.compile(
    r"^\s*(\w+)\s*=\s*os\.path\.dirname\s*\(.*abspath\s*\(\s*__file__", re.M)
_PATHLIB = re.compile(
    r"^\s*(\w+)\s*=\s*Path\s*\(\s*__file__\s*\)\s*\.resolve\(\)(?:\s*\.parent)+", re.M)


def _colle_etat(texte, nom):
    """Ce nom-la est-il joint a `etat` ou a `chambres` quelque part ?"""
    return re.search(
        r"(?:os\.path\.join|joinpath)\s*\(\s*%s\s*,\s*[\x22\x27](?:etat|chambres)[\x22\x27]"
        % re.escape(nom), texte) is not None or re.search(
        r"%s\s*/\s*[\x22\x27](?:etat|chambres)[\x22\x27]" % re.escape(nom),
        texte) is not None


def _fichiers_py():
    """Les `*.py` suivis par git. On ne juge pas ce qui n'est pas au depot."""
    import subprocess
    try:
        sortie = subprocess.check_output(
            ["git", "ls-files", "*.py"], cwd=DEPOT).decode("utf-8", "replace")
    except Exception:
        return []
    return [f.strip() for f in sortie.splitlines() if f.strip()]


def hors_porte():
    """Les fichiers qui gravent le monde dans le code, tries."""
    dehors = []
    for f in _fichiers_py():
        p = os.path.join(DEPOT, f)
        try:
            with io.open(p, encoding="utf-8") as fh:
                t = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        noms = set(_CALCULE.findall(t)) | set(_PATHLIB.findall(t))
        if any(_colle_etat(t, n) for n in noms):
            dehors.append(f)
    return sorted(dehors)


def _verifier(bavard=False):
    d = hors_porte()
    print(u"racines : %d fichier(s) decident seuls ou vit l'etat" % len(d))
    if d:
        for f in (d if bavard else d[:12]):
            print(u"    %s" % f)
        if not bavard and len(d) > 12:
            print(u"    ... et %d autre(s) — `--bavard` les donne tous" % (len(d) - 12))
        print(u"")
        print(u"Migration : import racines ; ETAT = racines.etat()")
        print(u"Un fichier par commit. Ce compte ne doit que descendre.")
    return 0


if __name__ == "__main__":
    import sys as _sys
    _args = _sys.argv[1:]
    if "--verifier" in _args:
        _sys.exit(_verifier("--bavard" in _args))
    print(u"monde courant : %s" % (courant() or u"(disposition heritee)"))
    print(u"racine        : %s" % racine())
    print(u"etat          : %s" % etat())
    print(u"mondes        : %s" % (u", ".join(mondes(tous=True)) or u"aucun"))
