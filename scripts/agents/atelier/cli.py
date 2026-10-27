"""Commandes lisibles de l'atelier, sans lancement implicite de PNJ."""
import argparse
import json
import sys

from agents.atelier import catalogue


def main(argv=None):
    p = argparse.ArgumentParser(description="Atelier de developpement de Barralfond")
    s = p.add_subparsers(dest="action", required=True)
    s.add_parser("equipe", help="Les noms et les responsabilites")
    for nom in ("dossier", "resultat", "historique", "essayer"):
        a = s.add_parser(nom)
        a.add_argument("item", choices=["90312"])
        a.add_argument("--json", action="store_true", help="Resultat structure complet")
        if nom == "essayer":
            a.add_argument("--profil", choices=catalogue.PROFILS, default="court")
            a.add_argument("--effectif", type=int)
            a.add_argument("--duree", type=float)
            a.add_argument("--limite", type=float, help="Secondes reelles maximum par variante")
            a.add_argument("--serveur", default="http://localhost:3129")
    args = p.parse_args(argv)
    try:
        if args.action == "equipe":
            for qui, (nom, role) in catalogue.EQUIPE.items():
                print(f"{nom} ({qui})\n  {role}")
            return 0
        if args.action == "dossier":
            resultat = {**catalogue.dossier(args.item), "dernier_essai": catalogue.dernier()}
        elif args.action == "resultat":
            resultat = catalogue.dernier() or {"statut": "aucun_essai", "conclusion": "Aucun essai de cet atelier."}
        elif args.action == "historique":
            resultat = catalogue.historique()
        else:
            from agents.atelier.essais import essayer
            resultat = essayer(args.profil, args.effectif, args.duree, args.limite,
                                args.serveur, annoncer=lambda t: print(t, file=sys.stderr, flush=True))
        if args.json:
            print(json.dumps(resultat, ensure_ascii=False, indent=2))
        else:
            afficher(resultat)
        if args.action == "essayer" and resultat["statut"] != "mesure_obtenue":
            return 1
        return 0
    except (OSError, ValueError, RuntimeError) as e:
        print(str(e), file=sys.stderr)
        return 2


def afficher(r):
    if "item_canonique" in r:
        print(r["nom"] + " — item " + r["item"])
        print("Affaire : " + r["affaire"])
        print("Source : " + r["cahier"])
        print("Code : " + r["source_code"])
        print(r["resultat_attendu"])
        print(r["portee"])
        if r.get("dernier_essai"):
            afficher(r["dernier_essai"])
        return
    if isinstance(r, list):
        for essai in r:
            demande = essai["demande"]
            print(f"\n{demande['effectif']} hommes demandes / {demande['duree_simulee_s']} s simulees")
            afficher(essai)
        return
    noms = {"mesure_obtenue": "Mesures obtenues", "echec": "Échec de l'essai",
            "delai_depasse": "Durée limite atteinte", "sans_resultat_final": "En cours ou interrompu",
            "aucun_essai": "Aucun essai"}
    print("État : " + noms.get(r["statut"], r["statut"]))
    print(r["conclusion"])
    for nom, variante in r.get("variantes", {}).items():
        mesure = variante.get("resultat")
        if mesure:
            print(f"{nom} : {mesure['duree_simulee_s']} s simulees, "
                  f"{mesure['ralliements']} ralliements, {mesure['morts']} morts, "
                  f"{mesure['appels_arbitre']} appels a l'arbitre, "
                  f"{mesure['decisions_ralliement']} decisions de ralliement.")
        else:
            print(nom + " : " + variante.get("derniere_etape", "aucun resultat"))
    if r.get("ecarts_arbitre_moins_temoin") is not None:
        print("Ecarts : " + json.dumps(r["ecarts_arbitre_moins_temoin"], ensure_ascii=False))
    if r.get("dossier_essai"):
        print("Preuves : " + r["dossier_essai"])
