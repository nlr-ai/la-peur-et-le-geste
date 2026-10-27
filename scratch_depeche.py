import subprocess
res = subprocess.run(['python', 'scripts/depecher.py', '--qui', 'leo-wyatt', '--mode', 'reponse', '--mission', 'Tu reviens du plan des Fondateurs au grenier auprès de Phoebe, Piper et Paige. Que leur dis-tu mot pour mot ?'], capture_output=True, text=True, encoding='utf-8')
print(res.stdout)
print(res.stderr)
