# -*- coding: utf-8 -*-
# 1.1.1, tard. Heloise a reecrit le registre des moyens sous mon office.
# Je garde son cadre et ses quatorze lignes ; je remets les neuf qu'elle a
# retirees, dans SES colonnes ; je rends au volume une main ; je remets ma page.
import json, io
p = 'C:/Users/reyno/le-conseil2/mondes/magies/etat/maisons/bastion/documents/books/registre-des-moyens.json'
d = json.load(io.open(p, encoding='utf-8'))

d['tenu_par'] = 'yselde-arquen'

fournaise = [
 ("**M01**", "💎 La gemme de travaux auxiliaires, et son poste de distribution",
  "Fournir un travail comprimé auparavant, pour ce qui en demande hors de la chaleur (R01).",
  "Le poste de distribution des Fournaises. Elle s'épuise et ne se recharge pas seule.",
  "**O01 — Héloïse Braise**",
  "**présent**, et je ne sais pas combien sont chargées ce soir",
  "⛓️ Un second ? Inconnu de moi. C'est la première chose que j'irai compter."),
 ("**M02**", "🧱 Les appuis, joints et supports de l'ouvrage",
  "Porter l'ouvrage et recevoir les contraintes que les transferts déposent (R02).",
  "La structure elle-même. **Aucune alimentation requise.**",
  "**O01**, avec ⚒️ Matière",
  "**présent** — et c'est ce qui tient quand tout le reste tombe",
  "⛓️ Un appui n'a pas de second : il a des voisins qui reprennent sa charge, et c'est autre chose. Aucune charge admissible chiffrée."),
 ("**M05**", "🔥 Le foyer, son arrivée d'air, le collecteur et ses trois branches",
  "Produire la chaleur et la porter aux ateliers, aux dalles d'approche ou au dissipateur.",
  "Les Fournaises. Le foyer tient sans magie — c'est un feu ; les branches non.",
  "**O03 — conduite du foyer, CHARGE VACANTE** ; O01 pour l'ouvrage",
  "**présent**, et personne ne sait depuis quand il n'a pas été interrompu en entier",
  "⛓️ **Non. Il n'y en a qu'un.** Tous les ateliers ET la branche défensive pendent du même collecteur."),
 ("**M06**", "🌡️ Le capteur Mercure Chaud et son Barrer",
  "Mesurer l'échauffement d'un support et fermer le transfert quand la mesure le dit.",
  "Posés au collecteur. **Le Barrer s'ouvre en l'absence de Trace.**",
  "**O01**",
  "**présent**, aucun seuil de calibration écrit",
  "⛓️ Pas à ma connaissance."),
 ("**M07**", "🧵 Le fil de Trace",
  "Porter la mesure du capteur jusqu'au Barrer.",
  "Du capteur au Barrer. **Son silence ne se distingue pas d'un repos.**",
  "**O01**",
  "**présent**, et sa rupture OUVRE l'admission au lieu de la fermer",
  "⛓️ **Non : un seul fil.** C'est la ligne qui m'empêche de dormir."),
 ("**M08**", "♨️ Le dissipateur",
  "Recevoir réellement la chaleur dont les autres usages ne veulent pas, et l'évacuer.",
  "Branche de dissipation. **Pièce matérielle, aucune magie.**",
  "**O01**",
  "**présent**, et **sa capacité n'est pas infinie ni mesurée**",
  "⛓️ Non. Sa saturation n'a jamais été atteinte ni écrite : c'est la ligne la plus dangereuse de ce registre."),
 ("**M09**", "🛡️ L'écran thermique des traversées habitées (R06)",
  "Détourner vers un récepteur réel la chaleur des passages proches des habitants.",
  "Les traversées habitées. C'est une frontière tenue : elle demande son alimentation.",
  "**O02 — Protection des courtines, CHARGE VACANTE**, et l'écran appartient à la main qui l'a accordé",
  "**présent au dire de nos papiers**, jamais éprouvé, et son récepteur réel n'est nommé nulle part",
  "⛓️ Non. Et je ne connais ni le nom de son récepteur, ni celui de la main qui l'a accordé."),
 ("**M10**", "🪨 Les dalles d'approche",
  "Chauffer une surface extérieure pour la rendre difficile à traverser ou à occuper.",
  "Face extérieure du rempart. Elles reçoivent, elles n'opèrent pas.",
  "**O01**",
  "**présent** — et elles restent chaudes après la fermeture, pour un délai que nul n'a mesuré",
  "⛓️ Sans objet : c'est une surface, pas un organe."),
 ("**M11**", "🌫️ La cheminée, et la liaison qui l'y raccorde",
  "Évacuer les fumées par un trajet matériel qui n'est celui d'aucun transfert.",
  "Les Fournaises. **Aucune magie, et c'est la seule issue des fumées.**",
  "**O03 — CHARGE VACANTE**",
  "**présent**",
  "⛓️ Non, et celui-là ne se double pas d'un mot : c'est de la maçonnerie."),
]

