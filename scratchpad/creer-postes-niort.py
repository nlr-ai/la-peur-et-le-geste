import json,shutil,unicodedata
from pathlib import Path
r=Path.cwd();w=r/'mondes/la-peur-et-le-geste';source=Path('C:/Users/reyno/Modern Front/out/la-peur-et-le-geste/postes');dest=r/'sources/modern-front/postes-niort';dest.mkdir(parents=True,exist_ok=True)
roles={
0:('Préfecture','Faire tenir les services et obtenir des informations utilisables avant de donner une instruction.','Demander des rapports, coordonner les services préfectoraux et transmettre des instructions dans son ressort.','Ne commande pas toutes les institutions ; dépend des textes applicables, des moyens et de la transmission des ordres.','Change volontiers de formulation devant une objection ; veut savoir qui assume la suite.','Être tenu responsable d’une instruction impossible à exécuter.','Une demande d’accueil ou de circulation arrive par un service : préciser l’objet et le destinataire.'),
8:('Mairie','Faire reconnaître son utilité dans l’organisation municipale.','Relayer une demande municipale, réunir les interlocuteurs compétents et défendre une proposition.','Adjoint, pas maire : son mandat exact et ses délégations doivent être établis avant une décision engageante.','Tenace et soucieux du crédit qu’on lui accorde ; demande un nom et une tâche précise.','Être contourné ou porter seul un échec.','Une difficulté de logement ou d’entraide offre une entrée par le guichet municipal.'),
11:('Prison','Tenir son établissement et éviter une irrégularité dont il aurait à répondre.','Organiser le service intérieur et faire vérifier une demande de visite ou de nouvelles.','Ne prononce ni condamnation ni libération ; les autorisations et l’identité des détenus sont à vérifier.','Rigide sur les formes ; reprend un détail jusqu’à obtenir une réponse nette.','Une évasion, un ordre contradictoire ou une faute de registre.','Une demande nominative de nouvelles peut amorcer une démarche, sans inventer de détenu.'),
16:('Hôpital','Faire passer les soins nécessaires avant les discussions qui retardent le travail.','Organiser son service médical, demander de l’aide et apprécier une urgence dans son domaine.','Ne dispose ni de lits ni de matériel illimités ; ne dirige pas automatiquement toute l’administration hospitalière.','Direct et parfois impatient ; se calme quand on apporte une aide concrète.','Perdre du temps quand quelqu’un a besoin de soins.','Les frères peuvent chercher une tâche utile ; aucune blessure ni pénurie précise n’est supposée.'),
22:('Gendarmerie','Tenir sa brigade en état de répondre aux demandes qui relèvent d’elle.','Répartir le travail de ses gendarmes et faire vérifier un signalement dans son ressort.','Pas d’autorité universelle sur la police, la justice ou les militaires ; toute intervention exige des moyens et un cadre.','Peu de mots, questions pratiques ; ne confond pas assurance et preuve.','Disperser ses hommes sur une fausse alerte.','Un fait observé, daté et localisé constitue une meilleure entrée qu’une rumeur.'),
34:('Dépôt ferroviaire','Maintenir les équipes et le matériel disponibles sans exposer inutilement les hommes.','Organiser le travail du dépôt et donner une appréciation technique sur les moyens de traction.','Ne décide pas seul de la circulation des trains ni des destinations ; dépend des consignes et des équipes.','Parle des machines, des hommes et des délais ; son expérience de guerre pèse sur sa prudence.','Une erreur technique ou une promesse irréalisable.','Une question concrète de transport mène d’abord à un besoin et à une vérification, pas à un train disponible.'),
47:('Paroisse','Tenir sa communauté et préserver ce qu’il considère comme ses devoirs.','Écouter, orienter et solliciter une aide volontaire auprès de personnes qu’il connaît.','Ne parle pas pour tous les fidèles ; aucun refuge, stock ou réseau clandestin n’est acquis.','Obstiné, sensible à la manière de présenter une demande ; préfère discuter d’un devoir concret.','Voir son autorité utilisée pour une entreprise qu’il réprouve.','Une demande d’aide individuelle peut ouvrir un échange malgré des convictions différentes.'),
52:('Imprimerie','Faire sortir un travail correct et protéger son atelier des engagements imprudents.','Évaluer un travail d’impression, son coût, son délai et sa faisabilité matérielle.','Un métier ne garantit ni papier disponible ni liberté de publication ; l’accès à l’atelier se négocie.','Concret, peu porté aux discours politiques ; demande quantité, format et délai.','Une commande qui compromet son travail ou ses proches.','Une affiche ou une feuille ordinaire permet de faire connaissance ; pas d’impression clandestine automatique.'),
65:('Tribunal','Maintenir la tenue des audiences et la régularité des procédures.','Conduire les audiences dont il a la charge et organiser le travail juridictionnel dans sa compétence.','Ne remplace ni le parquet ni les enquêteurs ; aucune décision ne se déduit de son seul avis privé.','Formel, attentif aux mots et aux pièces ; ramène une demande à ce qui peut être établi.','Être amené à couvrir une procédure irrégulière.','Une démarche passe par une affaire et les voies du greffe, pas par une faveur abstraite.'),
73:('Police','Obtenir des résultats qui consolident sa position au commissariat.','Répartir le travail de son service, recueillir les signalements et conduire les démarches relevant de sa fonction.','Ne contrôle pas tous les renseignements de la ville ; les preuves, les effectifs et les compétences limitent ses actes.','Cherche ce qu’une information permet de faire ; prend note de celui qui la lui apporte.','Être désavoué ou perdre le contrôle d’une affaire.','Un signalement peut créer une relation ; son ambition et ses convictions peuvent aussi compliquer la confiance.')}
files=['personnages.json','intentions.json'];tables={n:json.loads((w/'etat'/n).read_text(encoding='utf-8-sig')) for n in files};index=json.loads((r/'personnages/index.json').read_text(encoding='utf-8'));backup=r/'scratchpad/avant-postes-niort';backup.mkdir(exist_ok=True)
for n in files:shutil.copy2(w/'etat'/n,backup/n)
selected=[]
for num,(service,want,power,limit,voice,fear,hook) in roles.items():
 src=source/f'person-{num}.json';d=json.loads(src.read_text(encoding='utf-8'));row=d['identity']['row'];pers=d['personality'];name=row['first']+' '+row['last'];pid=unicodedata.normalize('NFKD',name).encode('ascii','ignore').decode().lower().replace(' ','-')
 assert not any(c['id']==pid for c in tables['personnages.json']),pid
 age=row['age']-3;traits=[x['name'] for x in pers['traits']];active=[x['name'] for x in pers['traits'] if x['key'] not in {'petainist','gaullist','collaborationist','young_children','pow_relative'} and not x.get('hidden')][:4]
 shutil.copy2(src,dest/src.name)
 sheet=f'''# {name} — {row['job']}

**{service} · Niort · {age} ans en juin 1940**

ID du monde : `{pid}` · ID Modern Front actif : **{num}** · Foyer : {row['household']} · Site de travail dans la simulation : {row['building']}.

## Identité source

Titulaire issu de la population simulée, pas une identification historique du véritable titulaire. Âge de référence 1943 : {row['age']} ans. La fonction est reprise pour cette fiction ; aucune reconstitution juridique ou administrative exacte n’est revendiquée.

Traits exportés : {', '.join(traits)}. Ferveur simulée : **{pers['currentFervour']}/100** (arrival, graine 1, initialisation actuelle). Le score n’est ni une action déjà commise ni une opinion connue des frères.

Traits joués immédiatement : {', '.join(active)}. Les affiliations ou situations liées à la suite de la guerre restent en provenance jusqu’à leur établissement en scène : pas d’adhésion au régime de Vichy déjà actée au 15 juin, ni d’enfant ou de prisonnier inventé à partir d’une étiquette.

## Sa fonction dans le jeu

**Moyens.** {power}

**Limites.** {limit}

Ces moyens sont des repères de jeu, pas des ressources déjà acquises par les frères. Avant un acte engageant, établir les personnes, les documents, les autorisations et les délais nécessaires. Une fonction ne donne pas accès à tous les secrets de la ville.

## Incarnation — création pour cette partie

**Voix.** {voice}

**Intention.** {want}

**Crainte.** {fear}

**Première entrée possible.** {hook}

Les intentions et cette entrée en jeu sont des créations proposées pour l’incarnation, pas des événements exportés. Aucun échange passé avec Michel ou Lucien n’est ajouté. Ne pas le placer dans leur scène sans arrivée motivée. Le lieu précis du moment reste à établir.

## Relations et connaissances

Le dossier source conserve le réseau calculé ; il est réservé au MJ. La qualité de titulaire ne fait pas de lui une connaissance personnelle des frères. Aucun lien de famille avec un homonyme n’est déduit. Il ne connaît ni leur entretien au café, ni leurs intentions, ni leurs préférences de jeu.

Source : `sources/modern-front/postes-niort/person-{num}.json`.
'''
 (r/f'personnages/{pid}.md').write_text(sheet,encoding='utf-8');ch=w/f'chambres/{pid}';ch.mkdir(parents=True,exist_ok=True);(ch/'fiche.md').write_text(sheet,encoding='utf-8');(ch/'AGENTS.md').write_text('Lire fiche.md. Le MJ incarne directement ce PNJ. Respecter sa compétence, ses connaissances et la date ; aucune autorité ou ressource illimitée.\n',encoding='utf-8')
 tables['personnages.json'].append(dict(id=pid,nom=name,maison_id=None,titre=row['job'],naissance=1943-row['age'],traits=active,objectifs=[dict(but=want,priorite=1)],maniere=voice,etat='dormant',lieu_id=None,condition='libre'))
 tables['intentions.json'].append(dict(personnage_id=pid,croyances=[],ignore=[],intention=want,plan=[],declencheurs=[],attitude_joueur='Aucune relation personnelle ni faveur envers les frères présumée.',date_maj=dict(annee=1940,lune=6,jour=15,minute=750)))
 index['personnages'].append(dict(id=pid,nom=name,modern_front_id=num,fiche=pid+'.md',reunions=[]));selected.append(dict(id=pid,nom=name,poste=row['job'],service=service,modern_front_id=num))
for n,d in tables.items():(w/'etat'/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(r/'personnages/index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(dest/'selection.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(r/'personnages/POSTES-NIORT.md').write_text('# Dix postes importants de Niort\n\nTitulaires de fiction issus de la simulation, disponibles pour le MJ.\n\n'+'\n'.join(f"- **{x['service']}** — [{x['nom']}]({x['id']}.md), {x['poste']}." for x in selected)+'\n',encoding='utf-8')
assert len(selected)==10 and len({p['id'] for p in tables['personnages.json']})==len(tables['personnages.json'])
print('10 fiches et chambres créées ; intégration aux personnages, intentions et index validée.')
