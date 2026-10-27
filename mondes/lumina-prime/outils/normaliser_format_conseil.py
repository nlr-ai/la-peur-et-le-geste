"""Aligne les champs sur le standard indiqué par le joueur, sans rejouer les actes."""
import json
import pathlib
import re
import sys
import unicodedata
ROOT = pathlib.Path(__file__).resolve().parents[1]
DEPOT = ROOT.parents[1]
sys.path[:0] = [str(DEPOT/'scripts'), str(DEPOT/'scripts/noyau')]
import bibliotheque

def nu(s):
    s = unicodedata.normalize('NFKD', s.replace('’', "'"))
    return re.sub(r'[^a-z0-9]+', ' ', ''.join(c for c in s.lower() if not unicodedata.combining(c))).strip()

ref = json.loads((DEPOT/'etat/maisons/maison-serenissima/documents/books/affaire-regles-champs-graphe.json').read_text(encoding='utf-8'))
canon = {t['titre'][0]: t for t in ref['tables'] if t['titre'].startswith(('🎯','🔒','🗝','⚔'))}
session = bibliotheque.ouvrir(str(ROOT/'etat'))
owners = {'aria':'affaire-memoire-cite','dev-lumina':'affaire-plans-lumina','quantum':'affaire-infrastructure-lumina','gaia':'affaire-espaces-publics','pitch':'affaire-habitants-collectifs','juris':'affaire-droits-usages'}
valences = {
 'affaire-accueil-radiant':'Les visiteurs trouvent leur destination et le travail municipal conserve ses espaces.',
 'affaire-memoire-cite':'Nova et le conseil peuvent reprendre leurs engagements depuis une mémoire commune consultable.',
 'affaire-plans-lumina':'Les choix d’aménagement reposent sur des plans vérifiables et des usages compatibles.',
 'affaire-infrastructure-lumina':'Les habitants disposent de services dont les capacités et garanties sont établies.',
 'affaire-espaces-publics':'Les espaces communs restent praticables, compréhensibles et ouverts à leurs usages.',
 'affaire-habitants-collectifs':'Les personnes et collectifs trouvent des lieux adaptés et une suite à leurs demandes.',
 'affaire-droits-usages':'Les habitants peuvent connaître leurs droits et faire résoudre les conflits d’usage.',
}
lock_names = {'10001':'Les espaces d’accueil doivent disposer d’usages arrêtés et compatibles.',
 '30101':'Chaque lieu doit disposer d’un relevé distinguant mesures, conventions et inconnues.',
 '30102':'Chaque plan doit pouvoir être retrouvé dans les documents de la cité.',
 '30103':'Les moyens disponibles doivent être connus avant l’engagement d’un chantier.',
 '30104':'Les espaces concernés doivent disposer d’usages arrêtés.'}
key_names = {'10010':'Articuler l’accueil et le travail municipal dans les espaces existants',
 '30202':'Conserver les plans dans les documents de la cité'}
docs = [('M201','Plan du Radiant Core','plans/lumina-prime.json'),
 ('M202','Accès locaux','etat/chemins.json'),
 ('M203','Atlas des lieux','etat/maisons/cite-lumina/documents/books/atlas-lieux-lumina.json'),
 ('M204','Mandats du conseil','etat/maisons/cite-lumina/documents/books/registre-conseil-lumina.json'),
 ('M205','Projets des quartiers','etat/maisons/cite-lumina/documents/books/projets-quartiers-lumina.json')]
for i,who in enumerate(owners):
    docs.append((f'M{211+i}', 'Mémento de '+who, f'etat/maisons/cite-lumina/documents/books/dossier-metier-{who}.json'))
resources={who: f'M204 · M{211+i}' for i,who in enumerate(owners)}
spatial={'dev-lumina','gaia','pitch'}
base=dict(maison_id='cite-lumina',lieu_id='lumina-prime',salle_id='radiant-core')
if not any(b['id']=='registre-moyens-documentaires' for b in session.livres):
    for _,_,path in docs:
        assert (ROOT/path).is_file(),path
    session.livres.append(dict(base,id='registre-moyens-documentaires',titre='Les moyens documentaires du conseil',type='registre',tenu_par='aria',embleme='🧰',couleur='#856b39',
        colonnes=['N°','🏷️ Le moyen','Ce qu’il sait faire','Qui le tient','Où','État'],
        lignes=[dict(cellules=[code,title,'Document consultable pour instruire les affaires ; ne représente pas une capacité de calcul ou un budget.','cite-lumina',path,'présent']) for code,title,path in docs],
        pages=['Moyens documentaires existants référencés par le code M. Leur présence ne prouve ni les mesures ni la réalisation des projets qu’ils décrivent.']))

aliases={'l etat':'l etat','le verrou ouvert':'le verrou','le principe et sa valence':'le principe','la preuve attendue':'la preuve','decision':'decision','retenue':'decision','etat':'etat','ou ca en est':'etat'}
def key(col):
    x=nu(col)
    return aliases.get(x,x)

for b in session.livres:
    if b['id'] not in valences:
        continue
    backup=ROOT/'outils/sauvegardes-format'/ (b['id']+'.json')
    backup.parent.mkdir(parents=True,exist_ok=True)
    if not backup.exists():backup.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    who=b['tenu_par']
    means=resources[who] + (' · M201 · M202 · M203' if who in spatial else '')
    for t in b['tables']:
        genre=t['titre'][0]
        if genre not in canon:continue
        model=canon[genre]
        oldcols=t['colonnes']
        wanted=list(model['colonnes'])
        existing={key(c):i for i,c in enumerate(oldcols)}
        # Conserver les informations supplémentaires, dont Qui et Jour dû.
        wanted += [c for c in oldcols if key(c) not in {key(w) for w in wanted}]
        for row in t['lignes']:
            old=row['cellules']; new=[]
            ident=re.sub(r'[^0-9]','',str(old[0]))
            for col in wanted:
                k=key(col)
                value=old[existing[k]] if k in existing else ''
                if k=='valence' and not value:value=valences[b['id']]
                if k=='le verrou' and ident in lock_names:value=lock_names[ident]
                if k=='la clef' and ident in key_names:value=key_names[ident]
                if k=='moyens':
                    codes=re.findall(r'\bM\d+\b',str(value))
                    value=' · '.join(dict.fromkeys(codes+re.findall(r'M\d+',means)))
                if k=='sert' and value in ['', '—', '-']:value='racine'
                new.append(value)
            row['cellules']=new
        t['colonnes']=wanted
        t['titre']=model['titre'] if genre!='⚔' else '⚔️ Actions — état et décision par ligne'
    source='Format : STANDARD: Champs du graphe d’affaires, référence indiquée par le joueur. Les numéros, preuves, décisions et états existants sont conservés.'
    if source not in b.setdefault('pages',[]):b['pages'].append(source)

for i,who in enumerate(owners):
    b=next(x for x in session.livres if x['id']=='dossier-metier-'+who)
    b['type']='memento'
    b['embleme']=['📎','📏','🔬','🌿','🤝','⚖️'][i]
    reg=next(x for x in session.livres if x['id']=='registre-conseil-lumina')
    b['office']=reg['lignes'][i]['cellules'][1]
    link=f"Affaire de jeu : {owners[who]}. Les méthodes de ce mémento appuient ses pièces numérotées ; elles ne remplacent pas les décisions et les actions."
    if link not in b.setdefault('pages',[]):b['pages'].append(link)
session.sauver()
print('Sept affaires alignées, six mémentos qualifiés, moyens documentaires adressés.')
