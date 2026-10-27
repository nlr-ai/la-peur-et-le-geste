# -*- coding: utf-8 -*-
"""ROUTEUR MESSAGE — chaque message joueur passe une fois par le narrateur.

Les dialogues et réponses ciblées suivent le même chemin que les gestes.
Le narrateur reçoit les mots exacts et leur destinataire éventuel ; le routeur
ne les distribue pas aux habitants de la pièce.

Les gestes et les modes de régie restent du ressort du MJ. Jump conserve sa
préparation dédiée. Aucun classement d'affaire ni appel de sélection ne se
place entre le joueur et les gens devant lui.
"""
import argparse
import json
import os
import uuid

from agents import chambre
from etat.expose import tables
from temps.expose import presence


import racines

# `.agents-runtime/` est un dossier de travail du DEPOT : les recus de
# routage ne suivent pas le monde joue.
RACINE = racines.DEPOT
ETAT = racines.etat()
SORTIES = os.path.join(RACINE, ".agents-runtime", "routages")


def est_une_parole(action):
    mode = str(action.get("mode") or "").casefold()
    genre = str(action.get("type") or "").casefold()
    return mode in ("dire", "parler") or genre == "parler"


def action_par_ref(personnage, ref):
    """Retrouve l'unique pièce d'inbox portant ``ref``."""
    dossier = os.path.join(ETAT, "inbox", str(personnage))
    trouves = []
    if os.path.isdir(dossier):
        for nom in sorted(os.listdir(dossier)):
            if not (nom.startswith("action-") and nom.endswith(".json")):
                continue
            chemin = os.path.join(dossier, nom)
            try:
                action = tables.lire(chemin, {})
            except (OSError, ValueError):
                continue
            if isinstance(action, dict) and str(action.get("ref") or "") == str(ref):
                trouves.append((chemin, action))
    if len(trouves) != 1:
        raise ValueError("ref %s trouvée %d fois dans l'inbox de %s" %
                         (ref, len(trouves), personnage))
    return trouves[0]


def _joueurs():
    donnees = tables.lire("joueurs.json", []) or []
    if isinstance(donnees, dict):
        donnees = donnees.get("joueurs") or []
    return {str(j.get("personnage_id") or j.get("id"))
            for j in donnees if isinstance(j, dict)
            and (j.get("personnage_id") or j.get("id"))}


def _date_du_joueur(personnage):
    horloges = tables.lire("horloges.json", {}) or {}
    monde = tables.lire("monde.json", {}) or {}
    return horloges.get(str(personnage)) or monde.get("date") or {
        "annee": 129, "lune": 1, "jour": 1, "minute": 0}


def _meme_piece(a, b):
    if a.get("salle") and b.get("salle"):
        return a.get("salle") == b.get("salle")
    return bool(a.get("lieu") and a.get("lieu") == b.get("lieu"))


def gens_presents(personnage, positions=None, joueurs=None):
    """Habitants non joueurs arrêtés dans la même pièce que le joueur."""
    personnage = str(personnage)
    positions = (presence.resoudre(_date_du_joueur(personnage))
                 if positions is None else positions)
    joueurs = _joueurs() if joueurs is None else set(joueurs)
    ici = (positions or {}).get(personnage)
    if not ici or ici.get("etat") == "en-chemin":
        return []
    resultat = []
    for pid, ou in sorted((positions or {}).items()):
        pid = str(pid)
        if (pid == personnage or pid in joueurs or not isinstance(ou, dict)
                or ou.get("etat") == "en-chemin" or not _meme_piece(ici, ou)):
            continue
        if chambre.existe(pid):
            resultat.append(pid)
    return resultat


def _ecrire_sortie(chemin, valeur):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    temporaire = chemin + ".%s.tmp" % uuid.uuid4().hex
    with open(temporaire, "w", encoding="utf-8", newline="\n") as flux:
        json.dump(valeur, flux, ensure_ascii=False, indent=2)
        flux.write("\n")
    os.replace(temporaire, chemin)


def chemin_sortie(personnage, ref):
    return os.path.join(SORTIES, str(personnage), "%s.json" % ref)


