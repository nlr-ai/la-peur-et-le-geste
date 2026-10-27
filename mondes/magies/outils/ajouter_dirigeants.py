"""Import initial des six dirigeants demandés ; aucune scène jouée."""
import copy
import hashlib
import json
import os
from pathlib import Path
import sys

WORLD = Path(__file__).resolve().parents[1]
ROOT = WORLD.parents[1]
SOURCE = Path(r'C:\Users\reyno\univers-magiciens')
os.environ['CONSEIL_MONDE'] = 'magies'
os.environ.pop('CONSEIL_RACINE', None)
sys.path.insert(0, str(ROOT / 'scripts'))

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

DATA = [
    ('11-yselde-arquen', 'Yselde Arquen', 'heloise-braise', ['protectrice', 'ambitieuse', 'possessive'], 'Faire du Bastion une protection humaine assez désirable pour concurrencer les superviseurs de Non-Vivants.', 'Rendre les refuges de quartier capables de fonctionner après la perte du commandement.', ['PROTECTION_V1', 'MATIERE_V1', 'ENCHANTEMENT_V1']),
    ('12-oren-sangle', 'Oren Sangle', 'naim-des-seuils', ['precis', 'negociateur', 'pragmatique'], 'Rendre la Ligue indispensable à la traversée de la catastrophe tout en donnant un poids aux petites stations.', 'Préparer des itinéraires alternatifs avec des équipes et des accueils réellement consentis.', ['ESPACE_V1', 'MATIERE_V1']),
    ('13-sevran-orme', 'Sévran Orme', 'ariane-veille', ['rigoureux', 'prudent', 'ambitieux'], 'Faire des preuves partageables du Collège la référence des décisions de survie.', 'Conserver les provenances et publier les divergences sans transformer une hypothèse en verdict.', ['DIVINATION_V1', 'MORT_V1']),
    ('14-talie-sorne', 'Talie Sorne', 'malo-veyre', ['federatrice', 'artisane', 'influente'], 'Faire de la Communion une puissance capable de bâtir sans réclamer la tutelle des personnes.', 'Faire durer des œuvres et des responsabilités matérielles après la ferveur des assemblées.', ['EMOTIONS_V1', 'ESPRIT_V1', 'MATIERE_V1']),
    ('15-mael-orsan', 'Maël Orsan', 'soeur-cendre', ['methodique', 'calme', 'prudent'], 'Empêcher une organisation de rendre son pouvoir inarrêtable par les dépendances humaines qu’elle installe.', 'Préparer des solutions de remplacement avant toute cessation d’une infrastructure vitale.', ['PROTECTION_V1']),
    ('16-eline-vare', 'Éline Vare', 'vesper-ronce', ['solidaire', 'pragmatique', 'independante'], 'Garantir la possibilité matérielle de quitter une puissance sans que la Fédération devienne une nouvelle tutelle.', 'Rendre les refuges capables de continuer après le départ de leur fondateur.', ['PROTECTION_V1', 'ENCHANTEMENT_V1']),
]

