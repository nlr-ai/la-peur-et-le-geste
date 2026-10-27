from pathlib import Path
import json,base64,re
r=Path.cwd(); w=r/'mondes/la-peur-et-le-geste'; assert not w.exists()
def save(rel,obj):
 p=w/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
date={'annee':1940,'lune':6,'jour':19,'minute':540}
save('manifeste.json',{'id':'la-peur-et-le-geste','nom':'La peur et le geste','calendrier':{'lunes':12,'jours_par_lune':30,'dit':'%(jour)d / %(lune)d / %(annee)d'},'monnaie':{'unites':['franc','francs']},'depart':{'lieu':'niort','siege':'michel'}})
manual='''# La peur et le geste

Le joueur incarne Michel à Niort. Départ de cette adaptation : 19 juin 1940, au lendemain des trois réunions du corpus. La cible 1943 de Modern Front ne déplace pas automatiquement ces scènes de 1940. Michel reste nommé par son seul prénom, sans biographie ni âge historique inventés. Lucien est son petit frère fictionnel, trois ans plus jeune.

Le MJ joue directement les paroles, gestes et décisions des PNJ. Aucune dépêche ni session PNJ n'est nécessaire. Le joueur garde la parole et les décisions de Michel. Lire les fiches sous `personnages/` à la racine du dépôt et les sources sous `sources/modern-front/`. Le registre des personnages du monde est désormais dans `etat/personnages.json` de ce paquet.

L'ouverture chez Michel et Lucien est une nouvelle scène fictionnelle. Les scènes de Raymond servent de continuité narrative aux seuls participants indiqués. Michel et Lucien n'y ont pas assisté et ne connaissent pas automatiquement ces gens, leurs secrets ou leurs projets. Les lieux de domicile des six participants sont tirés des instantanés, sans prétendre importer toute la carte ou la simulation C# de Modern Front. Le logement de Michel est une création de cette adaptation, sans adresse géographique précise.

Les portraits sont synthétiques. Aucun revolver acquis, aucun engagement collectif dans la lutte armée, aucune information exacte captée à la fin de R3. Les propos restent des propos. Ni dragons, ni noblesse de Westeros, ni création de maison féodale. Aucun champ inventé dans les tables du jeu. Les familles utilisent maisons.json comme conteneur technique, sans argent ou personnel présumés.
'''
for name in ['AGENTS.md','manuel.md']:(w/name).write_text(manual,encoding='utf-8')
(w/'chambres/mj').mkdir(parents=True);(w/'chambres/mj/claude.md').write_text('Le MJ incarne directement les PNJ. Respecter le manuel local et les connaissances de chacun.\n',encoding='utf-8')
idx=json.loads((r/'personnages/index.json').read_text(encoding='utf-8'))['personnages']
people=[{'id':'michel','nom':'Michel','maison_id':'foyer-michel','titre':'Vous','traits':[],'objectifs':[],'maniere':'La parole et les décisions appartiennent au joueur.','etat':'actif','lieu_id':'niort','condition':'libre'}]
intentions=[]; maisons=[{'id':'foyer-michel','nom':'Foyer de Michel et Lucien','siege_id':'niort','suzerain_id':None,'canon':False}]
for p in idx:
 ident=p['id'];fiche=(r/'personnages'/p['fiche']).read_text(encoding='utf-8-sig'); family='foyer-michel' if ident.startswith('lucien') else ('foyer-moreau' if ident in ['raymond-moreau','josette-moreau'] else 'foyer-'+ident)
 if not any(x['id']==family for x in maisons):maisons.append({'id':family,'nom':family.replace('foyer-','Foyer ').replace('-',' '),'siege_id':'niort','suzerain_id':None,'canon':False})
 image=r/'personnages'/p['portrait'];svg=r/'ecrans/portraits'/(ident+'.svg');assert not svg.exists()
 svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 128 128"><image width="128" height="128" preserveAspectRatio="xMidYMid slice" href="data:image/png;base64,'+base64.b64encode(image.read_bytes()).decode()+'"/></svg>',encoding='utf-8')
 if p['modern_front_id'] and p['modern_front_id']!=790:
  dossier=json.loads((r/f'sources/modern-front/out/pnj/reunion-raymond-sauvegarde/person-{p["modern_front_id"]}.json').read_text(encoding='utf-8-sig'))
  traits=[x['name'] for x in dossier['personality']['traits']][:4];titre=dossier['identity']['row']['job'];age=dossier['identity']['row']['age']
 else:traits=['à l’écoute','imaginatif','délicat','curieux'] if ident.startswith('lucien') else [];titre='Petit frère de Michel' if ident.startswith('lucien') else 'Interprète du tribunal';age=None if ident.startswith('lucien') else 36
 voice=fiche.split('## Manière de parler')[1].split('## ')[0].strip() if '## Manière de parler' in fiche else 'Écoute avant de répondre et propose des idées avec délicatesse.'
 row={'id':ident,'nom':p['nom'],'maison_id':family,'titre':titre,'traits':traits,'objectifs':[],'maniere':voice,'portrait':{'fichier':'ecrans/portraits/'+ident+'.svg','physique':'Portrait fictionnel ; voir la fiche de référence.'},'etat':'actif' if ident.startswith('lucien') else 'dormant','lieu_id':'niort','condition':'libre'}
 if age:row['naissance']=1940-age
 people.append(row)
 chamber=w/'chambres'/ident;chamber.mkdir(parents=True);(chamber/'fiche.md').write_text(fiche,encoding='utf-8')
 intentions.append({'personnage_id':ident,'croyances':[],'ignore':['Ce que Michel ne lui a pas dit.'],'intention':'Écouter Michel et lui laisser le temps de parler.' if ident.startswith('lucien') else 'Poursuivre ses occupations ; relire sa fiche avant toute initiative.','plan':[],'declencheurs':[],'attitude_joueur':'Fraternelle' if ident.startswith('lucien') else 'Aucune relation établie avec Michel.','date_maj':date})
