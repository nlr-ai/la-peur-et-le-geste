from pathlib import Path
import json, hashlib, shutil, unicodedata, re
root=Path.cwd(); source=Path('C:/Users/reyno/Modern Front')
out=root/'personnages'; archive=root/'sources/modern-front'
out.mkdir(exist_ok=True); archive.mkdir(parents=True,exist_ok=True)
names=['reunion-raymond-moreau-1940-06-17.json','seconde-reunion-raymond-moreau-1940-06-17.json','troisieme-reunion-raymond-moreau-1940-06-18.json']
scenes=[json.loads((source/'docs/rp'/n).read_text(encoding='utf-8')) for n in names]
participants={p['id']:p['name'] for s in scenes for p in s['scene']['participants']}
manifest=[]
def copy(rel):
 p=source/rel; q=archive/rel; q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,q)
 digest=hashlib.sha256(p.read_bytes()).hexdigest(); assert hashlib.sha256(q.read_bytes()).hexdigest()==digest
 manifest.append({'source':rel,'copie':q.relative_to(root).as_posix(),'sha256':digest})
for n in names:copy('docs/rp/'+n)
b='out/pnj/reunion-raymond-sauvegarde/'
for n in ['meeting.json','preparation-rp.md']+[f'person-{i}.json' for i in participants if i!=790]:copy(b+n)
dossiers={i:json.loads((archive/b/f'person-{i}.json').read_text(encoding='utf-8-sig')) for i in participants if i!=790}
prep=(archive/b/'preparation-rp.md').read_text(encoding='utf-8')
sections={int(m.group(2)):m.group(3).strip() for m in re.finditer(r'(?ms)^## (.*?) — (\d+)\n(.*?)(?=^## |\Z)',prep)}
notes={
3050:{'role':'Artisan ; hôte des trois réunions. Joué par l’utilisateur à partir de la troisième.',
'voix':'Parle depuis sa famille et ses convictions républicaines. D’abord hésitant, il négocie des engagements modestes ; dans la troisième réunion, il devient pressant, emploie des oppositions tranchées et scande son refus de l’occupation. Ses compagnons peuvent le contredire. Ne pas gommer cette évolution en lui donnant une assurance constante.',
'peur':'Perdre ses enfants, sa femme et la maîtrise de ce qui entre ou sort de sa maison. Sa volonté de protéger peut le conduire à engager les autres avant de les avoir consultés.',
'liens':'Josette est son épouse et une interlocutrice autonome ; Solange est sa sœur, proche malgré leur désaccord politique. Émile peut le reprendre sans rompre leur amitié. Jacques et Ernest transforment sa réunion prudente en travail collectif.',
'parcours':['R1, messages 2–10 : propose d’attendre, puis accepte l’écoute comparée et une transmission précisant la source, même quand la nouvelle est mauvaise.','R2, messages 2–6 : distingue les mots entendus de ses propres commentaires, accepte de garder les feuilles sans les prêter et inscrit « Mon avis » sous son ajout.','R3, messages 3–10 : annonce vouloir un revolver et refuser l’occupation ; demande une liste des pertes redoutées, puis reporte la décision de posture au lendemain et revient à l’écoute radio.'],
'ouvert':'Aucun revolver acquis. Aucun accord collectif pour la lutte armée. Le père et les enfants évoqués ne reçoivent ni noms, ni nouvelles fiches, ni biographie inventée. Les chiffres et dangers annoncés dans sa harangue sont ses paroles, pas des faits validés.',
'jeu':'À la reprise de R3, Raymond appartient au joueur : ne pas écrire ses décisions ou ses pensées sans délégation. Laisser exister la tension entre protéger sa famille et risquer de l’exposer.'},
3431:{'role':'Cultivatrice ; sœur de Raymond ; présente à la première réunion seulement.',
'voix':'Interpellations directes, questions qui éprouvent ce que les autres affirment. S’appuie sur le prestige du Maréchal, refuse d’être rangée avec les communistes. Peut concéder un point pratique sans renoncer à ses convictions.',
'peur':'Que les propos circulent déformés et que les fréquentations de son frère exposent son foyer. Le temps pris sur le travail et la distance parcourue comptent aussi.',
'liens':'Forte confiance réciproque avec Raymond. Friction avec Émile autour de Pétain ; elle défend néanmoins la confidentialité de ses propos. Elle reconnaît le souci de Jacques pour son proche prisonnier.',
'parcours':['R1, messages 4–8 : conteste l’attente sans action et la confiance donnée aux stations étrangères ; rappelle qu’une information peut être mensongère même si plusieurs personnes l’entendent.','R1, messages 8–10 : demande de ne pas répéter les positions personnelles exprimées dans la pièce ; accepte d’être tenue au courant sans rejoindre les idées de Raymond.','R2–R3 : absente. Aucun changement de conviction ni réception des nouvelles de ces réunions n’est établi.'],
'ouvert':'Ne pas la convertir rétrospectivement au groupe ou à la résistance. Aucun savoir automatique sur la troisième réunion. Les armes du foyer sont attribuées à Guy Joubert, pas à elle.',
'jeu':'Jouer une sœur attachée à Raymond et capable d’un accord concret, pas une opposition systématique. Sa prudence peut protéger ceux dont elle désapprouve les idées.'},
7472:{'role':'Artisan ; ancien de 14–18 ; présent aux première et troisième réunions.',
'voix':'Interventions franches, parfois sèches. Son expérience de la guerre donne du poids à ses questions. Il demande ce qu’on sait réellement et accepte de reconnaître qu’il peut se tromper.',
'peur':'Le sort d’un proche prisonnier, la disparition du travail et de la possibilité de dire non. Craint qu’un enthousiasme armé transforme un ami en danger pour lui-même et les autres.',
'liens':'Proche de Raymond ; Maurice lui accorde une confiance très supérieure à la confiance inverse. Avec Jacques, partage le souci d’un prisonnier sans que leur parenté avec ces captifs soit précisée. Peut approuver une mise en garde de Solange.',
'parcours':['R1, messages 4–10 : veut faire circuler les nouvelles, corrige la promesse de certitude de Raymond, dit à Maurice qu’il peut se tromper et promet de lui rapporter ce qu’il a entendu.','R2 : absent ; ne lui attribuer ni l’écoute ni la rédaction des notes de cette soirée.','R3, messages 2–10 : rapporte l’interrogation de Maurice, demande l’usage envisagé du revolver, promet de rester disponible pour Raymond sans renoncer à le contredire, ajoute le travail et la possibilité de dire non à la liste.'],
'ouvert':'L’identité du prisonnier n’est pas établie. Le trait « Mari ou fils prisonnier » ne permet pas d’identifier Bernard, quatre ans, comme le captif. La présence du trait d’ancien combattant ne donne pas une biographie militaire complète.',
'jeu':'La solidarité n’est pas une obéissance politique. Ses biens cachés restent un savoir privé : ne pas les faire connaître à la table sans transmission.'},
2181:{'role':'Artisan ; présent aux trois réunions.',
'voix':'Calme, regard direct, questions précises. Distingue ce qui a été entendu de ce qui a été compris. Peut être blessant sans le vouloir lorsqu’il corrige les notes d’un autre ; accepte aussi une correction de Josette.',
'peur':'Le sort d’un proche prisonnier et l’impossibilité de savoir à qui demander. Refuse de donner un nom avant de connaître son destinataire et de confondre solidarité avec engagement armé.',
'liens':'Connaît Raymond comme collègue et habitué ; relation plus modeste avec Ernest. Josette accepte de chercher une voie de renseignement pour lui. Émile partage son inquiétude pour un prisonnier.',
'parcours':['R1, messages 4–10 : propose d’écouter d’autres stations, notamment Londres, obtient de revenir chez Raymond et reconnaît vouloir entendre que tout n’est pas fini.','R2, messages 2–6 : exige la distinction citation/interprétation, accepte de noter aussi Stuttgart ; demande une personne à qui poser une question sur les prisonniers.','R3, messages 2–10 : veut connaître le destinataire d’un nom de prisonnier, sépare refus de l’occupation et prise d’armes, promet de revenir, demande de ne pas inscrire les personnes à protéger sur la liste.'],
'ouvert':'Le captif n’est pas identifié. La recherche d’un contact ne prouve ni contact trouvé ni nouvelles obtenues. Aucun accord pour prendre les armes. Aucune émission précise reçue à la fin de R3.',
'jeu':'Sa rigueur vient d’un enjeu personnel. Lui laisser proposer des gestes faisables, pas seulement corriger les autres. Son poste à galène ne vaut pas un poste à ondes courtes.'},
7479:{'role':'Artisan de vingt et un ans ; présent à la première réunion seulement.',
'voix':'Phrases brèves ; reprend ce que vient de dire une personne qu’il estime. Cherche le regard et l’approbation d’Émile. Les réponses concrètes le rassurent plus que la discussion politique.',
'peur':'Ne pas comprendre les nouvelles, rester sans personne à croire ou sans indication de ce qu’il faut faire. Cette lecture de sa peur est une synthèse des scènes, pas un trait supplémentaire de simulation.',
'liens':'Confiance très forte envers Émile (92/100 donnée, 67 reçue dans l’instantané). Confiance envers Raymond ; lien bien plus faible avec Ernest. Vit avec Henriette et Colette Schneider.',
'parcours':['R1, messages 4–10 : soutient d’abord qu’on ne peut pas tout dire à la radio, préfère compter sur Émile pour comprendre, demande à être informé même des mauvaises nouvelles.','R2 : absent.','R3, message 2 : Émile rapporte que Maurice lui a demandé ce qu’il devait faire. C’est une parole rapportée, pas une présence à la réunion.'],
'ouvert':'Aucune adhésion à un réseau, aucune nouvelle posture politique établie. Ne pas lui transférer les informations de R2 ou R3 simplement parce que le lecteur les connaît.',
'jeu':'Influençable ne veut pas dire incapable ou comique. Il peut poser la question simple que les autres évitent. Les objets de valeur cachés ne sont connus que des détenteurs indiqués dans son dossier.'},
7581:{'role':'Artisan ; présent aux trois réunions ; possède notamment un camion dans l’instantané.',
'voix':'Cherche à rendre le travail utile : quoi faire, quoi transmettre, comment vérifier. Parle calmement, peut s’irriter d’être soupçonné de mal rapporter. Manipule et replie ses feuilles dans le RP.',
'peur':'Perdre ses moyens de travail, particulièrement camion et essence ; engager involontairement quelqu’un qui voulait seulement informer sa femme. Le trait de parent de jeunes enfants n’est pas accompagné de noms d’enfants dans son foyer.',
'liens':'Connaît bien Raymond ; liens plus faibles avec Jacques et Maurice. Avec Jacques, une coopération exigeante autour de l’exactitude des notes. Demande à Josette si son travail peut ouvrir une voie de renseignement.',
'parcours':['R1, messages 4–10 : défend la circulation des nouvelles, propose d’écouter chez lui puis de comparer les stations et les heures.','R2, messages 2–6 : apporte ses notes, reconnaît ses ajouts, conserve son exemplaire sans le prêter et s’engage à distinguer annonces et remarques personnelles.','R3, messages 2–10 : rapporte une demande de copie sans l’avoir satisfaite, réclame une tâche concrète, inscrit camion et essence parmi les pertes possibles puis reporte la copie pour vérifier le texte.'],
'ouvert':'Le demandeur de copie et sa femme restent non identifiés. Aucune copie distribuée. Ni camion ni carburant promis au groupe ; possession ne vaut pas mise à disposition.',
'jeu':'Faire surgir la politique à partir de l’utilité et du coût des gestes. Son courage coexiste avec la protection des siens et de son travail.'},
790:{'role':'Interprète du tribunal, trente-six ans ; épouse de Raymond, membre du foyer et participante à partir de R2.',
'voix':'Phrases nettes, questions concrètes, limites explicites. Corrige une simplification ou une promesse trop large sans avoir besoin d’un discours politique. N’attend pas que Raymond l’autorise à prendre part à ce qui se passe chez elle.',
'peur':'Perdre la maison comme lieu où l’on choisit qui entre et où l’on peut parler sans peur. Être engagée dans une décision prise en son nom, notamment l’entrée d’une arme dans le foyer.',
'liens':'Épouse de Raymond ; revendique d’être consultée avant les décisions qui les exposent. Accepte d’aider Jacques à chercher un interlocuteur. Corrige les notes de Raymond et Ernest et reconnaît le travail collectif sans adopter toutes leurs idées.',
'parcours':['R1 : mentionnée, mais absente de la liste des participants.','R2, messages 2–6 : impose le respect du repas, refuse de quitter sa propre maison, propose de signer les commentaires ajoutés ; accepte de demander par quelle voie se renseigner sur les prisonniers.','R3, messages 2–10 : dit avoir posé une question mais n’a ni nom ni destinataire à donner ; refuse que son aide vaille adhésion aux décisions de Raymond, demande de baisser la voix et d’être consultée avant toute décision.'],
'ouvert':'Aucun service de recherche de prisonniers établi. Aucune approbation du revolver. Le code technique d’allégeance « vichy » est présent dans la ligne de simulation du foyer ; il ne suffit pas à établir ses convictions détaillées au 17 juin 1940. Aucun portrait physique détaillé extrait pour elle.',
'jeu':'Jouer une participante qui raisonne, propose et agit en son nom. Ne pas la réduire à freiner son mari ou à s’occuper de la table.'}
}
index=[]
for pid,name in participants.items():
 slug=re.sub('[^a-z0-9]+','-',unicodedata.normalize('NFKD',name).encode('ascii','ignore').decode().lower()).strip('-')
 n=notes[pid]; present=[i+1 for i,s in enumerate(scenes) if any(p['id']==pid for p in s['scene']['participants'])]
 dossier=dossiers.get(pid)
 if dossier:
  row=dossier['identity']['row']; a=dossier['identity']['appearance']
  physical=' ; '.join([str(a['heightCm'])+' cm']+[v.get('nameF') or v['name'] if row['sex']=='f' else v['name'] for k,v in a.items() if k in ['build','eyes','face','nose','hairColor','hairStyle','facialHair','mark'] and v])
  clothing=', '.join(x['text'] for x in dossier['identity']['worn'])
  facts=sections[pid].split('Connaissances détaillées, lieux, apparence')[0].strip()
  facts=re.sub(r'(?m)^Voix : .*\n?', '', facts)
  base_source=f'../sources/modern-front/{b}person-{pid}.json'
 else:
  row=next(x for x in dossiers[3050]['household']['members'] if x['id']==790)
  physical='Non documenté dans les sources retenues.'; clothing='Non documenté ; le torchon et les gestes domestiques appartiennent à la mise en scène RP.'
  facts='36 ans ; interprète du tribunal (`court_interpreter`, bâtiment 64). Foyer 782, avec Raymond, à Niort. La simulation la déclare `head`, Raymond `spouse`. Un bracelet du foyer lui est attribué (ID 790) ; le poste à ondes courtes est une ressource du foyer. Aucun trait de tempérament individuel exporté pour elle dans ce corpus.'
  base_source=f'../sources/modern-front/{b}person-3050.json'
 refs='\n'.join(f'- [R{i+1} — {s["scene"]["date"]}](../sources/modern-front/docs/rp/{names[i]}) : `/transcript/messages`, index des messages indiqués ci-dessus.' for i,s in enumerate(scenes) if i+1 in present)
 text=f'''# {name}

**{n['role']}**

Identifiant Modern Front : **{pid}** · Identifiant de fiche : `{slug}` · Présence : {', '.join('R'+str(i) for i in present)}.

Fiche MJ arrêtée au dernier passage de la troisième réunion (18 juin 1940). Les données ci-dessous distinguent l’instantané de simulation du début de R1, la continuité RP et les consignes d’incarnation. Les trois transcriptions portent `appliedToSimulation: false`.

## Base issue de la simulation

{facts}

## Apparence

{physical}

Tenue de l’instantané : {clothing}

## Manière de parler et d’agir

Synthèse d’incarnation tirée des scènes : {n['voix']}

## Ce qu’il ou elle craint de perdre

{n['peur']}

## Liens dans le groupe

{n['liens']}

## Évolution dans les réunions

'''+ '\n'.join('- '+x for x in n['parcours'])+f'''

## Ce qui reste ouvert

{n['ouvert']}

## Pour le MJ

{n['jeu']}

Le MJ joue directement ce personnage s’il est PNJ ; ses connaissances restent limitées à ce qu’il a vécu ou appris. Les ressources, relations chiffrées et secrets ci-dessus sont des données de préparation MJ, jamais un savoir automatiquement partagé avec le groupe. Les bilans RP ne modifient pas rétroactivement l’instantané de simulation.

## Sources

- [Instantané de simulation]({base_source}) : '''+('`/identity`, `/personality`, `/household`, `/resources`, `/relations`, `/secrets`.' if dossier else '`/household/members` (ID 790) et `/resources/householdGoods`.')+f'''
- [Préparation de R1](../sources/modern-front/{b}preparation-rp.md).
{refs}
'''
 (out/(slug+'.md')).write_text(text,encoding='utf-8')
 index.append({'id':slug,'modern_front_id':pid,'nom':name,'fiche':slug+'.md','reunions':present})
