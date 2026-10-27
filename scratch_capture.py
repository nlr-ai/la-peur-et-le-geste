import subprocess
proc = subprocess.Popen(['python', 'scripts/depecher.py', '--qui', 'leo-wyatt', '--mode', 'reponse', '--mission', 'Leo, que réponds-tu mot pour mot ?'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
out, err = proc.communicate()
for line in out.splitlines():
    if 'reponse :' in line:
        with open('leo_reponse_full.txt', 'w', encoding='utf-8') as f:
            f.write(line.split('reponse :', 1)[1].strip())
