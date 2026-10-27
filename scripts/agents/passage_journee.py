"""Un passage demandé explicitement : préparation, pilotes, notification au MJ joueur."""
import json
import os
import subprocess
import sys
from pathlib import Path


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--dossier", required=True)
    ap.add_argument("--joueur", default="michel")
    ap.add_argument("--port", type=int, default=3212)
    a = ap.parse_args()
    from agents import mj
    depot = Path(__file__).resolve().parents[2]
    monde = Path(os.environ["CONSEIL_RACINE"])
    dossier = Path(a.dossier).resolve()
    dossier.mkdir(parents=True, exist_ok=True)
    manifeste = dossier / "selection.json"
    statut = {"phase": "selection", "resultats": []}
    def sauver():
        (dossier / "statut.json").write_text(json.dumps(statut, ensure_ascii=False, indent=2), encoding="utf-8")
    sauver()
    consigne = (depot / "scripts/agents/prompts/passage-journee.md").read_text(encoding="utf-8")
    try:
        mj.appeler_mj(a.joueur, consigne + "\nManifest à écrire : " + str(manifeste), "POST",
                      routage={"mj_commun_journee": True, "preparation_passage": True})
        choix = json.loads(manifeste.read_text(encoding="utf-8-sig"))
        roster = json.loads((monde / "etat/joueurs.json").read_text(encoding="utf-8-sig"))
        humains = {p["personnage_id"] for p in roster if p.get("occupe")}
        personnages = {p["id"] for p in json.loads((monde / "etat/personnages.json").read_text(encoding="utf-8-sig"))}
        selection = choix["acteurs"]
        ids = [x["id"] for x in selection]
        if len(ids) != len(set(ids)) or any(i not in personnages or i in humains for i in ids):
            raise ValueError("Sélection invalide : doublon, personnage absent ou siège humain.")
        if any(not x.get("motif") or x.get("messages") not in (1, 2) for x in selection):
            raise ValueError("Chaque acteur doit avoir un motif et 1 ou 2 messages.")
        for x in selection:
            ident = x["id"]
            if not (monde / "chambres" / ident / "joueur.md").is_file():
                raise ValueError("Point de vue manquant : " + ident)
        statut["selection"] = selection
        for x in selection:
            ident = x["id"]
            statut.update(phase="pilotes", acteur=ident)
            sauver()
            with (dossier / (ident + ".log")).open("w", encoding="utf-8") as log:
                retour = subprocess.run([sys.executable, str(depot / "scripts/joueur_pnj.py"),
                    "--monde", monde.name, "--qui", ident, "--port", str(a.port),
                    "--journee", "--messages", str(x["messages"])], cwd=depot,
                    stdout=log, stderr=subprocess.STDOUT)
            statut["resultats"].append({"id":ident, "code":retour.returncode})
            sauver()
        statut["phase"] = "notification"
        sauver()
        message = ("BILAN DU PASSAGE HORS SCENE demandé par le joueur. Lis " + str(manifeste) +
                   " et " + str(dossier / "statut.json") + ". Vérifie les actes réellement persistés et les journaux des pilotes dans ce dossier. "
                   "Intègre les conséquences à la continuité de Michel ; ne lui révèle que les nouvelles qui peuvent lui parvenir, avec leurs délais. "
                   "Ne rejoue aucun acteur, ne relance aucun passage. Signale les échecs dans ton suivi hors fiction. "
                   "N'avance pas automatiquement l'horloge de Michel et ne consomme pas son action en attente.")
        mj.appeler_mj(a.joueur, message, "POST")
        statut["phase"] = "termine"
        sauver()
    except Exception as e:
        statut.update(phase="echec", erreur=str(e))
        sauver()
        raise
