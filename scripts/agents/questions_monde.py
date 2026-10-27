"""Consultation factuelle du MJ, distincte d'un tour joueur pour éviter le blocage imbriqué."""
import json
import os
import re
import tempfile
import uuid
from pathlib import Path
from racines import racine, DEPOT
from scenes_partagees import Scenes, lire

MANUEL = """Tu es le MJ consulté par un PNJ sur un fait manquant du monde.
Cette consultation technique est explicitement autorisée, malgré l'ancien
interdit de demander des informations au MJ. Réponds sur les faits, routes,
institutions, propriétés et limites de ce que le PNJ peut définir.
Lis les sources canoniques et docs/schema.md avant toute écriture. Un fait
établi prime. Si le détail manque et relève du MJ, définis-le de manière
cohérente, consigne-le dans la table ou le canon approprié, puis cite la source.
Ne transforme pas une supposition en fait écrit. Ne modifie pas docs/schema.md.
Ne joue ni PNJ ni PJ, ne décide pas à leur place, ne pousse rien au flux,
ne touche ni aux horloges, ni aux présences, ni aux inbox, ni aux relais.
Ne livre aucun secret auquel l'habitant n'a accès : distingue vérité du monde
et connaissance de cet habitant. Si c'est caché, indique une source à chercher.
Une demande de permission ou de décision reste à la charge du PNJ ; explique-le.
Rends une réponse utile, sourcée, avec ce qui est établi et ce qui reste inconnu.
N'appelle aucune autre session MJ ou PNJ. Aucun exemple Westeros ne vaut dans
un autre monde. La consultation est hors fiction, jamais une voix entendue.
"""

def demander(de, question, modele=None, contexte_id=None, ref=None):
    if not re.fullmatch(r"[a-z0-9][a-z0-9_.-]*", de or "") or not question.strip():
        raise ValueError("Identité PNJ et question nécessaires.")
    monde = Path(racine())
    if not lire(monde / ".agents-runtime/questions-monde.json", {}).get("pnj_autorises"):
        raise ValueError("Consultations PNJ non activées dans ce monde.")
    gens = lire(monde / "etat/personnages.json", [])
    if isinstance(gens, dict):
        gens = gens.get("personnages", [])
    fiche = next((p for p in gens if p.get("id") == de), None)
    if not fiche:
        raise ValueError("PNJ inconnu du monde courant.")
    joueurs = lire(monde / "etat/joueurs.json", [])
    if any(j.get("personnage_id") == de and j.get("occupe") for j in joueurs):
        raise ValueError("Un joueur utilise son canal joueur.")
    identite = os.environ.get("LE_CONSEIL_QUI")
    if identite and identite not in (de, "mj", "dev"):
        raise ValueError("La session ne peut parler au nom d'un autre PNJ.")
    from agents import runtime, billet
    # Pas de verrou de tour : ce tour peut précisément attendre le PNJ.
    with Scenes(monde).verrou("questions-monde"):
        billet.deposer(de, "mj", "[QUESTION MONDE — HORS FICTION] " + question,
                       contexte_id=contexte_id, ref=ref)
        cle = str(uuid.uuid5(uuid.NAMESPACE_URL, str(monde) + "/questions/" + de + "/" +
                            question + "/" + str(ref or "") + "/" + str(contexte_id or "")))
        cible = monde / ".agents-runtime/questions-monde" / (cle + ".json")
        ancien = lire(cible)
        if ancien:
            return ancien["reponse"]
        rep = runtime.appeler(role="mj", manuel=MANUEL,
            message=json.dumps({"monde": str(monde), "demandeur": fiche,
                "question": question, "contexte_id": contexte_id,
                "instructions_locales": [str(monde / "AGENTS.md"), str(monde / "manuel.md")],
                "consigne": "L'autorisation factuelle ci-dessus prime sur l'ancien interdit PNJ→MJ."}, ensure_ascii=False),
            session_id=str(uuid.uuid5(uuid.NAMESPACE_URL, str(monde) + "/mj/consultation-faits/" + de)),
            modele=modele, timeout=None,
            cwd=os.path.join(tempfile.gettempdir(), "le-conseil-mj-faits"),
            add_dirs=[str(monde), DEPOT], tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
            env={"CONSEIL_RACINE": str(monde), "LE_CONSEIL_SCENE": "", "LE_CONSEIL_REF": ""})
        reponse = (rep.get("result") or "").strip()
        if not reponse:
            raise RuntimeError("Consultation sans réponse ; question laissée ouverte.")
        cible.parent.mkdir(parents=True, exist_ok=True)
        tmp = cible.with_suffix(".tmp")
        tmp.write_text(json.dumps({"de": de, "question": question, "reponse": reponse,
            "contexte_id": contexte_id, "ref": ref}, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, cible)
        billet.deposer("mj", de, "[REPONSE MONDE — HORS FICTION] " + reponse,
                       contexte_id=contexte_id, ref=ref)
        return reponse
