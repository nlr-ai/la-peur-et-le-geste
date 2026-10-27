import subprocess
proc = subprocess.Popen(['python', 'scripts/depecher.py', '--qui', 'leo-wyatt', '--mode', 'reponse', '--mission', 'Répète mot pour mot ta réplique exacte en une seule phrase pour Phoebe.'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
out, err = proc.communicate()
with open('leo_out.txt', 'w', encoding='utf-8') as f:
    f.write(out)
