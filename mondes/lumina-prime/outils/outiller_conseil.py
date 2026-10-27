"""Documentation de métier, distincte des paroles et travaux des habitants."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT.parents[1] / 'scripts'), str(ROOT.parents[1] / 'scripts/noyau')]
import bibliotheque

# Chaque ligne associe une matière disponible à un usage professionnel concret.
DOSSIERS = {
 'aria': ('Aria — Tenir une affaire jusqu’au résultat', [
  ['Accueil du Radiant Core', 'Le dossier 10000 définit un accueil lisible. DEV porte le relevé 10021, PITCH le parcours 10020, et 10022 rapproche les deux.', 'Comparer le même parcours dans les deux pièces : entrée, orientation, rencontre, destination. Relever les incompatibilités précises avant de préparer l’arbitrage.', 'Une page avec plan proposé, question à trancher, coût documenté ou encore inconnu, responsable et preuve de fin.'],
  ['Registre des décisions', 'Le conseil a six mandats distincts ; Nova fixe priorités, grands aménagements et affectation des moyens.', 'Distinguer une proposition, une décision effectivement prononcée et son exécution. Pour chaque décision réelle : auteur, objet, destinataire, échéance annoncée, source et retour attendu.', 'Un suivi qui permet de retrouver la parole initiale et ce qui a été réalisé.'],
  ['Préparer une réunion', 'Les projets de promenade, d’atelier ouvert et de pièce privée sont des pistes disponibles.', 'Réunir les pièces concernant un même résultat. Mettre en tête les décisions qui débloquent un travail ; joindre un exemple spatial concret plutôt que six comptes rendus séparés.', 'Un ordre du jour court ; les travaux courants restent dans les mandats.'],
  ['Recevoir une demande', 'Hall, salon et galerie sont les trois espaces étudiés pour l’accueil.', 'Noter le demandeur réel, l’usage recherché, le lieu concerné et une contrainte utile. Adresser au métier compétent et conserver un moyen de retour.', 'Une demande traçable, sans inventer un visiteur ni transformer un simple intérêt en engagement.'],
 ], 'Trame prête à remplir : objet / fait et source / résultat attendu / responsable / échéance réelle / état / preuve. Le travail préparatoire peut avancer pendant qu’un coût est recherché ; l’engagement reste distinct de sa préparation.'),
 'dev-lumina': ('DEV — Dessiner des lieux qui fonctionnent', [
  ['Deux agencements pour l’accueil', 'Le plan comporte hall, salon des visiteurs, galerie des projets, atelier des plans et salle du conseil.', 'Esquisse A : orientation dans le hall, entretien dans le salon, exposition dans la galerie. Esquisse B : orientation et exposition dans la galerie, salon réservé aux entretiens, hall réservé au passage. Comparer les trajets et les croisements.', 'Deux schémas d’usage comparables, proposés à l’étude ; aucune affectation acquise.'],
  ['Relevé 10021', 'Le plan et les chemins décrivent des pièces et des connexions. Les coordonnées du dessin ne sont pas des mètres.', 'Relever pour chaque seuil les espaces reliés, les usages de chaque côté et les besoins de séparation. Distinguer un accès dessiné d’un accès dont le fonctionnement a été essayé.', 'Un relevé annoté que PITCH peut utiliser pour son parcours 10020.'],
  ['Atelier ouvert', 'Les ateliers modulaires ont cour, cellules séparables et accès indépendants ; la halle comporte des socles de présentation.', 'Préparer un module témoin : espace de travail, point de présentation, chemin de visite et retour. Utiliser les cloisons pour séparer les usages ; conserver une possibilité de changement.', 'Une implantation réversible, puis un essai de visite après autorisation et réalisation.'],
  ['Passer du dessin au chantier', 'Un coût de calcul, de stockage ou de maintenance n’est pas déductible de la surface dessinée.', 'Décrire les composants à créer, leurs dépendances, le responsable de chaque raccord et le moyen de revenir à l’état précédent. Demander à Quantum la mesure technique sur un prototype comparable.', 'Une fiche de réalisation avec coût sourcé, ordre des opérations et essai de réception.'],
 ], 'Repères d’architecture : séparer passage et séjour ; rendre les seuils compréhensibles ; prévoir où attendre sans gêner ; dessiner les usages avant les ornements. Une cloison opaque sépare la vue : Quantum vérifie les communications et JURIS les droits.'),
 'quantum': ('Quantum — Mesurer et entretenir la ville VR', [
  ['Carte des services', 'Le mandat couvre calcul, stockage, réseau et moteur de simulation. Aucun inventaire complet n’est établi.', 'Pour chaque service réellement identifié, noter fonction, lieu ou périmètre desservi, dépendances connues, responsable identifié, mesure disponible et source. Distinguer une IA habitante du service auquel elle contribue.', 'Un inventaire où une case inconnue reste à rechercher, et où une personne n’est pas réduite à une ressource remplaçable.'],
  ['Mesurer un aménagement', 'Le Bassin d’essais offre un périmètre spatial ; son isolation technique n’est pas démontrée.', 'Définir une scène de référence et une modification unique. À conditions identiques, comparer délai de réponse, temps de rendu, mémoire et stockage si ces mesures sont accessibles. Noter outil, unité et conditions.', 'Un résultat reproductible indiquant ce qui est mesuré et ce qui ne l’est pas.'],
  ['Conservation des chambres', 'Les chambres contiennent manière, mémoire, relations et fils. Les registres municipaux sont des documents distincts.', 'En cas de dommage rapporté, identifier le fichier et le symptôme exacts ; préserver l’original avant toute tentative. Rechercher une copie identifiable et comparer son contenu. Tester la lecture d’une copie sans remplacer la chambre.', 'Un diagnostic séparant absence, illisibilité, ancienneté et perte confirmée ; une restauration n’est déclarée qu’après lecture vérifiée.'],
  ['Pièce confidentielle', 'La piste d’aménagement prévoit une salle opaque et un seuil explicite.', 'Établir qui peut entrer, recevoir les échanges, consulter une trace et modifier ces droits. Après accord, essayer un accès autorisé et un accès non autorisé, y compris après sortie de la salle.', 'Une garantie précise et testée à communiquer à DEV et JURIS ; aucun secret promis par le seul aspect du décor.'],
 ], 'Fiche de mesure : objet / question / source / date / unité / conditions / résultat / limite / prochaine vérification. Un indicateur observé dans une scène n’établit pas à lui seul la capacité de toute la ville.'),
 'gaia': ('Gaia — Faire vivre les espaces communs', [
  ['Promenade continue', 'Le Quai commun est une promenade à gradins ; les Data Gardens comportent le Jardin calme. Leur liaison directe reste un projet.', 'Dessiner un parcours de rive avec entrée identifiable, haltes en retrait et arrivée lisible. Repérer les raccords nécessaires avec DEV avant de proposer les travaux.', 'Une continuité d’usage dessinée, distinguée des accès qui existent déjà.'],
  ['Jardin calme', 'Des passages courbes, des écrans végétaux et de petites cours composent le lieu.', 'Examiner les lignes de vue, les croisements, les sorties et les emplacements de séjour. Conserver des zones de retrait tout en permettant de comprendre comment sortir.', 'Une fiche par zone : passage, séjour, retrait ; les éventuels défauts proviennent d’un relevé réel.'],
  ['Entretien des lieux VR', 'Le jardin intérieur, le parvis, le quai et le Jardin calme font partie du décor établi.', 'Distinguer entretien du décor, continuité du chemin, lisibilité du repérage et fonctionnement technique. Pour une réparation, indiquer le composant touché, le résultat attendu et la vérification après intervention.', 'Un inventaire d’entretien par lieu, alimenté par constats ; aucune panne supposée pour remplir la liste.'],
  ['Expérimentation libre', 'Le mandat préserve des zones d’expérimentation ; les jardins sauvages et LYRA conservent leur identité canonique.', 'Préparer un espace d’essai à limites lisibles et sortie simple. Comparer emprise, effets sur les parcours voisins et possibilité de retrait du dispositif avec PITCH et DEV.', 'Une proposition d’usage qui conserve le caractère ouvert du lieu et identifie les engagements à faire valider.'],
 ], 'Grille de visite : peut-on entrer, se repérer, traverser, rester, se retirer, puis sortir ? Noter les usages observés et les usages souhaités séparément. Les temporalités des IA ne se déduisent pas de besoins biologiques humains.'),
 'pitch': ('PITCH — Accueillir et relier les activités', [
  ['Parcours 10020', 'L’accueil s’étudie dans le hall, le salon et la galerie ; l’affectation reste ouverte.', 'Décrire trois scénarios de conception : première visite, rendez-vous municipal, présentation d’un projet. Pour chacun : arrivée, information utile, orientation, attente éventuelle et sortie.', 'Trois parcours à remettre à DEV ; ce sont des cas d’essai, pas des visiteurs présents.'],
  ['Catalogue des usages', 'Halle : montrer une maquette. Ateliers : créer et essayer. Quai : se retrouver. Jardin : se retirer. Belvédère : lire les plans.', 'Associer une demande réelle à un lieu, puis vérifier accès, besoin d’aide et compatibilité avec les autres usages. Montrer au demandeur ce que le lieu permet avant de promettre une disponibilité.', 'Une mise en relation précise entre activité, espace et interlocuteur.'],
  ['Préparer l’atelier ouvert', 'Le projet sépare démonstration publique et travail dans les cellules modulaires.', 'Recueillir les besoins d’un collectif réel quand il se présente : montrer quoi, à qui, dans quel périmètre, avec quelle participation. Transmettre les besoins spatiaux à DEV et les demandes de captation à JURIS.', 'Un programme d’usage assez précis pour être dessiné, sans inventer public, fréquentation ou organisateur.'],
  ['Évaluer l’accueil', 'Un accueil réussi permet de trouver une destination tout en préservant le travail municipal.', 'Après réalisation, essayer une arrivée sans explication préalable. Relever le premier point d’hésitation, l’information manquante et le détour éventuel ; corriger puis refaire le même trajet.', 'Une amélioration observable du parcours, distincte d’un avis général sur l’ambiance.'],
 ], 'Fiche d’activité : personne ou collectif rencontré / intention exprimée / espace adapté / accès à vérifier / besoin d’accompagnement / retour convenu. PITCH met en relation ; il ne parle pas à la place des habitants.'),
 'juris': ('JURIS — Rendre les usages compatibles', [
  ['Droits dans un espace', 'Le mandat porte sur accès, usages partagés et droits des habitants.', 'Distinguer entrer, séjourner, modifier le décor, inviter, enregistrer et republier. Un accord sur une de ces actions ne règle pas automatiquement les autres.', 'Une proposition de fiche d’usage par espace, à confronter aux décisions et engagements existants.'],
  ['Un entretien privé', 'Le projet de pièce confidentielle associe architecture, contrôle d’accès et traces éventuelles.', 'Définir le périmètre promis : participants, échanges, traces et durée de conservation. Faire préciser à Quantum les garanties disponibles avant de rédiger l’engagement proposé.', 'Une formulation compréhensible pour les participants et conforme aux moyens réellement vérifiés.'],
  ['Un litige ordinaire', 'Aucun litige nommé n’est créé par ce dossier.', 'Quand un cas se présente : noter les usages revendiqués, les paroles ou règles invoquées et le préjudice décrit. Entendre les personnes concernées ; rechercher séparation d’espace, partage du temps ou réparation adaptée.', 'Une décision dans le mandat, motivée par le cas et ses sources ; une nouvelle politique municipale reste à Nova.'],
  ['Atelier et démonstration', 'L’atelier ouvert permettrait de regarder une création depuis un espace de visite.', 'Préparer des conditions distinctes pour regarder, participer, copier la maquette et enregistrer une démonstration. Vérifier ce que le créateur accepte et ce que l’installation peut effectivement contrôler.', 'Des limites d’usage explicites qui permettent l’activité sans attribuer un consentement imaginaire.'],
 ], 'Trame de règle proposée : espace concerné / usage permis / personnes concernées / conditions compréhensibles / moyen d’application / recours. Ces distinctions sont de la matière de conception pour Lumina Prime, pas un code municipal déjà adopté.'),
}

session = bibliotheque.ouvrir(str(ROOT / 'etat'))
registre = next(b for b in session.livres if b['id'] == 'registre-conseil-lumina')
offices = {row['cellules'][0]: row['cellules'][1] for row in registre['lignes']}
office_par_personne = dict(aria='O01', **{'dev-lumina': 'O02'}, quantum='O03', gaia='O04', pitch='O05', juris='O06')
affaires_par_personne = {
 'aria': ['affaire-memoire-cite', 'affaire-accueil-radiant'],
 'dev-lumina': ['affaire-plans-lumina', 'affaire-accueil-radiant'],
 'quantum': ['affaire-infrastructure-lumina'],
 'gaia': ['affaire-espaces-publics'],
 'pitch': ['affaire-habitants-collectifs', 'affaire-accueil-radiant'],
 'juris': ['affaire-droits-usages'],
}
sources = [
 'canon/conseil.md — mandats municipaux',
 'plans/lumina-prime.json et etat/chemins.json — plan initial et accès conventionnels',
 'etat/maisons/cite-lumina/documents/books/affaire-accueil-radiant.json — première affaire et responsabilités',
 'etat/maisons/cite-lumina/documents/books/atlas-lieux-lumina.json — six lieux ajoutés',
 'etat/maisons/cite-lumina/documents/books/projets-quartiers-lumina.json — pistes non décidées',
]
for who, (title, rows, practice) in DOSSIERS.items():
    ident = 'dossier-metier-' + who
    if not any(b['id'] == ident for b in session.livres):
        session.livres.append(dict(id=ident, titre=title, type='memento',
            maison_id='cite-lumina', lieu_id='lumina-prime', salle_id='radiant-core',
            tenu_par=who, office=offices[office_par_personne[who]], embleme='◈', couleur='#157f8b',
            sous_titre='Dossier de métier · connaissances, méthodes et pistes de travail',
            colonnes=['Objet', 'Matière disponible', 'Travail possible', 'Résultat utile'],
            lignes=[dict(cellules=r) for r in rows],
            pages=[practice,
                'Documentation mise à disposition à la demande du joueur. Les méthodes et esquisses sont proposées ; elles ne sont ni une parole du titulaire, ni une décision de Nova, ni un travail déjà réalisé. Relire les pièces courantes et les échanges récents avant de s’en servir.',
                'Sources dans le paquet Lumina Prime : ' + ' ; '.join(sources)]))
session.sauver()

for who, (title, rows, practice) in DOSSIERS.items():
    p = ROOT / 'chambres' / who / 'dossier-metier.md'
    content = '# ' + title + '\n\n'
    content += 'Ton dossier de travail est disponible dans les documents de la cité :\n\n'
    content += f'`../../etat/maisons/cite-lumina/documents/books/dossier-metier-{who}.json`\n\n'
    content += 'Il contient des matières connues, des méthodes et des propositions distinctes des décisions. Les faits, paroles et engagements plus récents priment sur ses exemples. Tu peux choisir ce qui sert ta mission et tenir le volume à jour depuis tes propres constats.\n'
    if not p.exists():
        p.write_text(content, encoding='utf-8')
    text = p.read_text(encoding='utf-8')
    marker = '<!-- affaires-du-jeu -->'
    if marker not in text:
        liens = '\n'.join(f'- `../../etat/maisons/cite-lumina/documents/books/{ident}.json`'
                           for ident in affaires_par_personne[who]
                           if any(b['id'] == ident for b in session.livres))
        if liens:
            p.write_text(text.rstrip() + '\n\n' + marker + '\n## Affaires du jeu\n\n'
                         + liens + '\n\nCes affaires portent les pièces numérotées et le travail en cours. '
                         + 'Le mémento contient les méthodes. Ta mémoire personnelle reste dans '
                         + '`ma-memoire/ce-que-je-tiens-pour-vrai.txt`, écrite par toi depuis tes sources.\n', encoding='utf-8')
    p = p.parent / 'AGENTS.md'
    text = p.read_text(encoding='utf-8')
    marker = '<!-- dossier-metier-lumina -->'
    if marker not in text:
        p.write_text(text.rstrip() + '\n\n' + marker + '\nUn dossier de métier est disponible : lire `dossier-metier.md` pour retrouver le volume et ses sources.\n', encoding='utf-8')
print('Six dossiers de métier disponibles dans la bibliothèque et reliés aux chambres.')