save('etat/personnages.json',people);save('etat/maisons.json',maisons);save('etat/intentions.json',intentions)
save('etat/monde.json',{'date':date,'phase':'avant-occupation','tension':25,'deviations':[]})
save('etat/lieux.json',[{'id':'niort','nom':'Niort','region':'Deux-Sèvres','type':'ville','controle_id':None,'jours_de_pr':0}])
save('etat/joueurs.json',[{'personnage_id':'michel','nom':'Michel','jeton':'michel-la-peur-et-le-geste','role':'principal','occupe':True,'pnj':[],'lieu':'niort','depuis':0}])
save('etat/journal.json',{'maison_joueur_id':'foyer-michel','personnage_joueur_id':'michel','scenes':[],'scene_courante':{'lieu_id':'niort','salle_id':'chez-michel','participants':['michel','lucien-frere-de-michel'],'resume':'Michel et Lucien chez eux, le matin du 19 juin 1940. Nouvelle ouverture fictionnelle.'}})
save('etat/horloges.json',{'michel':date})
save('etat/presence.json',{'presence':{i:{'salle':'chez-michel','lieu':'Chez Michel et Lucien, Niort','date':date} for i in ['michel','lucien-frere-de-michel']}})
save('etat/relations.json',[{'source_id':a,'cible_id':b,'opinion':50,'liens':['frère'],'connue_du_joueur':True} for a,b in [('michel','lucien-frere-de-michel'),('lucien-frere-de-michel','michel')]])
for name in ['actes','paroles','annales','evenements','info','objectifs','routines','rapporteurs','chemins']:save('etat/'+name+'.json',[])
(w/'etat/flux.jsonl').write_text('',encoding='utf-8')
(w/'etat/inbox/michel').mkdir(parents=True);(w/'etat/maisons/foyer-michel/documents/books').mkdir(parents=True)
opening=[{'type':'effacer'},{'type':'salle','lieu':'Chez Michel et Lucien, Niort','salle':'chez-michel','moment':'19 juin 1940 — matin','tension':25,'presents':['michel','lucien-frere-de-michel']},{'type':'recit','texte':'La lumière du matin tombe sur la table. Devant Lucien, une feuille porte le dessin inachevé d’une maison et plusieurs petits essais dans les marges. Vous êtes chez vous, à Niort.','duree':1},{'type':'replique','locuteur_id':'lucien-frere-de-michel','texte':'J’ai gardé une feuille pour toi. Tu veux qu’on fasse quelque chose ensemble ce matin ?','duree':1}]
save('ouverture.json',opening)
print('Paquet créé : 9 personnages, siège Michel, 8 portraits raccordés.')