def _router_jump(personnage, ref, action, modele=None):
    from agents import jump, mj
    preparation = jump.preparer_scene(str(action.get("texte") or ""),
                                joueurs=sorted(_joueurs()))
    date_action = action.get("date_atteinte")
    if isinstance(date_action, dict) and all(
            k in date_action for k in ("annee", "lune", "jour", "minute")):
        preparation["depart"] = dict(date_action)
    routage = {
        "ref": ref,
        "decision": "jump",
        "jump": preparation,
        "consigne": (
            "PASSER : rejoins la prochaine scène d'intérêt selon le skill injecté. "
            "Les événements fournis sont des pistes, pas une cible imposée. "
            "Résume les transitions, avance réellement la date, puis ouvre une "
            "scène concrète et rends la main à la première décision du joueur."),
    }
    resultat = mj.appeler_mj(personnage, "", "JOUEUR", modele=modele,
                             refs=[ref], routage=routage)
    return {"mode": "jump", "mj": {"appele": True,
            "resultat": str(resultat or "")[-500:]}}


def _router_mj(personnage, ref, action, modele=None):
    from agents import mj
    routage = {
        "ref": ref,
        "decision": "direct",
        "destinataire_id": action.get("destinataire_id"),
        "consigne": ("Cette action arrive directement du joueur, sans sélection intermédiaire. "
                     "Aucun habitant n'a reçu ce message par le routeur. "
                     "S'il porte un destinataire_id, le joueur s'adresse à cette personne seule."),
    }
    if action.get("pilote_mode") == "pnjpj-journee":
        routage["mj_commun_journee"] = True
        routage["consigne"] += (
            " MODE PNJ-PJ JOURNEE : tu es le MJ commun des acteurs hors scène de ce monde. "
            "Croise leurs démarches avec les actes déjà établis et arbitre leurs conséquences. "
            "Traite la journée du demandeur en un ou deux messages, sans exiger des microgestes. "
            "Ta mémoire commune ne donne aucun savoir supplémentaire aux personnages. "
            "Respecte l'audience du siège demandeur et les délais de circulation des nouvelles. "
            "Ne fais pas avancer automatiquement les autres sièges ni le joueur humain.")
    if est_une_parole(action):
        routage["transmission_pnj"] = {
            "de": str(personnage), "ref": str(ref),
            "texte_exact": str(action.get("texte") or ""),
            "destinataire_id": action.get("destinataire_id"),
        }
        routage["consigne"] += (
            " APRES ta premiere tranche visible, joue directement la reponse "
            "et les gestes du PNJ depuis sa fiche, ses intentions et ses connaissances. "
            "Les mots du joueur restent exactement ceux de texte_exact. "
            "Respecte destinataire_id quand il est present. Aucun reveil autonome, "
            "aucune depeche ni transmission au parloir ne sont requis. "
            "Consigne la parole et les actes du PNJ puis publie-les dans le flux.")

    resultat = mj.appeler_mj(personnage, "", "JOUEUR", modele=modele,
                             refs=[ref], routage=routage)
    return {"mode": str(action.get("mode") or action.get("type") or "action"),
            "mj": {"appele": True,
                   "resultat": str(resultat or "")[-500:]}}


def router_ref(personnage, ref, modele=None):
    """Route une ref d'inbox et conserve un reçu hors fiction."""
    chemin_action, action = action_par_ref(personnage, ref)
    sortie = chemin_sortie(personnage, ref)
    document = {
        "version": "routage-presence/1",
        "joueur_id": str(personnage),
        "ref": str(ref),
        "action": os.path.abspath(chemin_action),
    }
    try:
        # Les réponses intermédiaires sont conservées dans l'inbox, mais
        # l'entretien ne réveille le MJ qu'après sa dernière question.
        question = str(action.get("demande_id") or "")
        if (question.startswith("michel-lucien-gouts-v1-")
                and question != "michel-lucien-gouts-v1-5"
                and action.get("reponse") != "expliquer"):
            document["routage"] = {"mode": "entretien", "mj": {
                "appele": False, "raison": "questionnaire en cours"}}
            _ecrire_sortie(sortie, document)
            return document
        mode = str(action.get("mode") or "").casefold()
        if mode == "jump":
            document["routage"] = _router_jump(personnage, ref, action,
                                                 modele=modele)
        else:
            document["routage"] = _router_mj(personnage, ref, action,
                                               modele=modele)
        _ecrire_sortie(sortie, document)
        return document
    except Exception as exc:
        document["erreur"] = "%s: %s" % (type(exc).__name__, str(exc))
        _ecrire_sortie(sortie, document)
        raise


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--de", required=True,
                    help="personnage du siège qui a posté")
    ap.add_argument("--ref", required=True,
                    help="référence exacte posée par POST /action")
    ap.add_argument("--modele", default=None)
    a = ap.parse_args(argv)
    print(json.dumps(router_ref(a.de, a.ref, modele=a.modele),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
