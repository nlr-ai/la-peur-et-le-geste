"""Consigner une conséquence de choix attesté, sans analyser arbitrairement le texte."""
import argparse
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / 'mondes/la-peur-et-le-geste'
CONFIG = WORLD / 'liaison-ferveurs.json'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ref', required=True)
    parser.add_argument('--delta', type=int, choices=range(-10, 11), required=True)
    parser.add_argument('--raison', required=True)
    args = parser.parse_args()
    target = Path(json.loads(CONFIG.read_text(encoding='utf-8-sig'))['choix_joueur'])
    data = json.loads(target.read_text(encoding='utf-8'))
    player = next(p for p in data if p['id'] == 406 and p['first'] == 'Michel' and p['last'] == 'Sauzeau')
    if any(c['ref'] == args.ref for c in player['choices']):
        print('Choix déjà compté : aucune modification.'); return
    actions = [json.loads(p.read_text(encoding='utf-8-sig')) for p in (WORLD/'etat/inbox/michel').glob('action-*.json')]
    action = next((a for a in actions if a.get('ref') == args.ref), None)
    if not action or action.get('joueur_id') != 'michel':
        parser.error('Référence de décision de Michel introuvable.')
    if action.get('mode') in ('meta', 'commenter', 'intervention', 'composer', 'run', 'jump'):
        parser.error('Une commande hors fiction ne change pas la ferveur.')
    if action.get('type') == 'demande' and (action.get('reponse') not in ('voie', 'libre') or
            action.get('demande_id', '').startswith('michel-lucien-gouts-v1-') and not action.get('demande_id').endswith('-1')):
        parser.error('Cette réponse ne porte pas un engagement en fiction.')
    date = action.get('date_atteinte')
    if not date or not all(k in date for k in ('annee','lune','jour')):
        parser.error('La décision doit avoir une date de fiction explicite.')
    minute = date.get('minute', 0)
    at = datetime(date['annee'],date['lune'],date['jour'],minute//60,minute%60).isoformat()
    player['choices'].append({'ref': args.ref, 'at': at, 'delta': args.delta, 'reason': args.raison, 'texte': action.get('texte', '')})
    temporary = target.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    temporary.replace(target)
    print('Ferveur :', max(0,min(100,player['baseline']+sum(c['delta'] for c in player['choices']))))

if __name__ == '__main__': main()
