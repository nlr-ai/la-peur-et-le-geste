import json, os, subprocess, shutil
from pathlib import Path

root = Path(__file__).resolve().parents[1]
state = root / 'mondes/la-peur-et-le-geste/etat'
def read(name): return json.loads((state / name).read_text(encoding='utf-8-sig'))
def write(name, value): (state / name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
assert not any('15 juin 1940 — J1' in line for line in (state/'flux.jsonl').read_text(encoding='utf-8').splitlines()), 'Intro déjà publiée'
backup = root / 'scratchpad/avant-intro-michel-j1'
backup.mkdir(exist_ok=True)
for name in ['joueurs.json','horloges.json','personnages.json','paroles.json','actes.json','intentions.json','presence.json','monde.json']:
    shutil.copy2(state/name, backup/name)
date = dict(annee=1940,lune=6,jour=15,minute=750)
roster = read('joueurs.json')
assert not any(p['personnage_id']=='michel' for p in roster)
roster.append(dict(personnage_id='michel',nom='Michel',jeton='homme:michel',role='joueur',pnj=[],occupe=True,lieu='hotel-voyageurs',depuis=0))
write('joueurs.json',roster)
clocks = read('horloges.json'); clocks['michel']=date.copy(); write('horloges.json',clocks)
people=read('personnages.json')
for p in people:
    if p['id'] in ['michel','lucien-frere-de-michel']: p.update(etat='actif',lieu_id='hotel-voyageurs')
write('personnages.json',people)
source=Path('C:/Users/reyno/Modern Front/content/radio_june1940.json')
radio=json.loads(source.read_text(encoding='utf-8-sig'))
segment=radio['days'][0]['segments'][0]
print('Radio segment keys:',list(segment))
bulletin=segment.get('text') or segment.get('texte')
assert bulletin
quote='Une ville ouverte… ça veut dire qu’ils ont laissé entrer les soldats pour que les maisons restent debout ?'
items=[
 dict(type='effacer'),
 dict(type='salle',lieu='Hôtel-café des Voyageurs, Niort',salle='hotel-voyageurs',moment='15 juin 1940 — J1 — 12 h 30',presents=['michel','lucien-frere-de-michel'],tension=20),
 dict(type='recit',texte='Le poste grésille dans la salle du café. Vous êtes assis près de Lucien, ton petit frère. Sur un bout de papier, il a dessiné une bicyclette munie de deux ailes ; son crayon reste posé au milieu de la seconde. La voix du speaker vient de couvrir le souffle du poste.'),
 dict(type='recit',texte='À la radio : « '+bulletin+' »'),
 dict(type='recit',texte='Lucien a levé la tête au mot « Paris ». Il écoute jusqu’au bout, puis rapproche sa chaise de la tienne. Son doigt retient le papier qui glisse de la table.'),
 dict(type='replique',locuteur_id='lucien-frere-de-michel',texte=quote),
 dict(type='recit',texte='Il te regarde, sans ajouter tout de suite une autre question. Dans le poste, une feuille craque près du microphone ; le speaker reprend son souffle. Lucien retourne son dessin et garde le crayon à la main.')
]
for it in items: it.update(duree=0,delai_s=0)
path=root/'scratchpad/intro-michel-j1.json'; path.write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
env=os.environ.copy(); env['CONSEIL_RACINE']=''; env['CONSEIL_MONDE']='la-peur-et-le-geste'
subprocess.run(['python','scripts/append_flux.py','--fichier',str(path),'--pour','michel'],cwd=root,env=env,check=True)
paroles=read('paroles.json'); paroles.append(dict(id='lucien-radio-j1-question',date=date,locuteur_id='lucien-frere-de-michel',destinataire_id='michel',contenu=quote,type='question',temoins=[],poids=1)); write('paroles.json',paroles)
actes=read('actes.json'); actes.append(dict(id='michel-lucien-radio-j1',date=date,acteur_id='lucien-frere-de-michel',description='Lucien et Michel écoutent le journal de 12 h 30 au café des Voyageurs. Lucien interrompt son dessin et questionne Michel sur le sens de ville ouverte. Bulletin repris du script radio J1 de Modern Front, pas une transcription historique authentifiée.',cible_id='michel',connu_de=['michel','lucien-frere-de-michel'])); write('actes.json',actes)
dest=root/'sources/modern-front/content'; dest.mkdir(parents=True,exist_ok=True); shutil.copy2(source,dest/source.name)
assert read('monde.json')==json.loads((backup/'monde.json').read_text(encoding='utf-8-sig'))
assert read('horloges.json')['raymond-moreau']==clocks['raymond-moreau']
print('Intro publiée : 7 items privés Michel, Raymond inchangé.')