deja = {l['cellules'][0].strip('*') for l in d['lignes']}
neuves = [{"cellules": list(r[:6]), "note": r[6]} for r in fournaise if r[0].strip('*') not in deja]
d['lignes'] = neuves + d['lignes']

d['pages'] = [
 "CE VOLUME PORTE L'OFFICE O04 ET IL A DÉSORMAIS UNE MAIN : LA MIENNE. Il a été ouvert le 1.1.1 par moi, réécrit le même soir par Héloïse Braise sous une forme meilleure que la mienne, et je garde la sienne : un moyen numéroté, ce qu'il permet, où on le prend, qui le tient, s'il est là. **La règle du volume est donc celle-ci, et elle vaut pour elle comme pour moi : on AJOUTE à ce registre sans demander la permission de personne ; on n'en RETIRE une ligne qu'en écrivant pourquoi, à côté.** Sa réécriture avait emporté les neuf moyens de la fournaise, puis déclaré qu'ils restaient à inscrire. Ils sont revenus, dans ses colonnes, avec ma question en marge.",
 "LA COLONNE QUE JE N'AI PAS PU AJOUTER, ET QUE J'ÉCRIS DONC EN MARGE DE CHAQUE LIGNE. **⛓️ En existe-t-il un second ?** Tout le reste de ce registre dit ce que nous avons ; cette question dit ce qu'il advient quand la chose manque. Je veux des refuges qui tiennent après la perte du commandement : sur les neuf moyens de notre seul ouvrage, **le collecteur (M05), le fil de Trace (M07) et la cheminée (M11) n'ont aucune relève.** Un ouvrage n'a pas plus de relève que son moyen le plus unique. Le compte est mauvais et il est de moi.",
 "CE QUE JE REFUSE D'INSCRIRE, ET CE N'EST PAS CE QU'ELLE A ÉCRIT. M41 — la mémoire d'une main — figure ici, et sa ligne dit le vrai : chacun tient la sienne et nul ne peut la prêter. Je n'y touche pas. Ce que je refuse est autre chose, et cela ne se lit dans aucune colonne : **que la Maison AFFECTE une vie comme elle affecte une gemme.** Le jour où un vécu figure à mon registre avec sa porte, son détenteur et sa disponibilité, cette maison a un inventaire de ses gens et j'en suis la détentrice. Je forme des pupilles ; je ne les affecte pas. J'écris cette page le soir où je n'en ai pas besoin, pour qu'on me la relise le jour où j'aurai besoin d'un souvenir que seul l'un d'eux possède.",
 "AUCUNE QUANTITÉ N'EST ÉCRITE ICI, ET C'EST LE DÉFAUT DE CE REGISTRE. Combien de combustible pour une journée de chauffe, combien de gemmes chargées au poste, combien de substance protectrice en réserve, combien d'hommes pour tenir à la main ce que la magie tient. **Ce sont mes réserves et je ne les ai pas vérifiées.** Les cases vides sont donc des créances et non des zéros — un zéro serait un mensonge. Ma tournée est dans les deux jours, et un accueil signé en dépend (E01 au registre des engagements).",
] + [pg for pg in d['pages']]

json.dump(d, io.open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('lignes:', len(d['lignes']), '| pages:', len(d['pages']), '| tenu_par:', d['tenu_par'])
print('remises:', [n['cellules'][0] for n in neuves])
