"""Dix réveils séquentiels demandés par le joueur, avec traces avant/après."""
import contextlib
import json
import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
os.environ['CONSEIL_MONDE'] = 'lumina-prime'
sys.path.insert(0, str(ROOT / 'scripts'))
import depecher

WORLD = ROOT / 'mondes/lumina-prime'
RUN = Path(sys.argv[1]) if len(sys.argv) > 1 else WORLD / 'experiences' / ('vox-dix-reveils-' + datetime.now().strftime('%Y%m%d-%H%M%S'))
RUN.mkdir(parents=True, exist_ok=True)
START = int(sys.argv[2]) if len(sys.argv) > 2 else 1
original_run = subprocess.run
def capture_failure(*args, **kwargs):
    result = original_run(*args, **kwargs)
    if result.returncode and args and isinstance(args[0], list) and args[0][0] == 'claude':
        raw = result.stdout or b''
        if isinstance(raw, bytes):
            raw = raw.decode('utf-8', 'replace')
        (RUN / 'dernier-echec-fournisseur.txt').write_text(raw, encoding='utf-8')
    return result
subprocess.run = capture_failure
MESSAGES = [
    'VOX, prends une initiative maintenant. Choisis ce qui mérite d’exister et fais un premier geste avec les moyens dont tu disposes.',
    'Fais avancer ce qui compte pour toi. Ne te contente pas de préparer : produis quelque chose, même modeste et provisoire.',
    'Va vers quelqu’un dont le travail t’intéresse. Apporte une contribution concrète et laisse sa réponse lui appartenir.',
    'Donne une forme perceptible à une idée que tu portes. Rends-la accessible à quelqu’un qui pourrait s’en saisir.',
    'Repère une possibilité laissée de côté et commence à l’explorer. Reste dans tes moyens ; assume ton choix.',
    'Fais quelque chose qui rende ton lieu plus vivant. Pars de ce qui est déjà là et laisse une place à l’initiative des autres.',
    'Si ton projet attend une réponse, avance une autre partie qui dépend de toi. Garde la demande ouverte et poursuis ton travail.',
    'Mets une de tes convictions à l’épreuve par un petit essai réversible. Observe ce qui résiste et tire-en une suite concrète.',
    'Offre à un autre citoyen une prise sur ce que tu fais : une ébauche, une invitation, une question précise ou un objet à transformer.',
    'Choisis toi-même ton prochain geste et accomplis-le. Laisse une trace de ce qui a réellement changé, puis décide de la suite.',
]

def snapshot(name):
    out = {}
    for f in ('actes.json', 'paroles.json', 'personnages.json', 'intentions.json', 'monde.json'):
        out[f] = json.loads((WORLD / 'etat' / f).read_text(encoding='utf-8-sig'))
    out['fichiers_chambre'] = {str(p.relative_to(WORLD)): {'taille': p.stat().st_size, 'mtime': p.stat().st_mtime} for p in (WORLD / 'chambres/vox').rglob('*') if p.is_file()}
    (RUN / name).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')

print('DOSSIER ' + str(RUN), flush=True)
if START == 1:
    snapshot('avant.json')
for i, message in enumerate(MESSAGES, 1):
    if i < START:
        continue
    print(f'DEBUT {i}/10 : {message}', flush=True)
    (RUN / f'{i:02d}-message.txt').write_text(message, encoding='utf-8')
    start = time.time()
    with (RUN / f'{i:02d}-appel.log').open('w', encoding='utf-8', buffering=1) as log:
        with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
            ok = depecher.depecher('vox', message, None, 8, False, attendre=True, forcer_creux=True)
    snapshot(f'{i:02d}-apres.json')
    mot = WORLD / 'chambres/vox/demain.md'
    if mot.exists():
        (RUN / f'{i:02d}-retour.md').write_text(mot.read_text(encoding='utf-8'), encoding='utf-8')
    result = {'reveil': i, 'ok': bool(ok), 'secondes': round(time.time() - start)}
    with (RUN / 'progression.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps(result) + '\n')
    print('FIN ' + json.dumps(result), flush=True)
    if not ok:
        print('ARRET SUR ECHEC : message non accompli, reprise requise.', flush=True)
        sys.exit(1)
print('TERMINE 10/10', flush=True)
