"""Run the reviewed Juris comparator on a captured, bounded input set."""
import argparse
import datetime
import difflib
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

VERSION = 'c87da5d2ee8439a46ffd8e60c3977cc56ffe9ddba45d8bb28f7973442405ff99'
MEMORIES = ['ma-memoire/ce-que-je-tiens-pour-vrai.txt', 'ma-memoire/croyances-etat.txt']

def digest(data):
    return hashlib.sha256(data).hexdigest()

def capture(chamber, destination):
    chamber = chamber.resolve()
    files = [chamber / name for name in MEMORIES]
    files += list((chamber / 'brouillons').glob('temoin-*'))
    files += list((chamber / 'fil').glob('*')) + list((chamber / 'fil/contextes').glob('*'))
    manifest = []
    total = 0
    for file in sorted(set(files)):
        if not file.exists() or file.is_dir():
            continue
        if file.is_symlink() or not file.resolve().is_relative_to(chamber):
            raise ValueError('source_hors_chambre')
        data = file.read_bytes()
        total += len(data)
        if total > 20_000_000 or len(manifest) >= 2000:
            raise ValueError('sources_trop_grandes')
        relative = file.relative_to(chamber)
        out = destination / relative
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        manifest.append({'path': relative.as_posix(), 'sha256': digest(data), 'bytes': len(data)})
    return manifest

def run(chamber, script, evidence):
    source = script.read_bytes()
    if digest(source) != VERSION:
        raise ValueError('version_non_examinée')
    evidence.mkdir(parents=True, exist_ok=False)
    snapshot = evidence / 'inputs'
    snapshot.mkdir()
    manifest = capture(chamber, snapshot)
    executable = evidence / 'comparateur.py'
    executable.write_bytes(source)
    flags = {'creationflags': subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {}
    child = subprocess.run([sys.executable, '-I', '-B', '-X', 'utf8', str(executable.resolve()), str(snapshot.resolve())],
                           cwd=evidence, capture_output=True, text=True, encoding='utf8',
                           env={**os.environ, 'PYTHONIOENCODING':'utf-8'}, timeout=20, **flags)
    if child.returncode:
        raise RuntimeError(child.stderr[-2000:])
    raw = json.loads(child.stdout)
    comparisons = []
    for row in raw:
        name = row['fichier']
        if name not in MEMORIES:
            raise ValueError('sortie_invalide')
        current = snapshot / name
        witness = row.get('temoin')
        if not witness:
            comparisons.append({'file':name, 'status':'source ou témoin absent', 'diff':None})
            continue
        if Path(witness).name != witness:
            raise ValueError('temoin_invalide')
        baseline = snapshot / 'brouillons' / witness
        before, after = baseline.read_bytes(), current.read_bytes()
        diff = '\n'.join(difflib.unified_diff(before.decode('utf8').splitlines(), after.decode('utf8').splitlines(),
                                             fromfile=witness, tofile=name, lineterm=''))
        comparisons.append({'file':name, 'witness':witness, 'before':digest(before), 'after':digest(after),
                            'status':'identique' if before == after else 'modifié', 'diff':diff,
                            'bytesChangedWithoutLineDiff':before != after and not diff})
    stable = all((chamber / x['path']).is_file() and digest((chamber / x['path']).read_bytes()) == x['sha256'] for x in manifest)
    report = {'ok':stable, 'executed':True, 'script_version':VERSION,
              'capturedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'canonicalChanged':False, 'inputs':manifest, 'comparisons':comparisons, 'script_result':raw,
              'checks':[{'name':'Comparateur exécuté sur la version examinée', 'ok':True},
                        {'name':'Sources inchangées pendant la comparaison', 'ok':stable}],
              'method':'Python sur copie des fichiers de Juris ; diff ordonné indépendant avec difflib.',
              'limits':['Le témoin est choisi par le script selon le nom, sans garantie du plus récent.',
                        'Une différence ne prouve ni son auteur ni sa cause.',
                        'La recherche de provenance est textuelle ; les canaux du parloir ne sont pas consultés.',
                        'Un témoin absent reste inconnu ; aucune copie de référence n’est inventée.']}
    (evidence / 'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    return report

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--chamber',type=Path,required=True)
    parser.add_argument('--script',type=Path,required=True)
    parser.add_argument('--evidence',type=Path,required=True)
    args=parser.parse_args()
    sys.stdout.reconfigure(encoding='utf8')
    print(json.dumps(run(args.chamber,args.script,args.evidence),ensure_ascii=False))
