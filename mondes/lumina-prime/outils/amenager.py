"""Installe les deux plans et le dossier initial, sans rejouer une scène.

Les plans sont des adaptations spatiales de partie. Les livres existants et
leurs décisions ne sont jamais réinitialisés lors d'un second passage.
"""
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEPOT = ROOT.parents[1]
sys.path[:0] = [str(DEPOT / 'scripts'), str(DEPOT / 'scripts/noyau')]
import bibliotheque


def put(name, value):
    p = ROOT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    if not p.exists() or p.read_text(encoding='utf-8') != text:
        p.write_text(text, encoding='utf-8')


def polygon(cx, cy, rx, ry, n=12, phase=0):
    points = [(cx + rx * math.cos(phase + i * math.tau / n),
               cy + ry * math.sin(phase + i * math.tau / n)) for i in range(n)]
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in points) + ' Z'


def salle(id, nom, rect, lignes, quoi, dehors=False):
    x, y, w, h = rect
    return dict(id=id, nom=nom, forme={'r': [x, y, w, h, 12]},
                etiq=[x + w/2, y + 16], lignes=lignes, quoi=quoi,
                motifs=[nom.lower()], alias=[], cle=True, dehors=dehors)


rooms = [
    salle('bureau-nova', 'Bureau de Nova', [200, 100, 155, 95], ['Bureau', 'de Nova'],
          'Travail de la maire et entretiens confidentiels.'),
    salle('registre-municipal', 'Registre municipal', [445, 100, 155, 95], ['Registre', 'municipal'],
          'Dossiers, plans consultables et suivi des engagements municipaux.'),
    dict(id='radiant-core', nom='Salle du conseil', forme={'c': [400, 290, 86]},
         etiq=[400, 245], lignes=['Salle du', 'conseil'], cle=True,
         quoi='Au cœur du Radiant Core : la table des plans et des décisions.',
         motifs=['salle du conseil', 'radiant core'], alias=[]),
    salle('galerie-projets', 'Galerie des projets', [125, 240, 155, 100], ['Galerie des', 'projets'],
          'Présentation des projets de quartier et de leurs maquettes.'),
    salle('atelier-plans', 'Atelier des plans', [520, 240, 155, 100], ['Atelier des', 'plans'],
          'Espace de travail sur les implantations et les usages ; DEV garde son foyer aux Towers of Knowledge.'),
    salle('salon-visiteurs', 'Salon des visiteurs', [170, 395, 170, 105], ['Salon des', 'visiteurs'],
          'Pièce existante au départ ; son usage dans le futur accueil reste à décider.'),
    salle('jardin-interieur', 'Jardin intérieur', [460, 395, 170, 105], ['Jardin', 'intérieur'],
          'Espace commun végétal et lumineux, ouvert sur la lagune.'),
    salle('hall-arrivees', 'Hall des arrivées', [340, 435, 120, 95], ['Hall des', 'arrivées'],
          'Entrée publique du Radiant Core et accès vers les quartiers.'),
    salle('parvis-radiant', 'Parvis du Radiant Core', [280, 555, 240, 58], ['Parvis · lagune'],
          'Espace public au bord de la lagune, devant le hall.', True),
    salle('towers-of-knowledge', 'Towers of Knowledge', [20, 25, 195, 52], ['Towers of Knowledge'],
          'Accès au quartier des bibliothèques et au foyer de DEV.', True),
    salle('innovation-fields', 'Innovation Fields', [585, 25, 195, 52], ['Innovation Fields'],
          'Accès aux laboratoires de Quantum.', True),
    salle('creative-nexus', 'Creative Nexus', [20, 550, 195, 52], ['Creative Nexus'],
          'Accès au Nexus et au lieu de VOX.', True),
    salle('data-gardens', 'Data Gardens', [585, 550, 195, 52], ['Data Gardens'],
          'Accès aux jardins publics et aux zones sauvages.', True),
]
paths = [
    ('bureau-nova','radiant-core'), ('registre-municipal','radiant-core'),
    ('galerie-projets','radiant-core'), ('atelier-plans','radiant-core'),
    ('salon-visiteurs','hall-arrivees'), ('jardin-interieur','hall-arrivees'),
    ('hall-arrivees','radiant-core'), ('hall-arrivees','parvis-radiant'),
    ('galerie-projets','salon-visiteurs'), ('atelier-plans','jardin-interieur'),
    ('towers-of-knowledge','bureau-nova'), ('innovation-fields','registre-municipal'),
    ('creative-nexus','parvis-radiant'), ('data-gardens','parvis-radiant'),
]
centres = {r['id']: r['etiq'] for r in rooms}
links = ' '.join(f'M{centres[a][0]},{centres[a][1]} L{centres[b][0]},{centres[b][1]}' for a,b in paths)
put('plans/lumina-prime.json', dict(
    nom='Radiant Core — Lumina Prime', viewBox='0 0 800 650',
    fonds=[dict(classe='lp-lagune', d='M0,0 H800 V650 H0 Z'),
           dict(classe='lp-socle', d=polygon(400,310,318,255,12,math.pi/12))],
    decor=[dict(classe='lp-liaisons', d=links),
           dict(classe='lp-anneau', d=polygon(400,290,107,107,48))],
    mur='', guet=[], rose=None,
    etiquettes=[dict(x=400,y=45,texte='RADIANT CORE'),dict(x=400,y=638,texte='LUMINA PRIME · ESPACES PUBLICS ET MUNICIPAUX')],
    salles=rooms,
    _='Implantation initiale de partie, non extraite des récits. Les quatre rectangles extérieurs sont des accès aux quartiers ; leurs parcours VR sont conventionnels.'))
