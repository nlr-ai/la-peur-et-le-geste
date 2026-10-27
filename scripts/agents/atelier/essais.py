"""Une comparaison conserve ses entrees et toutes ses sorties, meme en echec."""
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import time
import uuid

from agents import runtime, work_identity
from agents.atelier import catalogue
from agents.atelier.processus import executer, verrou


def ecrire(chemin, valeur):
    temporaire = chemin.with_suffix(".tmp")
    temporaire.write_text(json.dumps(valeur, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporaire.replace(chemin)


def empreintes(racine):
    return {p.relative_to(racine).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(racine.rglob("*")) if p.is_file() and p.suffix in (".js", ".json")}


def figer(dossier):
    source = catalogue.RACINE / catalogue.SOURCE / "ecrans/modules"
    avant = empreintes(source)
    if not avant:
        raise ValueError("Les sources de l'essai sont absentes.")
    destination = dossier / "source/ecrans/modules"
    for nom in avant:
        cible = destination / nom
        cible.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / nom, cible)
    if avant != empreintes(source) or avant != empreintes(destination):
        raise ValueError("Sources modifiees pendant la copie ; recommencer l'essai.")
    banc = dossier / "comparer-ralliement.js"
    shutil.copyfile(catalogue.RACINE / catalogue.BANC, banc)
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=catalogue.RACINE,
                              capture_output=True, text=True, check=True).stdout.strip()
    return {"depot": str(catalogue.RACINE), "revision": revision,
            "origine": str(source), "copie": str(destination), "fichiers": avant,
            "banc_sha256": hashlib.sha256(banc.read_bytes()).hexdigest()}


def verifier_sortie(r, variante, effectif, duree):
    if not isinstance(r, dict) or r.get("version") != "resultat-ralliement/1":
        raise ValueError("Sortie absente ou format de resultat inconnu.")
    if r.get("variante") != variante or r.get("effectif_demande") != effectif:
        raise ValueError("La sortie ne correspond pas a la variante ou a l'effectif demande.")
    for cle in ("duree_simulee_s", "duree_demandee_s", "effectif_observe", "appels_arbitre",
                "appels_ralliement", "decisions_ralliement", "ralliements", "morts", "blesses", "fuyards"):
        n = r.get(cle)
        if isinstance(n, bool) or not isinstance(n, (int, float)) or not math.isfinite(n) or n < 0:
            raise ValueError(f"Mesure invalide : {cle}.")
    if abs(r["duree_simulee_s"] - duree) > 0.001 or r["duree_demandee_s"] != duree:
        raise ValueError("La simulation n'a pas atteint la duree demandee.")
    if r["effectif_observe"] < 1 or not r.get("donnees") or not r.get("etat_initial_sha256"):
        raise ValueError("Scenario ou provenance des donnees manquants.")
    if any(x.get("status") != 200 or not x.get("sha256") for x in r["donnees"].values()):
        raise ValueError("Donnees incompletes.")
    if variante == "temoin" and r["appels_arbitre"] != 0:
        raise ValueError("Le temoin utilise l'arbitre.")
    if variante == "arbitre" and r["appels_arbitre"] < 1:
        raise ValueError("L'arbitre est charge mais jamais appele.")


def comparer(temoin, arbitre):
    for cle in ("effectif_demande", "effectif_observe", "duree_demandee_s", "duree_simulee_s",
                "graine", "etat_initial_sha256", "donnees"):
        if temoin.get(cle) != arbitre.get(cle):
            raise ValueError(f"Variantes non comparables : {cle} differe.")
    ecarts = {cle: arbitre[cle] - temoin[cle] for cle in ("ralliements", "morts", "blesses", "fuyards")}
    exerce = temoin["decisions_ralliement"] > 0 and arbitre["decisions_ralliement"] > 0
    conclusion = ("Mesures comparables ; le passage de decision du ralliement a ete exerce dans les deux variantes. "
                  "L'utilite du changement reste a juger sur ces resultats."
                  if exerce else "Non concluant sur le ralliement : le passage de decision n'a pas ete exerce dans les deux variantes.")
    return {"ecarts_arbitre_moins_temoin": ecarts, "ralliement_exerce": exerce,
            "conclusion": conclusion,
            "limites": ["Retirer l'arbitre agit aussi sur d'autres comportements ; cet ecart n'isole pas le seul branchement de rallier.",
                        "Le hasard partage ne permet pas d'attribuer chaque ecart individuel a une cause.",
                        "Une mesure technique ne cloture pas l'affaire et ne livre pas le moteur courant."]}


def verifier_absence_processus(base):
    # Un pilote tue brutalement peut laisser un enfant. Ne pas le confondre avec un essai termine.
    for p in base.glob("*/processus.json"):
        if (p.parent / "resultat.json").exists():
            continue
        ancien = catalogue.lire_json(p)
        naissance = ancien.get("naissance")
        if naissance and runtime._identite_processus(ancien["pid"]) == naissance:
            raise RuntimeError(f"Un processus d'essai est encore vivant : {ancien['pid']} ({p.parent}).")


