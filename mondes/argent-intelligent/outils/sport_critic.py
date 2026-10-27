"""Observateur local : huit messages communs, une critique indépendante.

python mondes/argent-intelligent/outils/sport_critic.py --watch
--voir : compte seulement, aucun appel ni écriture.
Au premier démarrage, commence au premier message joueur (pas aux rappels).
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import uuid

WORLD = Path(__file__).resolve().parents[1]
ROOT = WORLD.parents[1]
STATE = WORLD / '.agents-runtime' / 'sport-critic'
FLUX = WORLD / 'etat' / 'flux.jsonl'
TYPES = {'vous', 'recit', 'reponse', 'replique', 'geste', 'evenement'}


def lire_flux():
    rows = []
    for n, line in enumerate(FLUX.read_text(encoding='utf-8').splitlines(), 1):
        try:
            rows.append((n, json.loads(line)))
        except ValueError:
            # Un append peut être en cours : ne pas dépasser une ligne incomplète.
            break
    return rows


def commun(item):
    audience = item.get('pour')
    return item.get('commun') is True or isinstance(audience, list) and {'usages', 'economie', 'blockchain', 'ia', 'gouvernance', 'red-team'} <= set(audience)


def messages(rows):
    started = False
    out = []
    for n, item in rows:
        if item.get('type') == 'vous':
            started = True
        if (started and commun(item) and item.get('type') in TYPES
                and item.get('qui') != 'sport-critic'
                and not str(item.get('ref', '')).startswith('sport-critic-')
                and item.get('texte')
                and not str(item.get('ref', '')).startswith(('argent-ouverture-', 'argent-critic-activation'))):
            out.append((n, item))
    return out


def sauver(path, data):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    temp.replace(path)


def cycle():
    rows = lire_flux()
    cursor_file = STATE / 'curseur.json'
    cursor = json.loads(cursor_file.read_text(encoding='utf-8')).get('ligne', 0) if cursor_file.exists() else 0
    batch = [(n, i) for n, i in messages(rows) if n > cursor][:8]
    if len(batch) < 8:
        return False
    fingerprint = hashlib.sha256(json.dumps(batch, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]
    ref = 'sport-critic-' + fingerprint
    # Reprise après une publication réussie mais avant écriture du curseur.
    if any(i.get('ref') == ref for _, i in rows):
        sauver(cursor_file, {'ligne': batch[-1][0], 'ref': ref})
        return True
    output = STATE / (ref + '.json')
    if not output.exists():
        sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'scripts' / 'noyau')]
        import agents.expose  # initialise la porte du container
        from agents import runtime
        brief = '\n\n'.join('Message %d — %s (%s) :\n%s' %
                               (n, i.get('joueur_id') or i.get('qui') or 'MJ', i['type'], i['texte'])
                               for n, i in batch)
        manual = (WORLD / 'manuel.md').read_text(encoding='utf-8')
        result = runtime.appeler('sport-critic', (WORLD / 'prompts/sport-critic.md').read_text(encoding='utf-8'),
                                 'Règles de la partie :\n' + manual + '\n\nHuit messages à analyser :\n' + brief,
                                 str(uuid.uuid4()), cwd=tempfile.mkdtemp(prefix='sport-critic-'),
                                 timeout=600, reprendre=False)
        text = (result.get('result') or '').strip()
        if not text:
            raise RuntimeError('Commentaire vide ; curseur conservé.')
        sauver(STATE / (ref + '-preuve.json'), {'messages': batch, 'provider': result.get('provider'),
                                               'model': result.get('model'), 'result': text})
        sauver(output, [{'type': 'reponse', 'qui': 'sport-critic', 'texte': text,
                         'ref': ref, 'duree': 0}])
    subprocess.run([sys.executable, str(ROOT / 'scripts/append_flux.py'), '--pour', 'tous',
                    '--fichier', str(output)], cwd=ROOT, check=True)
    sauver(cursor_file, {'ligne': batch[-1][0], 'ref': ref})
    print('Publié : ' + ref, flush=True)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--watch', action='store_true')
    ap.add_argument('--voir', action='store_true')
    args = ap.parse_args()
    if args.voir:
        print(json.dumps({'messages_eligibles': len(messages(lire_flux()))}))
        return
    os.environ['CONSEIL_MONDE'] = 'argent-intelligent'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    STATE.mkdir(parents=True, exist_ok=True)
    # Verrou système libéré même après crash du processus.
    lock = open(STATE / 'watch.lock', 'a+b')
    lock.seek(0); lock.write(b'0'); lock.flush(); lock.seek(0)
    if os.name == 'nt':
        import msvcrt
        msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
    else:
        import fcntl
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    failures = 0
    try:
        while True:
            try:
                done = cycle()
                failures = 0
            except Exception as exc:
                failures += 1
                print('Erreur, curseur conservé : ' + str(exc), flush=True)
                if not args.watch or failures >= 3:
                    raise
                time.sleep(30)
                continue
            if not args.watch:
                return
            time.sleep(5 if not done else 1)
    finally:
        lock.close()


if __name__ == '__main__':
    main()
