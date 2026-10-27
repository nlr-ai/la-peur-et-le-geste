import json,shutil,unicodedata
from pathlib import Path
r=Path.cwd();w=r/'mondes/la-peur-et-le-geste';src=Path('C:/Users/reyno/Modern Front/out/la-peur-et-le-geste/allemands');dest=r/'sources/modern-front/allemands';dest.mkdir(parents=True,exist_ok=True)
for p in src.glob('*.json'):shutil.copy2(p,dest/p.name)
temps={p['resident']:p for p in json.loads((src/'temperaments.json').read_text(encoding='utf-8'))}
roles={
350:('major-greis','Major Greis','Vénal, mais capable de passer sur un affront lorsqu’il y trouve son compte. Parle par décisions courtes, laisse à ses subordonnés les détails.','Installer son autorité et obtenir l’exécution des demandes de son service.','Recevoir les autorités civiles, donner des instructions dans son ressort et faire instruire une demande.','Ne dirige pas toutes les unités allemandes ni les polices spéciales. Son intérêt matériel ne garantit ni corruption accessible ni bienveillance.','Une demande officielle ou une contestation de réquisition peut parvenir à son bureau.','Être publiquement désavoué ou perdre la maîtrise de ses subordonnés.'),
352:('gerhard-vogt','Gerhard Vogt','Comptable dans ses formulations ; retient un affront et revient sur un engagement qu’il estime mal tenu.','Obtenir logements et fournitures demandés à son service, avec des comptes qu’il puisse défendre.','Recenser des besoins, préparer des demandes et suivre l’exécution du cantonnement et des réquisitions.','Les quantités, les ordres et les autorisations doivent exister avant d’être joués ; aucune réquisition précise déjà accomplie.','Un désaccord sur un local ou une quantité peut mettre les frères en présence de son service.','Une livraison manquante qui lui serait imputée.'),
353:('paul-ritter','Paul Ritter','Patient et ferme ; demande de répéter un mot ambigu, sans hâter une traduction importante.','Faire comprendre les demandes et préserver l’exactitude de ce qu’il transmet.','Traduire, clarifier les termes d’un échange et signaler une ambiguïté à son supérieur.','Interpréter ne lui donne pas le pouvoir d’annuler un ordre. Courage et patience ne prouvent aucune opposition au régime.','Une phrase mal comprise peut faire de lui un interlocuteur décisif sans en faire un allié.','Qu’une formulation inexacte soit retenue comme un engagement.'),
399:('bruno-haas','Bruno Haas','Obstiné, répète sa demande plutôt que d’élever immédiatement la voix. Veut une réponse vérifiable.','Tenir les contrôles relevant de son détachement et rendre des comptes cohérents.','Organiser son détachement et faire vérifier les documents ou mouvements qui relèvent de ses consignes.','Pas de pouvoir universel sur les civils ; établir le lieu, la consigne et les moyens de chaque contrôle.','Un trajet peut conduire à un contrôle, sans supposer qu’un barrage existe déjà aujourd’hui.','Qu’un passage accordé soit ensuite présenté comme sa faute.'),
373:('walter-weber','Walter Weber','Parle simplement de ce qu’il doit faire ; peut hésiter devant une demande concrète sans renier son uniforme.','Accomplir sa tâche et tenir les exigences de son service à distance de ses scrupules personnels.','Exécuter une garde, transmettre une demande et solliciter son supérieur selon l’affectation reçue.','Aucune autorité d’officier. Une conscience religieuse ne garantit ni secours, ni refus d’un ordre, ni innocence de tout acte futur.','Un échange ordinaire pendant un service permet de découvrir un individu, sans fabriquer une amitié.','Se trouver devant un ordre qu’il ne sait pas concilier avec sa conscience.')}
translate={'greedy':'Vénal','forgiving':'Indulgent','vengeful':'Rancunier','brave':'Courageux','patient':'Patient','stubborn':'Obstiné','catholic_conscience':'Catholique de conscience','young_children':'Parent de jeunes enfants','french_lover':'Liaison avec une Française'}
paths=['personnages.json','intentions.json'];data={n:json.loads((w/'etat'/n).read_text(encoding='utf-8')) for n in paths};idx=json.loads((r/'personnages/index.json').read_text(encoding='utf-8'));selection=[]
backup=r/'scratchpad/avant-allemands';backup.mkdir(exist_ok=True)
for n in paths:shutil.copy2(w/'etat'/n,backup/n)
for num,(pid,name,voice,want,power,limit,hook,fear) in roles.items():
 d=json.loads((src/f'person-{num}.json').read_text(encoding='utf-8'));row=d['identity']['row'];t=temps[num];traits=t['personality']['traits'];active=[translate[k] for k in traits if k not in {'young_children','french_lover'}]
 assert not any(p['id']==pid for p in data['personnages.json'])
 sheet=f'''# {name}

**{row['job']} · {row['age']-3} ans en 1940 · arrivée source : {row['from']}**

ID du monde : `{pid}` · ID de simulation : **{num}** · Site professionnel : {row['building']}.

## Identité et chronologie

Personnage repris de la simulation Modern Front ; cette fiche n’atteste pas une biographie historique. Le prénom de Greis n’est pas renseigné dans la source : ne pas en inventer un. Âges source en 1943 : {row['age']} ans.

Ce personnage est absent de Niort avant le **28 juin 1940** selon la donnée `from`. Ne pas le faire intervenir dans l’introduction du 15 juin. Aucune arrivée, affectation précise, rencontre ou action passée n’est jouée par la création de cette fiche.

## Tempérament exporté — réservé au MJ

Profil : {t['personality']['profile']}. Traits source : {', '.join(translate[k] for k in traits)}. Indice de ferveur occupant : **{t['fervour']}/100** ; il appartient au modèle des occupants et ne signifie pas une disposition à la Résistance française.

Traits retenus immédiatement : {', '.join(active)}. Les étiquettes de jeunes enfants ou de liaison restent des données brutes à contextualiser : aucun enfant, conjoint, partenaire ou secret connu du joueur n’en est inventé. Les traits ne sont pas déduits de la nationalité et n’effacent ni les responsabilités ni le cadre de l’occupation.

## Incarnation — création pour le jeu

**Voix.** {voice}

**Intention.** {want}

**Crainte.** {fear}

**Moyens de fonction.** {power}

**Limites.** {limit}

**Rencontre possible après son arrivée.** {hook}

Ces intentions et pistes sont des propositions d’incarnation adoptées pour cette partie, pas des actes exportés. Ne lui attribuer ni violence déjà commise, ni acte de secours, ni connivence avec les frères sans événement établi.

## Connaissances et relations

Il ne connaît pas l’entretien de Michel et Lucien au café, leurs objectifs ou les réunions privées des Français. Aucune relation personnelle aux frères n’est créée. Les relations sources sont conservées dans le dossier MJ ; le grade ne vaut ni omniscience ni accès sans délai à tous les services.

Sources : `sources/modern-front/allemands/person-{num}.json` et `temperaments.json`. Le tempérament est lu par le système des occupants, distinct du champ de tempérament civil qui est nul pour ces personnages.
'''
 (r/f'personnages/{pid}.md').write_text(sheet,encoding='utf-8');ch=w/f'chambres/{pid}';ch.mkdir(parents=True,exist_ok=True);(ch/'fiche.md').write_text(sheet,encoding='utf-8');(ch/'AGENTS.md').write_text('Lire fiche.md. Arrivée source le 28 juin 1940 : absent avant cette date. Le MJ incarne directement ce personnage, dans ses moyens et ses connaissances.\n',encoding='utf-8')
 data['personnages.json'].append(dict(id=pid,nom=name,maison_id=None,titre=row['job'],naissance=1943-row['age'],traits=active,objectifs=[dict(but=want,priorite=1)],maniere=voice+' Absent avant le 28 juin 1940.',etat='dormant',lieu_id=None,condition='libre'))
 data['intentions.json'].append(dict(personnage_id=pid,croyances=[],ignore=[],intention='À son arrivée, prévue dans la source le 28 juin 1940 : '+want,plan=[],declencheurs=[],attitude_joueur='Aucune connaissance des frères établie.',date_maj=dict(annee=1940,lune=6,jour=15,minute=750)))
 idx['personnages'].append(dict(id=pid,nom=name,modern_front_id=num,fiche=pid+'.md',reunions=[]));selection.append(dict(id=pid,nom=name,poste=row['job'],arrivee=row['from'],modern_front_id=num))
for n,a in data.items():(w/'etat'/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(r/'personnages/index.json').write_text(json.dumps(idx,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(dest/'selection.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2),encoding='utf-8')
(r/'personnages/ALLEMANDS.md').write_text('# Cinq Allemands — fiches MJ\n\nArrivée prévue par les données : 28 juin 1940. Absents de la scène actuelle.\n\n'+'\n'.join(f"- [{p['nom']}]({p['id']}.md) — {p['poste']}." for p in selection)+'\n',encoding='utf-8')
assert len({p['id'] for p in data['personnages.json']})==len(data['personnages.json'])
print('Cinq fiches intégrées, personnages dormants sans localisation actuelle.')