def main():
    state = WORLD / 'etat'
    chars = read(state / 'personnages.json')
    ids = {c['id']: c for c in chars}
    new_ids = [row[0][3:] for row in DATA]
    if any(i in ids for i in new_ids):
        raise SystemExit('Import déjà appliqué ou partiel : vérifier avant toute reprise.')
    heads = read(state / 'intentions.json')
    presence = read(state / 'presence.json')
    routines = read(state / 'routines.json')
    date = read(state / 'monde.json')['date']
    books = state / 'maisons/_sans-maison/documents/books'
    order = read(books / '_ordre.json')
    provenance = []
    for filename, name, partner, traits, want, project, schools in DATA:
        ident = filename[3:]
        raw = (SOURCE / 'personnages' / (filename + '.md')).read_bytes()
        source = raw.decode('utf-8-sig')
        # Identité, mandat et capacités retenus ; anecdotes et scènes ne sont pas jouées.
        title = source.split('**Fonction proposée :** ')[1].split('  \n')[0].strip()
        physique = source.split('## 🎨 Présence et caractère\n\n')[1].split('\n\n')[0]
        base = ids[partner]
        char = dict(id=ident, nom=name, maison_id=base['maison_id'], titre=title,
                    traits=traits, objectifs=[{'but': want, 'priorite': 1}, {'but': project, 'priorite': 2}],
                    portrait={'physique': physique}, etat='actif', lieu_id=base['lieu_id'],
                    maniere='Parler selon sa présence et son caractère décrits dans sa fiche ; distinguer engagements, moyens et limites de son mandat.', condition='libre')
        chars.append(char)
        pos = copy.deepcopy(presence['presence'][partner])
        pos['motif'] = 'Installation initiale du dirigeant demandée par le joueur ; aucun déplacement joué.'
        presence['presence'][ident] = pos
        routines['gens'][ident] = dict(modele='resident', poste={'salle': pos['salle'], 'lieu': pos['lieu']})
        steps = [project, 'Vérifier les moyens et accords disponibles avant de promettre une contribution.']
        if partner == 'heloise-braise':
            steps.append('Préserver les issues et les responsabilités locales dans les arbitrages d’accueil.')
        heads.append(dict(personnage_id=ident,
            croyances=[f'Mon lieu initial est {pos["lieu"]}.', 'Mon mandat est limité par les moyens réels et l’autonomie de mes partenaires.', 'Les Non-Vivants ne sont pas des auxiliaires déjà acquis.'] + (['Héloïse est maîtresse des ouvrages du Bastion.'] if partner == 'heloise-braise' else []),
            ignore=['Les réserves exactes non vérifiées.', 'Les intentions privées des autres personnages.'],
            intention=project,
            plan=[dict(id=f'{ident}-{n}', quoi=s, etat='en-cours', jours_restants=None, depend_de=[], cout=['Sources accessibles et accords des personnes concernées'], si_bloque='Chercher les moyens manquants ou réduire le projet ; ne pas inventer son accomplissement.') for n, s in enumerate(steps, 1)],
            declencheurs=[dict(si='Une demande ou une menace documentée concerne mon mandat.', alors='Évaluer les moyens disponibles et prendre en charge ce qui relève de mon mandat, sans promettre ceux d’autrui.', une_fois=False)],
            attitude_joueur='Maîtresse des ouvrages du Bastion ; interlocutrice dans les limites de nos compétences respectives.', date_maj={k: date[k] for k in ('annee', 'lune', 'jour')}))
        target = WORLD / 'canon/univers-magiciens/personnages' / (filename + '.md')
        target.write_bytes(raw)
        bookid = 'source-magies-personnages-' + filename
        write(books / (bookid + '.json'), dict(id=bookid, maison_id='_sans-maison', titre=name, sous_titre='Dossier de conception importé ; scènes et chronologie non acquises.', type='dossier', pages=[source]))
        order.append(bookid)
        provenance.append(dict(source=str(SOURCE / 'personnages' / (filename + '.md')), sha256=hashlib.sha256(raw).hexdigest(), personnage_id=ident, document_id=bookid))
        own = source.split('## 🤝 Relations proposées')[0]
        intro = '# Initialisation du dirigeant\n\nIdentité, fonction, capacités et objectifs retenus pour cette partie sur demande du joueur. Les biographies conditionnelles, exemples de paroles et scènes proposées ne sont pas des souvenirs ni des actes accomplis. Aucun traité ni stock n’est acquis. Les fonctions des six personnages existants sont conservées.\n\n'
        chamber = WORLD / 'chambres' / ident
        chamber.mkdir(parents=True, exist_ok=True)
        (chamber / 'fiche-initiale.md').write_text(intro + f'Position initiale : {pos["lieu"]}.\n\nObjectifs :\n- {want}\n- {project}\n\n' + own, encoding='utf-8')
        supplement = intro + own + '\n\n## Références techniques personnelles\n'
        for school in schools:
            supplement += '\n' + (WORLD / 'canon/univers-magiciens/magies' / (school + '.md')).read_text(encoding='utf-8-sig')
        (chamber / 'ajouts-systeme.md').write_text(supplement, encoding='utf-8')
    write(state / 'personnages.json', chars)
    write(state / 'intentions.json', heads)
    write(state / 'presence.json', presence)
    write(state / 'routines.json', routines)
    write(books / '_ordre.json', order)
    write(WORLD / 'import/dirigeants-provenance.json', provenance)
    journal = read(state / 'journal.json')
    journal['scene_courante']['participants'].append('yselde-arquen')
    journal['scene_courante']['resume'] = 'Héloïse et Yselde sont dans la salle du conseil du Bastion couronné. Les autres dirigeants et représentants sont chacun au siège de leur organisation. Installation initiale, aucune scène jouée.'
    write(state / 'journal.json', journal)
    from agents.expose import chambre
    for ident in new_ids:
        chambre.ouvrir(ident)
    note = '\n\n## Six dirigeants ajoutés\n\nDouze personnages sont installés, deux par organisation. Héloïse reste le seul PJ. Les fonctions de direction des six nouvelles fiches sont retenues comme situation initiale ; les anecdotes, accords et scènes proposés ne sont pas des événements acquis.\n\n' + '\n'.join('- ' + row[1] + ' : ' + ids[row[2]]['maison_id'] for row in DATA) + '\n'
    for target in [WORLD / 'prompts/mj.md', WORLD / 'README.md']:
        with target.open('a', encoding='utf-8') as out:
            out.write(note)
    print(json.dumps({'personnages': len(chars), 'pnj': len(heads), 'ajoutes': new_ids}, ensure_ascii=False))

if __name__ == '__main__':
    main()
