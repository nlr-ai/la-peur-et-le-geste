"""Relais techniques entre scènes : aucun fait ni horloge de fiction écrit ici."""
import json
import os
import time
import uuid
from contextlib import contextmanager
from pathlib import Path


def lire(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        return default


class Scenes:
    def __init__(self, racine):
        self.racine = Path(racine)
        self.dossier = self.racine / ".agents-runtime" / "scenes"

    @property
    def active(self):
        return bool(lire(self.dossier / "config.json", {}).get("active"))

    @contextmanager
    def verrou(self, nom="registre", timeout=1200):
        self.dossier.mkdir(parents=True, exist_ok=True)
        path = self.dossier / (nom + ".lock")
        limite = time.monotonic() + timeout
        while True:
            try:
                fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
                break
            except FileExistsError:
                if time.monotonic() >= limite:
                    raise RuntimeError("Scène occupée ; verrou conservé, réessayer après son retour.")
                time.sleep(.2)
        try:
            yield
        finally:
            path.unlink(missing_ok=True)

    def ecrire(self, nom, objet):
        self.dossier.mkdir(parents=True, exist_ok=True)
        target = self.dossier / nom
        tmp = target.with_suffix("." + uuid.uuid4().hex + ".tmp")
        tmp.write_text(json.dumps(objet, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, target)

    def activer(self):
        self.ecrire("config.json", {"active": True})

    def etat(self):
        return lire(self.dossier / "registre.json", {"relais": [], "communes": []})

    def physique(self, membres):
        etat = self.racine / "etat"
        presence = lire(etat / "presence.json", {}).get("presence", {})
        horloges = lire(etat / "horloges.json", {})
        joueurs = lire(etat / "joueurs.json", [])
        if isinstance(joueurs, dict):
            joueurs = joueurs.get("joueurs", [])
        occupes = {j["personnage_id"] for j in joueurs if j.get("occupe")}
        if not set(membres) <= occupes:
            raise ValueError("Un destinataire n'est pas un siège occupé.")
        positions = {m: presence.get(m, {}).get("salle") for m in membres}
        dates = {m: horloges.get(m) for m in membres}
        ok = (all(positions.values()) and len(set(positions.values())) == 1
              and all(dates.values()) and all(d == dates[membres[0]] for d in dates.values()))
        return {"compatible": bool(ok), "positions": positions, "horloges": dates}

    def proposer(self, de, a, dossier):
        if os.environ.get("LE_CONSEIL_SCENE") and os.environ["LE_CONSEIL_SCENE"] != de:
            raise ValueError("La session ne peut proposer au nom de l'autre scène.")
        if de == a:
            raise ValueError("Le relais exige deux scènes distinctes.")
        # Le dossier porte faits, actions en attente et savoirs séparés par PJ.
        for cle in ("faits", "actions_en_attente", "savoirs_par_joueur", "contraintes"):
            if cle not in dossier:
                raise ValueError("Dossier incomplet : " + cle)
        self.physique([de, a])
        with self.verrou():
            registre = self.etat()
            relais = {"id": uuid.uuid4().hex, "de": de, "a": a,
                      "statut": "propose", "dossier": dossier,
                      "instant_propose": self.physique([de, a])}
            registre["relais"].append(relais)
            self.ecrire("registre.json", registre)
            return relais

    def repondre(self, identifiant, de, pret, message):
        if os.environ.get("LE_CONSEIL_SCENE") and os.environ["LE_CONSEIL_SCENE"] != de:
            raise ValueError("La session ne peut accuser réception au nom de l'autre scène.")
        with self.verrou():
            registre = self.etat()
            relais = next(r for r in registre["relais"] if r["id"] == identifiant)
            if relais["a"] != de or relais["statut"] not in ("propose", "a_preparer"):
                raise ValueError("Seul le destinataire répond à un relais encore ouvert.")
            membres = [relais["de"], de]
            physique = self.physique(membres)
            relais["reponse"] = {"de": de, "pret": pret, "message": message,
                                  "physique": physique}
            if pret and not physique["compatible"]:
                raise ValueError("Fusion refusée : lieux ou horloges différents ; jouer le rattrapage puis répondre.")
            if pret and any(p["a"] in membres and p["statut"] in ("envoyee", "a_completer")
                            for p in registre.get("passations", [])):
                raise ValueError("Recevoir les passations privées avant une nouvelle fusion.")
            relais["statut"] = "fusionne" if pret else "a_preparer"
            if pret:
                if any(set(c["membres"]) & set(membres) for c in registre["communes"]):
                    raise ValueError("Un siège appartient déjà à une scène commune.")
                registre["communes"].append({"id": identifiant, "membres": membres,
                    "responsable": relais["de"], "salle": physique["positions"][de],
                    "debut_flux": len((self.racine / "etat" / "flux.jsonl").read_text(encoding="utf-8").splitlines())
                        if (self.racine / "etat" / "flux.jsonl").exists() else 0})
            self.ecrire("registre.json", registre)
            return relais

    def separer(self, identifiant, raison=None, dossiers=None):
        if not raison or not raison.strip():
            raise ValueError("La team se suit par défaut : une séparation exige une raison explicite (choix PJ ou empêchement constaté).")
        with self.verrou():
            registre = self.etat()
            if not any(c["id"] == identifiant for c in registre["communes"]):
                raise ValueError("Scène commune inconnue.")
            scene = next(c for c in registre["communes"] if c["id"] == identifiant)
            identite = os.environ.get("LE_CONSEIL_SCENE")
            if identite and identite != scene["responsable"]:
                raise ValueError("Seul le MJ responsable du duo prépare la séparation.")
            if dossiers is not None and (not isinstance(dossiers, dict) or set(dossiers) != set(scene["membres"])):
                raise ValueError("Un dossier distinct est requis pour chaque membre, sans destinataire supplémentaire.")
            from passations_scenes import dossier_sortie
            relais = next(r for r in registre["relais"] if r["id"] == identifiant)
            passations = []
            for membre in scene["membres"]:
                passations.append({"id": uuid.uuid4().hex, "scene_source": identifiant,
                    "de": scene["responsable"], "a": membre, "statut": "envoyee",
                    "dossier": dossier_sortie(self.racine, scene, membre, raison, relais,
                                               (dossiers or {}).get(membre))})
            registre.setdefault("passations", []).extend(passations)
            registre["communes"] = [c for c in registre["communes"] if c["id"] != identifiant]
            relais["statut"] = "separe"
            relais["raison_separation"] = raison
            self.ecrire("registre.json", registre)
            return passations

    def recevoir(self, identifiant, de, pret, message):
        """Chaque session privée accuse elle-même réception de son dossier."""
        identite = os.environ.get("LE_CONSEIL_SCENE")
        if identite and identite != de:
            raise ValueError("La session ne peut recevoir au nom de l'autre MJ privé.")
        if not message or not message.strip():
            raise ValueError("Un accusé ou une demande de complément explicite est nécessaire.")
        with self.verrou():
            registre = self.etat()
            passage = next(p for p in registre.get("passations", []) if p["id"] == identifiant)
            if passage["a"] != de:
                raise ValueError("Seul le MJ destinataire peut recevoir cette passation.")
            if passage["statut"] == "recue":
                return passage  # accusé idempotent
            if passage["statut"] not in ("envoyee", "a_completer"):
                raise ValueError("Passation fermée.")
            passage["accuse"] = {"de": de, "pret": bool(pret), "message": message}
            passage["statut"] = "recue" if pret else "a_completer"
            self.ecrire("registre.json", registre)
            return passage

    def passations_non_recues(self, joueur):
        return [p for p in self.etat().get("passations", []) if p["a"] == joueur
                and p["statut"] in ("envoyee", "a_completer")]

    def completer(self, identifiant, de, bilan):
        identite = os.environ.get("LE_CONSEIL_SCENE")
        if identite and identite != de:
            raise ValueError("La session ne peut compléter au nom d'un autre MJ.")
        with self.verrou():
            registre = self.etat()
            p = next(p for p in registre.get("passations", []) if p["id"] == identifiant)
            if p["de"] != de or p["statut"] not in ("envoyee", "a_completer"):
                raise ValueError("Seul le MJ émetteur complète une passation ouverte.")
            p["dossier"]["bilan_du_mj_duo"] = bilan
            p["statut"] = "envoyee"
            self.ecrire("registre.json", registre)
            return p

    def suivre_mouvement(self, membres, salle):
        """Le groupe change de salle sans perdre son responsable ni son accord."""
        if not salle:
            return
        with self.verrou():
            registre = self.etat()
            for scene in registre["communes"]:
                if set(scene["membres"]) == set(membres):
                    scene["salle"] = salle
                    self.ecrire("registre.json", registre)
                    return

    def reprendre(self, identifiant, raison):
        """Rétablir un accord réel antérieur après une séparation indue."""
        if not raison:
            raise ValueError("La reprise exige une raison explicite.")
        with self.verrou():
            registre = self.etat()
            relais = next(r for r in registre["relais"] if r["id"] == identifiant)
            if not relais.get("reponse", {}).get("pret"):
                raise ValueError("Pas d'accord réel antérieur à reprendre.")
            membres = [relais["de"], relais["a"]]
            physique = self.physique(membres)
            if not physique["compatible"]:
                raise ValueError("Reprise impossible : positions ou heures différentes.")
            if any(set(c["membres"]) & set(membres) for c in registre["communes"]):
                raise ValueError("Un siège appartient déjà à une scène commune.")
            # Conserver le responsable désigné dans l'accord initial.
            responsable = relais.get("responsable", relais["de"])
            relais["statut"] = "fusionne"
            for p in registre.get("passations", []):
                if p["scene_source"] == identifiant and p["statut"] in ("envoyee", "a_completer"):
                    p["statut"] = "annulee"
            relais.setdefault("reprises", []).append({"raison": raison, "physique": physique})
            flux = self.racine / "etat" / "flux.jsonl"
            registre["communes"].append({"id": identifiant, "membres": membres,
                "responsable": responsable, "salle": physique["positions"][membres[0]],
                "debut_flux": len(flux.read_text(encoding="utf-8").splitlines()) if flux.exists() else 0})
            self.ecrire("registre.json", registre)

    def responsable(self, joueur):
        for scene in self.etat()["communes"]:
            if joueur in scene["membres"]:
                if not self.physique(scene["membres"])["compatible"]:
                    raise ValueError("Scène commune désynchronisée : séparer avant de continuer.")
                return scene["responsable"]
        return joueur

    def audience(self, joueur, locuteur=None, ref=None):
        """Une réponse à une parole publique suit sa scène ; une question reste privée."""
        if not self.active:
            return joueur
        for scene in self.etat()["communes"]:
            if joueur not in scene["membres"] or not self.physique(scene["membres"])["compatible"]:
                continue
            if locuteur:
                presence = lire(self.racine / "etat" / "presence.json", {}).get("presence", {})
                if presence.get(locuteur, {}).get("salle") != scene["salle"]:
                    return joueur
                if not ref:
                    return joueur
                flux = self.racine / "etat" / "flux.jsonl"
                origine = next((json.loads(l) for l in flux.read_text(encoding="utf-8").splitlines()[scene.get("debut_flux", 0):]
                               if l.strip() and json.loads(l).get("ref") == ref), None)
                if not origine or origine.get("type") != "vous":
                    return joueur
                if not isinstance(origine.get("pour"), list) or not set(scene["membres"]) <= set(origine["pour"]):
                    return joueur
            return sorted(scene["membres"])
        return joueur

    def brief(self, joueur):
        registre = self.etat()
        # Une session redevenue privée reçoit seulement sa projection des savoirs.
        prive = not any(joueur in c["membres"] for c in registre["communes"])
        relais = []
        for r in registre["relais"]:
            if joueur not in (r["de"], r["a"]):
                continue
            copie = json.loads(json.dumps(r))
            if r["statut"] in ("separe", "annule"):
                # Clos : son dossier a déjà servi, seule sa trace reste utile.
                copie = {k: r[k] for k in ("id", "de", "a", "statut",
                         "raison_separation", "raison_annulation") if k in r}
            if prive and "dossier" in r and r["statut"] not in ("propose", "a_preparer"):
                copie["dossier"] = {"savoirs_par_joueur": {
                    joueur: r["dossier"].get("savoirs_par_joueur", {}).get(joueur, [])}}
            relais.append(copie)
        # Une passation reçue a été lue et accusée : la recopier entière à
        # chaque réveil coûtait 20 à 30 ko par tour. Sa trace suffit.
        passations = [p if p["statut"] in ("envoyee", "a_completer") else
                      {"id": p["id"], "scene_source": p.get("scene_source"),
                       "de": p["de"], "a": p["a"], "statut": p["statut"],
                       "raison_separation": (p.get("dossier") or {}).get("raison_separation")}
                      for p in registre.get("passations", []) if p["a"] == joueur][-5:]
        return {"scene_responsable": self.responsable(joueur),
                "passations_privees": passations,
                "complements_demandes": [p for p in registre.get("passations", [])
                    if p["de"] == joueur and p["a"] != joueur and p["statut"] == "a_completer"],
                "communes": [c for c in registre["communes"] if joueur in c["membres"]],
                "relais": relais[-5:]}
