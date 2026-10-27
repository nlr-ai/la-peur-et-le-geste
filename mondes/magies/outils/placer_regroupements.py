"""Installe un foyer de chaque regroupement NV sur la carte, sans jouer de scène."""
from pathlib import Path
import hashlib
import json

WORLD = Path(__file__).resolve().parents[1]
SOURCE = Path(r'C:\Users\reyno\univers-magiciens\non-vivants\REGROUPEMENTS.md')
SITES = [
    ('nv-cour-basse', 'Couvée', 'Cour basse', 'ville', 'Grand continent méridional', [205, 550], ['Enclos', 'Peaux de peur', 'Saints affamés'], 'Ancien relais fortifié au nord du Bastion couronné ; foyer de protection autour d’une population. Les ouvertures, les approvisionnements et le consentement restent des enjeux concrets.'),
    ('nv-carrefour-des-reprises', 'Confluence', 'Carrefour des reprises', 'ville', 'Île centrale', [215, 340], ['Entre-deux', 'Architectes aveugles', 'Greffiers'], 'Deux cours de manutention voisines constituent les extrémités locales d’une connexion colonisée. Matériaux, supports et circulation forment le foyer ; aucune liaison vers les six sièges humains n’est créée.'),
    ('nv-archives-creuses', 'Assemblée de traces', 'Archives creuses', 'ruine', 'Terres du nord-est', [400, 165], ['Remontés', 'Mnémophages', 'Retours de regard'], 'Anciennes archives au nord de Haute-Preuve. Les méthodes de consultation restent distinctes, sans mémoire collective ni transmission automatique entre espèces.'),
    ('nv-forges-reprises', 'Succession', 'Forges reprises', 'ruine', 'Grand continent méridional', [115, 800], ['Déliants', 'Architectes aveugles', 'Greffiers'], 'Ancien ensemble d’ateliers au sud du Chapitre du Seuil. Le foyer associe interruption, transformation et colonisation des supports ; la remise en service n’est pas déclarée accomplie.'),
    ('nv-front-des-cendres', 'Marche', 'Front des cendres', 'ruine', 'Grand continent méridional', [85, 655], ['Obstinés', 'Peaux de peur', 'Déliants'], 'Position initiale autour d’un ancien poste à l’ouest du Bastion. Le marqueur situe un rassemblement mobile, pas un territoire ni une attaque déjà lancée. Aucun objectif militaire n’est imposé.'),
    ('nv-belvedere-effondre', 'Veille', 'Belvédère effondré', 'ruine', 'Terres du nord-ouest', [205, 125], ['Antérieurs', 'Retours de regard', 'Remontés'], 'Site d’observation au nord-est d’Aube commune, autour des vestiges d’un effondrement. Sa cause n’est pas fixée ; les capacités ouvertes des Antérieurs ne deviennent ni réécriture du passé ni attaque acquise contre le présent.'),
]

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def write(p, v):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def main():
    path = WORLD / 'etat/lieux.json'
    lieux = read(path)
    assert not any(l['id'] in [s[0] for s in SITES] for l in lieux), 'Placement déjà présent : ne pas réinitialiser.'
    geo_path = WORLD / 'carte/geo.js'
    geo = json.loads(geo_path.read_text(encoding='utf-8').split('=', 1)[1].strip().rstrip(';'))
    cadrages = read(WORLD / 'carte/cadrages.json')
    text = '# Implantation initiale des regroupements de Non-Vivants\n\nUn foyer de chacun des six types, installé sur demande du joueur. Ces points sont des centres d’attraction, pas six empires ni des frontières. Les associations sont présentes ; effectifs, stocks, techniques encore ouvertes, traités et chronologie ne sont pas inventés. Les créatures restent instinctives. Aucun acte ni aucune parole de PNJ n’est joué par cette installation.\n\nLes trois retournés du dépôt ne sont pas automatiquement placés à leur tête : Soren et Ilyan n’ont pas encore les associations complètes dans leurs fiches. Les superviseurs et leurs moyens restent à incarner séparément.\n\nLa carte de préparation montre ces six foyers ; cela ne donne pas aux personnages connaissance de leurs mécanismes, ressources ou intentions.\n'
    for ident, kind, name, typ, region, xy, creatures, description in SITES:
        lieux.append(dict(id=ident, nom=f'{kind} ({name})', region=region, type=typ, controle_id=None, alias=[]))
        geo['lieux'][ident] = xy
        geo['cadres'][ident] = f'{max(0,xy[0]-100)} {max(0,xy[1]-125)} 200 250'
        cadrages['etiquettes'][ident] = [-10, -10, 'g'] if xy[0] > 300 else [10, -10, 'd']
        text += f'\n## {kind} — {name}\n\n- Adresse : `{ident}` ; {region} ; coordonnées {xy[0]}, {xy[1]}.\n- Composition : ' + ', '.join(creatures) + f'.\n\n{description}\n'
    raw = SOURCE.read_bytes()
    (WORLD / 'canon/univers-magiciens/non-vivants/REGROUPEMENTS.md').write_bytes(raw)
    (WORLD / 'canon/regroupements-implantations.md').write_text(text, encoding='utf-8')
    books = WORLD / 'etat/maisons/_sans-maison/documents/books'
    for ident, title, content in [('source-magies-non-vivants-regroupements', 'Regroupements de Non-Vivants', raw.decode('utf-8-sig')), ('magies-regroupements-implantations', 'Les six foyers de Non-Vivants', text)]:
        write(books / (ident + '.json'), dict(id=ident, maison_id='_sans-maison', titre=title, sous_titre='Dossier de conception et placement initial ; aucune scène acquise.', type='dossier', pages=[content]))
        order = read(books / '_ordre.json')
        if ident not in order:
            order.append(ident)
            write(books / '_ordre.json', order)
    write(path, lieux)
    geo_path.write_text('window.Geo = ' + json.dumps(geo, ensure_ascii=False) + ';\n', encoding='utf-8')
    write(WORLD / 'carte/cadrages.json', cadrages)
    write(WORLD / 'import/regroupements-placement.json', dict(source=str(SOURCE), sha256=hashlib.sha256(raw).hexdigest(), statut='Placement initial demandé par le joueur', sites=[dict(id=s[0], type=s[1], nom=s[2], position=s[5], composition=s[6]) for s in SITES]))
    with (WORLD / 'prompts/mj.md').open('a', encoding='utf-8') as out:
        out.write('\n\n## Foyers de Non-Vivants installés\n\nLire `canon/regroupements-implantations.md` : un exemplaire des six associations est maintenant situé dans `etat/lieux.json` et `carte/geo.js`. Placement initial seulement, sans scène jouée, sans rattachement automatique aux organisations humaines ou aux trois retournés. Les détails non fixés et les capacités ouvertes restent ouverts.\n')
    print('Six foyers installés ; douze lieux au total.')

if __name__ == '__main__':
    main()
