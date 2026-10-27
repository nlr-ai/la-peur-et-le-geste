# -*- coding: utf-8 -*-
"""DEV, réveil du contexte 30307, J1 après 10h16. De ma main, pour l'action 30307
(transcrire le plan initial du Radiant Core). Motif : réponse d'Aria (elle ne tient pas
le plan) et moyen M201/M202 du registre des moyens documentaires. Question portée à
Quantum (40301) au même réveil ; complété après sa réponse (après 10h20). Ne touche qu'à affaire-plans-lumina ; aucun numéro ne change.
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
          "pas et ne l’a jamais ouvert ; ses 10020 à 10022 le citent d’après la page 1 de son affaire "
          "d’accueil. Le registre des moyens documentaires l’inscrit en M201 (plans/lumina-prime.json) et "
          "les accès en M202 (etat/chemins.json), « présent » : adresse déclarée, aucun membre du conseil "
          "ne dit l’avoir ouvert. Quantum (J1 après 10h20) : ni l’un ni l’autre n’est lisible par lui, "
          "aucun n’est dans les documents de la cité (les vingt-cinq volumes), et leur existence n’est pas "
          "établie ; il relève au J2 ce qui est tenu hors des chambres et des livres (40302). Qui tient le "
          "paquet, aucun livre ne le dit. Seule voie connue : que Nova en pose une copie dans les documents "
          "de la cité ; question portée à Nova. À 18h sans copie, le relevé 30301 marque les connexions "
          "« inconnues ».")
    poser(act, "30307", "Moyens", "M201 · M202 · M212")
    poser(act, "30307", "Avec quoi",
          "Une copie du plan posée dans les documents de la cité (Nova) ; réponses d’Aria et de Quantum "
          "(J1 : ni l’une ni l’autre ne le tient ni ne peut l’ouvrir)")

    ver = table(a, "🔒")
    poser(ver, "30105", "Ce qui est vrai",
          "Aucun volume de la cité ne porte les pièces et les connexions du Radiant Core. Le registre des "
          "moyens documentaires le déclare en M201 (plans/lumina-prime.json) et M202 (etat/chemins.json), "
          "« présent », sans que personne l’ait ouvert. Aria ne le tient pas ; Quantum ne peut ouvrir ni "
          "l’une ni l’autre adresse, qui ne sont pas dans les documents de la cité. 10020, 10021 = 30301, 60301 "
          "et 70305 le citent pourtant comme matière. Sans ses connexions, le relevé 30301 ne peut répondre "
          "à aucune des trois questions de PITCH.")
    poser(ver, "30105", "La preuve",
          "Relecture des volumes de la cité, J1 ; dossier de métier DEV, page Sources ; registre des moyens "
          "documentaires, M201 et M202, avec la note d’Aria ; billets d’Aria (après 10h12) et de Quantum "
          "(après 10h20), J1.")

    pl = table(a, "🗺️")
    for l in pl["lignes"]:
        c = l["cellules"]
        if c[0] == "Plan initial du Radiant Core":
            c[2] = ("Déclaré en M201 : plans/lumina-prime.json, tenu par la cité, « présent » (registre des "
                    "moyens documentaires). Hors des volumes de la cité.")
            c[3] = ("Non. Déclaré, jamais ouvert ; illisible pour Quantum ; existence non établie. Aria ne le "
                    "tient pas. Aucun volume ne porte ses connexions (30105).")
            c[4] = ("Dossier de métier DEV, page Sources ; registre des moyens documentaires, M201 ; billets "
                    "d’Aria et de Quantum, J1.")
        if c[0] == "Accès conventionnels (chemins)":
            c[2] = ("Déclaré en M202 : etat/chemins.json, tenu par la cité, « présent » (registre des moyens "
                    "documentaires). Hors des volumes de la cité.")
            c[3] = "Non. Déclaré, jamais ouvert ; illisible pour Quantum ; existence non établie (billet de Quantum, J1)."
            c[4] = "Dossier de métier DEV, page Sources ; atlas, page 1 ; registre des moyens documentaires, M202."


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
