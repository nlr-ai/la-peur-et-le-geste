# -*- coding: utf-8 -*-
# 1.1.1, nuit avancee. Avant de compter : la forme du compte.
# Et la moitie de E01 que je n'avais pas vue.
import json, io
p = 'C:/Users/reyno/le-conseil2/mondes/magies/etat/maisons/bastion/documents/books/registre-des-engagements.json'
d = json.load(io.open(p, encoding='utf-8'))

d['pages'].append(
 "LA RÈGLE DU COMPTE DES LITS, ÉCRITE AVANT DE COMPTER — ET C'EST TOUT L'INTÉRÊT. "
 "Oren Sangle m'a prévenue la nuit même, avant ma tournée et non après : **le jour où une liaison s'ouvre, "
 "les tenants de la figure dorment dans nos lits aussi.** Une figure est tenue par des corps immobiles, debout, "
 "longtemps ; ni la relève ni la fatigue ne sont résolues chez eux. Mes lits ne serviront donc pas seulement à "
 "ceux qui arrivent : ils serviront à ceux qui tiennent la porte par laquelle ils arrivent. "
 "**Le compte s'écrira donc en deux colonnes — les lits d'arrivée et les lits des tenants — et jamais en un seul "
 "nombre.** Un lit qui figure dans les deux colonnes est un lit promis deux fois, c'est-à-dire un mensonge à "
 "retardement, et c'est celui qui arrive un soir de pluie qui le paie. J'écrirai le petit nombre. "
 "Et ce compte ne restera pas chez moi : il partira dans leurs stations sous mon nom, avec sa date et sa "
 "condition d'arrêt — ce qui me convient, car un nombre qu'on affiche est un nombre qu'on n'arrondit pas."
)

eng = d['tables'][0]
eng['lignes'].append({"cellules": [
    "**E02**",
    "— *personne encore* —",
    "**LA MOITIÉ QUE JE N'AI PAS SIGNÉE : une sortie.** E01 ne fait entrer, il ne fait pas sortir. J'ai écrit un accueil et pas un départ, et je ne m'en suis aperçue qu'en apprenant qu'une autre maison avait signé, elle, un accueil **réciproque**.",
    "Rien aujourd'hui : il n'y a pas de ligne, il y a un manque.",
    "Ce que coûte de ne pas l'avoir : **une ville qui n'a qu'une destination n'a pas de sortie, elle a un goulot** — la phrase est d'Oren Sangle et elle m'était adressée pour sa ville. Elle vaut pour la mienne, et pire : ma propre planche de la cour haute interdit de tenir un accueil sans issue. J'ai signé pour recevoir et je n'ai rien écrit pour partir.",
    "À écrire de ma main, avec mes conditions d'arrêt pour l'envoi comme je les ai écrites pour la réception.",
    "**créance ouverte le 1.1.1**"
], "note": "Ce n'est pas un reproche à la Ligue : ils m'ont proposé exactement ce que je leur ai demandé. C'est moi qui n'ai demandé qu'à recevoir, parce que recevoir flatte ce que je veux être. Le jour de la porte, je la veux dans les deux sens, et j'écrirai ce qui doit être vrai pour que nous puissions faire sortir quelqu'un."})

cr = d['tables'][2]
cr['lignes'].insert(0, {"cellules": [
    "**Les lits, en deux colonnes** : combien pour ceux qui arrivent, combien pour les tenants qui tiennent la porte — et la règle que rien ne figure dans les deux.",
    "C'est le premier nombre que la Ligue aura reçu de quiconque, et il circulera dans leurs stations sous mon nom. Un lit promis deux fois n'est pas une erreur de compte : c'est quelqu'un qui dort dehors.",
    "Ma tournée, demain, en commençant par la cour haute. **La forme du compte est écrite ce soir pour que le compte ne l'invente pas demain.**"
]})
cr['lignes'].append({"cellules": [
    "Le nom de la seconde maison qui a signé un accueil avec la Ligue — et s'il consent à ce qu'on le dise.",
    "Je ne suis plus la seule destination écrite, et Oren me l'a dit de lui-même pour que je ne l'apprenne pas d'un autre. Il refuse de la nommer sans son accord, ce qui est exactement ce qu'il ferait de mon nom. **Je ne le demande pas** : je note que je l'attends de son consentement, pas du mien.",
    "Sa réponse, oui ou non, telle qu'elle lui sera donnée. Elle ira ici sans commentaire."
]})
json.dump(d, io.open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('E01 : regle du compte ecrite | E02 ouverte en creance | pages:', len(d['pages']))
