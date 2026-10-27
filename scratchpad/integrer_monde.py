from pathlib import Path
import json,re,shutil,secrets
r=Path.cwd(); w=r/'mondes/la-peur-et-le-geste'
assert json.loads((w/'etat/personnages.json').read_text(encoding='utf-8')) == [], 'Personnages déjà intégrés : arrêt.'
original_manual=(w/'manuel.md').read_text(encoding='utf-8')
e=w/'etat'
def save(p,d):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def txt(p,t):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
idx=json.loads((r/'personnages/index.json').read_text(encoding='utf-8'))['personnages']
present=['raymond-moreau','josette-moreau','jacques-augereau','emile-guillon','ernest-gaillard']
date={'annee':1940,'lune':6,'jour':18,'minute':1260}
base=r/'sources/modern-front/out/pnj/reunion-raymond-sauvegarde'
ps=[]; intents=[]; fiches={}
for x in idx:
 t=(r/'personnages'/x['fiche']).read_text(encoding='utf-8-sig'); fiches[x['id']]=t
 def section(title):
  m=re.search(r'(?ms)^## '+re.escape(title)+r'\n(.*?)(?=^## |\Z)',t);return m.group(1).strip() if m else ''
 pid=x['modern_front_id']; d=json.loads((base/f'person-{pid}.json').read_text(encoding='utf-8')) if pid and pid!=790 else None
 traits=[v['name'] for v in d['personality']['traits']][:4] if d else (['à l’écoute','imaginatif','délicat','loyal'] if not pid else ['précise','indépendante','pragmatique'])
 p={'id':x['id'],'nom':x['nom'],'maison_id':None,'titre':'Petit frère de Michel' if not pid else ('Interprète du tribunal' if pid==790 else d['identity']['row']['job']), 'traits':traits,'objectifs':[], 'maniere':section('Manière de parler et d’agir') or section('Manière de parler'),'portrait':{'physique':section('Apparence').split('\n\n')[0] if pid else 'Cheveux mal peignés, petits papiers et dessins dans les poches.'},'etat':'actif' if x['id'] in present else 'dormant','lieu_id':'maison-moreau' if x['id'] in present else None,'condition':'libre'}
 if pid:p['naissance']=1940-(36 if pid==790 else d['identity']['row']['age'])
 ps.append(p)
 txt(w/'chambres'/x['id']/'fiche.md',t)
 txt(w/'chambres'/x['id']/'AGENTS.md',"Lire fiche.md pour l’identité et la continuité. Le MJ incarne directement ce personnage ; aucun réveil autonome requis. Les secrets ne sont pas partagés automatiquement.\n")
 if x['id']!='raymond-moreau':
  intents.append({'personnage_id':x['id'],'croyances':[],'ignore':[],'intention':section('Ce qui reste ouvert') or 'Écouter Michel, comprendre ses préoccupations et proposer des idées sans décider pour lui.','plan':[],'declencheurs':[],'attitude_joueur':'Voir la fiche personnelle ; aucun accord ou savoir supplémentaire supposé.','date_maj':date})
