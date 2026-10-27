"""Ajouts de décor autorisés ; aucun ordre, acte de PNJ ou chantier exécuté."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEPOT = ROOT.parents[1]
sys.path[:0] = [str(DEPOT / 'scripts'), str(DEPOT / 'scripts/noyau')]
import bibliotheque

SITES = [
    ('quai-commun', 'Quai commun', 'lumina-prime', [365, 580],
     'Une promenade basse au bord de la lagune, avec des gradins tournés vers la ville et des alcôves ouvertes.',
     'Se retrouver, attendre quelqu’un et observer les quartiers depuis un espace commun.',
     'Un ruban lumineux incrusté dans le sol distingue la promenade des accès au Radiant Core.'),
    ('halle-maquettes', 'Halle des maquettes', 'creative-nexus', [205, 380],
     'Une halle à toiture translucide ; des socles de tailles différentes accueillent des modèles spatiaux.',
     'Comparer des projets à plusieurs échelles et montrer ce que changerait un aménagement.',
     'Les socles sont vides au départ : aucun projet n’est présenté comme déjà approuvé.'),
    ('ateliers-modulaires', 'Ateliers modulaires', 'creative-nexus', [205, 545],
     'Des cellules de travail autour d’une cour, avec des cloisons démontables et des accès indépendants.',
     'Assembler des décors, travailler à plusieurs et essayer des agencements temporaires.',
     'Un rail de cloisons permet de séparer une démonstration publique d’un espace de travail.'),
    ('belvedere-plans', 'Belvédère des plans', 'towers-of-knowledge', [405, 265],
     'Une terrasse en retrait des bibliothèques, bordée de pupitres et d’une rambarde de verre mat.',
     'Lire la ville en coupe : volumes, circulations, niveaux et raccordements entre quartiers.',
     'Un pupitre porte une coupe schématique ; elle distingue les espaces publics des pièces fermées.'),
    ('bassin-essais', 'Bassin d’essais', 'innovation-fields', [570, 415],
     'Une plateforme entourée d’un anneau vide, avec un accès unique et une galerie d’observation.',
     'Préparer des essais d’environnements VR dans un périmètre identifiable.',
     'La limite est visible dans l’espace ; l’isolation technique reste à vérifier avant tout essai.'),
    ('jardin-calme', 'Jardin calme', 'data-gardens', [490, 610],
     'Des passages courbes entre des volumes végétaux opaques, des petites cours et des assises isolées.',
     'Se retirer des espaces collectifs et se rencontrer à l’écart du passage.',
     'Les écrans végétaux coupent la vue ; ils ne garantissent pas à eux seuls la confidentialité des échanges.'),
]

def save(path, value):
    text = json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    if not path.exists() or path.read_text(encoding='utf-8') != text:
        path.write_text(text, encoding='utf-8')

locations = json.loads((ROOT / 'etat/lieux.json').read_text(encoding='utf-8'))
for ident, name, parent, position, architecture, usage, detail in SITES:
    if not any(x['id'] == ident for x in locations):
        locations.append(dict(id=ident, nom=name, region='Lumina Prime', type='ville',
                              controle_id='cite-lumina', alias=[]))
save(ROOT / 'etat/lieux.json', locations)

p = ROOT / 'carte/geo.js'
geo = json.loads(p.read_text(encoding='utf-8').split('window.Geo=', 1)[1].strip().rstrip(';'))
for ident, name, parent, position, *_ in SITES:
    geo['lieux'].setdefault(ident, position)
    rid = 'acces-' + ident
    if not any(r['id'] == rid for r in geo['routes']):
        start = geo['lieux'][parent]
        geo['routes'].append(dict(id=rid, nom='Accès : ' + name,
                                 d=f'M{start[0]},{start[1]} L{position[0]},{position[1]}'))
text = '// Carte schématique ; positions et tracés ne valent pas distances mesurées.\n"use strict";\nwindow.Geo=' + json.dumps(geo, ensure_ascii=False) + ';\n'
if p.read_text(encoding='utf-8') != text:
    p.write_text(text, encoding='utf-8')

p = ROOT / 'etat/chemins.json'
paths = json.loads(p.read_text(encoding='utf-8'))
for ident, _, parent, *_ in SITES:
    if not any(set(e[:2]) == {ident, parent} for e in paths['aretes']):
        paths['aretes'].append([parent, ident, 1])
save(p, paths)

session = bibliotheque.ouvrir(str(ROOT / 'etat'))
base = dict(maison_id='cite-lumina', lieu_id='lumina-prime', salle_id='radiant-core',
            type='registre', tenu_par='aria', couleur='#157f8b')
books = [dict(base, id='atlas-lieux-lumina', titre='Six lieux à parcourir', embleme='◈',
    sous_titre='Architecture et usages · extensions de partie',
    colonnes=['Lieu', 'Quartier', 'Architecture', 'Usage', 'À regarder'],
    lignes=[dict(cellules=[name, next((s['nom'] for s in locations if s['id']==parent),parent), arch, use, detail])
            for ident,name,parent,pos,arch,use,detail in SITES],
    pages=['Ces six lieux appartiennent au décor initial enrichi à la demande du joueur. Ils figurent sur la carte. Les tracés sont schématiques ; chaque accès local vaut conventionnellement une minute de navigation VR.',
           'Les lieux ne prouvent ni un effectif, ni une capacité technique, ni un budget. Aucun occupant nommé ou chantier accompli ne leur est attribué.']),
    dict(base, id='projets-quartiers-lumina', titre='Trois projets pour les quartiers', embleme='◇',
    sous_titre='Pistes d’aménagement · aucun chantier lancé',
    colonnes=['Projet', 'Résultat recherché', 'Aménagement', 'À établir', 'Domaine'],
    lignes=[dict(cellules=row) for row in [
      ['La promenade continue', 'Relier le Quai commun aux Data Gardens par un parcours lisible.', 'Un chemin de rive, des seuils repérables et des haltes hors du passage.', 'Continuité des accès, usages existants et coût de maintien du décor.', 'Gaia · DEV'],
      ['Un atelier ouvert', 'Permettre de voir une création sans traverser tous les espaces de travail.', 'Un atelier témoin, une galerie de visite et une zone de travail séparée.', 'Besoins des collectifs, règles d’accès et moyens de réalisation.', 'PITCH · DEV'],
      ['Une pièce vraiment privée', 'Pouvoir mener un entretien municipal confidentiel.', 'Une salle opaque, un seuil explicite et une gestion vérifiée des accès et de la captation.', 'Ce que garantit réellement le système ; coût et droits d’usage.', 'Quantum · DEV · JURIS']]],
    pages=['Ces pistes sont disponibles pour la suite de la partie. Elles ne constituent ni des décisions de Nova, ni des demandes faites par les conseillers. La première affaire reste l’accueil du Radiant Core.',
           'Leur ouverture en affaire et leur réalisation suivent les décisions du joueur et le travail effectif des habitants.'])]
for book in books:
    if not any(x['id'] == book['id'] for x in session.livres):
        session.livres.append(book)
session.sauver()
print('Six lieux cartographiés, six accès et deux volumes ajoutés.')
