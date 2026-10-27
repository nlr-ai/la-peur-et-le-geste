"""Ouvre la confrontation demandée par Nova, sans modifier le monde joué."""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
os.environ['CONSEIL_MONDE'] = 'lumina-prime'
sys.path.insert(0, str(ROOT / 'scripts' / 'noyau'))
from partie_greffe import Partie

WORLD = ROOT / 'mondes' / 'lumina-prime'
DEST = WORLD / 'etat' / 'parties'
ID = 'citoyen-oriente-competent'
DEST.mkdir(parents=True, exist_ok=True)
source = WORLD / 'etat/maisons/cite-lumina/documents/books/affaire-citoyen-oriente-competent.json'
snapshot = DEST / 'sources' / (ID + '.json')
snapshot.parent.mkdir(exist_ok=True)
if not snapshot.exists():
    snapshot.write_bytes(source.read_bytes())
config = {
    'partie': ID, 'camps': ['defense', 'attaque'], 'coups_par_camp': 1,
    'note': 'Nova attaque ; assistant défend. Épreuve contradictoire du dossier figé dans sources/citoyen-oriente-competent.json. Aucun coup ne vaut exécution dans la ville. Un tour ne fait pas avancer la date du monde. Les hypothèses restent des hypothèses.',
    'portee': {
        'attaque': 'Montrer un contre-exemple compatible avec le dossier, une contradiction ou une condition indispensable sans solution. Aucune attaque tactique ne sera inventée à la place de Nova.',
        'defense': 'Défendre le parcours proposé avec ses sources et critères. Ni disponibilité inventée, ni réussite présumée. Une modification est une concession explicite, jamais une réécriture du dossier initial.'
    },
    'fin': {'regle': 'Attaque : faille décisive reconnue qui empêche un des trois résultats. Défense : réponse vérifiable à chaque attaque effectivement posée. Le silence ne prouve rien et tenir le débat ne prouve pas la réussite réelle du parcours. Tout désaccord sur un constat reste ouvert.'}
}
cfg = DEST / (ID + '.json')
if not cfg.exists():
    cfg.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
p = Partie(str(DEST / (ID + '.jsonl')))
if not p.lignes:
    moves = [
        {'camp': 'defense', 'coup': 'viser', 'id': 'parcours-defendable', 'texte': 'Le parcours proposé est défendable : relier le choix du citoyen à une activité accessible, apprendre par essai et retour, vérifier une contribution utile puis un second cas comparable avec une aide ciblée. Les trois résultats 13000, 13100 et 13200 doivent rester atteignables ; aucune réussite ni disponibilité n’est présumée.'},
        {'camp': 'defense', 'coup': 'demander', 'id': 'dossier-defense', 'nombre': 1, 'texte': 'Dossier figé : états 13000/13100/13200, quatre clefs proposées et sept actions proposées. Source lisible dans le livre Un citoyen orienté et compétent.'},
        {'camp': 'arbitre', 'coup': 'arbitrer', 'sur': 'dossier-defense', 'verdict': 'accorde', 'motif': 'Source : copie exacte du livre à l’ouverture, sources/citoyen-oriente-competent.json. Accord documentaire seulement ; aucun citoyen, temps de mentor ou résultat accordé.'},
        {'camp': 'attaque', 'coup': 'demander', 'id': 'examen-critique', 'nombre': 1, 'texte': 'Examen du même dossier : contradictions, conditions manquantes et contre-exemples explicitement hypothétiques compatibles avec ses engagements. Le premier argument appartient à Nova.'},
        {'camp': 'arbitre', 'coup': 'arbitrer', 'sur': 'examen-critique', 'verdict': 'accorde', 'motif': 'Source : demande du joueur « je dois démonter tu dois protéger ». Moyen de confrontation logique ; ne crée aucun fait dans la ville. La pertinence de chaque contre-exemple doit être examinée.'},
    ]
    for move in moves:
        refus = p.ecrire(move)
        if refus:
            raise RuntimeError(refus)
(DEST / '_courante.json').write_text(json.dumps({'partie': ID, 'camp': 'attaque'}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'partie': ID, 'tour': p.tour, 'lignes': len(p.lignes), 'camps': p.camps()}, ensure_ascii=False))
