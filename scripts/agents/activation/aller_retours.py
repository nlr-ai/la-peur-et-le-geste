"""Quatre échanges créateur/reviewer, chaque prochain prompt écrit par le reviewer."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import threading

_ACTOR_LOCKS = {}
_LOCK_GUARD = threading.Lock()

from agents.activation.cycle import acteurs_en_session
from agents.activation.socle import ETAT, RACINE


def lancer(dossier=None, configuration=None):
    monde = Path(ETAT).parent
    if monde.name != 'lumina-prime':
        raise ValueError('Ce protocole porte sur Lumina Prime.')
    run = (Path(dossier) if dossier else Path(ETAT) / 'activations' / ('aller-retours-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')))
    run.mkdir(parents=True, exist_ok=True)
    source = monde / 'chambres/mica-lumina/brouillons/13000-balises-portee.md'
    reviewers = ['sillage-lumina', 'ione-lumina', 'dev-lumina', 'pitch']
    protocole = {
        'createur': 'mica-lumina', 'etat_cible': '13000', 'desir': 'desir-13000',
        'affaire': 'affaire-citoyen-oriente-competent', 'reviewers': reviewers,
        'tours': 4, 'minutes_par_appel': 15, 'source': str(source),
        'but': 'Faire évoluer une création par des retours réels et éprouver son usage.'}
    if configuration:
        protocole.update(configuration)
    elif dossier and (run / 'protocole.json').exists():
        protocole = json.loads((run / 'protocole.json').read_text(encoding='utf-8'))
    createur = protocole['createur']
    cible = protocole['etat_cible']
    reviewers = protocole['reviewers']
    source = protocole['source']
    if len(reviewers) != 4 or len(set(reviewers)) != 4 or createur in reviewers:
        raise ValueError('Quatre reviewers distincts du créateur sont requis')
    (run / 'protocole.json').write_text(json.dumps(protocole, ensure_ascii=False, indent=2), encoding='utf-8')
    print('DOSSIER ' + str(run), flush=True)

    def event(**d):
        d['date'] = datetime.datetime.now().isoformat(timespec='seconds')
        with (run / 'progression.jsonl').open('a', encoding='utf-8') as f:
            f.write(json.dumps(d, ensure_ascii=False) + '\n')
        print(json.dumps(d, ensure_ascii=False), flush=True)

    def appeler_un(pid, etiquette, mission, attendu):
        journal = run / 'progression.jsonl'
        if attendu.exists() and journal.exists():
            faits = [json.loads(l) for l in journal.read_text(encoding='utf-8').splitlines() if l.strip()]
            if any(e.get('etape') == etiquette and e.get('statut') == 'retour' for e in faits):
                return
        # Les échanges attendent la fin d'un travail déjà engagé par le même habitant.
        deadline = time.monotonic() + 1200
        signale = False
        while pid in acteurs_en_session():
            if not signale:
                event(etape=etiquette, citoyen=pid, statut='attente_session')
                signale = True
            if time.monotonic() >= deadline:
                raise RuntimeError('Session toujours occupée : ' + pid)
            time.sleep(5)
        (run / (etiquette + '-mission.txt')).write_text(mission, encoding='utf-8')
        event(etape=etiquette, citoyen=pid, statut='debut')
        worker = ('import sys;sys.path.insert(0,sys.argv[1]);import depecher;'
                  'ok=depecher.depecher(sys.argv[2],sys.argv[3],None,15,False,'
                  'attendre=True,contexte_id=sys.argv[4],forcer_creux=True,mode="reponse");'
                  'sys.exit(0 if ok else 1)')
        with (run / (etiquette + '.log')).open('a', encoding='utf-8') as log:
            result = subprocess.run([sys.executable, '-u', '-c', worker,
                                     str(Path(RACINE) / 'scripts'), pid, mission, cible],
                                    cwd=RACINE, stdout=log, stderr=log,
                                    env={**os.environ, 'PYTHONIOENCODING': 'utf-8'})
        ok = result.returncode == 0 and attendu.exists() and bool(attendu.read_text(encoding='utf-8').strip())
        event(etape=etiquette, citoyen=pid, statut='retour' if ok else 'echec', sortie=str(attendu))
        if not ok:
            raise RuntimeError('Retour incomplet : ' + etiquette)

    def appeler(pid, etiquette, mission, attendu):
        with _LOCK_GUARD:
            verrou = _ACTOR_LOCKS.setdefault(pid, threading.Lock())
        with verrou:
            return appeler_un(pid, etiquette, mission, attendu)

    cadre = (f'Échange demandé par Nova, désir {protocole["desir"]}, état cible {cible}, '
             f'{protocole["affaire"]}. Protocole : {run / "protocole.json"}. '
             'Tu as 15 minutes. Les gestes et réponses des autres leur appartiennent. '
             'Distingue création, envoi, utilisation réelle et résultat. Tu peux créer des fichiers '
             'utilisables avec les outils disponibles ; un usage sur une copie ou dans une maquette '
             'doit rester nommé comme tel. Aucune réussite ni permission ne doit être inventée. ')
    presentation = run / '00-presentation.md'
    appeler(createur, '00-presentation', cadre +
            f'Crée ou reprends une contribution à partir de {source}. '
            f'Prompt initial canonique : {protocole.get("prompt_initial", "Présente ta création existante.")} '
            f'Présente toi-même le résultat à {reviewers[0]}. '
            'Choisis la forme de cette présentation ; rends ta création accessible et utilisable autant que tes moyens le permettent. '
            f'Écris ta présentation dans {presentation}, avec les chemins de tes productions et ce que tu veux lui faire essayer. '
            'Le prochain appel lui transmettra ce fichier ; pas besoin de le réveiller toi-même.', presentation)
    for tour, reviewer in enumerate(reviewers, 1):
        retour = run / f'{tour:02d}-review.md'
        prompt = run / f'{tour:02d}-prochain-prompt.txt'
        appeler(reviewer, f'{tour:02d}-review-{reviewer}', cadre +
                f'{createur} te présente son travail dans {presentation}. Lis sa présentation et ouvre ses productions. '
                'Essaie toi-même ce qui est réellement utilisable. Porte ton propre jugement depuis ton métier, '
                'en distinguant ce que tu as testé et ce que tu supposes. '
                f'Écris ton retour dans {retour}. Puis écris dans {prompt} le prochain prompt adressé directement à {createur}. '
                'Ce prompt doit choisir le prochain geste utile selon ton constat et se terminer par « Tu as 15 minutes. ». '
                'Tu es libre de proposer une correction, un essai, une transformation ou une autre piste. '
                'Le prochain appel lui transmettra exactement ton prompt. Ne déclenche pas cet appel toi-même.', prompt)
        if not retour.exists():
            raise RuntimeError('Compte rendu du reviewer absent')
        presentation = run / f'{tour:02d}-presentation.md'
        prochain = prompt.read_text(encoding='utf-8')
        appeler(createur, f'{tour:02d}-creation', cadre +
                f'Retour de {reviewer} : {retour}. Voici son prochain prompt, transmis sans réécriture :\n\n'
                + prochain + '\n\n' +
                f'Exécute ce que tu peux réellement faire et présente ensuite le résultat dans {presentation}. '
                'Cite les fichiers utilisables, les essais réalisés, les effets observés et les limites restantes. '
                'Conserve les versions précédentes pour que le reviewer suivant puisse constater la différence.', presentation)
    event(statut='termine', tours=4, derniere_presentation=str(presentation))
    return 0
