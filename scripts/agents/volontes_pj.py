"""Suivi technique des volontés déclarées : le MJ constate, il ne choisit pas pour les PJ."""
import argparse
import json
import os
import time
import uuid
from pathlib import Path
from racines import racine
from scenes_partagees import Scenes, lire

class Volontes:
    def __init__(self, monde):
        self.monde = Path(monde)
        self.scenes = Scenes(monde)
        self.path = self.monde / ".agents-runtime/mj/volontes-pj.json"

    def registre(self):
        return lire(self.path, {"tour": 0, "volontes": []})

    def ecrire(self, registre):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix("." + uuid.uuid4().hex + ".tmp")
        tmp.write_text(json.dumps(registre, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, self.path)

    def source(self, joueur, ref):
        path = self.monde / "etat/flux.jsonl"
        for ligne in path.read_text(encoding="utf-8").splitlines():
            item = json.loads(ligne)
            if item.get("ref") == ref and item.get("type") == "vous" and item.get("joueur_id") == joueur:
                return item["texte"]
        raise ValueError("La volonté doit citer une parole ou action réellement déclarée par ce PJ.")

    def poser(self, joueur, ref, objectif):
        source = self.source(joueur, ref)
        with self.scenes.verrou("volontes"):
            r = self.registre()
            if any(v["source_ref"] == ref for v in r["volontes"]):
                raise ValueError("Cette volonté est déjà enregistrée ; actualiser sa progression.")
            v = {"id": ref, "joueur": joueur, "source_ref": ref, "mots_du_joueur": source,
                 "objectif": objectif, "statut": "active", "sans_progression": 0,
                 "tour_progression": r["tour"], "cree_a": time.time(), "preuves": []}
            r["volontes"].append(v)
            self.ecrire(r)
            return v

    def declarer(self, joueur, ref, resume):
        """Ce que le PJ a dit de lui-même et qui doit survivre à toute
        compaction : identité donnée, qui il rejoint, ce qu'il a raconté."""
        source = self.source(joueur, ref)
        if not (resume or "").strip():
            raise ValueError("--resume est nécessaire.")
        with self.scenes.verrou("volontes"):
            r = self.registre()
            decl = r.setdefault("declarations", [])
            if any(d["ref"] == ref for d in decl):
                raise ValueError("Cette déclaration est déjà enregistrée.")
            d = {"joueur": joueur, "ref": ref, "mots_du_joueur": source,
                 "resume": resume.strip(), "cree_a": time.time()}
            decl.append(d)
            self.ecrire(r)
            return d

    def objectifs(self, joueur):
        path = self.monde / "etat/joueurs" / joueur / "objectifs.json"
        try:
            liste = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return []
        return [o for o in liste if isinstance(o, dict)
                and o.get("statut", "en-cours") == "en-cours"]

    def actualiser(self, identifiant, statut, preuve, ref=None):
        if statut not in {"active", "bloquee", "attente_joueur", "atteinte", "abandonnee"} or not preuve.strip():
            raise ValueError("Statut valide et constat concret nécessaires.")
        with self.scenes.verrou("volontes"):
            r = self.registre()
            v = next(v for v in r["volontes"] if v["id"] == identifiant)
            if statut == "abandonnee":
                if ref == v["source_ref"]:
                    raise ValueError("L'abandon exige une nouvelle déclaration du joueur.")
                self.source(v["joueur"], ref)
            v["statut"] = statut
            v["preuves"].append({"constat": preuve, "ref": ref, "tour": r["tour"]})
            if statut != "bloquee":
                v["tour_progression"] = r["tour"]
                v["sans_progression"] = 0
            self.ecrire(r)
            return v

    def debut_tour(self, joueurs):
        with self.scenes.verrou("volontes"):
            r = self.registre()
            r["tour"] += 1
            for v in r["volontes"]:
                if v["joueur"] in joueurs and v["statut"] in ("active", "bloquee"):
                    v["sans_progression"] += 1
            self.ecrire(r)
        return self.brief(joueurs)

    def brief(self, joueurs):
        r = self.registre()
        volontes = [v for v in r["volontes"] if v["joueur"] in joueurs and v["statut"] not in ("atteinte", "abandonnee")]
        return {"volontes": volontes, "a_debloquer": [v["id"] for v in volontes
            if v["statut"] in ("active", "bloquee") and v["sans_progression"] >= 2],
            # Permanent : ni atteint ni compacte. C'est la memoire longue du
            # MJ sur ce que chaque PJ a dit de lui-meme et sur ses buts.
            "declarations": [d for d in r.get("declarations", [])
                             if d["joueur"] in joueurs],
            "objectifs": {j: self.objectifs(j) for j in joueurs}}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("operation", choices=["etat", "poser", "actualiser", "declarer"])
    p.add_argument("--joueur")
    p.add_argument("--ref")
    p.add_argument("--objectif")
    p.add_argument("--id")
    p.add_argument("--statut")
    p.add_argument("--preuve", default="")
    p.add_argument("--resume", default="")
    a = p.parse_args()
    v = Volontes(racine())
    if a.operation == "poser":
        if not a.objectif:
            p.error("--objectif est nécessaire")
        result = v.poser(a.joueur, a.ref, a.objectif)
    elif a.operation == "declarer":
        result = v.declarer(a.joueur, a.ref, a.resume)
    elif a.operation == "actualiser":
        result = v.actualiser(a.id, a.statut, a.preuve, a.ref)
    else:
        result = v.registre()
    print(json.dumps(result, ensure_ascii=False, indent=2))
