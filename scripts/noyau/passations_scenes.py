"""Dossiers de sortie : copies sourcées, projetées pour un seul joueur."""
import json
from pathlib import Path

from scenes_partagees import lire


def dossier_sortie(monde, scene, joueur, raison, relais, complement=None):
    monde = Path(monde)
    etat = monde / "etat"
    flux = etat / "flux.jsonl"
    lignes = flux.read_text(encoding="utf-8").splitlines() if flux.exists() else []
    vecu = []
    for ligne in lignes[scene.get("debut_flux", 0):]:
        if not ligne.strip():
            continue
        item = json.loads(ligne)
        audience = item.get("pour")
        if audience == joueur or isinstance(audience, list) and joueur in audience:
            vecu.append(item)
    actions = []
    for path in sorted((etat / "inbox" / joueur).glob("action-*.json")):
        actions.append(lire(path))
    suivi = lire(monde / ".agents-runtime/mj/volontes-pj.json", {})
    return {
        "joueur": joueur, "raison_separation": raison,
        "position": lire(etat / "presence.json", {}).get("presence", {}).get(joueur),
        "horloge": lire(etat / "horloges.json", {}).get(joueur),
        "faits_vecus": vecu,
        "savoirs_initiaux": relais.get("dossier", {}).get("savoirs_par_joueur", {}).get(joueur, []),
        "volontes": [v for v in suivi.get("volontes", []) if v.get("joueur") == joueur],
        "actions_en_attente": actions,
        "contraintes": ["Les items copiés sont déjà affichés : ne pas les republier.",
                        "Vérifier les effets des références avant de rejouer une action d'inbox.",
                        "Le dossier de l'autre PJ et ses secrets ne sont pas transmis.",
                        "La réception technique ne crée aucune parole ni connaissance du personnage."],
        "bilan_du_mj_duo": complement or {},
        "sources": {"flux_debut": scene.get("debut_flux", 0), "flux_fin": len(lignes),
                    "scene_commune": scene["id"]},
    }
