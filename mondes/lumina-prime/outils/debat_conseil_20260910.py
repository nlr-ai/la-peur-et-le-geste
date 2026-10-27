"""Invitation simultanée du conseil, deux passages dans un Markdown commun."""
import contextlib
import json
import os
import sys
import subprocess
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORLD = ROOT / 'mondes/lumina-prime'
os.environ['CONSEIL_MONDE'] = 'lumina-prime'
sys.path.insert(0, str(ROOT / 'scripts'))
import depecher

DOC = WORLD / 'discussions/2026-09-10-conseil-ville-reveils-prompts-24h.md'
RUN = WORLD / 'experiences/debat-conseil-20260910'
RUN.mkdir(parents=True, exist_ok=True)
PEOPLE = [('aria', 'Aria'), ('dev-lumina', 'DEV'), ('quantum', 'Quantum'),
          ('gaia', 'Gaia'), ('pitch', 'PITCH'), ('juris', 'JURIS')]

def event(**data):
    data['date'] = datetime.now().isoformat(timespec='seconds')
    with (RUN / 'progression.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')
    print(json.dumps(data, ensure_ascii=False), flush=True)

if len(sys.argv) == 1:
    children = []
    for who, name in PEOPLE:
        if who == 'aria':
            continue  # Son appel initial continue dans son processus propre.
        log = (RUN / f'worker-1-{who}.log').open('a', encoding='utf-8')
        children.append(subprocess.Popen([sys.executable, '-u', __file__, '1', who], stdout=log, stderr=log))
    for child in children:
        child.wait()
    deadline = time.time() + 600
    while '## Tour 1 — Aria' not in DOC.read_text(encoding='utf-8') and time.time() < deadline:
        time.sleep(2)
    children = []
    for who, name in PEOPLE:
        if who == 'aria' and '## Tour 1 — Aria' not in DOC.read_text(encoding='utf-8'):
            event(qui=who, etat='premier_retour_absent')
            continue
        log = (RUN / f'worker-2-{who}.log').open('a', encoding='utf-8')
        children.append(subprocess.Popen([sys.executable, '-u', __file__, '2', who], stdout=log, stderr=log))
    for child in children:
        child.wait()
    event(etat='termine', contributions=DOC.read_text(encoding='utf-8').count('## Tour '))
    sys.exit(0)

for tour in (int(sys.argv[1]),):
    for who, name in PEOPLE:
        if who != sys.argv[2]:
            continue
        heading = f'## Tour {tour} — {name}'
        if heading in DOC.read_text(encoding='utf-8'):
            continue
        angle = ('Présente ta position personnelle sur les cinq questions, convergence comprise.' if tour == 1 else
                 'Lis toutes les positions du premier tour. Réponds explicitement à au moins deux propositions de collègues, explique tes accords ou désaccords et précise ce que tu proposes pour les 24 h. Tu peux changer d’avis. Ne fabrique aucun consensus.')
        mission = (
            f'Le joueur convoque tout le conseil pour débattre dans {DOC}. '
            'Lis ce fichier et ses cinq questions, ainsi que les sources locales nécessaires. '
            f'{angle} Ajoute toi-même en fin de ce fichier une contribution sous le titre exact « {heading} ». '
            'Les collègues travaillent simultanément : relis le fichier avant de contribuer. Ajoute en mode append uniquement, en une seule écriture ; ne réécris jamais le fichier entier. Écris environ 400 à 700 mots utiles. Préserve tout le contenu existant. '
            'Tu es invité à une discussion de conception, sans exécuter les propositions : '
            'ne modifie ni code, ni prompts actifs, ni état du monde. N’envoie pas d’autres invitations ; '
            'les six membres reçoivent déjà celle-ci. Termine par une courte confirmation du chemin écrit.'
        )
        (RUN / f'{tour}-{who}-invitation.txt').write_text(mission, encoding='utf-8')
        event(tour=tour, qui=who, etat='appel')
        try:
            with (RUN / f'{tour}-{who}.log').open('a', encoding='utf-8', buffering=1) as log:
                with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
                    ok = depecher.depecher(who, mission, None, 10, False,
                        attendre=True, forcer_creux=True, mode='discussion')
            present = heading in DOC.read_text(encoding='utf-8')
            event(tour=tour, qui=who, etat='contribution' if present else 'sans_contribution', appel_ok=bool(ok))
        except Exception as exc:
            event(tour=tour, qui=who, etat='erreur', detail=str(exc))
event(etat='termine', contributions=DOC.read_text(encoding='utf-8').count('## Tour '))
