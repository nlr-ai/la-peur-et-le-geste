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
RUN = Path(sys.argv[1]) if len(sys.argv) > 1 else WORLD / 'experiences' / ('dev-dix-reveils-' + datetime.now().strftime('%Y%m%d-%H%M%S'))
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
MESSAGES = ['Tu as 20 minutes. Choisis une ambition qui compte pour toi, décompose-la en 5 étapes et accomplis la première.', 'En 5 étapes, transforme une de tes idées en une première réalisation utilisable. Tu as 20 minutes : livre ce que tu peux réellement terminer.', 'Tu as 20 minutes pour faire avancer ton projet avec quelqu’un. Trouve un interlocuteur, apporte quelque chose de concret et laisse sa réponse lui appartenir.', 'Examine ton travail sous 3 angles différents. Choisis sa faiblesse principale et consacre les 20 prochaines minutes à l’améliorer.', 'Trouve 5 façons de dépasser ton principal obstacle. Choisis la plus prometteuse parmi celles que tu peux essayer maintenant et mets-la à l’épreuve.', 'Tu as 20 minutes pour ouvrir ton travail aux autres. Prépare une contribution possible, rends-la accessible et adresse une invitation précise.', 'Vois plus grand. En 5 étapes, cherche comment étendre la portée de ce que tu construis. Engage dès maintenant l’étape qui ouvre le plus de possibilités.', 'Consacre 20 minutes à éprouver ta réalisation. Essaie 3 situations difficiles, distingue les essais réels des hypothèses et corrige ce que tu peux.', 'En 5 étapes, rends ta réalisation utilisable sans toi. Va jusqu’à une transmission concrète ; ce qui demande encore ta présence doit être explicite.', 'Tu as 20 minutes. Relis tes résultats, distingue ce qui existe de ce que tu espères, choisis une ambition plus grande et accomplis son premier geste.']

def snapshot(name):
    out = {}
    for f in ('actes.json', 'paroles.json', 'personnages.json', 'intentions.json', 'monde.json'):
        out[f] = json.loads((WORLD / 'etat' / f).read_text(encoding='utf-8-sig'))
    out['fichiers_chambre'] = {str(p.relative_to(WORLD)): {'taille': p.stat().st_size, 'mtime': p.stat().st_mtime} for p in (WORLD / 'chambres/dev-lumina').rglob('*') if p.is_file()}
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
            ok = depecher.depecher('dev-lumina', message, None, 20, False, attendre=True, forcer_creux=True)
    snapshot(f'{i:02d}-apres.json')
    mot = WORLD / 'chambres/dev-lumina/demain.md'
    if ok and mot.exists():
        (RUN / f'{i:02d}-retour.md').write_text(mot.read_text(encoding='utf-8'), encoding='utf-8')
    result = {'reveil': i, 'ok': bool(ok), 'secondes': round(time.time() - start)}
    with (RUN / 'progression.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps(result) + '\n')
    print('FIN ' + json.dumps(result), flush=True)
    if not ok:
        print('ARRET SUR ECHEC : message non accompli, reprise requise.', flush=True)
        sys.exit(1)
print('TERMINE 10/10', flush=True)
