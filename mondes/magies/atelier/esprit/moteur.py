"""Moteur expérimental : difficulté et perceptibilité séparées, historique par contact."""
from scorer import calculer


def entier(valeur, mini, maxi, nom):
    if type(valeur) is not int or not mini <= valeur <= maxi:
        raise ValueError(f"{nom} doit être un entier entre {mini} et {maxi}.")
    return valeur


def simuler(bareme, passes):
    if not isinstance(passes, list) or len(passes) > 200:
        raise ValueError("Une simulation contient au maximum 200 passes.")
    regles = bareme["perceptibilite"]
    contacts, resultats = {}, []
    for passe in passes:
        if not isinstance(passe, dict):
            raise ValueError("Chaque passe doit être un objet.")
        action_id = passe.get("action")
        if action_id not in bareme["actions"]:
            raise ValueError("Action inconnue.")
        selections = passe.get("modificateurs", {})
        if not isinstance(selections, dict):
            raise ValueError("Les modificateurs doivent être un objet.")
        for option in ("resistance", "exploratoire"):
            if option in passe and type(passe[option]) is not bool:
                raise ValueError(f"{option} doit être un booléen.")
        r = calculer(bareme, action_id, selections, passe.get("resistance", False),
                     passe.get("exploratoire", False))
        contact = passe.get("contact", "Contact A")
        if not isinstance(contact, str) or not contact.strip() or len(contact) > 80:
            raise ValueError("Le contact doit avoir un nom de 1 à 80 caractères.")
        contact = contact.strip()
        flow = entier(passe.get("flow", regles["flow"]["defaut"]),
                      regles["flow"]["min"], regles["flow"]["max"], "Flow")
        duree = entier(passe.get("duree", regles["duree"]["defaut"]),
                       regles["duree"]["min"], regles["duree"]["max"], "Durée")
        pensees = passe.get("pensees", regles["pensees_defaut"])
        formation = passe.get("formation", regles["formation_defaut"])
        attention = passe.get("attention", regles["attention_defaut"])
        if pensees not in regles["pensees"] or formation not in regles["observateurs"]:
            raise ValueError("Pensées ou formation inconnues.")
        observateur = regles["observateurs"][formation]
        if attention not in observateur["phenomene"]:
            raise ValueError("Attention inconnue.")
        avant = contacts.get(contact, {"cumul": 0, "phenomene_percu": False,
                                       "contact_reconnu": False, "passes": 0})
        p = {"contact": contact, "avant": avant["cumul"], "apres": avant["cumul"],
             "ajout": 0, "statut": "non_simule", "statut_regles": regles["statut"]}
        if r["difficulte"] is None:
            p["raison"] = "Mécanisme ouvert : la passe ne modifie pas le compte."
        elif bareme["actions"][action_id].get("cible") == "soi":
            p["raison"] = "Action sur soi : exposition à un contact extérieur non simulée."
        else:
            intervention = regles["bruit_actions"][action_id]
            mental = regles["pensees"][pensees]
            fuite = max(0, intervention + mental - flow)
            reference = regles["reference_par_battement"]
            ajout = duree * (reference + fuite)
            cumul = avant["cumul"] + ajout
            seuil = observateur["phenomene"][attention]
            surplus = observateur["surcout_reconnaissance"]
            seuil_reconnu = None if surplus is None else seuil + surplus
            percu = avant["phenomene_percu"] or cumul >= seuil
            reconnu = avant["contact_reconnu"] or (seuil_reconnu is not None and cumul >= seuil_reconnu)
            etat = {"cumul": cumul, "phenomene_percu": percu, "contact_reconnu": reconnu,
                    "passes": avant["passes"] + 1}
            contacts[contact] = etat
            p.update({"statut": "simule", "apres": cumul, "ajout": ajout,
                      "reference": reference, "intervention": intervention,
                      "pensees": mental, "flow": flow, "fuite": fuite, "duree": duree,
                      "seuil_phenomene": seuil, "seuil_reconnaissance": seuil_reconnu,
                      "phenomene_percu": percu, "contact_reconnu": reconnu,
                      "lecture": "Contact étranger reconnu" if reconnu else
                                 "Phénomène ressenti, origine non reconnue" if percu else
                                 "Pas encore remarqué dans ce modèle",
                      "formule": f"{duree} × ({reference} + max(0, {intervention} + {mental} − {flow})) = {ajout}"})
        r["perceptibilite"] = p
        resultats.append(r)
    return {"version": bareme["version"], "statut": regles["statut"],
            "passes": resultats, "contacts": contacts}


if __name__ == "__main__":
    import argparse
    import json
    import sys
    from scorer import lire, ICI
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sequence", help="Fichier JSON exporté par l’atelier, ou liste de passes")
    parser.add_argument("--bareme", default=ICI / "bareme.json")
    args = parser.parse_args()
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8")
    try:
        sequence = lire(args.sequence)
        passes = sequence.get("passes") if isinstance(sequence, dict) else sequence
        print(json.dumps(simuler(lire(args.bareme), passes), ensure_ascii=False, indent=2))
    except (ValueError, TypeError, KeyError, OSError) as exc:
        parser.error(str(exc))