ps.append({'id':'michel','nom':'Michel','maison_id':None,'titre':'Frère aîné de Lucien','traits':[],'objectifs':[],'maniere':'À définir avec le joueur ; ne pas lui attribuer une biographie historique.','etat':'dormant','lieu_id':None,'condition':'libre'})
save(e/'personnages.json',ps);save(e/'intentions.json',intents)
save(w/'manifeste.json',{'id':'la-peur-et-le-geste','nom':'La peur et le geste','calendrier':{'lunes':12,'jours_par_lune':30,'dit':'%(jour)d / %(lune)d / %(annee)d'},'monnaie':{'unites':['franc','francs']},'depart':{'lieu':'niort','siege':'raymond-moreau'}})
save(e/'monde.json',{'date':date,'phase':'avant-occupation','tension':35,'deviations':[]})
save(e/'lieux.json',json.loads((e/'lieux.json').read_text(encoding='utf-8'))+[{'id':'niort','nom':'Niort','region':'Deux-Sèvres','type':'ville','controle_id':None,'jours_de_pr':0},{'id':'maison-moreau','nom':'Chez Raymond et Josette Moreau','region':'Niort','type':'maison','controle_id':None,'jours_de_pr':0}])
save(e/'journal.json',{'maison_joueur_id':None,'personnage_joueur_id':'raymond-moreau','scenes':[{'date':{'annee':1940,'lune':6,'jour':17},'lieu_id':'maison-moreau','participants':present,'resume':'Deux premières réunions importées du RP : comparer les annonces et distinguer mots entendus et commentaires. Josette cherche une voie de renseignement sur les prisonniers. Voir les transcriptions sources pour les présences exactes.','choix_fait':'Garder les feuilles sans les prêter ; préciser source et heure des annonces.'}], 'scene_courante':{'lieu_id':'maison-moreau','salle_id':'maison-moreau','participants':present,'resume':'Fin de la troisième réunion. La radio vient d’être allumée ; aucune émission identifiée. La posture est reportée au lendemain, le revolver non acquis et la copie demandée à Ernest différée.'}})
save(e/'joueurs.json',[{'personnage_id':'raymond-moreau','nom':'Raymond Moreau','jeton':'raymond-'+secrets.token_hex(12),'role':'principal','pnj':[],'occupe':True,'lieu':'niort','depuis':0}])
save(e/'horloges.json',{'raymond-moreau':date})
save(e/'presence.json',{'presence':{i:{'salle':'maison-moreau','lieu':'Chez Raymond et Josette Moreau, Niort','date':date} for i in present},'resolu':{}})
for name in ['maisons','actes','paroles','evenements','info','objectifs','annales','pensees']:save(e/(name+'.json'),[])
rels=[]
for a,b,link in [('raymond-moreau','josette-moreau','époux'),('raymond-moreau','solange-joubert','frère et sœur'),('michel','lucien-frere-de-michel','frères')]:
 for s,c in [(a,b),(b,a)]:rels.append({'source_id':s,'cible_id':c,'opinion':0,'liens':[link],'connue_du_joueur':a!='michel'})
