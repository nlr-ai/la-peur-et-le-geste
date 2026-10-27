"""Récupère des notes effectivement écrites/lues dans les sessions des habitants."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
LOGS = pathlib.Path.home() / '.claude/projects'

for who in ['aria', 'dev-lumina', 'quantum', 'gaia', 'pitch', 'juris']:
    found = {}
    for logfile in (LOGS / ('C--Users-reyno-le-conseil2-mondes-lumina-prime-chambres-' + who)).glob('*.jsonl'):
        calls = {}
        for line in logfile.read_text(encoding='utf-8').splitlines():
            try:
                event = json.loads(line)
            except ValueError:
                continue
            content = (event.get('message') or {}).get('content') or []
            if not isinstance(content, list):
                continue
            for item in content:
                if not isinstance(item, dict):
                    continue
                if item.get('type') == 'tool_use':
                    calls[item['id']] = item
                elif item.get('type') == 'tool_result' and not item.get('is_error'):
                    call = calls.get(item.get('tool_use_id'), {})
                    args = call.get('input', {})
                    text = ''
                    target = str(args.get('file_path', args.get('path', ''))).replace('\\', '/')
                    if target.endswith('/ma-memoire/ce-que-je-tiens-pour-vrai.txt'):
                        if call.get('name') == 'Edit':
                            text = args.get('new_string', '')
                        elif call.get('name') == 'Write':
                            text = args.get('content', '')
                        elif call.get('name') == 'Read':
                            text = item.get('content', '')
                    elif call.get('name') == 'Bash' and 'cat ' in args.get('command', '') and 'ce-que-je-tiens-pour-vrai.txt' in args.get('command', ''):
                        raw = item.get('content', '')
                        if isinstance(raw, str) and 'CE QUE JE TIENS POUR VRAI' in raw:
                            text = raw.split('CE QUE JE TIENS POUR VRAI', 1)[1]
                    if not isinstance(text, str):
                        continue
                    text = re.sub(r'^\s*\d+→', '', text, flags=re.M)
                    started = False
                    for paragraph in re.split(r'\n\s*\n', text):
                        paragraph = paragraph.strip()
                        if paragraph.startswith('- '):
                            started = True
                            # Une note se conserve comme témoignage daté, pas comme nouvelle croyance.
                            found.setdefault(paragraph, dict(session=logfile.stem, date=event.get('timestamp'), texte=paragraph))
                        elif started and paragraph:
                            break
    p = ROOT / 'chambres' / who / 'ma-memoire' / 'ce-que-je-tiens-pour-vrai.txt'
    current = p.read_text(encoding='utf-8')
    missing = [x for x in found.values() if x['texte'] not in current]
    if missing:
        current += '\n\nNOTES PERSONNELLES RETROUVÉES — écritures antérieures, à relire avec les nouvelles plus récentes.\n\n'
        current += '\n\n'.join(x['texte'] for x in missing) + '\n'
        p.write_text(current, encoding='utf-8')
        evidence = p.parent / 'recuperation-notes.json'
        old = json.loads(evidence.read_text(encoding='utf-8')) if evidence.exists() else []
        evidence.write_text(json.dumps(old + missing, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(who, len(missing), 'notes retrouvées')