(archive/'provenance.json').write_text(json.dumps({'source_root':str(source),'statut':'Copies de référence ; aucun effet rejoué dans la simulation.','fichiers':manifest},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(out/'index.json').write_text(json.dumps({'titre':'La peur et le geste — participants des trois premières réunions politiques','date_limite_rp':'1940-06-18','personnages':index},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(out/'README.md').write_text('''# Personnages — La peur et le geste

Les sept participants aux trois premières réunions politiques chez Raymond Moreau à Niort : R1 dans la nuit du 16 au 17 juin 1940, R2 le 17 au soir, R3 le 18 après le repas. Les réunions d’institutions et de préfecture sont hors de ce lot.

Ces fiches sont le dossier de référence du MJ pour ce groupe. Chaque fiche distingue les données simulées au début de R1, l’évolution jouée dans les transcriptions et les conseils d’incarnation. Les sources RP ne sont pas des documents historiques et n’ont pas été appliquées à la simulation. Les secrets restent réservés au MJ.

| Personnage | R1 | R2 | R3 |
|---|---|---|---|
'''+''.join(f'| [{x["nom"]}]({x["fiche"]}) | '+ ' | '.join('présent' if i in x['reunions'] else '—' for i in [1,2,3])+' |\n' for x in index)+'''
Raymond est joué par l’utilisateur dans R3. Solange et Maurice n’assistent pas aux deux réunions suivantes ; Josette est seulement mentionnée en R1. Aucun parent, prisonnier ou demandeur de copie seulement évoqué n’a reçu une identité inventée.

Les JSON et les six dossiers de simulation complets ont été copiés dans [les sources](../sources/modern-front/provenance.json), avec leurs empreintes SHA-256. Josette est identifiée dans le foyer du dossier de Raymond ; les limites de cette documentation sont explicites dans sa fiche.

Ces fiches ne sont pas encore raccordées à `etat/personnages.json`, qui contient toujours les données héritées de Le Conseil. Elles n’avancent aucune horloge et ne rejouent aucune action.
''',encoding='utf-8')
assert set(participants)=={x['modern_front_id'] for x in index}
assert len(index)==7
print('7 fiches créées ; 11 fichiers sources copiés et vérifiés ; index des présences complet.')
