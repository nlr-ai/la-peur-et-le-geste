import json
from pathlib import Path

state = Path(__file__).resolve().parents[1] / 'etat'
def load(name):
    return json.loads((state / (name + '.json')).read_text(encoding='utf-8-sig'))
def save(name, value):
    (state / (name + '.json')).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

people = load('personnages')
next(p for p in people if p['id'] == 'nicolas')['lieu_id'] = 'lisiere-craigh'
save('personnages', people)
seats = load('joueurs')
next(s for s in seats if s['personnage_id'] == 'nicolas')['lieu'] = 'lisiere-craigh'
save('joueurs', seats)
presence = load('presence')
presence['presence']['nicolas'].update(salle='lisiere-craigh', lieu='Lisière sous les pierres')
save('presence', presence)
journal = load('journal')
journal['scene_courante'].update(participants=['aurore'], resume='Départ corrigé : Aurore arrive seule au cercle ; Nicolas arrive à la lisière. Ils ne se voient pas et ignorent leur position respective.')
save('journal', journal)
print('Positions séparées et journal mis à jour.')
