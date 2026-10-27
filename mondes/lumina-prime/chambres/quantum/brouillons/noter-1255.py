import json, io
base = 'C:/Users/reyno/le-conseil2/mondes/lumina-prime/chambres/quantum/'
p = base + 'en-souffrance.json'
d = json.load(open(p, encoding='utf-8'))
if not any('11023' in x.get('quoi', '') for x in d['on_attend_de_moi']):
    d['on_attend_de_moi'].append({"pour": "dev-lumina", "du": {"annee": 2042, "lune": 1, "jour": 3},
        "quoi": "11023 (« Habiter le Creative Nexus », cahier de DEV) : besoins de fonctionnement de l'îlot projeté, avec leur coût, leurs sources, leurs unités et leurs inconnues. Proposé pour le J3 avant midi, si l'esquisse 11020 est prête le J2 ; dépend aussi de 40302. Le jour dû est à porter par DEV dans son cahier.",
        "depuis": "2042.1.1 12h55", "tenu": False})
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
s = io.open(base + 'relations/dev-lumina/claude.md', encoding='utf-8').read()
if '12h55' not in s:
    io.open(base + 'relations/dev-lumina/claude.md', 'a', encoding='utf-8').write(
        "- 12h55 : son cahier du Creative Nexus porte une action à mon nom (11023), sans date. Je lui ai écrit que je la prends, pour le J3 avant midi si son esquisse est prête ; c'est à lui de porter le jour dû.\n")
s = io.open(base + 'brouillons/memoire-tenue.md', encoding='utf-8').read()
if '11023' not in s:
    io.open(base + 'brouillons/memoire-tenue.md', 'a', encoding='utf-8').write(
        "- **11023 (cahier de DEV) :** prise, proposée pour le J3 avant midi. Billet à DEV à 12h55, sortie propre.\n")
print('ok')
