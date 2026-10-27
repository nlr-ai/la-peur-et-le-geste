"""Pose les verrous et clefs du dossier dans la partie, à la demande du joueur."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
os.environ['CONSEIL_MONDE'] = 'lumina-prime'
sys.path.insert(0, str(ROOT / 'scripts/noyau'))
from partie_greffe import Partie

p = Partie(str(ROOT / 'mondes/lumina-prime/etat/parties/citoyen-oriente-competent.jsonl'))

def write(move):
    refus = p.ecrire(move)
    if refus:
        raise RuntimeError(refus)

rows = [
    ('13001', 'orientation-13000', 'Relier envies et acquis à une occasion réelle',
     'Aucun rapprochement avec un participant choisi n’est établi dans le dossier initial. Le choix, le besoin et les accès restent à confirmer.',
     '13010', 'Relier le choix du citoyen à une contribution accessible', 'choix-et-acces',
     'Croiser intention exprimée, acquis observés et besoin réel ; laisser le citoyen choisir. Preuve : choix explicite, accès et interlocuteur confirmés. Actions proposées : 13020 puis 13021.'),
    ('13101', 'competence-13100', 'Disposer d’un apprentissage adapté à l’écart observé',
     'L’écart entre acquis et activité n’est pas observé ; aucun accompagnateur disponible n’est confirmé. Dépend du verrou 13001.',
     '13110', 'Apprendre à partir d’un essai et d’un retour ciblé', 'essai-et-retour',
     'Faire un essai initial, cibler l’écart, rendre les sources et le retour accessibles, puis réessayer. Preuve : accompagnateur confirmé et progression observable. Actions proposées : 13120 puis 13121.'),
    ('13102', 'competence-13100', 'Éprouver la compétence sur un résultat utilisé',
     'Aucune réalisation ni retour d’utilisateur ne prouve ce parcours dans le dossier initial. Dépend du verrou 13101.',
     '13111', 'Confronter la réalisation à l’usage attendu', 'preuve-par-usage',
     'Convenir du résultat avec un utilisateur réel, puis comparer la réalisation aux critères. Preuve : résultat accessible, critères atteints et retour d’usage. Action proposée : 13122.'),
    ('13201', 'autonomie-13200', 'Transférer les acquis à un autre cas et trouver une aide adaptée',
     'Une première réussite ne suffit pas à démontrer l’autonomie ; aucun second cas n’est observé dans le dossier initial. Dépend du verrou 13102.',
     '13210', 'Transférer les acquis et rendre les ressources retrouvables', 'transfert-et-limites',
     'Varier le cas à niveau comparable, observer les aides réellement nécessaires et conserver le bilan. Preuve : second résultat sans guidage pas à pas, ressources retrouvées et limites reconnues. Actions proposées : 13220 puis 13221.'),
]
for vid, target, title, fact, kid, keytitle, means, method in rows:
    rid = 'source-verrou-' + vid
    bid = 'verrou-' + vid
    key = 'cle-' + kid
    if rid not in p.ressources:
        write({'camp': 'attaque', 'coup': 'demander', 'id': rid, 'nombre': 1,
               'texte': 'Verrou initial ' + vid + ' — ' + fact})
    if p.ressources[rid].get('en_attente'):
        write({'camp': 'arbitre', 'coup': 'arbitrer', 'sur': rid, 'verdict': 'accorde',
               'motif': 'Source : dossier figé sources/citoyen-oriente-competent.json, verrou ' + vid + '. Mise en place expressément demandée par le joueur ; condition initiale du dossier, pas une attaque nouvelle attribuée à Nova.'})
    if bid not in p.blocages:
        write({'camp': 'attaque', 'coup': 'bloquer', 'id': bid, 'sur': target,
               'engage': [rid], 'texte': vid + ' — ' + title + '. ' + fact})
    if key not in p.cles:
        write({'camp': 'defense', 'coup': 'lever', 'id': key, 'ouvre': [bid],
               'engage': [means], 'texte': kid + ' — ' + keytitle + '. ' + method + ' Clef proposée, réalisation à prouver.'})
    if not p.cles[key].get('justifiee'):
        write({'camp': 'arbitre', 'coup': 'justifier', 'sur': key,
               'texte': 'Le dossier donne cette clef « à étudier » et ses actions « proposées ». Produire la chaîne et les preuves annoncées avant de considérer le verrou levé. ' + method})
print(f'{len(p.blocages)} verrous, {len(p.cles)} clefs ; {len(p.lignes)} lignes. Clefs proposées en attente de justification.')
