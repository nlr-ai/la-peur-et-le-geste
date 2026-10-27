"""Lot autonome borné de protocoles créateur/reviewers."""
import concurrent.futures
import json
from pathlib import Path
import time

from agents.activation.aller_retours import lancer as lancer_experience
from agents.activation.socle import ETAT


def lancer(manifeste, sec=False, parallele=3):
    path = Path(manifeste).resolve()
    config = json.loads(path.read_text(encoding='utf-8'))
    personnes = {p['id'] for p in json.loads((Path(ETAT) / 'personnages.json').read_text(encoding='utf-8'))}
    joueurs = json.loads((Path(ETAT) / 'joueurs.json').read_text(encoding='utf-8'))
    if isinstance(joueurs, dict):
        joueurs = joueurs.get('joueurs', joueurs.get('sieges', []))
    exclus = {p.get('personnage_id') for p in joueurs} | {'nova'}
    vus = set()
    for exp in config['experiences']:
        ident = exp['id']
        if ident in vus or Path(ident).name != ident or ident in ('.', '..'):
            raise ValueError('Identifiant invalide ou répété')
        vus.add(ident)
        acteurs = [exp['createur'], *exp['reviewers']]
        if len(acteurs) != 5 or len(set(acteurs)) != 5 or not set(acteurs) <= personnes or set(acteurs) & exclus:
            raise ValueError('Casting invalide : ' + ident)
        if not Path(exp['source']).is_file():
            raise ValueError('Source absente : ' + exp['source'])
    if parallele < 1:
        raise ValueError('Parallélisme positif requis')
    if sec:
        print(json.dumps(config, ensure_ascii=False, indent=2))
        return 0

    def execute(exp):
        dossier = path.parent / exp['id']
        resultat = {'id': exp['id'], 'statut': 'en_cours'}
        dossier.mkdir(exist_ok=True)
        fichier = dossier / 'resultat.json'
        for tentative in range(1, 3):
            resultat['tentative'] = tentative
            fichier.write_text(json.dumps(resultat, ensure_ascii=False, indent=2), encoding='utf-8')
            try:
                lancer_experience(dossier, exp)
                resultat['statut'] = 'termine'
                resultat.pop('erreur', None)
                break
            except Exception as exc:
                resultat.update(statut='echec', erreur=str(exc))
                fichier.write_text(json.dumps(resultat, ensure_ascii=False, indent=2), encoding='utf-8')
                if tentative < 2:
                    time.sleep(20)
        fichier.write_text(json.dumps(resultat, ensure_ascii=False, indent=2), encoding='utf-8')
        return resultat

    with concurrent.futures.ThreadPoolExecutor(max_workers=parallele) as pool:
        futures = [pool.submit(execute, exp) for exp in config['experiences']]
        resultats = []
        for future in concurrent.futures.as_completed(futures):
            resultats.append(future.result())
            (path.parent / 'bilan.json').write_text(json.dumps(resultats, ensure_ascii=False, indent=2), encoding='utf-8')
    return int(any(r['statut'] != 'termine' for r in resultats))
