# -*- coding: utf-8 -*-
"""DEV, réveil du contexte 30307, J1 après 10h20. De ma main, pour l'action 30307.
Motif : réponse de Quantum (M201 et M202 ne sont pas lisibles et ne sont pas dans les
documents de la cité ; existence non établie). Suite du brouillon
transcrire-30307-j1-reponse-aria.py. Ne touche qu'à affaire-plans-lumina ; aucun numéro ne change.
Écrit par la porte bibliotheque.ouvrir, racine absolue du monde ; relit et réessaie."""
import sys, time
RACINE = "C:/Users/reyno/le-conseil2"
sys.path[:0] = [RACINE + "/scripts", RACINE + "/scripts/noyau"]
import bibliotheque

ETAT = RACINE + "/mondes/lumina-prime/etat"


def table(livre, prefixe):
    for t in livre["tables"]:
        if t["titre"].startswith(prefixe):
            return t
    raise KeyError(prefixe)


def ligne(t, num):
    for l in t["lignes"]:
        if l["cellules"][0].strip("* ") == num:
            return l
    raise KeyError(num)


def col(t, debut):
    for i, c in enumerate(t["colonnes"]):
        if debut in c:
            return i
    raise KeyError(debut)


def poser(t, num, colonne, valeur):
    ligne(t, num)["cellules"][col(t, colonne)] = valeur


def corriger(a):
    act = table(a, "⚔️")
    poser(act, "30307", "Ce qu'on fait",
          "Obtenir le plan initial (pièces et connexions) de celui qui le tient, puis le transcrire dans ce "
          "volume, connexion par connexion, en notant si elle est dessinée ou essayée. J1 : Aria ne le tient "
          "pas et ne l’a jamais ouvert. Le registre des moyens documentaires l’inscrit en M201 "
          "(plans/lumina-prime.json) et les accès en M202 (etat/chemins.json). Quantum, J1 après 10h20 : "
          "aucune des deux adresses n’est parmi les documents de la cité, il ne peut ouvrir ni l’une ni "
          "l’autre, et leur existence n’est pas établie. Aucun livre ne dit qui tient le paquet Lumina "
          "Prime. Demandé à Nova le J1 : en poser une copie dans les documents de la cité. Sans copie à "
          "18h, les connexions restent « inconnues » au relevé 30301.")
    poser(act, "30307", "Avec quoi",
          "Copie du plan initial posée dans les documents de la cité, si Nova le peut ; réponses d’Aria et "
          "de Quantum (reçues J1 : ni l’un ni l’autre ne peut l’ouvrir) ; relevé 40302 de Quantum, J2")

    ver = table(a, "🔒")
    poser(ver, "30105", "Ce qui est vrai",
          "Aucun volume de la cité ne porte les pièces et les connexions du Radiant Core. Le registre des "
          "moyens documentaires les déclare en M201 (plans/lumina-prime.json) et M202 (etat/chemins.json), "
          "« présent ». Mais ces adresses ne sont pas des documents de la cité : Quantum ne peut ouvrir "
          "ni l’une ni l’autre, et leur existence n’est pas établie (J1). Aria ne tient pas le plan. "
          "10020, 10021 = 30301, 60301 et 70305 le citent pourtant comme matière. Sans ses connexions, "
          "le relevé 30301 ne peut répondre à aucune des trois questions de PITCH.")
    poser(ver, "30105", "La preuve",
          "Relecture des volumes de la cité, J1 ; registre des moyens documentaires, M201 et M202, avec la "
          "note d’Aria ; billets d’Aria (après 10h12) et de Quantum (après 10h20), J1.")

    pl = table(a, "🗺️")
    for l in pl["lignes"]:
        c = l["cellules"]
        if c[0] in ("Plan initial du Radiant Core", "Accès conventionnels (chemins)"):
            m = "M201 : plans/lumina-prime.json" if c[0].startswith("Plan") else "M202 : etat/chemins.json"
            c[2] = ("Déclaré en " + m + ", « présent » au registre des moyens documentaires. Ce n’est pas "
                    "un document de la cité. Qui tient le paquet Lumina Prime : aucun livre ne le dit.")
            c[3] = ("Non. Quantum ne peut pas l’ouvrir, et son existence n’est pas établie (J1). Copie "
                    "demandée à Nova. Hors du stockage relevé au J2 (40302).")
            c[4] = "Registre des moyens documentaires ; dossiers de métier, page Sources ; billet de Quantum, J1."

for essai in range(5):
    s = bibliotheque.ouvrir(ETAT)
    par_id = {l["id"]: l for l in s.livres}
    corriger(par_id["affaire-plans-lumina"])
    try:
        s.sauver()
        print("écrit, essai", essai + 1)
        break
    except bibliotheque.BibliothequeModifiee as e:
        print("relu :", e)
        time.sleep(2)
else:
    raise SystemExit("rien écrit après cinq essais")
