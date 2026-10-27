"""Fondation explicite des dix lieux ; refuse de remplacer un état existant."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(r"C:\Users\reyno\Modern Front\content\map\map.json")
# Identités reprises de la carte ; intérieurs créés pour cette fiction.
LIEUX = [
    (49, 'hotel-voyageurs', 'Hôtel-café des Voyageurs', 'Niort', 'Une salle commune ouverte sur la rue, des chambres au-dessus.', ['Salle du café', 'Comptoir', 'Cuisine', 'Palier', 'Chambre sur rue', 'Cour arrière']),
    (68, 'imprimerie-progres', 'Imprimerie du Progrès', 'Niort', 'Le papier, les caractères et les presses occupent un atelier profond.', ['Accueil', 'Composition', 'Salle des presses', 'Réserve de papier', 'Bureau', 'Cour de livraison']),
    (22, 'gare-niort', 'Gare de Niort', 'Niort', 'Un seuil entre la ville et le départ, organisé autour du hall et du quai.', ['Hall', 'Guichet', 'Salle d’attente', 'Quai', 'Bagagerie', 'Bureau de gare']),
    (71, 'atelier-photographie', 'Atelier de photographie', 'Niort', 'Une boutique sur rue ; le travail des images se fait derrière.', ['Boutique', 'Studio de prise de vue', 'Chambre noire', 'Réserve', 'Bureau', 'Cour']),
    (169, 'ferme-coulon', 'Ferme de Coulon', 'Coulon', 'Une cour distribue le logis et les bâtiments de travail.', ['Cour de ferme', 'Cuisine du logis', 'Chambre', 'Grange', 'Étable', 'Remise']),
    (65, 'hotel-breche', 'Hôtel de la Brèche', 'Niort', 'Un hôtel retenu par le corpus comme logement d’officiers.', ['Vestibule', 'Réception', 'Salle à manger', 'Cuisine de service', 'Palier des chambres', 'Chambre']),
    (50, 'papeterie-centre', 'Papeterie du Centre', 'Niort', 'Le comptoir et les rayonnages séparent la boutique de la réserve.', ['Boutique', 'Comptoir', 'Rayonnages', 'Arrière-boutique', 'Réserve', 'Bureau']),
    (0, 'prefecture', 'Préfecture — secrétariat général', 'Niort', 'Un parcours de guichets et de bureaux autour des dossiers.', ['Vestibule', 'Accueil du public', 'Salle d’attente', 'Secrétariat', 'Bureau', 'Archives']),
    (171, 'cafe-commerce-coulon', 'Café du Commerce', 'Coulon', 'Une salle de café et ses pièces de service, à l’échelle du bourg.', ['Salle du café', 'Comptoir', 'Cuisine', 'Arrière-salle', 'Réserve', 'Cour']),
    (4, 'maison-arret', 'Maison d’arrêt de Niort', 'Niort', 'Les seuils séparent l’accueil, les visites et la détention.', ['Entrée extérieure', 'Poste de garde', 'Accueil des visiteurs', 'Parloir', 'Couloir intérieur', 'Cellule']),
]


def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    if (ROOT / 'etat/lieux.json').exists():
        raise SystemExit('Les lieux existent déjà : aucune réinitialisation autorisée.')
    sites = {s['id']: s for s in json.loads(SOURCE.read_text(encoding='utf-8'))['sites']}
    places, provenance, edges = [], [], []
    overview = dict(nom='Niort et le marais', viewBox='0 0 1000 720', fonds=[], mur='', guet=[], decor=[], etiquettes=[], salles=[])
    rects = [(80,90,260,125),(360,90,260,125),(640,90,280,125),(80,250,260,125),(360,250,260,125),(640,250,280,125)]
    for index, (sid, ident, nom, commune, desc, rooms) in enumerate(LIEUX):
        src = sites[sid]
        origin = src['osm']
        status = 'Lieu généré par Modern Front' if origin.startswith('special/') else ('Dossier historique de Modern Front' if origin.startswith('historic/') or sid in (0,4) else 'Fond cartographique moderne de Modern Front')
        places.append(dict(id=ident, nom=nom, region=commune, type='chateau', controle_id=None, alias=[src['name']]))
        provenance.append(dict(id=ident, source_site_id=sid, source_nom=src['name'], source_reference=origin, source_position={'x':src['x'],'y':src['y']}, statut_source=status, statut_jeu='canonique', interieur='Création de fiction, non-relevé historique'))
        plan = dict(nom=nom, viewBox='0 0 1000 480', fonds=[], mur='', guet=[], decor=[], etiquettes=[], salles=[], **{'_':'Plan de fiction canonique. Disposition schématique ; aucun relevé historique revendiqué.'})
        ids=[]
        for n,(room, rect) in enumerate(zip(rooms,rects)):
            rid=ident if n==0 else f'{ident}-piece-{n+1}'
            ids.append(rid)
            x,y,w,h=rect
            words=room.split(); half=max(1,len(words)//2)
            lines=[room] if len(room)<21 else [' '.join(words[:half]),' '.join(words[half:])]
            plan['salles'].append(dict(id=rid,nom=room,forme={'r':[x,y,w,h,2]},etiq=[x+w/2,y+h/2-4],lignes=lines,cle=True,quoi=f'{room} — {nom}.',motifs=[f'{room}, {nom}'],alias=[]))
        # Deux rangées, traversées par un couloir commun et des portes.
        for a,b in [(0,1),(1,2),(0,3),(1,4),(2,5),(3,4),(4,5)]:
            edges.append([ids[a],ids[b],1])
            ra,rb=rects[a],rects[b]
            ax,ay=ra[0]+ra[2]/2,ra[1]+ra[3]/2; bx,by=rb[0]+rb[2]/2,rb[1]+rb[3]/2
            plan['decor'].append(dict(classe='plan-passage',d=f'M{ax},{ay} L{bx},{by}',style='fill:none;stroke:#9d805a;stroke-width:3;stroke-dasharray:5 5'))
        save(ROOT/f'plans/{ident}.json',plan)
        col=index%3; row=index//3
        x=42+col*320; y=52+row*165
        overview['salles'].append(dict(id=ident,nom=nom,forme={'r':[x,y,280,120,2]},etiq=[x+140,y+48],lignes=[nom],cle=True,quoi=f'{desc} {commune}. {status}.',motifs=[nom],alias=[]))
    overview['_']='Répertoire spatial schématique, sans échelle ni itinéraires entre les sites. Les coordonnées source sont conservées dans provenance-lieux.json.'
    save(ROOT/'plans/niort-et-marais.json',overview)
    save(ROOT/'etat/lieux.json',places)
    save(ROOT/'provenance-lieux.json',dict(source=str(SOURCE),sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),lieux=provenance))
    save(ROOT/'etat/chemins.json',{'_':'Passages intérieurs de fiction : une minute par passage. Aucun trajet entre sites n’est encore arbitré.', 'alias':{},'aretes':edges})
    for name in ['personnages','maisons','relations','intentions','evenements','info','objectifs','paroles','actes','plis','joueurs','routines']:
        save(ROOT/f'etat/{name}.json',[])
    save(ROOT/'etat/presence.json',{'presence':{}})
    save(ROOT/'etat/journal.json',{'maison_joueur_id':None,'personnage_joueur_id':None,'scenes':[],'scene_courante':None})
    save(ROOT/'manifeste.json',{'id':'la-peur-et-le-geste','nom':'La peur et le geste','calendrier':{'lunes':12,'jours_par_lune':30,'dit':'%(jour)d / %(lune)d / %(annee)d'},'monnaie':{'unites':['franc','francs']},'depart':{}})
    (ROOT/'etat/flux.jsonl').write_text('',encoding='utf-8')
    (ROOT/'manuel.md').write_text('''# La peur et le geste

Le MJ incarne directement les PNJ, selon le socle commun du dépôt. Le monde reprend les lieux de Modern Front autour de Niort et Coulon. Les dix lieux de `etat/lieux.json` et leurs intérieurs sont canoniques pour cette fiction.

`provenance-lieux.json` conserve les identités et coordonnées sources. Les lieux générés ne deviennent pas des établissements historiques attestés par leur adoption dans le canon. Tous les intérieurs sont des créations de fiction. Le type technique `chateau` désigne ici un bâtiment doté de pièces, pas un château médiéval.

Les plans sont schématiques, sans échelle. Les passages intérieurs sont établis ; les trajets entre sites, les accès autorisés, les occupants et la scène de départ ne le sont pas encore. La pièce nommée « Cellule » est un espace représentatif, pas le relevé complet de la prison. Le répertoire public des plans n’accorde aucun droit d’entrée au personnage.

Aucun personnage, aucune date de départ ni aucune scène ne sont initialisés par la création des lieux. Ne pas ouvrir une partie Westeros à cause du journal vide. Le moteur de simulation Modern Front n’est pas encore raccordé.
''',encoding='utf-8')
    print('10 lieux canoniques, 60 pièces, 70 passages et 11 plans créés.')


if __name__ == '__main__':
    main()
