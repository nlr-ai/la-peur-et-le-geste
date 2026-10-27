"""Complète la mise en place demandée ; ne joue aucune attaque de Nova."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
os.environ['CONSEIL_MONDE'] = 'lumina-prime'
sys.path.insert(0, str(ROOT / 'scripts/noyau'))
from partie_greffe import Partie

p = Partie(str(ROOT / 'mondes/lumina-prime/etat/parties/citoyen-oriente-competent.jsonl'))
states = [
    ('orientation-13000', 'Le citoyen sait où et comment contribuer. Je défends un choix éclairé : partir de son envie et de ses acquis, présenter un besoin réel, puis confirmer lieu, interlocuteur et accès avant de commencer. Preuve exigée : il retrouve sa destination et explique son prochain geste. Une affectation imposée ou une adresse sans accès ne satisfait pas cet état. Source : 13000, 13010, 13020–13021.'),
    ('competence-13100', 'Le citoyen produit une contribution utile. Je défends un apprentissage ciblé : essai initial, écart observé, retour d’une personne compétente, nouvel essai puis résultat pour un utilisateur réel. La compétence se juge sur les critères convenus et la réalisation conservée. Lire les dossiers ou obtenir un avis flatteur ne suffit pas. Source : 13100, 13110–13111, 13120–13122.'),
    ('autonomie-13200', 'Le citoyen réussit un autre cas comparable et reconnaît ses limites. Je défends une autonomie située : retrouver ses ressources, agir sans consignes pas à pas, demander une aide précise au bon moment. La seconde situation doit éprouver un transfert ; recopier le premier résultat ne prouve rien. Cette preuve vaut pour l’activité observée, jamais pour tous les métiers. Source : 13200, 13210, 13220–13221.'),
]
for ident, text in states:
    if ident not in p.etats:
        refusal = p.ecrire({'camp': 'defense', 'coup': 'viser', 'id': ident, 'sert': 'parcours-defendable', 'texte': text})
        if refusal:
            raise RuntimeError(refusal)

resources = [
    ('choix-et-acces', 'Choix et accès confirmés — argument de défense : le rapprochement entre envie, acquis et besoin évite d’envoyer le citoyen vers une activité arbitraire. Les registres servent à chercher ; l’accès doit être confirmé pour ce citoyen. Si aucune occasion compatible n’est trouvée, l’orientation reste ouverte.', '13010 et 13020–13021 ; moyens documentaires M203, M204, M215.'),
    ('essai-et-retour', 'Essai et retour ciblé — argument de défense : observer une difficulté précise permet de choisir quoi apprendre et de comparer avant et après. Un accompagnateur compétent et disponible reste à identifier ; un mémento ne remplace pas cette disponibilité. Sans retour accessible, cette étape reste bloquée.', '13110 et 13120–13121 ; moyens documentaires M211, M215.'),
    ('preuve-par-usage', 'Réalisation et usage — argument de défense : un besoin identifié, des critères convenus et le retour d’un utilisateur réel donnent une prise pour contester la compétence. Je dois montrer le résultat et le comparer aux critères ; la satisfaction déclarée seule ne suffit pas.', '13111 et 13122 ; état 13100.'),
    ('transfert-et-limites', 'Second cas et limites — argument de défense : varier le cas permet de distinguer une réussite guidée d’une capacité réutilisable. Les aides effectivement reçues doivent être conservées dans le bilan. Si elles dictent chaque geste, l’autonomie n’est pas prouvée ; si le cas n’est pas comparable, la conclusion doit être limitée.', '13210 et 13220–13221 ; état 13200.'),
]
for ident, text, source in resources:
    if ident not in p.ressources:
        refusal = p.ecrire({'camp': 'defense', 'coup': 'demander', 'id': ident, 'nombre': 1, 'texte': text})
        if refusal:
            raise RuntimeError(refusal)
    if p.ressources[ident].get('en_attente'):
        refusal = p.ecrire({'camp': 'arbitre', 'coup': 'arbitrer', 'sur': ident, 'verdict': 'accorde', 'motif': 'Pièce argumentative du dossier figé, sources/citoyen-oriente-competent.json : ' + source + ' Accord de la source documentaire uniquement ; validité de l’argument contestable, aucune réalisation ni ressource humaine accordée.'})
        if refusal:
            raise RuntimeError(refusal)
print(f'{len(p.etats)} états ; {len(p.ressources)} pièces ; {len(p.lignes)} lignes. Mise en place complétée, aucune attaque jouée.')