save(e/'relations.json',rels)
chemins=json.loads((e/'chemins.json').read_text(encoding='utf-8'));chemins.setdefault('alias',{})['chez-raymond']='maison-moreau';save(e/'chemins.json',chemins)
for name in ['carte','ville','terrain']:save(e/(name+'.json'),{})
txt(e/'flux.jsonl','')
manual='''# La peur et le geste — Niort

Monde indépendant de Westeros. Le départ jouable reprend la fin de la troisième réunion chez Raymond et Josette, le 18 juin 1940. L’heure de 21 h est une convention technique de mise en place ; le RP ne fixe que « après le repas ». Le calendrier du moteur garde ses mois de trente jours.

Raymond est le personnage joueur à la reprise. Aucune création de maison féodale. Le MJ joue directement les PNJ, avec leurs fiches sous chambres/<id>/fiche.md. Consigner paroles et actes ; ne pas réveiller une session séparée par réplique.

Les trois sources RP sous sources/modern-front/docs/rp/ à la racine du dépôt définissent la continuité adoptée pour ce nouveau monde. Elles n’ont pas modifié Modern Front. Les possessions et secrets de l’instantané sont des données de préparation ; ne pas en faire des connaissances partagées. Les fiches complètes sont dans personnages/ à la racine du dépôt et dans les chambres de ce monde.

Reprise : Raymond, Josette, Jacques, Émile et Ernest sont dans la maison Moreau. Solange et Maurice sont absents ; leur position précise reste inconnue. Michel et Lucien ne participent pas à la réunion ; leur lieu, leur âge absolu et leur nom de famille restent à établir. Michel est une fiche minimale de liaison familiale, pas Michel Vinet importé. Lucien a trois ans de moins que lui. Aucun événement du RP ne leur est connu automatiquement.

Aucun revolver acquis ; aucune adhésion collective à la lutte armée. Les feuilles sont conservées sans être prêtées. Ernest a différé la copie ; Josette cherche encore à qui adresser les demandes sur les prisonniers. Les captifs et les demandeurs anonymes restent sans identité inventée. Aucune émission précise n’a été établie à la fin de la scène.

Les réunions de 1940 sont le départ de cette branche. La cible Michel/Niort 1943 de Modern Front n’autorise aucun saut silencieux de trois ans. Le moteur .NET de Modern Front n’est pas raccordé au présent serveur narratif.
'''
manual += '\n## Lieux déjà établis\n\n'+original_manual.replace('Aucun personnage, aucune date de départ ni aucune scène ne sont initialisés par la création des lieux.', 'Les personnages et la scène de reprise sont désormais initialisés séparément de la création des lieux.')
txt(w/'manuel.md',manual);txt(w/'AGENTS.md',manual);txt(w/'CLAUDE.md',manual)
txt(w/'chambres/mj/claude.md','Lire le manuel local, le journal, les intentions et les fiches des présents. Faire jouer et parler directement les PNJ.\n')
# Le manuel MJ reçoit les fiches de référence, sans les rendre publiques.
txt(w/'prompts/mj.md',(r/'scripts/agents/prompts/mj-socle.md').read_text(encoding='utf-8')+'\n\n'+manual+'\n\n'+'\n\n---\n\n'.join(fiches.values()))
save(w/'habillage/habillage.json',{'titre':'La peur et le geste','bandeau':{'titre':'La peur et le geste — Niort, juin 1940'}})
txt(w/'habillage/habillage.css',':root { --or:#8c4b35; }\n')
save(w/'plans/niort.json',{'nom':'Niort — maison Moreau','viewBox':'0 0 640 480','fonds':[],'mur':'','guet':[],'decor':[],'salles':[{'id':'maison-moreau','nom':'Chez Raymond et Josette','cle':True,'forme':{'r':[190,140,260,190,3]},'etiq':[320,230]}]})
# Export lisible dans la bibliothèque du siège, sans secrets de préparation.
book={'id':'carnet-reunions','titre':'Les réunions chez les Moreau','type':'carnet','lecteurs':['raymond-moreau'],'pages':['17 et 18 juin 1940. Nous comparons les annonces en notant les stations et les heures. Les mots entendus restent distincts de nos commentaires. Les feuilles ne sont pas prêtées.','Josette cherche par quelle voie demander des nouvelles des prisonniers. Ernest attend avant de donner une copie. La posture du groupe reste à décider demain. Aucun accord n’a été donné pour une arme dans la maison.']}
save(e/'maisons/_sans-maison/documents/books/carnet-reunions.json',book);save(e/'maisons/_sans-maison/documents/books/_ordre.json',['carnet-reunions'])
save(w/'ouverture.json',[{'type':'effacer'},{'type':'salle','lieu':'Chez Raymond et Josette Moreau, Niort','salle':'maison-moreau','moment':'18 juin 1940 — après le repas','presents':present,'tension':35},{'type':'recit','texte':'Les conversations viennent de cesser devant le poste. Sur la table, les feuilles des annonces côtoient la liste de ce que chacun craint de perdre. La décision sur la posture du groupe attendra demain.','duree':0},{'type':'recit','texte':'Josette est revenue s’asseoir. Jacques a rapproché sa chaise du poste pour entendre sans monter le son ; Ernest garde son crayon près de la feuille. Émile est auprès d’eux. Aucune annonce n’a encore été distinguée.','duree':0}])
print('Monde créé : 9 personnages, 5 présents, 1 siège joueur, manuel MJ et carnet intégrés.')
