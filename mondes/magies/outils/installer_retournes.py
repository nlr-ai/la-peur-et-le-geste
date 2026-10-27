"""Place les trois retournés et installe Ilyan au siège joueur."""
import copy
import hashlib
import json
import os
from pathlib import Path
import sys

W = Path(__file__).resolve().parents[1]
ROOT = W.parents[1]
SOURCE = Path(r'C:\Users\reyno\univers-magiciens')
os.environ['CONSEIL_MONDE'] = 'magies'
os.environ.pop('CONSEIL_RACINE', None)
sys.path.insert(0, str(ROOT / 'scripts'))

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def write(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

ROWS = [
    ('08-soren-dalle', 'Soren Dalle', 'nv-forges-reprises', 'Forges reprises', 'atelier-soren', 'Atelier de Soren', ['ambitieux', 'artisan', 'possessif'], 'Réparateur retourné ; superviseur d’un jeune Architecte aveugle.', 'Bâtir une puissance territoriale puis militaire où ceux qui savent réparer décident.', 'Rendre habitable une partie du milieu transformé par son Architecte, avec des moyens vérifiés.', ['MATIERE_V1', '../non-vivants/ARCHITECTES_AVEUGLES'], 'Présence auprès de la Succession, sans propriété ni supervision de tous ses membres : Soren ne possède au départ que son jeune Architecte, ses outils, un abri et des matériaux de récupération.'),
    ('09-daria-vanne', 'Daria Vanne', 'nv-cour-basse', 'Cour basse', 'relais-cour-basse', 'Relais de la Cour basse', ['ambitieuse', 'protectrice', 'autoritaire'], 'Gestionnaire retournée du relais de la Cour basse ; superviseuse d’une Couvée.', 'Fédérer des refuges sous une autorité qu’elle dirigerait, avec contributions et force commune.', 'Préserver simultanément ouvertures, approvisionnements et confiance autour de la Couvée.', ['PROTECTION_V1', 'EMOTIONS_V1', '../non-vivants/ENCLOS', '../non-vivants/SAINTS_AFFAMES', '../non-vivants/PEAUX_DE_PEUR'], 'La Couvée de la Cour basse est celle de sa fiche. La supervision ne garantit pas un arrêt absolu de l’Enclos ni une commande volontaire des Peaux.'),
    ('10-ilyan-sere', 'Ilyan Sere', 'nv-archives-creuses', 'Archives creuses', 'atelier-ilyan', 'Atelier des témoins d’Ilyan', ['ambitieux', 'methodique', 'calculateur'], 'Devin retourné ; superviseur d’un Retour de regard et gardien de témoins matériels.', 'Contrôler l’accès aux informations vérifiables dont dépendent les puissances.', 'Développer des consultations utiles en recoupant les relevés et en conservant la provenance des témoins.', ['DIVINATION_V1', 'ENCHANTEMENT_V1', '../non-vivants/RETOURS_DE_REGARD'], 'Son atelier se trouve aux Archives creuses. Il conserve seulement les moyens initiaux de sa fiche, dont son Retour de regard ; la présence de l’Assemblée ne lui donne ni Mort, ni Esprit, ni maîtrise des autres créatures.'),
]

def head(char, date):
    ident = char['id']
    return dict(personnage_id=ident,
        croyances=['Mes moyens restent ceux de ma fiche et des sources vérifiées.', 'La coopération d’un partenaire ne découle pas de mes ambitions.', 'Les Non-Vivants poursuivent leurs fonctionnements propres.'],
        ignore=['Les intentions privées des autres personnes.', 'Les stocks et moyens que je n’ai pas vérifiés.'],
        intention=char['objectifs'][1]['but'],
        plan=[dict(id=ident+'-moyens', quoi=char['objectifs'][1]['but'], etat='en-cours', jours_restants=None, depend_de=[], cout=['Moyens matériels et accès réellement disponibles'], si_bloque='Chercher les moyens manquants et limiter le projet sans prétendre son résultat acquis.')],
        declencheurs=[dict(si='Une demande ou un danger concerne mes moyens et mon domaine.', alors='Évaluer les sources et agir dans mes capacités, en laissant les conséquences incertaines ouvertes.', une_fois=False)],
        attitude_joueur='Ilyan est un interlocuteur possible pour vérifier des informations ; aucun contrat ni accord n’est acquis.', date_maj={k:date[k] for k in ('annee','lune','jour')})

def main():
    state = W / 'etat'
    chars = read(state/'personnages.json')
    assert not any(c['id']=='ilyan-sere' for c in chars), 'Installation déjà présente.'
    date = read(state/'monde.json')['date']
    heads = read(state/'intentions.json')
    presence = read(state/'presence.json')
    routines = read(state/'routines.json')
    houses = read(state/'maisons.json')
    chemins = read(state/'chemins.json')
    books = state/'maisons/_sans-maison/documents/books'
    order = read(books/'_ordre.json')
    provenance = []
    for filename, name, place, placename, house, housename, traits, title, want, project, refs, limitation in ROWS:
        ident = filename[3:]
        raw = (SOURCE/'personnages'/(filename+'.md')).read_bytes()
        source = raw.decode('utf-8-sig')
        own = source.split('## 🤝 Relations proposées')[0]
        physical = source.split('## 🎨 Présence et parcours\n\n')[1].split('\n\n')[0]
        char = dict(id=ident, nom=name, maison_id=house, titre=title, traits=traits, objectifs=[dict(but=want,priorite=1),dict(but=project,priorite=2)], portrait={'physique':physical}, etat='actif', lieu_id=place, maniere='Distinguer les faits observés, les moyens possédés et les engagements négociés ; suivre sa fiche personnelle.', condition='libre')
        chars.append(char)
        houses.append(dict(id=house,nom=housename,devise='',siege_id=place,suzerain_id=None,canon=True))
        room = place+'-atelier'
        presence['presence'][ident] = dict(salle=room,lieu='Atelier, '+placename,date=date,motif='Placement initial demandé par le joueur.')
        if ident!='ilyan-sere':
            heads.append(head(char,date))
            routines['gens'][ident] = dict(modele='resident',poste={'salle':room,'lieu':placename})
        plan = copy.deepcopy(read(W/'plans/haute-preuve.json'))
        plan['nom'] = placename
        for idx,salle in enumerate(plan['salles']):
            salle['id'] = place+('-entree' if idx==0 else '-atelier')
            salle['nom'] = 'Entrée' if idx==0 else 'Atelier'
            salle['lignes'] = [salle['nom']]
            salle['quoi'] = 'Accès local.' if idx==0 else limitation
        write(W/'plans'/(place+'.json'),plan)
        chemins['aretes'].append([place+'-entree',room,1])
        (W/'canon/univers-magiciens/personnages'/(filename+'.md')).write_bytes(raw)
        bookid = 'source-magies-personnages-'+filename
        write(books/(bookid+'.json'),dict(id=bookid,maison_id='_sans-maison',titre=name,sous_titre='Fiche source ; scènes proposées non jouées.',type='dossier',pages=[source]))
        if bookid not in order:order.append(bookid)
        intro = '# Installation initiale\n\nIdentité, compétences et moyens de départ de la fiche sont retenus. Les ambitions futures ne sont pas réalisées ; les scènes et relations proposées ne sont ni jouées ni conclues.\n\n'+limitation+'\n\n'
        chamber = W/'chambres'/ident
        chamber.mkdir(parents=True,exist_ok=True)
        (chamber/'fiche-initiale.md').write_text(intro+f'Position : {placename}.\n\n'+own,encoding='utf-8')
        supplement = intro+own+'\n\n## Références de pratique et de supervision\n'
        for ref in refs:
            refpath = SOURCE/'magies'/(ref+'.md')
            supplement += '\n'+refpath.read_text(encoding='utf-8-sig')
        if ident=='ilyan-sere':supplement = '# Siège joueur\n\nIlyan est le PJ. Ne jamais lui attribuer une décision ou une action autonome.\n\n'+supplement
        (chamber/'ajouts-systeme.md').write_text(supplement,encoding='utf-8')
        provenance.append(dict(source=str(SOURCE/'personnages'/(filename+'.md')),sha256=hashlib.sha256(raw).hexdigest(),personnage_id=ident,lieu_id=place))
    heloise = next(c for c in chars if c['id']=='heloise-braise')
    heads.append(head(heloise,date))
    heads[-1]['croyances']=['Je suis maîtresse des ouvrages du Bastion.', 'Yselde dirige la Maison et ses arbitrages de ressources.', 'Une issue utilisable compte autant que les murs qui protègent.']
    pos = presence['presence']['heloise-braise']
    routines['gens']['heloise-braise'] = dict(modele='resident',poste={'salle':pos['salle'],'lieu':pos['lieu']})
    for name,data in [('personnages',chars),('intentions',heads),('presence',presence),('routines',routines),('maisons',houses),('chemins',chemins)]:write(state/(name+'.json'),data)
    write(books/'_ordre.json',order)
    write(W/'import/retournes-provenance.json',provenance)
    oldroster = read(state/'joueurs.json')
    write(state/'archive/installation-avant-ilyan/joueurs.json',oldroster)
    write(state/'archive/installation-avant-ilyan/journal.json',read(state/'journal.json'))
    write(state/'joueurs.json',[dict(personnage_id='ilyan-sere',nom='Ilyan Sere',jeton='magies-ilyan-sere',lieu='nv-archives-creuses',depuis=0,occupe=True)])
    clocks = read(state/'horloges.json');clocks['ilyan-sere']=date
    write(state/'horloges.json',clocks)
    journal = read(state/'journal.json')
    journal.update(maison_joueur_id='atelier-ilyan',personnage_joueur_id='ilyan-sere',scene_courante=dict(lieu_id='nv-archives-creuses',participants=['ilyan-sere'],resume='Ilyan est dans son atelier aux Archives creuses. Installation demandée par le joueur ; aucune consultation ni décision jouée.'))
    write(state/'journal.json',journal)
    manifest=read(W/'manifeste.json');manifest['depart']=dict(lieu='nv-archives-creuses',siege='ilyan-sere');write(W/'manifeste.json',manifest)
    from agents.expose import chambre
    for row in ROWS:chambre.ouvrir(row[0][3:])
    prompt=W/'prompts/mj.md'
    text=prompt.read_text(encoding='utf-8')
    old=text.split('\n\n')[2]
    text=text.replace(old,'Ilyan Sere est le PJ courant, dans son atelier aux Archives creuses. Relire journal.personnage_joueur_id. Ne lui imposer ni parole, ni geste, ni décision, ni plan autonome. Héloïse est désormais PNJ au Bastion ; les quatorze PNJ ont leurs intentions propres. Carte monde-002-portrait. Relire les positions : personne ne se téléporte.',1)
    text=text.replace('Héloïse reste le seul PJ.','Le siège joueur courant est défini par journal.personnage_joueur_id.').replace('sans rattachement automatique aux organisations humaines ou aux trois retournés.','Les placements des trois retournés sont précisés dans canon/retournes-implantations.md.')
    prompt.write_text(text+'\n\n## Siège Ilyan\n\nLire `canon/retournes-implantations.md` et `chambres/ilyan-sere/fiche-initiale.md` pour ses moyens personnels. Ne pas importer les intentions privées de Daria ou Soren dans sa connaissance.\n',encoding='utf-8')
    note='# Retournés : positions et siège joueur\n\nIlyan est le seul PJ ; Héloïse redevient PNJ au Bastion, avec ses objectifs conservés.\n\n'+ '\n\n'.join(f'## {r[1]} — {r[3]}\n\n{r[-1]}' for r in ROWS)+'\n\nLes ateliers sont des organisations locales modestes, pas des empires. Les positions ne valent pas prise de contrôle des foyers.\n'
    (W/'canon/retournes-implantations.md').write_text(note,encoding='utf-8')
    write(W/'import/ilyan-entree.json',[dict(type='salle',lieu='Atelier, Archives creuses',salle='nv-archives-creuses-atelier',presents=[],duree=0),dict(type='recit',texte='Vous êtes **Ilyan Sere**, dans votre atelier aux **Archives creuses**. Un bassin, des boîtes de témoins étiquetées et les coupelles du Retour de regard occupent les tables. Vos pratiques sont la Divination et l’Enchantement ; les autres créatures présentes dans ces archives ne sont pas sous votre contrôle acquis.',duree=0)])
    print('15 personnages ; Ilyan seul PJ ; 14 têtes PNJ ; trois placements.')

if __name__=='__main__':main()