put('etat/chemins.json', {'_':'Durées de navigation VR de partie, en minutes ; aucune distance physique inter-cités déduite.',
                         'alias':{}, 'aretes':[[a,b,1 if not (a in ['towers-of-knowledge','innovation-fields','creative-nexus','data-gardens']) else 3] for a,b in paths]})

# La vue royaume : les quatre cités canoniques, avec Lumina Prime détaillée.
islands = [
    ('lumina', 'Lumina Prime', 390,430,275,215),
    ('etheria', 'Etheria', 790,140,135,90),
    ('atlantis', 'Nova Atlantis', 825,490,140,125),
    ('chronopolis', 'Chronopolis', 235,115,130,75),
]
regions=[dict(id=id,nom=nom,court='',d=polygon(x,y,rx,ry,12,math.pi/12),etiquette=[x,y]) for id,nom,x,y,rx,ry in islands]
positions={'lumina-prime':[390,435], 'creative-nexus':[220,465],
           'towers-of-knowledge':[290,295], 'innovation-fields':[520,325],
           'data-gardens':[525,530], 'etheria':[790,140],
           'nova-atlantis':[825,490], 'chronopolis':[235,115]}
geo=dict(viewBox='0 0 1000 700',largeur=1000,hauteur=700,regions=regions,
         fonds={},lieux=positions,terre=' '.join(r['d'] for r in regions),
         eaux='',relief={},rivieres='',bourgs=[],
         routes=[dict(id='parcours-'+id,nom='Parcours vers '+id.replace('-',' '),
                      d=f'M390,435 L{x},{y}') for id,(x,y) in positions.items()
                 if id in ['creative-nexus','towers-of-knowledge','innovation-fields','data-gardens']],
         cadres={'cites':'0 0 1000 700','lumina':'85 200 620 460'})
p=ROOT/'carte/geo.js';p.parent.mkdir(exist_ok=True)
p.write_text('// Implantation schématique des Cités de Lumière ; les espacements inter-cités ne sont pas des distances de voyage.\n"use strict";\nwindow.Geo='+json.dumps(geo,ensure_ascii=False)+';\n',encoding='utf-8')
put('carte/cadrages.json',dict(cadrages={'tout':'cites','repos':'cites'},
    titre='Les Cités de Lumière',date='%(annee)d — mois %(lune)d, jour %(jour)d',allegeances=False,
    etiquettes={id:[0,20,'c'] for id in positions},regions={r['id']:None for r in regions},
    mers=[[520,75,'LES CITÉS DE LUMIÈRE'],[420,675,'Réseau de cités · implantation schématique']],
    _='Les autres cités sont des interlocutrices autonomes ; aucun contrôle de Nova ni liaison ouverte n’est inféré de leur position.'))
locations=json.loads((ROOT/'etat/lieux.json').read_text(encoding='utf-8'))
new=[('creative-nexus','Creative Nexus','Lumina Prime'),('towers-of-knowledge','Towers of Knowledge','Lumina Prime'),
     ('innovation-fields','Innovation Fields','Lumina Prime'),('data-gardens','Data Gardens','Lumina Prime'),
     ('etheria','Etheria','Cités de Lumière'),('nova-atlantis','Nova Atlantis','Cités de Lumière'),
     ('chronopolis','Chronopolis','Cités de Lumière')]
for id,nom,region in new:
    if not any(x['id']==id for x in locations):
        locations.append(dict(id=id,nom=nom,region=region,type='ville',controle_id='cite-lumina' if region=='Lumina Prime' else None,alias=[]))
put('etat/lieux.json',locations)

put('habillage/habillage.json', {'titre':'Lumina Prime — 2042'})

# Une première affaire est un vrai volume de la bibliothèque municipale.
session=bibliotheque.ouvrir(str(ROOT/'etat'))
def add(book):
    if not any(b['id']==book['id'] for b in session.livres):
        session.livres.append(book)
def table(title,cols,rows):
    return dict(titre=title,colonnes=cols,lignes=[dict(cellules=r) for r in rows])
