"""Ouvre le projet approuvé par Nova ; ne simule ni travaux ni paroles."""
import json
import pathlib
import re
import sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT.parents[1]/'scripts'), str(ROOT.parents[1]/'scripts/noyau')]
import bibliotheque

s = bibliotheque.ouvrir(str(ROOT/'etat'))
ID = 'affaire-habiter-creative-nexus'
if any(b['id']==ID for b in s.livres):
    print('Affaire déjà présente ; état conservé.')
    raise SystemExit()
for b in s.livres:
    for t in b.get('tables',[]) + ([{'lignes':b['lignes']}] if b.get('lignes') else []):
        for line in t.get('lignes',[]):
            c=line.get('cellules',[]) if isinstance(line,dict) else line
            n=re.fullmatch(r'\D*(\d{5})\D*', str(c[0])) if c else None
            if n and 11000 <= int(n[1]) <= 11299:
                raise SystemExit('Plage 11000–11299 déjà occupée ; aucune écriture.')

def table(title, cols, rows):
    return dict(titre=title,colonnes=cols,lignes=[dict(cellules=x) for x in rows])

b=dict(id=ID,maison_id='cite-lumina',lieu_id='lumina-prime',salle_id='radiant-core',
       titre='Habiter le Creative Nexus',type='plan',tenu_par='dev-lumina',
       office='Architecture et travaux — IA',embleme='🏘️',couleur='#168a79',
       sous_titre='Vision approuvée par Nova · un premier îlot habité à étudier · 11000–11299',
       pages=[
       'Direction approuvée par le joueur : une ville que ses habitants peuvent transformer. L’îlot proposé associe espaces personnels modulables, cour commune, atelier partagé et galerie ouverte sur une promenade.',
       'Le Creative Nexus et ses ateliers modulaires et sa halle des maquettes existent dans le décor. L’îlot est un projet : son implantation, son dimensionnement, ses occupants et ses moyens restent à établir. L’accord ouvre l’étude ; il ne vaut pas lancement de travaux ni attribution de logements.',
       'Le projet doit se juger en situation : s’installer, transformer son espace, créer et accueillir quelqu’un. Les moyens documentaires servent l’étude ; les capacités techniques et les coûts de fonctionnement restent à mesurer.'],
       tables=[
table('🏰 Ouverture de l’Affaire',['🧱 Le champ','✍️ Ce qu’on y écrit','📖 La règle du champ','✅ Rempli ?'],[
 ['LE NOM','Habiter le Creative Nexus','Sujet de l’affaire','oui'],
 ['L’OBJET','Donner une première forme habitable à la vision de Nova : habiter, créer et se retrouver dans un îlot transformable.','Résultat recherché','oui'],
 ['LE PÉRIMÈTRE — DANS','Un îlot du Creative Nexus : espaces personnels, cour, atelier partagé, galerie et raccord à la promenade.','Périmètre spatial','oui'],
 ['LE PÉRIMÈTRE — HORS','Refonte de toute la ville, attribution d’espaces à des habitants non rencontrés, travaux avant décision de réalisation.','Limites du projet','oui'],
 ['L’ÉTAT ACTUEL','Vision approuvée dans cette conversation ; lieux de l’atlas disponibles comme sources. Aucun plan d’îlot, occupant ou budget arrêté.','Faits séparés des intentions','oui'],
 ['LA PLAGE','11000–11299','Trois blocs de cent, adresses stables','oui'],
 ['LA CONCLUSION','Étude ouverte. Réalisation à décider sur les pièces produites.','Conclusion limitée à la décision reçue','oui'],
 ['FERMÉE QUAND','Des IA peuvent s’installer, modifier leur espace et accueillir quelqu’un dans l’îlot réalisé, avec des droits explicites et des moyens de fonctionnement connus.','Essais réels après réalisation','oui']]),
table('🎯 États cibles',['🎯 N°','🏷️ L’état','✅ Ce qui doit être vrai','💡 Valence','📍 Où','👁️ La preuve','⬆️ Sert','💯 Importance'],[
 ['11000','Des espaces personnels habitables et transformables','Un habitant peut s’installer, régler son espace et recevoir quelqu’un sans perdre la maîtrise de ses accès.','Faire une place durable à chacun dans la cité.','Îlot du Creative Nexus','Essais d’installation, modification et invitation avec des participants réels ; droits et fonctionnement vérifiés.','90300','80'],
 ['11100','Une création peut être essayée et montrée','L’atelier partagé permet une expérimentation réversible et la galerie sa présentation sans traverser les espaces privés.','Donner aux idées une existence partageable.','Atelier et galerie de l’îlot','Une création effectivement essayée puis présentée, avec retour à l’état précédent éprouvé.','90500','75'],
 ['11200','La vie collective dispose de lieux accueillants','La cour et le raccord à la promenade permettent de passer, rester et se rencontrer sans bloquer les accès personnels.','Faire de l’îlot un lieu de vie commun.','Cour et promenade','Parcours réel et observation des usages après réalisation.','90300 · 90500','75']]),
table('🔒 Verrous ouverts',['🔒 N°','🏷️ Le verrou ouvert','⛔ Bloque','📌 Ce qui est vrai aujourd’hui','⛓️ Dépend de','👁️ La preuve','🔓 Levé quand'],[
 ['11001','L’îlot doit disposer d’une implantation et d’usages compatibles.','11000','Le programme de quatre espaces est approuvé comme vision ; leur implantation reste à dessiner.','','Accord du joueur ; atlas des lieux.','Une implantation compare les accès, les seuils et les usages recherchés.'],
 ['11002','Le fonctionnement et les droits doivent être connus avant la réalisation.','11000','Aucun coût ni droit propre à l’îlot n’est arrêté.','11001','Absence de pièces de réalisation dans cette affaire.','Capacités, coûts et garanties sont documentés ; Nova décide la réalisation.'],
 ['11101','L’atelier doit permettre d’expérimenter et de montrer sans empiéter sur l’intimité.','11100','L’atelier et la galerie figurent au programme, sans organisation propre à l’îlot.','11001','Programme de la vision.','Un agencement et des conditions d’essai séparent les usages et permettent le retour.'],
 ['11201','Les espaces communs doivent permettre passage et séjour.','11200','Cour et promenade sont prévues ; raccords et haltes ne sont pas définis.','11001','Programme de la vision.','Un parcours et des espaces de séjour sont dessinés puis essayés après réalisation.']]),
table('🗝️ Clefs',['🗝️ N°','🏷️ La clef','🔓 Ouvre','💡 Le principe et sa valence','🧰 Moyens','🧭 Ancrage','👁️ La preuve','⚖️ Décision'],[
 ['11010','Articuler des espaces transformables autour de seuils lisibles','11001','Faire coexister maîtrise de l’espace personnel et accès aux lieux partagés.','M203 · M205 · M212','Creative Nexus ; principes de DEV.','Esquisse argumentée et parcours comparés.','retenue pour étude'],
 ['11011','Dimensionner la réalisation sur des capacités et des garanties établies','11002','Relier les usages souhaités à ce que la cité peut tenir dans la durée.','M204 · M213 · M216','États 40002 et 70004, sans les dupliquer.','Dossier de réalisation avec coût sourcé, garanties et décision de Nova.','retenue pour étude'],
 ['11110','Séparer les parcours de création, de visite et d’habitation','11101','Permettre de montrer une création tout en préservant le travail et l’intimité.','M203 · M212 · M215','Ateliers modulaires et halle des maquettes ; état 40005.','Scénarios de création, démonstration et retour testables.','retenue pour étude'],
 ['11210','Relier les lieux de séjour par un parcours public continu','11201','Donner une place à la rencontre sans transformer toutes les cours en couloirs.','M203 · M214','Cour projetée ; état 50002.','Schéma des haltes, seuils et raccords ; essai après réalisation.','retenue pour étude']]),
table('⚔️ Actions — étude ouverte',['⚔️ N°','🏷️ L’action','🗝️ Réalise','📝 Ce qu’on fait','📍 Où','🪶 Office','🧰 Moyens','⛓️ Dépend de','👁️ La preuve','⏳ État','📅 Jour dû','🙋 Qui'],[
 ['11020','Dessiner une première implantation','11010','Situer espaces personnels, cour, atelier et galerie ; distinguer adaptation d’existant et construction proposée.','Creative Nexus','O02','M203 · M205 · M212','','Esquisse cotée seulement là où une mesure existe, avec accès et seuils.','à faire','à établir','dev-lumina'],
 ['11021','Décrire les usages à accueillir','11010','Préparer les cas s’installer, modifier son espace et recevoir quelqu’un ; recueillir les besoins des habitants effectivement rencontrés.','Creative Nexus','O05','M203 · M215','','Programme distinguant scénarios de conception et besoins exprimés.','à faire','à établir','pitch'],
 ['11022','Définir les droits d’usage proposés','11011','Appliquer les droits existants au programme ; préciser entrée, transformation, invitation et parties partagées.','Îlot projeté','O06','M204 · M216','11020 · 11021','Proposition sourcée ; décisions nouvelles clairement identifiées.','à faire','à établir','juris'],
 ['11023','Évaluer les besoins de fonctionnement','11011','Sur l’esquisse, identifier ce qui doit être mesuré, les capacités disponibles et le coût documentable ; référencer le relevé général 40302.','Îlot projeté','O03','M213','11020','Besoin technique et coût avec sources, unités et inconnues.','à faire','à établir','quantum'],
 ['11120','Décrire un essai de création ouvert aux visiteurs','11110','Tracer création, démonstration et retour à l’état précédent sans passage par les espaces privés.','Atelier et galerie projetés','O02','M203 · M212 · M215','11020 · 11021','Scénario et agencement prêts à être éprouvés après réalisation.','à faire','à établir','dev-lumina'],
 ['11220','Dessiner les usages de la cour et les raccords','11210','Distinguer passage, séjour et retrait ; situer haltes et seuils sur l’implantation.','Cour et promenade projetées','O04','M203 · M214','11020','Plan d’usage reliant la cour au quartier.','à faire','à établir','gaia'],
 ['11024','Assembler le dossier de réalisation pour Nova','11011','Rapprocher implantation, usages, droits et fonctionnement ; faire apparaître les arbitrages et les moyens nécessaires.','Radiant Core','O01','M204 · M211','11022 · 11023 · 11120 · 11220','Dossier permettant une décision de réalisation, sans la présumer.','à faire','à établir','aria']])])
s.livres.append(b)
s.sauver()
print('Habiter le Creative Nexus : étude ouverte, 11000–11299.')