def essayer(profil="court", effectif=None, duree=None, limite=None, serveur="http://localhost:3129", annoncer=print):
    n, secondes, plafond = catalogue.PROFILS[profil]
    effectif = n if effectif is None else effectif
    duree = secondes if duree is None else duree
    limite = plafond if limite is None else limite
    if (isinstance(effectif, bool) or not isinstance(effectif, int) or effectif < 1
            or not math.isfinite(duree) or duree < 0.05 or abs(duree * 20 - round(duree * 20)) > 1e-6
            or not math.isfinite(limite) or limite <= 0):
        raise ValueError("Effectif positif, duree multiple de 0.05 et limite positive requis.")
    contexte = catalogue.dossier()
    base = catalogue.RUNTIME / "90312"
    with verrou(catalogue.RUNTIME / "banc.lock"):
        verifier_absence_processus(base)
        cle = f"atelier:90312:ralliement:{effectif}:{duree:g}"
        identite = work_identity.admettre(cle)
        dossier = base / (time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8])
        dossier.mkdir(parents=True)
        demande = {"version": "essai-atelier/1", "nom": contexte["nom"], "contexte": contexte,
                   "identite_travail": identite,
                   "profil": profil if (effectif, duree) == (n, secondes) else "personnalise", "effectif": effectif,
                   "duree_simulee_s": duree, "limite_par_variante_s": limite,
                   "cree_a": time.time(), "serveur": serveur}
        ecrire(dossier / "demande.json", demande)
        rapport = {"version": "rapport-atelier/1", "statut": "echec", "demande": demande,
                   "variantes": {}, "conclusion": "Comparaison non obtenue."}

        def journal(texte):
            with (dossier / "journal.jsonl").open("a", encoding="utf-8") as f:
                f.write(json.dumps({"heure": time.time(), "message": texte}, ensure_ascii=False) + "\n")
            annoncer(texte)

        try:
            journal("Copie des sources de l'essai")
            provenance = figer(dossier)
            ecrire(dossier / "sources.json", provenance)
            demande["sources"] = str(dossier / "sources.json")
            ecrire(dossier / "demande.json", demande)
            for variante in ("temoin", "arbitre"):
                work_identity.noter(identite, progress="Essai " + variante,
                                    next_step="Lire " + str(dossier / "resultat.json"))
                commande = ["node", str(dossier / "comparer-ralliement.js"),
                            f"--source={dossier / 'source'}", f"--donnees={dossier / 'donnees'}",
                            f"--variante={variante}", f"--effectif={effectif}", f"--duree={duree}",
                            f"--serveur={serveur}"]
                if variante == "arbitre":
                    commande.append("--relire-donnees")
                journal("Lancement : " + variante)
                r = {"commande": commande, "cwd": str(dossier)}
                rapport["variantes"][variante] = r
                ecrire(dossier / (variante + "-commande.json"), r)
                r.update(executer(commande, dossier, dossier / (variante + ".json"),
                                  dossier / (variante + ".log"), limite, journal,
                                  lambda pid: ecrire(dossier / "processus.json", {
                                      "pid": pid, "naissance": runtime._identite_processus(pid), "variante": variante})))
                if r["limite_atteinte"]:
                    rapport["statut"] = "delai_depasse"
                    raise ValueError(f"{variante} : limite de {limite} s atteinte ; {r['derniere_etape']}")
                if r["code_sortie"] != 0:
                    raise ValueError(f"{variante} : code {r['code_sortie']} ; {r['derniere_etape']}")
                resultat = catalogue.lire_json(dossier / (variante + ".json"))
                verifier_sortie(resultat, variante, effectif, duree)
                r["resultat"] = resultat
                if provenance["fichiers"] != empreintes(dossier / "source/ecrans/modules"):
                    raise ValueError("La copie des sources a change pendant l'essai.")
            rapport.update(comparer(rapport["variantes"]["temoin"]["resultat"],
                                   rapport["variantes"]["arbitre"]["resultat"]))
            rapport["statut"] = "mesure_obtenue"
        except (Exception, KeyboardInterrupt) as e:
            rapport["conclusion"] = str(e) or "Essai interrompu."
            journal(rapport["conclusion"])
        finally:
            rapport["termine_a"] = time.time()
            rapport["dossier_essai"] = str(dossier)
            ecrire(dossier / "resultat.json", rapport)
            succes = rapport["statut"] == "mesure_obtenue"
            work_identity.terminer_attempt(identite, None, "succeeded" if succes else "failed",
                                           term=True, artifact=str(dossier / "resultat.json"))
        return rapport
