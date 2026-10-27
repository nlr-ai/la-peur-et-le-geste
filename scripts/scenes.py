"""Commande de relais hors fiction, isolée par monde."""
import argparse
import json
import sys
import subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "noyau"))
from racines import racine
from scenes_partagees import Scenes

def notifier(scenes, joueur, identifiant, message):
    from racines import DEPOT
    log = scenes.dossier / (identifiant + ".log")
    with log.open("a", encoding="utf-8") as sortie:
        worker = subprocess.Popen([sys.executable, str(Path(DEPOT) / "scripts/reveiller.py"),
            "--de", joueur, message], cwd=DEPOT, stdout=sortie, stderr=subprocess.STDOUT,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    return worker.pid

def main():
    p = argparse.ArgumentParser()
    p.add_argument("operation", choices=["activer", "etat", "proposer", "repondre", "separer", "recevoir", "completer"])
    p.add_argument("--de")
    p.add_argument("--a")
    p.add_argument("--id")
    p.add_argument("--dossier")
    p.add_argument("--pret", action="store_true")
    p.add_argument("--message", default="")
    p.add_argument("--raison")
    p.add_argument("--sans-reveil", action="store_true")
    args = p.parse_args()
    scenes = Scenes(racine())
    if args.operation == "activer":
        scenes.activer()
        result = {"active": True}
    elif args.operation == "etat":
        result = scenes.etat()
    elif args.operation == "proposer":
        result = scenes.proposer(args.de, args.a, json.loads(Path(args.dossier).read_text(encoding="utf-8-sig")))
        if not args.sans_reveil:
            from racines import DEPOT
            log = scenes.dossier / (result["id"] + ".log")
            with log.open("w", encoding="utf-8") as sortie:
                worker = subprocess.Popen([sys.executable, str(Path(DEPOT) / "scripts" / "reveiller.py"),
                    "--de", args.a, "Relais technique reçu : " + result["id"] +
                    ". Lis le dossier dans le brief et réponds depuis ta scène. "
                    "Si les heures diffèrent, réponds préparation nécessaire ; ne les aligne pas artificiellement."],
                    cwd=DEPOT, stdout=sortie, stderr=subprocess.STDOUT)
            result["notification_pid"] = worker.pid
    elif args.operation == "repondre":
        result = scenes.repondre(args.id, args.de, args.pret, args.message)
        if not args.sans_reveil:
            result["notification_pid"] = notifier(scenes, result["de"], result["id"],
                "Réponse technique reçue pour ton relais " + result["id"] + ": " + args.message +
                ". Lis le relais actualisé dans le brief avant de poursuivre. "
                "Intègre son statut et les contraintes nouvelles ; ne rejoue pas les faits déjà publiés. "
                "Ce message est entre MJ, pas une parole de personnage.")
    elif args.operation == "recevoir":
        result = scenes.recevoir(args.id, args.de, args.pret, args.message)
        if not args.pret and not args.sans_reveil:
            result["notification_pid"] = notifier(scenes, result["de"], result["id"],
                "Complément demandé pour ta passation " + result["id"] + ": " + args.message +
                ". Lis complements_demandes dans le brief. Complète le dossier par "
                "scripts/scenes.py completer --de <toi> --id <passation> --dossier <bilan.json>. "
                "Ce réveil est technique, ne rejoue pas une scène.")
        elif not args.sans_reveil and result["de"] != result["a"]:
            result["notification_pid"] = notifier(scenes, result["de"], result["id"],
                "Passation " + result["id"] + " reçue par la scène " + result["a"] + ": " + args.message +
                ". Lis son accusé dans le registre. Intègre ce résultat sans publier une scène "
                "ni envoyer un simple accusé en retour.")
    elif args.operation == "completer":
        result = scenes.completer(args.id, args.de,
            json.loads(Path(args.dossier).read_text(encoding="utf-8-sig")))
        if not args.sans_reveil:
            result["notification_pid"] = notifier(scenes, result["a"], result["id"],
                "Ta passation " + result["id"] + " a été complétée. Lis ton dossier et "
                "accuse réception avec scripts/scenes.py recevoir avant de reprendre le jeu.")
    else:
        dossiers = json.loads(Path(args.dossier).read_text(encoding="utf-8-sig")) if args.dossier else None
        result = scenes.separer(args.id, args.raison, dossiers)
        if not args.sans_reveil:
            from racines import DEPOT
            for passage in result:
                log = scenes.dossier / (passage["id"] + ".log")
                with log.open("w", encoding="utf-8") as sortie:
                    worker = subprocess.Popen([sys.executable, str(Path(DEPOT) / "scripts/reveiller.py"),
                        "--de", passage["a"], "Passation de séparation reçue : " + passage["id"] +
                        ". Lis TON dossier dans passations_privees du brief, puis accuse réception "
                        "avec scripts/scenes.py recevoir --de " + passage["a"] +
                        " --id " + passage["id"] + " --pret --message <bilan>. "
                        "Si une pièce manque, réponds sans --pret en précisant laquelle. "
                        "Ne rejoue aucun fait déjà affiché, ne publie pas de scène pour ce réveil technique."],
                        cwd=DEPOT, stdout=sortie, stderr=subprocess.STDOUT,
                        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                passage["notification_pid"] = worker.pid
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
