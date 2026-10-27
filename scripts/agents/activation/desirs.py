"""Lots bornés de réveils, prompts lus dans la méta-affaire du monde courant."""
import concurrent.futures
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from agents.activation.socle import ETAT, RACINE
from agents.activation.cycle import acteurs_en_session


def preparer(reveils):
    etat = Path(ETAT)
    catalogue = etat / 'maisons/cite-lumina/documents/books/affaire-reveils-par-desirs.json'
    livre = json.loads(catalogue.read_text(encoding='utf-8'))
    prompts = {r['cellules'][1]: r['cellules'] for r in livre['tables'][0]['lignes']}
    personnes = {p['id'] for p in json.loads((etat / 'personnages.json').read_text(encoding='utf-8'))}
    joueurs = json.loads((etat / 'joueurs.json').read_text(encoding='utf-8'))
    if isinstance(joueurs, dict):
        joueurs = joueurs.get('joueurs', joueurs.get('sieges', []))
    joueurs = {p.get('personnage_id') for p in joueurs}
    lots, vus = [], set()
    for spec in reveils:
        pid, cible = spec.split(':', 1)
        if pid not in personnes or pid in joueurs or pid in vus:
            raise ValueError('Citoyen absent, joueur ou répété : ' + pid)
        ident, _, source, titre, desir, prompt = prompts[cible]
        mission = (f'Réveil par désir : {ident}\nÉtat cible : {cible} — {titre}\n'
                   f'Affaire source : {source}\nCatalogue canonique : {catalogue}\n'
                   f'Désir : {desir}\n\n{prompt}\n\n'
                   'Lis le contexte dans l’affaire source. Agis depuis ta situation réelle. '
                   'À la fin, indique ce que tu as tenté, ce qui a changé, les chemins ou IDs '
                   'des productions et ce qui attend encore une réponse. Les actions des autres leur appartiennent.')
        lots.append((pid, cible, ident, mission))
        vus.add(pid)
    if not lots:
        raise ValueError('Fournir au moins un --reveil CITOYEN:ETAT')
    return lots


def lancer(args):
    lots = preparer(args.reveil)
    if args.parallele < 1:
        raise ValueError('--parallele doit être positif')
    if args.sec:
        for pid, cible, ident, mission in lots:
            print(json.dumps(dict(citoyen=pid, cible=cible, desir=ident, mission=mission), ensure_ascii=False))
        return 0
    occupes = acteurs_en_session()
    conflits = [p for p, *_ in lots if p in occupes]
    if conflits:
        raise RuntimeError('Sessions déjà actives : ' + ', '.join(conflits))
    dossier = Path(ETAT) / 'activations' / ('desirs-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
    dossier.mkdir(parents=True)
    print('DOSSIER ' + str(dossier), flush=True)

    def appel(lot):
        pid, cible, ident, mission = lot
        rec = dict(citoyen=pid, cible=cible, desir=ident, debut=datetime.datetime.now().isoformat(), minutes=15)
        (dossier / f'{pid}-mission.txt').write_text(mission, encoding='utf-8')
        (dossier / f'{pid}.json').write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding='utf-8')
        print('DEBUT ' + pid + ' ' + ident, flush=True)
        # Comme la boucle ordinaire, un réveil explicite emploie forcer_creux.
        # La CLI historique peut sortir avec 0 même si personne n'est parti.
        worker = ("import sys;sys.path.insert(0,sys.argv[1]);import depecher;"
                  "ok=depecher.depecher(sys.argv[2],sys.argv[4],None,15,False,"
                  "attendre=True,contexte_id=sys.argv[3],forcer_creux=True);"
                  "sys.exit(0 if ok else 1)")
        commande = [sys.executable, '-u', '-c', worker,
                    str(Path(RACINE) / 'scripts'), pid, cible, mission]
        debut = time.monotonic()
        with (dossier / f'{pid}.log').open('w', encoding='utf-8') as log:
            try:
                retour = subprocess.run(commande, cwd=RACINE, stdout=log, stderr=log,
                                        env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}, timeout=960)
                rec['code_sortie'] = retour.returncode
            except subprocess.TimeoutExpired:
                rec['code_sortie'] = 'timeout'
        rec['secondes'] = round(time.monotonic() - debut, 1)
        rec['fin'] = datetime.datetime.now().isoformat()
        rec['statut'] = 'appel_termine' if rec['code_sortie'] == 0 else 'echec'
        (dossier / f'{pid}.json').write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding='utf-8')
        print('FIN ' + json.dumps(rec, ensure_ascii=False), flush=True)
        return rec

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallele) as pool:
        resultats = list(pool.map(appel, lots))
    (dossier / 'bilan.json').write_text(json.dumps(resultats, ensure_ascii=False, indent=2), encoding='utf-8')
    return int(any(r['statut'] == 'echec' for r in resultats))
