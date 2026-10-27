"""Calculateur local et sans mutation de l'état joué. Python standard uniquement."""
import argparse
import json
from pathlib import Path
import sys

ICI = Path(__file__).resolve().parent


def lire(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def applicable(mod, action):
    return (action["skill"] in mod.get("skills", [action["skill"]])
            and (not mod.get("reecriture") or action.get("reecriture", False))
            and (not mod.get("cache") or action.get("cache", False))
            and (not mod.get("externe") or action.get("cible") != "soi"))


def calculer(bareme, action_id, selections=None, resistance=False, exploratoire=False):
    selections = dict(selections or {})
    if action_id not in bareme["actions"]:
        raise ValueError("Action inconnue : " + action_id)
    action = bareme["actions"][action_id]
    mods = bareme["modificateurs"]
    for cle in selections:
        if cle not in mods:
            raise ValueError("Modificateur inconnu : " + cle)
        if not applicable(mods[cle], action):
            raise ValueError(f"{cle} ne s’applique pas à {action_id}.")
    limites = []
    if action.get("proposee"):
        limites.append("Cette capacité est proposée, pas établie dans le lore.")
    details = []
    for cle, mod in mods.items():
        if not applicable(mod, action):
            continue
        valeur = selections.get(cle, action.get("defauts", {}).get(cle, mod["defaut"]))
        autorises = action.get("choix_autorises", {}).get(cle)
        if autorises is not None and valeur not in autorises:
            raise ValueError(f"{cle} pour {action_id} : choix autorisés = " + ", ".join(autorises))
        if "par_contact" in mod:
            if type(valeur) is not int or valeur < 0:
                raise ValueError(f"{cle} exige un entier positif ou nul.")
            delta = valeur * mod["par_contact"]
        else:
            if not isinstance(valeur, str) or valeur not in mod["choix"]:
                raise ValueError(f"Valeur invalide pour {cle} : {valeur}. Choix : "
                                 + ", ".join(mod["choix"]))
            delta = mod["choix"][valeur]
            if valeur in mod.get("non_definis", []):
                limites.append(f"Mécanisme à définir : {mod['libelle']} ({valeur}).")
        details.append({"id": cle, "libelle": mod["libelle"], "valeur": valeur,
                        "delta": delta, "defaut": cle not in selections})
    if resistance:
        limites.append("Franchir un refus actif : mécanisme et opposition non définis.")
    reference_cachee_active = action.get("cache") and selections.get("mobilisation") == "active"
    # Aucun nombre n'est rendu contre un refus, même en exploration : il n'a pas de barème.
    chiffrable = not resistance and not reference_cachee_active and (not limites or exploratoire)
    score = action["base"] + sum(d["delta"] for d in details) if chiffrable else None
    appreciation = None
    if score is not None:
        appreciation = next(e["libelle"] for e in bareme["echelle"]
                            if e["max"] is None or score <= e["max"])
    return {"action": action_id, "libelle": action["libelle"], "skill": action["skill"],
            "version": bareme["version"], "statut_bareme": bareme["statut"],
            "statut": "a_definir" if score is None else ("exploratoire" if limites else "calcule"),
            "base": action["base"], "details": details, "difficulte": score,
            "appreciation": appreciation, "limites": limites}


def afficher(r, titre=None, contexte=None):
    print(titre or r["libelle"])
    print(f"Skill : {r['skill']} | barème {r['version']} — proposition de calibration")
    if contexte:
        print(contexte)
    print(f"Base : {r['base']}")
    for d in r["details"]:
        if d["delta"] or not d["defaut"]:
            print(f"  {d['delta']:+d} {d['libelle']} : {d['valeur']}")
    defaults = [f"{d['id']}={d['valeur']}" for d in r["details"] if d["defaut"]]
    if defaults:
        print("Hypothèses par défaut : " + ", ".join(defaults))
    if r["difficulte"] is None:
        print("Difficulté non chiffrée — mécanisme à définir.")
    else:
        mention = " (exploratoire)" if r["statut"] == "exploratoire" else ""
        print(f"Difficulté : {r['difficulte']} — {r['appreciation']}{mention}")
    for limite in r["limites"]:
        print("À discuter : " + limite)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bareme", type=Path, default=ICI / "bareme.json")
    groupe = parser.add_mutually_exclusive_group(required=True)
    groupe.add_argument("--action")
    groupe.add_argument("--cas")
    groupe.add_argument("--catalogue", action="store_true")
    groupe.add_argument("--comparer", action="store_true")
    parser.add_argument("--mod", action="append", default=[], metavar="CLE=VALEUR")
    parser.add_argument("--resistance", action="store_true")
    parser.add_argument("--exploratoire", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        bareme = lire(args.bareme)
        cas = lire(ICI / "cas.json")
        if (args.catalogue or args.comparer) and (args.mod or args.resistance):
            raise ValueError("--mod et --resistance exigent --action ou --cas.")
        if args.catalogue:
            if args.json:
                print(json.dumps({"bareme": bareme, "cas": cas}, ensure_ascii=False, indent=2))
            else:
                print(bareme["statut"])
                for cle, a in bareme["actions"].items():
                    print(f"{cle}: {a['skill']} / base {a['base']} — {a['libelle']}"
                          + (" [capacité proposée]" if a.get("proposee") else ""))
                    if a.get("defauts") or a.get("choix_autorises") or a.get("cible"):
                        print(f"  cible={a.get('cible', 'autrui')}; défauts={a.get('defauts', {})}; "
                              f"choix restreints={a.get('choix_autorises', {})}")
                for cle, m in bareme["modificateurs"].items():
                    choix = m.get("choix", "entier >= 0")
                    scope = ("réécriture" if m.get("reecriture") else "cacher_pensee" if m.get("cache")
                             else ", ".join(m.get("skills", ["tous"])))
                    if m.get("externe"):
                        scope += ", cible extérieure"
                    print(f"{cle} ({scope}): {choix}; défaut={m['defaut']}")
                print("Cas : " + ", ".join(cas))
            return 0
        overrides = {}
        for item in args.mod:
            cle, sep, valeur = item.partition("=")
            if not sep or cle in overrides:
                raise ValueError("Modificateur mal formé ou répété : " + item)
            mod = bareme["modificateurs"].get(cle, {})
            overrides[cle] = int(valeur) if "par_contact" in mod else valeur
        if args.cas and args.cas not in cas:
            raise ValueError("Cas inconnu : " + args.cas)
        sources = list(cas.items()) if args.comparer else [(args.cas, cas[args.cas])] if args.cas else [
            (None, {"action": args.action, "modificateurs": {}})]
        resultats = []
        for ident, c in sources:
            selections = dict(c.get("modificateurs", {}), **overrides)
            r = calculer(bareme, c["action"], selections,
                         args.resistance or c.get("resistance", False), args.exploratoire)
            r.update({"cas": ident, "titre": c.get("titre"), "contexte": c.get("contexte")})
            resultats.append(r)
        if args.json:
            print(json.dumps(resultats if args.comparer else resultats[0], ensure_ascii=False, indent=2))
        else:
            for i, r in enumerate(resultats):
                if i:
                    print()
                afficher(r, r["titre"], r["contexte"])
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8")
    raise SystemExit(main())