base=dict(maison_id='cite-lumina',lieu_id='lumina-prime',salle_id='radiant-core')
add(dict(base,id='affaire-accueil-radiant',titre='Un accueil pour Lumina Prime',type='plan',couleur='#157f8b',
    sous_titre='Première affaire · Radiant Core · J1, 2042',tenu_par='aria',office='Coordination municipale',
    pages=[
        'Le Radiant Core accueille à la fois la vie municipale et les visiteurs de Lumina Prime. Le hall, le salon et la galerie des projets figurent sur son plan. Leur articulation comme accueil public est la première question d’aménagement de cette partie.',
        '**À décider par Nova :** quelle place donner aux visiteurs dans le Radiant Core, et quels espaces garder pour le travail municipal ? Le plan permet de situer les usages ; aucune affectation nouvelle n’est encore décidée.',
        'Le conseil dispose de mandats pour préparer et conduire l’aménagement. Les surfaces utiles, la fréquentation, le coût en calcul et la disponibilité des équipes restent à mesurer. Les personnes disponibles ne constituent pas une capacité illimitée.',
        '**Terminé quand :** un visiteur peut trouver l’entrée, s’orienter et rejoindre une activité accessible, tandis qu’un entretien municipal peut se tenir à l’écart. La vérification doit porter sur un parcours réellement essayé, après réalisation.'
    ],tables=[
        table('🏰 Ouverture de l’Affaire',['Le champ','Ce qui est établi'],[
            ['LE NOM','Un accueil pour Lumina Prime'],
            ['L’OBJET','Aménager l’entrée publique du Radiant Core et sa relation avec les lieux de travail.'],
            ['LE PILIER','Habitants, espaces publics et architecture'],
            ['L’ÉTAT ACTUEL','Hall, salon des visiteurs et galerie sont inscrits au plan initial. Aucun aménagement nouveau n’est validé.'],
            ['LA PLAGE','10000–10099, réservée à cette affaire dans Lumina Prime.'],
            ['FERMÉE QUAND','Un parcours visiteur et un entretien confidentiel fonctionnent dans les espaces réalisés.']]),
        table('🎯 États cibles',['N°','L’état','Ce qui doit être vrai','Où','La preuve','Sert','Importance'],[
            ['10000','Un accueil lisible et habitable','Les visiteurs trouvent leur destination ; le travail municipal conserve ses espaces.','Radiant Core','Essai du parcours et de la séparation des usages, après réalisation.','—','60']]),
        table('🔒 Verrous',['N°','Le verrou','Bloque','Ce qui est vrai aujourd’hui','La preuve','Levé quand'],[
            ['10001','L’usage des espaces d’accueil reste à décider','10000','Aucune décision d’affectation dans cette partie.','Registre des décisions sans affectation pour cet accueil.','Nova arrête les usages et leurs limites.']]),
        table('🗝️ Clefs',['N°','La clef','Ouvre','Le principe','Le prix','Ce que cela ferme','La preuve attendue','Décision'],[
            ['10010','Un programme d’accueil sur les espaces existants','10001','Préciser les usages avant de dessiner ou construire.','Étude du conseil ; coût des travaux non établi.','Aucun espace affecté avant décision.','Programme approuvé par Nova.','à décider']]),
        table('⚔️ Actions',['N°','L’action','Réalise','Ce qu’on fait','Où','Office','Avec quoi','Dépend de','La preuve','État','Jour dû','Qui'],[
            ['10020','Décrire le parcours visiteur','10010','Distinguer arrivée, orientation, rencontre et accès aux activités.','Hall des arrivées','O05','Plan initial ; mandat de PITCH','—','Besoins et parcours proposés, sans fréquentation inventée.','à faire','2042.1.1','pitch'],
            ['10021','Relever les espaces utilisables','10010','Documenter les accès, les usages actuels et les possibilités de séparation.','Radiant Core','O02','Plan initial ; mandat de DEV','—','Relevé distinguant mesures, conventions du plan et inconnues.','à faire','2042.1.1','dev-lumina'],
            ['10022','Présenter le programme à Nova','10010','Rapprocher besoins et possibilités ; faire apparaître la décision municipale.','Salle du conseil','O01','Dossier d’accueil','10020, 10021','Programme avec limites, coûts connus et inconnus, soumis à Nova.','à faire','2042.1.2','aria']])]))
add(dict(base,id='registre-conseil-lumina',titre='Le conseil de Lumina Prime',type='registre',
    sous_titre='Mandats municipaux · 2042',tenu_par='aria',colonnes=['Office',"L'office 🏷️",'Titulaire','Ce dont il répond'],
    lignes=[dict(cellules=['O%02d' % (i+1),p['titre'],p['nom'],p['objectifs'][0]['but']])
            for i,p in enumerate(p for p in json.loads((ROOT/'etat/personnages.json').read_text(encoding='utf-8')) if p['id']!='nova')],
    pages=['Nova décide des priorités, des grands aménagements et de l’affectation des moyens. Juris intervient sur les droits et litiges. Les décisions concernant le nouvel accueil restent ouvertes.']))
session.sauver()
if not (ROOT/'chambres/mj/books/_plages.json').exists():
    put('chambres/mj/books/_plages.json',{'plage':{'de':80000,'a':89999,'taille_bloc':500},'affaires':{}})
print('Plans, carte et bibliothèque municipale installés.')
