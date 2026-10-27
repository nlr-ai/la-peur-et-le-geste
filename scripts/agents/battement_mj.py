# -*- coding: utf-8 -*-
"""Le battement du MJ — une ligne au fil au moins une fois par minute.

Un MJ qui calcule laisse l'ecran muet : il lit l'etat, depeche un homme et
attend sa journee, et le joueur ne sait pas si le monde est mort ou au
travail. Le fournisseur Gemini rend la main d'un bloc (`subprocess.run`) : ni
evenement ni battement ne sortent du runtime avant la fin. Le battement tourne
donc A COTE de l'appel, dans un fil d'execution : toutes les cinq secondes il
regarde le flux ; si rien n'est tombe pour ce siege depuis une minute, il
pousse un item `statut`.

`statut` est HORS FICTION : zero minute, prive au siege, rien dans l'etat. Il
ne dit que ce que la machine sait — depuis combien de temps le MJ travaille,
et quels hommes sont dehors a vivre leur journee. Il n'invente aucun geste ni
aucune parole : la Regle Zero tient, ce n'est pas un PNJ qui parle.
"""
import io
import json
import os
import subprocess
import sys
import threading
import time

from agents import runtime

PERIODE = 60      # secondes de silence avant un statut
SONDE = 5         # secondes entre deux regards sur le flux


def _noms(etat):
    try:
        p = json.load(io.open(os.path.join(etat, "personnages.json"), encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    p = p if isinstance(p, list) else p.get("personnages", [])
    return {x.get("id"): x.get("nom") or x.get("id") for x in p if isinstance(x, dict)}


def _pour_lui(item, siege):
    pour = item.get("pour")
    if pour in (None, "tous"):
        return True
    return siege in pour if isinstance(pour, list) else pour == siege


def _dehors(depuis, noms):
    """Les hommes lances depuis le debut de ce calcul et encore vivants."""
    gens = []
    for d in runtime.activites_vivantes():
        homme = d.get("homme")
        if homme and homme != "mj" and (d.get("t") or 0) >= depuis - 5:
            nom = noms.get(homme, homme)
            if nom not in gens:
                gens.append(nom)
    return gens


def _texte(minutes, gens):
    duree = "une minute" if minutes <= 1 else "%d minutes" % minutes
    if gens:
        qui = gens[0] if len(gens) == 1 else ", ".join(gens[:-1]) + " et " + gens[-1]
        return "Le MJ attend %s — au travail depuis %s." % (qui, duree)
    return "Le MJ travaille — depuis %s." % duree


class Battement(object):
    """with Battement(siege, flux, etat, racine): ... — pousse un statut par
    minute de silence tant que le bloc tourne."""

    def __init__(self, siege, flux, etat, racine, periode=PERIODE):
        self.siege, self.flux, self.etat, self.racine = siege, flux, etat, racine
        self.periode = periode
        self.arret = threading.Event()
        self.fil = threading.Thread(target=self._tourner, daemon=True)

    def __enter__(self):
        self.debut = time.time()
        try:
            self.position = os.path.getsize(self.flux)
        except OSError:
            self.position = 0
        self.fil.start()
        return self

    def __exit__(self, *exc):
        self.arret.set()
        self.fil.join(timeout=10)
        return False

    def _nouveaux(self):
        try:
            with open(self.flux, "rb") as f:
                f.seek(self.position)
                brut = f.read()
        except OSError:
            return []
        fin = brut.rfind(b"\n")
        if fin < 0:
            return []
        self.position += fin + 1
        items = []
        for ligne in brut[:fin].decode("utf-8", "replace").splitlines():
            try:
                items.append(json.loads(ligne))
            except ValueError:
                continue
        return [i for i in items if isinstance(i, dict)]

    def _pousser(self, texte):
        item = json.dumps({"type": "statut", "texte": texte}, ensure_ascii=False)
        script = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              "append_flux.py")
        env = dict(os.environ, CONSEIL_RACINE=self.racine, PYTHONIOENCODING="utf-8")
        try:
            subprocess.run([sys.executable, script, "--pour", self.siege, item],
                           cwd=self.racine, env=env, capture_output=True, timeout=60,
                           **runtime._creation_sans_fenetre())
        except (OSError, subprocess.SubprocessError):
            pass  # un battement manque ne doit jamais faire tomber le tour

    def _tourner(self):
        dernier = time.time()
        noms = _noms(self.etat)
        while not self.arret.wait(SONDE):
            if any(_pour_lui(i, self.siege) and i.get("type") != "statut"
                   for i in self._nouveaux()):
                dernier = time.time()
            if time.time() - dernier >= self.periode and not self.arret.is_set():
                minutes = int(round((time.time() - self.debut) / 60.0))
                self._pousser(_texte(max(1, minutes), _dehors(self.debut, noms)))
                dernier = time.time()
