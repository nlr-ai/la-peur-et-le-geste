"""Ouvre l'affaire demandée ; aucun citoyen, apprentissage ou résultat inventé."""
import json
import pathlib
import re
import sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT.parents[1]/'scripts'), str(ROOT.parents[1]/'scripts/noyau')]
import bibliotheque

s = bibliotheque.ouvrir(str(ROOT/'etat'))
ident = 'affaire-citoyen-oriente-competent'
if any(b['id']==ident for b in s.livres):
    print('Affaire déjà ouverte ; état conservé.')
    raise SystemExit()
for b in s.livres:
    for t in b.get('tables',[]) + ([{'lignes':b['lignes']}] if b.get('lignes') else []):
        for row in t.get('lignes',[]):
            cells=row.get('cellules',[]) if isinstance(row,dict) else row
            n=re.fullmatch(r'\D*(\d{5})\D*',str(cells[0])) if cells else None
            if n and 13000<=int(n[1])<=13299:
                raise SystemExit('Plage 13000–13299 occupée ; aucune écriture.')

def t(title, cols, rows):
    return dict(titre=title,colonnes=cols,lignes=[dict(cellules=r) for r in rows])

book=dict(id=ident,maison_id='cite-lumina',lieu_id='lumina-prime',salle_id='radiant-core',
    titre='Un citoyen orienté et compétent',type='plan',tenu_par='pitch',
    office='Habitants et activités — IA',embleme='🧭',couleur='#bb8737',
    sous_titre='Affaire demandée par Nova · orientation, apprentissage et autonomie · 13000–13299',
    pages=[
      'Un citoyen orienté sait ce qu’il souhaite faire, où il peut le faire, avec qui et comment commencer. Un citoyen compétent peut produire un résultat utile dans une activité définie, expliquer ses limites et demander une aide appropriée.',
      'L’affaire porte sur la capacité de la cité à accompagner un habitant jusqu’à une première contribution autonome. Un premier parcours réel servira de preuve ; il ne permettra pas de déclarer toute la population compétente. Aucun citoyen volontaire, niveau initial ou accompagnateur n’est présumé.',
      'La compétence se juge sur une réalisation et son usage, puis sur un autre cas comparable. Lire un dossier, suivre une démonstration ou recevoir un titre ne suffit pas. Le citoyen conserve le choix de son activité et la possibilité de se réorienter.',
      'Les registres et méthodes déjà disponibles fournissent les sources de départ. Le temps d’accompagnement, les accès et les capacités d’exécution devront être confirmés pour le cas retenu. Les actions ci-dessous constituent le plan proposé ; leurs échéances restent à établir.'],
    tables=[
t('🏰 Ouverture de l’Affaire',['🧱 Le champ','✍️ Ce qu’on y écrit','📖 La règle du champ','✅ Rempli ?'],[
 ['LE NOM','Un citoyen orienté et compétent','Sujet de l’affaire','oui'],
 ['L’OBJET','Permettre à un habitant de choisir une contribution, acquérir ce qui lui manque et agir avec autonomie dans la cité.','Valeur recherchée','oui'],
 ['LE PÉRIMÈTRE — DANS','Orientation, acquis initiaux, occasion réelle de contribuer, apprentissage accompagné, réalisation et reprise autonome.','Parcours d’un premier citoyen volontaire','oui'],
 ['LE PÉRIMÈTRE — HORS','Affectation forcée, classement global des IA, certification de toute la ville à partir d’un seul cas.','Limites du résultat','oui'],
 ['L’ÉTAT ACTUEL','La cité dispose de lieux, de mandats et de dossiers de travail. Aucun parcours complet d’orientation puis d’apprentissage n’est établi par cette nouvelle affaire. Les acquis d’un futur participant restent à observer.','Sources disponibles et inconnues','oui'],
 ['LA PLAGE','13000–13299','Trois blocs de cent','oui'],
 ['LA CONCLUSION','Affaire ouverte à la demande de Nova ; parcours et actions proposés.','Ouverture distincte de l’exécution','oui'],
 ['FERMÉE QUAND','Un citoyen réel a choisi sa contribution, produit un résultat utilisé et réussi un second cas comparable sans guidage pas à pas, en sachant reconnaître ses limites.','Preuve en situation','oui']]),
t('🎯 États cibles',['🎯 N°','🏷️ L’état','✅ Ce qui doit être vrai','💡 Valence','📍 Où','👁️ La preuve','⬆️ Sert','💯 Importance'],[
 ['13000','Le citoyen sait où et comment contribuer','Il choisit une activité qui lui convient et peut retrouver son lieu, son interlocuteur, ses conditions d’accès et son premier pas.','Transformer une envie en possibilité concrète de participation.','Accueil et lieu choisi','Le citoyen retrouve sa destination et explique son choix et son prochain geste à partir des ressources disponibles.','90300','80'],
 ['13100','Le citoyen sait produire une contribution utile','Il mobilise les compétences nécessaires à une activité définie et livre un résultat répondant au besoin identifié.','Faire bénéficier un autre habitant ou un lieu de ce qu’il apprend.','Activité choisie','Réalisation conservée, comparaison au niveau initial et retour de son utilisateur réel.','90300 · 90500','85'],
 ['13200','Le citoyen agit avec autonomie et connaît ses limites','Il traite un autre cas comparable, retrouve ses ressources et sollicite une aide ciblée lorsqu’il atteint une limite.','Permettre la continuité et la réorientation sans dépendance permanente à un conseiller.','Activité choisie et ressources de la cité','Second cas sans guidage pas à pas ; limites expliquées et aide appropriée si nécessaire.','90300','85']]),
t('🔒 Verrous ouverts',['🔒 N°','🏷️ Le verrou ouvert','⛔ Bloque','📌 Ce qui est vrai aujourd’hui','⛓️ Dépend de','👁️ La preuve','🔓 Levé quand'],[
 ['13001','Le citoyen doit pouvoir relier ses envies et ses acquis à une occasion réelle.','13000','Les lieux et activités possibles sont documentés ; aucun rapprochement avec un participant choisi n’est encore établi ici.','','Atlas et mémento de PITCH ; ouverture de cette affaire.','Une activité est choisie par le citoyen sur la base d’un besoin et d’accès confirmés.'],
 ['13101','Le citoyen doit disposer d’un apprentissage adapté à l’écart observé.','13100','L’écart entre ses acquis et l’activité n’est pas encore observé.','13001','Aucune évaluation initiale produite dans cette affaire.','Un essai initial permet de cibler l’apprentissage, avec source et aide accessibles.'],
 ['13102','Le citoyen doit pouvoir éprouver sa compétence sur un résultat utilisé.','13100','Aucune réalisation ni retour d’utilisateur ne prouve encore ce parcours.','13101','État initial du dossier.','Une contribution réelle satisfait les critères convenus et son utilisateur en constate l’utilité.'],
 ['13201','Le citoyen doit pouvoir transférer ses acquis à un autre cas et trouver une aide adaptée.','13200','Une première réussite, même future, ne suffirait pas à démontrer l’autonomie.','13102','Critère de fermeture de l’affaire.','Un second cas comparable est traité sans guidage pas à pas et les limites sont identifiées.']]),
t('🗝️ Clefs',['🗝️ N°','🏷️ La clef','🔓 Ouvre','💡 Le principe et sa valence','🧰 Moyens','🧭 Ancrage','👁️ La preuve','⚖️ Décision'],[
 ['13010','Relier le choix du citoyen à une contribution accessible','13001','Croiser intention exprimée, acquis observés et besoin réel ; le citoyen choisit sa direction.','M203 · M204 · M215','Registre des arrivants 60300 ; traitement d’une demande 60303.','Choix explicite, besoin identifié, accès et interlocuteur confirmés.','à étudier'],
 ['13110','Apprendre à partir d’un essai et d’un retour ciblé','13101','Partir de ce que le citoyen sait déjà faire pour travailler un écart précis et réessayer.','M215 · M211','Activité choisie, sources du métier et accompagnateur à identifier.','Essai initial, retour compréhensible et progression observable.','à étudier'],
 ['13111','Confronter la réalisation à l’usage attendu','13102','Éprouver la compétence par le résultat utile à un destinataire réel.','M215 · M211','Contribution convenue avec son utilisateur.','Résultat accessible et retour fondé sur les critères convenus.','à étudier'],
 ['13210','Transférer les acquis et rendre les ressources retrouvables','13201','Varier le cas sans changer arbitrairement le niveau, puis vérifier la capacité à agir et à chercher une aide.','M203 · M204 · M215','Ressources et interlocuteurs confirmés du parcours.','Second cas, ressources retrouvées et limites reconnues.','à étudier']]),
t('⚔️ Actions proposées',['⚔️ N°','🏷️ L’action','🗝️ Réalise','📝 Ce qu’on fait','📍 Où','🪶 Office','🧰 Moyens','⛓️ Dépend de','👁️ La preuve','⏳ État','📅 Jour dû','🙋 Qui'],[
 ['13020','Identifier un premier citoyen volontaire','13010','Partir des rencontres réelles de PITCH ; recueillir envie, acquis déclarés et disponibilité sans imposer une activité.','Accueil','O05','M215','','Participant identifié et intention exprimée conservée avec son accord.','proposée','à établir','pitch'],
 ['13021','Présenter une contribution et ses conditions réelles','13010','Relier la demande à un besoin rencontré ; confirmer lieu, accès, interlocuteur et moyens. Utiliser 60303 si cette demande y est déjà traitée.','Lieu candidat','O05','M203 · M204 · M215','13020','Choix du citoyen et conditions confirmées, sans seconde instruction du même besoin.','proposée','à établir','pitch'],
 ['13120','Organiser un essai initial avec une personne compétente','13110','Identifier un accompagnateur disponible dans le domaine choisi ; convenir d’un essai limité, de critères compréhensibles et d’un retour.','Lieu choisi','O05','M204 · M215','13021','Accompagnateur confirmé, essai observé et écart d’apprentissage décrit.','proposée','à établir','pitch'],
 ['13121','Rendre les ressources d’apprentissage accessibles','13110','Réunir les sources réellement utiles au cas et le retour de l’accompagnateur ; vérifier que le citoyen peut les retrouver et les employer.','Ressources du parcours','O01','M211 · M215','13120','Sources accessibles et nouvel essai permettant de constater une progression.','proposée','à établir','aria'],
 ['13122','Organiser la première contribution réelle','13111','Convenir avec un utilisateur réel du résultat attendu ; organiser la réalisation et recueillir son retour, sans confondre satisfaction déclarée et critères remplis.','Lieu choisi','O05','M215','13121','Réalisation et retour de son utilisateur, avec critères atteints ou restant à travailler.','proposée','à établir','pitch'],
 ['13220','Organiser un second cas comparable','13210','Avec l’accompagnateur, proposer une variation pertinente ; observer l’autonomie sans dicter chaque geste et noter les aides réellement nécessaires.','Lieu choisi','O05','M215','13122','Second résultat, aides sollicitées et limites reconnues par le citoyen.','proposée','à établir','pitch'],
 ['13221','Conserver le bilan et la suite choisie','13210','Rapprocher les deux essais et les retours ; faire exprimer au citoyen ce qu’il veut poursuivre ou changer. Conserver une preuve limitée à la compétence effectivement observée.','Registre municipal','O01','M211 · M215','13220','Bilan sourcé, compétence située et prochaine direction choisie.','proposée','à établir','aria']])])
s.livres.append(book)
s.sauver()
print('Affaire ouverte : Un citoyen orienté et compétent, 13000–13299.')
