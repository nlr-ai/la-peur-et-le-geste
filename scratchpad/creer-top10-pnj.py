import json,shutil,unicodedata
from pathlib import Path
r=Path.cwd();w=r/'mondes/la-peur-et-le-geste';source=Path('C:/Users/reyno/Modern Front/out/la-peur-et-le-geste');dest=r/'sources/modern-front/contacts-freres';dest.mkdir(parents=True,exist_ok=True)
# Voix et intentions sont des créations de jeu fondées sur les métiers et traits exportés.
configs={
84:('Patiente, taiseuse, attentive aux détails. Pose une question courte avant de proposer un travail précis.','Préserver la discrétion de sa boutique et distinguer ce qui est attesté de ce qui circule.','Les confidences imprudentes qui exposent ses clients.','Une petite tâche de papier ou de photographie peut amorcer la confiance ; elle ne livre pas les affaires de ses clients.','Ferveur la plus élevée ; très forte asymétrie de confiance avec Lucien.'),
29:('Parle concrètement des trajets, des destinataires et des délais ; distingue une adresse sûre d’un bruit de couloir.','Rendre des nouvelles utiles à leurs destinataires sans compromettre sa tournée.','Promettre une nouvelle qu’il ne peut pas vérifier.','Une adresse ou une demande de nouvelles ouvre une scène ; aucun transport clandestin acquis.','Deuxième ferveur ; métier de facteur et contact des deux frères.'),
221:('Franc, précis, peu démonstratif ; propose de partager une tâche avant de parler de grands principes.','Tenir ses engagements de travail sans mettre son foyer en difficulté.','Faire payer aux siens une décision prise trop vite.','Un service partagé permet de parler franchement avec Michel. Son expérience de guerre ne lui donne pas une expertise universelle.','Troisième ferveur et collègue proche de Michel.'),
163:('Va droit au fait ; retient une injustice longtemps, mais demande ce qui est réalisable avant de promettre.','Faire respecter son travail et obtenir des engagements qui seront tenus.','Être utilisée puis laissée seule face aux conséquences.','Une petite injustice au travail peut lancer une scène si elle survient ; ne pas inventer un tort déjà subi.','Quatrième ferveur ; relation de jeunesse avec Michel et potentiel de conflit.'),
207:('Réponses nettes ; reconnaît ce qu’il ignore et ne cède pas à une explication qui lui semble fausse.','Faire correctement sa part et obtenir la même franchise des autres.','Devoir couvrir un mensonge pour rendre service.','Un collègue utile pour une vérification ou une tâche commune ; sa confiance ne vaut pas obéissance.','Cinquième ferveur ; confiance forte avec Michel.'),
76:('Bavard, volontiers descriptif ; les détails de procédure lui viennent plus facilement que les grandes convictions.','Être utile à son poste et tenir correctement les demandes qui passent entre ses mains.','Être rendu responsable d’une indiscrétion.','Une démarche ordinaire peut faire apparaître ce qu’il sait ; il ne fournit ni dossier confidentiel ni accès libre au commissariat.','Accès professionnel intéressant et discrétion faible ; camarade de Michel.'),
19:('Questions concrètes, ton calme ; ramène la conversation à ce qui peut être fait pour la personne devant elle.','Soigner avec les moyens disponibles et préserver la confiance de ses patients.','Une rumeur ou une exigence politique qui gêne les soins.','Chercher où aider peut mener à elle ; aucun blessé ni pénurie précise ne sont inventés avant la scène.','Médecin connue des deux frères ; ouvre des scènes d’entraide.'),
30:('Pèse ses mots et vérifie ce qu’on lui demande ; reprend confiance lorsqu’une tâche est claire et limitée.','Faire son travail sans se laisser entraîner dans des conversations qui la dépassent.','Une indiscrétion professionnelle dont elle supporterait seule le prix.','Une question de communication permet une rencontre ; elle ne connaît pas le contenu de tous les appels.','Téléphoniste, jeune connaissance de Michel ; dilemmes de discrétion et de confiance.'),
160:('Ferme sur les engagements, peu sensible aux effets de manche ; peut discuter longuement d’un cas concret.','Tenir son commerce et traiter les engagements pris envers elle comme réciproques.','Que le désordre et les promesses non tenues ruinent son travail.','Un besoin matériel ouvre une négociation ; ni crédit ni soutien politique garantis.','Commerçante connue des deux frères, convictions distinctes et confiance asymétrique.'),
230:('Assuré, cherche à faire valoir son jugement ; teste les désaccords et mesure ce qu’une conversation peut lui rapporter.','Gagner de la considération au travail et se ménager des appuis.','Être marginalisé ou perdre l’avantage dans une relation.','Collègue politiquement hostile possible ; il reste capable d’un service ordinaire. Aucune dénonciation ni trahison déjà commise n’est inventée.','Ferveur nulle : contrepoint idéologique, ambition et relation professionnelle avec Michel.')}
rels=json.loads((source/'relations-freres.json').read_text(encoding='utf-8'));tables={n:json.loads((w/'etat'/n).read_text(encoding='utf-8-sig')) for n in ['personnages.json','relations.json','intentions.json']};index=json.loads((r/'personnages/index.json').read_text(encoding='utf-8'))
backup=r/'scratchpad/avant-pnj-top10';backup.mkdir(exist_ok=True)
for n in tables:shutil.copy2(w/'etat'/n,backup/n)
selection=[]
for num,(voice,want,fear,hook,why) in configs.items():
 src=source/f'candidats/person-{num}.json';d=json.loads(src.read_text(encoding='utf-8'));row=d['identity']['row'];pers=d['personality'];name=row['first']+' '+row['last'];pid=unicodedata.normalize('NFKD',name).encode('ascii','ignore').decode().lower().replace(' ','-');age=row['age']-3
 assert not any(p['id']==pid for p in tables['personnages.json']),pid
 shutil.copy2(src,dest/src.name)
 traits=[t['name'] for t in pers['traits']];keys=[t['key'] for t in pers['traits']]
 # Les affiliations ou situations datées de 1943 ne deviennent pas des faits de juin 1940.
 excluded={'gaullist','petainist','collaborationist','pow_relative','young_children','sto_refractory'}
 active=[t['name'] for t in pers['traits'] if t['key'] not in excluded and not t.get('hidden')][:4]
 connections=[]
 for seat in rels:
  match=next((c for c in seat['relations'] if c['id']==num),None)
  if not match:continue
  sid='michel' if seat['id']==406 else 'lucien-frere-de-michel'
  nature={'Colleague':'collègues','Schoolmate':'connaissances de jeunesse','Regular':'contact régulier'}[match['kinds']]
  connections.append(f"- {seat['name']} : {nature}. Confiance du frère vers ce PNJ : {match['outgoing']}/100 ; du PNJ vers le frère : {match['incoming']}/100 (données MJ).")
  for a,b in [(sid,pid),(pid,sid)]:
   tables['relations.json'].append(dict(source_id=a,cible_id=b,opinion=0,liens=[nature],connue_du_joueur=True))
 sheet=f'''# {name}

**{age} ans en juin 1940 · {row['job']} · Niort**

Identifiant : `{pid}` · Modern Front actif : **{num}** · Foyer : {row['household']}.

## Données de simulation

Ferveur : **{pers['currentFervour']}/100**, scénario arrival, graine 1, population actuelle. Ce score situe la disposition simulée à la résistance ; ce n’est ni une action accomplie ni une connaissance du joueur. Âge source en 1943 : {row['age']} ans.

Traits exportés : {', '.join(traits)}.

Traits retenus pour l’incarnation immédiate : {', '.join(active)}.

Les affiliations politiques liées à la suite de la guerre et les situations familiales générées restent en provenance tant que leur chronologie ou leur cohérence n’est pas établie. Notamment, aucun gaullisme déjà constitué le 15 juin, aucun parti futur, aucun proche prisonnier ni enfant n’est ajouté sur la seule foi d’un trait. Les traits cachés restent au MJ.

## Relations avec les frères

{chr(10).join(connections)}

Les scores de confiance ne sont pas convertis en opinion : `opinion: 0` est une valeur technique non renseignée. La nature du contact est connue ; les convictions, les scores et les secrets ne le sont pas automatiquement. Aucun lien familial avec les autres PNJ ne découle d’un nom commun.

## Incarnation — création pour cette partie

**Voix.** {voice}

**Ce que ce personnage veut.** {want}

**Ce qui l’inquiète.** {fear}

**Entrée en jeu possible.** {hook}

Ces intentions et possibilités sont adoptées pour le jeu ; elles ne sont pas des actes exportés de la simulation. Aucun dialogue passé, service accordé ou déplacement n’est inventé. Le lieu précis et l’activité du moment restent à établir avant de faire entrer le personnage en scène.

## Motif de sélection

{why}

Source complète : `sources/modern-front/contacts-freres/person-{num}.json`. Ne pas confondre les IDs actuels de la population réduite avec ceux des anciens exports de réunions.
'''
 (r/f'personnages/{pid}.md').write_text(sheet,encoding='utf-8');ch=w/f'chambres/{pid}';ch.mkdir(parents=True,exist_ok=True);(ch/'fiche.md').write_text(sheet,encoding='utf-8');(ch/'AGENTS.md').write_text('Lire fiche.md. Le MJ incarne directement ce PNJ. Respecter la date, les sources et les connaissances ; aucune présence aux réunions ou à la scène des frères présumée.\n',encoding='utf-8')
 tables['personnages.json'].append(dict(id=pid,nom=name,maison_id=None,titre=row['job'],naissance=1943-row['age'],traits=active,objectifs=[dict(but=want,priorite=1)],maniere=voice,etat='dormant',lieu_id=None,condition='libre'))
 tables['intentions.json'].append(dict(personnage_id=pid,croyances=[],ignore=[],intention=want,plan=[],declencheurs=[],attitude_joueur='Voir les liens exportés ; aucun accord avec les frères présumé.',date_maj=dict(annee=1940,lune=6,jour=15,minute=750)))
 index['personnages'].append(dict(id=pid,nom=name,modern_front_id=num,fiche=pid+'.md',reunions=[]))
 selection.append(dict(id=pid,nom=name,modern_front_id=num,ferveur=pers['currentFervour'],motif=why))
for n,value in tables.items():(w/'etat'/n).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(r/'personnages/index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(dest/'selection.json').write_text(json.dumps({'methode':'5 ferveurs les plus élevées parmi les 24 contacts, puis 5 profils complémentaires ; intérêt narratif évalué éditorialement, pas score simulé.','selection':selection},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(r/'personnages/CONTACTS-FRERES.md').write_text('# Dix contacts à jouer\n\nCinq premières ferveurs, puis cinq profils complémentaires parmi les contacts des frères.\n\n'+'\n'.join(f"- [{s['nom']}]({s['id']}.md) — ferveur {s['ferveur']}/100. {s['motif']}" for s in selection)+'\n',encoding='utf-8')
assert len(selection)==10 and len({p['id'] for p in tables['personnages.json']})==len(tables['personnages.json'])
ids={p['id'] for p in tables['personnages.json']};assert all(x['source_id'] in ids and x['cible_id'] in ids for x in tables['relations.json'])
print('10 fiches créées et intégrées ; relations valides. Aucun PNJ ajouté à la scène en cours.')
for s in selection:print(s['nom'],s['ferveur'])
