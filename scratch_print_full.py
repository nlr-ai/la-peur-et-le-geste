import subprocess
proc = subprocess.Popen(['python', 'scripts/depecher.py', '--qui', 'leo-wyatt', '--mode', 'reponse', '--beats-jump', '--event-jump', 'placeholder', '--mission', 'test'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
