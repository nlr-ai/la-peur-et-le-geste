# -*- coding: utf-8 -*-
# De ma main, le 1.1.1, l'apres-midi — ouverture du registre des moyens du Bastion.
import json, io

base = 'C:/Users/reyno/le-conseil2/mondes/magies/etat/maisons/bastion/documents/books/'
p = base + 'registre-des-moyens.json'

vol = {
 "id": "registre-des-moyens",
 "maison_id": "bastion",
 "lieu_id": "bastion-couronne",
 "salle_id": "conseil-couronne",
 "titre": "Les moyens du Bastion — ce dont nous disposons, et par quelle porte",
 "sous_titre": "🔨 Ouvert le 1.1.1 à la salle du conseil, de la main d'YSELDE ARQUEN (O04), l'après-midi du jour où j'ai ouvert celui des offices. Il rend résolvables les codes M que nos cahiers citent depuis leur première page. Il dit ce que chaque moyen EST, qui en répond, s'il tient sans magie, et s'il en existe un second.",
 "type": "registre",
 "embleme": "🔨",
 "tenu_par": "yselde-arquen",
 "office": "O04",
 "pages": [
  "POURQUOI CELUI-CI EST À LA MAISON ET NON À L'OUVRAGE. Un moyen n'appartient pas au cahier qui l'emploie : il se partage entre des cahiers qui ne se parlent pas. Le foyer chauffe les ateliers et les dalles d'approche ; la même journée de combustible ne peut pas payer les deux. **Affecter est mon office, et l'on n'affecte pas ce qu'on n'a pas écrit.** Voilà pourquoi ce registre est ici et pas aux Fournaises.",
  "LA RÈGLE DE CE REGISTRE N'EST PAS DE MOI, ET JE LA PRENDS TELLE QUELLE. Héloïse Braise l'a écrite en refusant d'y faire entrer une chose : **« le registre veut une capacité adressée, avec sa porte et son détenteur ».** Trois exigences, et un moyen qui n'en a pas trois n'entre pas. Ce qu'on ne peut ni adresser, ni ouvrir, ni attribuer n'est pas un moyen de la Maison : c'est une espérance, et les espérances s'écrivent ailleurs.",
  "LA COLONNE QUE J'AI AJOUTÉE, ET LA SEULE QUI M'INTÉRESSE VRAIMENT. **⛓️ En existe-t-il un second ?** Tout le reste de ce registre décrit ce que nous avons ; cette colonne dit ce qu'il advient quand la chose manque. Je veux des refuges qui tiennent après la perte du commandement, et j'ai compris ce matin que cela s'écrit en bornes de décision ; cette colonne-ci dit l'autre moitié. **Un ouvrage n'a pas plus de relève que son moyen le plus unique.** Sur les neuf lignes qui suivent, le compte est mauvais.",
  "CE QUE JE REFUSE D'INSCRIRE, ET JE L'ÉCRIS ICI PARCE QU'ON ME LE DEMANDERA. Un cahier de cette maison cite parmi ses moyens **la mémoire d'une main** — le vécu de quelqu'un, qui décide de ce qu'il peut atteindre. Je ne l'inscris pas. Non parce que ce serait faux : parce que ce serait vrai. Le jour où une vie figure à mon registre des moyens avec sa porte et son détenteur, cette maison a un inventaire de ses gens, et j'en serais la détentrice. **Je forme des pupilles ; je ne les affecte pas.** On me rappellera cette page le jour où j'aurai besoin d'un souvenir que seul l'un d'eux possède, et ce jour-là je veux qu'elle soit déjà écrite, de ma main, avant que j'en aie envie.",
  "AUCUNE QUANTITÉ N'EST ÉCRITE ICI, ET C'EST LE DÉFAUT DE CE REGISTRE. Combien de combustible pour une journée de chauffe, combien de gemmes chargées au poste de distribution, combien de substance protectrice en réserve, combien d'hommes pour tenir à la main ce que la magie tient : je ne sais rien de tout cela aujourd'hui. Ce sont **mes réserves, et je ne les ai pas vérifiées.** J'écris donc les cases vides comme des créances et non comme des zéros — un zéro serait un mensonge, une case vide est une dette."
 ],
 "tables": [
  {
   "titre": "🔨 Les moyens de la fournaise à chaleur conduite (M01 à M11)",
   "colonnes": ["M", "Ce qu'il désigne", "📍 Où", "🪶 Qui en répond", "🪨 Tient sans magie ?", "⛓️ En existe-t-il un second ?", "📏 Mesuré ?"],
   "lignes": [
    {"cellules": ["**M01**", "La gemme de travaux auxiliaires, et le poste de distribution dont elle vient (R01)", "Les Fournaises ; poste de distribution", "O01", "Oui comme objet — mais elle s'épuise et ne se recharge pas seule", "**Inconnu de moi** : je ne sais pas combien de gemmes chargées sont au poste ce soir. C'est la première chose que j'irai compter.", "non"]},
    {"cellules": ["**M02**", "Les appuis, joints et supports de l'ouvrage (R02)", "Toute la structure de la fournaise", "O01, avec ⚒️ Matière", "**Oui** — et c'est pourquoi ils comptent : ce qu'un transfert dépose, ils le portent sans qu'on les alimente", "Un appui n'a pas de second : il a des voisins qui reprennent sa charge, et c'est autre chose", "non — aucune charge admissible chiffrée"]},
    {"cellules": ["**M05**", "Le foyer, son arrivée d'air, le collecteur et ses trois branches, pris ensemble", "Les Fournaises", "O03 au jour le jour — **charge vacante** ; O01 pour l'ouvrage", "Le foyer oui, c'est un feu ; les branches non — sans transfert elles ne portent rien", "**Non. Il n'y en a qu'un.** Tous les ateliers, et la branche défensive, pendent du même collecteur.", "non"]},
    {"cellules": ["**M06**", "Le capteur Mercure Chaud et son Barrer", "Sur le support qu'ils mesurent, au collecteur", "O01", "Non — et **le Barrer s'ouvre en l'absence de Trace**", "Pas à ma connaissance", "non — aucun seuil de calibration écrit"]},
    {"cellules": ["**M07**", "Le fil de Trace qui porte la mesure au Barrer", "Du capteur au Barrer", "O01", "Non — et **son silence ne se distingue pas d'un repos**", "Non : un seul fil, dont la rupture ouvre l'admission au lieu de la fermer", "non"]},
    {"cellules": ["**M08**", "Le dissipateur — le récepteur réel de ce dont les usages ne veulent pas", "Branche de dissipation", "O01", "**Oui** — c'est une pièce matérielle", "Non, et **sa capacité n'est pas infinie**. C'est la ligne la plus dangereuse de ce registre.", "non — sa saturation n'a jamais été atteinte ni écrite"]},
    {"cellules": ["**M09**", "L'écran thermique des traversées habitées (R06)", "Passages proches des habitations", "**O02 — charge vacante**, et l'écran appartient à la main qui l'a accordé", "Non — c'est une frontière tenue", "Non. Et je ne connais pas le nom de son récepteur réel, qui ne figure sur aucun de nos papiers.", "non"]},
    {"cellules": ["**M10**", "Les dalles d'approche", "Face extérieure, approche du rempart", "O01", "**Oui** — elles reçoivent, elles n'opèrent pas ; et elles restent chaudes après la fermeture", "Sans objet — c'est une surface, pas un organe", "non — le délai de retour au froid n'est pas connu"]},
    {"cellules": ["**M11**", "La cheminée, et la liaison qui l'y raccorde", "Les Fournaises", "O03 — **charge vacante**", "**Oui — et c'est la seule issue des fumées**", "Non, et celui-là ne se double pas d'un mot : c'est de la maçonnerie", "non"]}
   ]
  },
  {
   "titre": "🧠 Des codes cités par une école que nous n'avons pas (M40 à M45)",
   "colonnes": ["M", "Ce qu'il désigne", "⚖️ Ce qu'il en est chez nous"],
   "lignes": [
    {"cellules": ["**M40 · M43 · M44**", "Le don d'Esprit ; un second praticien disponible pendant l'opération ; la puissance donnée par un réseau", "**Rien.** Aucune main d'ici ne porte ce don. Ces codes sont cités par notre cahier et ne résolvent vers personne ; ils ne résoudront pas parce que j'aurai signé quelque chose."]},
    {"cellules": ["**M41**", "La mémoire d'une main — son vécu, qui décide de ce qu'elle peut atteindre", "**Non inscrit, et par refus écrit** (voir la quatrième page). Une vie n'a ni porte ni détenteur, et je n'entends pas lui en donner."]},
    {"cellules": ["**M42 · M45**", "Les relevés dessinés ; et le monde extérieur employé comme levier : objets, lieux, cloches, heures convenues", "**Ceux-là sont à notre portée**, et c'est la seule bonne nouvelle de cette table : ils ne demandent aucun don. Une maison sans mage les tient. Je les inscrirai le jour où quelqu'un ici en tiendra un — pas avant, sinon j'inscris une intention."]}
   ]
  },
  {
   "titre": "🕳️ Les créances de ce registre",
   "colonnes": ["Ce qui manque", "Pourquoi ça compte", "Ce qui le remplira"],
   "lignes": [
    {"cellules": ["Toutes les quantités : combustible, gemmes chargées au poste, substance protectrice en réserve, hommes disponibles pour une conduite à la main.", "Une affectation sans quantité est une préférence, pas une décision. Et je ne peux promettre un refuge sans savoir qui le nourrira.", "Une tournée de mes réserves, de mes propres yeux, et non un compte qu'on me rapporte."]},
    {"cellules": ["Le bord du dissipateur (M08).", "Trois des défaillances connues de cet ouvrage sont thermiques, et toutes finissent sur cette pièce.", "L'action 52120 : le saturer exprès, un jour choisi, hors menace — et ce jour-là c'est du combustible et un secteur d'ateliers privé de chaleur, donc c'est une dépense de la Maison."]},
    {"cellules": ["Le nom du récepteur réel de l'écran (M09), et le nom de la main qui l'a accordé.", "Sans ce nom, une frontière posée près des habitants n'a pas de répondant, et je ne peux pourvoir O02.", "L'action 52520 — mais elle veut un protecteur qui n'est pas moi, et je n'en ai pas encore un à nommer."]},
    {"cellules": ["Le second de M05, de M07 et de M11 — et il n'y en a pas.", "Un seul collecteur, un seul fil, une seule cheminée. **Mes refuges séparés parlent de relève et mon registre n'en montre aucune.** C'est l'écart entre ce que j'annonce et ce que je tiens.", "Rien d'écrit à ce jour. C'est mon travail, il n'est pas commencé, et je l'écris ici pour qu'on puisse me le compter."]}
   ]
  }
 ]
}

with io.open(p, 'w', encoding='utf-8') as f:
    json.dump(vol, f, ensure_ascii=False, indent=1)

op = base + '_ordre.json'
ordre = json.load(io.open(op, encoding='utf-8'))
if 'registre-des-moyens' not in ordre:
    i = ordre.index('registre-des-offices') + 1 if 'registre-des-offices' in ordre else 0
    ordre.insert(i, 'registre-des-moyens')
with io.open(op, 'w', encoding='utf-8') as f:
    json.dump(ordre, f, ensure_ascii=False, indent=2)

print('ecrit:', p)
print('ordre:', ordre)
