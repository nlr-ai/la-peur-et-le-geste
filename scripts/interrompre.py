# -*- coding: utf-8 -*-
"""INTERROMPRE — glisser un message, hors fiction, a qui joue : PJ, PNJ ou PNJ-PJ.

    python scripts/interrompre.py --qui otto "Laisse Borros de cote, va au tresor."
    python scripts/interrompre.py --monde vampire-counts --qui teodor "Plus vite."
    python scripts/interrompre.py --qui gerardys "La reine veut le registre a midi."
    python scripts/interrompre.py --qui rhaenyra --comme pj "..."     # force le canal

Le canal se deduit de qui tient le personnage, dans cet ordre :

  pnj-pj  un joueur PNJ (scripts/joueur_pnj.py) tient le siege EN CE MOMENT
          (son verrou est vivant). Le message va dans sa boite,
          .agents-runtime/joueur-pnj/<monde>--<qui>.interruptions.jsonl. Il
          coupe son attente, le lit en tete de son tour suivant, et joue
          aussitot en en tenant compte. Rien n'entre au flux ni dans l'etat.
  pj      un siege de <monde>/etat/joueurs.json, sans joueur PNJ dessus : un
          humain au clavier. Le message tombe dans SON fil en item `reponse`
          (hors fiction, prive, zero minute) via append_flux.py --pour <qui>.
  pnj     tout autre personnage : le parloir, `parloir.py --dire --de mj --a
          <qui>` — un billet qui le reveille dans sa propre session.

Pour un PNJ, la Regle Zero tient : on lui pose une question ou on lui donne
une nouvelle, on n'ecrit jamais sa replique a sa place.
"""
import argparse
import io
import json
import os
import subprocess
import sys
import time

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERROUS = os.path.join(RACINE, ".agents-runtime", "joueur-pnj")


def base_monde(monde):
    return os.path.join(RACINE, "mondes", monde) if monde else RACINE


def boite(monde, qui):
    """La boite d'un joueur PNJ — meme nom que son verrou (joueur_pnj.py)."""
    return os.path.join(VERROUS, "%s--%s.interruptions.jsonl" % (monde or "racine", qui))


def pnj_pj_vivant(monde, qui):
    f = os.path.join(VERROUS, "%s--%s.lock" % (monde or "racine", qui))
    try:
        pid = int(io.open(f, encoding="utf-8").read().strip() or 0)
    except (OSError, ValueError):
        return False
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from joueur_pnj import vivant
    return bool(pid) and vivant(pid)


def est_siege(monde, qui):
    try:
        roster = json.load(io.open(os.path.join(base_monde(monde), "etat", "joueurs.json"), encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return any(s.get("personnage_id") == qui for s in roster)


def env_monde(monde):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    if monde:
        env["CONSEIL_MONDE"] = monde
    return env


def main():
    ap = argparse.ArgumentParser(description="Interrompre un PJ, un PNJ ou un PNJ-PJ avec un message.")
    ap.add_argument("--qui", required=True, help="personnage_id")
    ap.add_argument("--monde", default="", help="id sous mondes/ ; vide = la partie racine")
    ap.add_argument("--de", default="la direction de jeu", help="signature du message")
    ap.add_argument("--comme", choices=["pnj-pj", "pj", "pnj"], help="force le canal au lieu de le deduire")
    ap.add_argument("texte", nargs="+")
    a = ap.parse_args()
    texte = " ".join(a.texte).strip()
    if not texte:
        raise SystemExit("message vide")

    canal = a.comme or ("pnj-pj" if pnj_pj_vivant(a.monde, a.qui)
                        else "pj" if est_siege(a.monde, a.qui) else "pnj")

    if canal == "pnj-pj":
        os.makedirs(VERROUS, exist_ok=True)
        with io.open(boite(a.monde, a.qui), "a", encoding="utf-8") as f:
            f.write(json.dumps({"t": time.time(), "de": a.de, "texte": texte}, ensure_ascii=False) + "\n")
        print("pnj-pj : depose dans la boite de %s — il le lira a son prochain tour, sans attendre." % a.qui)
        return 0

    if canal == "pj":
        item = {"type": "reponse", "qui": a.de, "texte": texte}
        r = subprocess.run([sys.executable, os.path.join(RACINE, "scripts", "append_flux.py"),
                            "--pour", a.qui, json.dumps(item, ensure_ascii=False)],
                           cwd=RACINE, env=env_monde(a.monde), capture_output=True,
                           text=True, encoding="utf-8")
        sys.stdout.write(r.stdout)
        sys.stderr.write(r.stderr)
        if r.returncode == 0:
            print("pj : pousse dans le fil de %s (hors fiction, zero minute)." % a.qui)
        return r.returncode

    r = subprocess.run([sys.executable, os.path.join(RACINE, "scripts", "parloir.py"),
                        "--dire", "--de", "mj", "--a", a.qui, texte],
                       cwd=RACINE, env=env_monde(a.monde))
    if r.returncode == 0:
        print("pnj : billet depose au parloir de %s, qui est reveille." % a.qui)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
