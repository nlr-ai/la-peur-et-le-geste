"""Initialisation additive du départ Outlander ; refuse un état préexistant."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'etat'
if STATE.exists():
    raise SystemExit('État déjà présent : aucune réinitialisation autorisée.')

DATE = {'annee': 1743, 'lune': 5, 'jour': 4, 'minute': 600}

def write(name, value):
    path = STATE / (name + '.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

write('monde', {'date': DATE, 'phase': 'arrivee-des-voyageurs', 'tension': 20,
                'deviations': [{'date': DATE, 'cause': 'Départ validé par le joueur',
                                'description': 'Aurore et Nicolas arrivent depuis notre époque à Craigh na Dun, après Claire.'}]})
write('journal', {'maison_joueur_id': None, 'personnage_joueur_id': 'aurore',
                  'scenes': [], 'scene_courante': None})
write('horloges', {pid: DATE for pid in ('aurore', 'nicolas')})
write('joueurs', [{'personnage_id': pid, 'nom': pid.title(), 'jeton': 'outlander-' + pid,
                   'role': 'principal' if pid == 'aurore' else 'second', 'pnj': [],
                   'occupe': True, 'lieu': 'craigh-na-dun', 'depuis': 0}
                  for pid in ('aurore', 'nicolas')])

places = [
    ('craigh-na-dun', 'Craigh na Dun', 'colline', None),
    ('lisiere-craigh', 'Lisière sous les pierres', 'bois', None),
    ('croisee-craigh', 'Croisée du chemin de la colline', 'chemin', None),
    ('ferme-du-ruisseau', 'Ferme du ruisseau', 'ferme', None),
    ('inverness', 'Inverness', 'ville', None),
    ('leoch', 'Château Leoch', 'chateau', 'mackenzie'),
    ('cranesmuir', 'Cranesmuir', 'village', None),
]
write('lieux', [{'id': pid, 'nom': name, 'region': 'Highlands', 'type': kind,
                 'controle_id': owner, 'alias': []} for pid, name, kind, owner in places])
write('chemins', {'alias': {}, 'aretes': [
    ['craigh-na-dun', 'lisiere-craigh', 8],
    ['lisiere-craigh', 'croisee-craigh', 7],
    ['croisee-craigh', 'ferme-du-ruisseau', 12]],
    '_': 'Géographie locale ajoutée pour cette partie. Durées conventionnelles en minutes à pied. Aucun raccord canonique distant encore mesuré.'})
write('maisons', [{'id': 'mackenzie', 'nom': 'MacKenzie de Leoch', 'siege_id': 'leoch',
                  'suzerain_id': None, 'canon': True}])

people = [{'id': pid, 'nom': pid.title(), 'maison_id': None, 'titre': '', 'traits': [],
           'objectifs': [], 'maniere': '', 'etat': 'actif', 'lieu_id': 'craigh-na-dun',
           'condition': 'libre'} for pid in ('aurore', 'nicolas')]
actors = [
    ('claire-randall', 'Claire Randall', None, 'leoch', 'Infirmière, étrangère à Leoch',
     ['résolue', 'observatrice'], 'Directe ; pose des questions concrètes.',
     'Comprendre les possibilités de regagner son époque sans dévoiler son origine.',
     ['Elle vient d’une autre époque.', 'Elle se trouve à Leoch.'],
     ['L’arrivée d’Aurore et Nicolas.', 'Les conditions certaines d’un retour.']),
    ('jamie-fraser', 'Jamie Fraser', None, 'leoch', 'Highlander, lié aux MacKenzie',
     ['loyal', 'prudent'], 'Mesuré, avec un humour discret.',
     'Préserver sa sécurité et ses attaches à Leoch.', ['Il séjourne à Leoch.'],
     ['L’arrivée des deux PJ.', 'L’origine temporelle de Claire.']),
    ('colum-mackenzie', 'Colum MacKenzie', 'mackenzie', 'leoch', 'Laird de Leoch',
     ['calculateur', 'attentif'], 'Calme ; cherche des faits précis.',
     'Tenir les affaires de Leoch et apprécier les étrangers qui y arrivent.',
     ['Claire est une étrangère présente à Leoch.'], ['L’arrivée des deux PJ.', 'L’origine temporelle de Claire.']),
    ('dougal-mackenzie', 'Dougal MacKenzie', 'mackenzie', 'leoch', 'Frère de Colum',
     ['énergique', 'engagé'], 'Franche, orientée vers les actes.',
     'Servir les intérêts du clan et ses convictions jacobites.',
     ['Claire est présente à Leoch.'], ['L’arrivée des deux PJ.', 'L’origine temporelle de Claire.']),
]
heads = []
for pid, name, house, place, title, traits, manner, intention, beliefs, unknown in actors:
    people.append({'id': pid, 'nom': name, 'maison_id': house, 'titre': title,
                   'traits': traits, 'objectifs': [{'but': intention, 'priorite': 1}],
                   'maniere': manner, 'etat': 'actif', 'lieu_id': place, 'condition': 'libre'})
    heads.append({'personnage_id': pid, 'croyances': beliefs, 'ignore': unknown,
                  'intention': intention, 'plan': [], 'declencheurs': [],
                  'attitude_joueur': 'Ne connaît ni Aurore ni Nicolas.', 'date_maj': DATE})
write('personnages', people)
write('intentions', heads)
for name in ('relations', 'evenements', 'info', 'actes', 'paroles', 'annales', 'objectifs', 'plis', 'books'):
    write(name, [])
write('pensees', {'pensees': []})
write('presence', {'presence': {pid: {'salle': 'craigh-na-dun', 'lieu': 'Craigh na Dun', 'date': DATE}
                               for pid in ('aurore', 'nicolas')}})
write('routines', {'gens': {}})
(STATE / 'flux.jsonl').write_text('', encoding='utf-8')
for pid in ('aurore', 'nicolas'):
    for name, value in [('objectifs', []), ('info', []), ('jetons', {'jetons': []}),
                        ('vues', {'vues': []}), ('fils', {'fils': []})]:
        write('joueurs/' + pid + '/' + name, value)
    (STATE / 'inbox' / pid).mkdir(parents=True, exist_ok=True)
for pid in ('mj', *(actor[0] for actor in actors)):
    chamber = ROOT / 'chambres' / pid
    chamber.mkdir(parents=True, exist_ok=True)
    (chamber / 'AGENTS.md').write_text(
        '# ' + pid + '\n\nLire ../../AGENTS.md et ../../manuel.md. '
        'Lire les tables du monde outlander avant toute action. '
        'Aucune scène antérieure ni connaissance des PJ ne se déduit de ce dossier.\n', encoding='utf-8')
print('État Outlander créé : 2 PJ, 4 PNJ, 7 lieux, 3 chemins ; flux vide.')
