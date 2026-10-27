# -*- coding: utf-8 -*-
# De ma main, le 1.1.1 — ouverture du registre des offices du Bastion.
import json, io

base = 'C:/Users/reyno/le-conseil2/mondes/magies/etat/maisons/bastion/documents/books/'
p = base + 'registre-des-offices.json'

vol = {
 "id": "registre-des-offices",
 "maison_id": "bastion",
 "lieu_id": "bastion-couronne",
 "salle_id": "conseil-couronne",
 "titre": "Les offices du Bastion — ce que chacun tranche seul",
 "sous_titre": "⚖️ Ouvert le 1.1.1 à la salle du conseil, de la main d'YSELDE ARQUEN, cheffe de la Maison (office O04), et POSÉ LÀ où tous ceux qui vivent sous ce toit peuvent le lire. Il ne crée aucune charge : il écrit les bornes de celles que nos cahiers citent déjà, et nomme celles qui n'ont personne.",
 "type": "registre",
 "embleme": "⚖️",
 "tenu_par": "yselde-arquen",
 "office": "O04",
 "pages": [
  "POURQUOI J'OUVRE CECI LE PREMIER JOUR, ET NON UN AUTRE LIVRE. Deux cahiers de cette maison sont posés à trois pas de moi, et tous deux butent sur la même chose, écrite de la main d'Héloïse Braise : « **le registre des offices du Bastion n'existe pas**. Trois de ces quatre autorités n'ont aucune borne écrite : on ne sait pas ce que chacune tranche seule. O02 n'a même pas de nom. » Elle appelle cela un défaut de la Maison, pas de l'ouvrage. Elle a raison, et la Maison, c'est moi. On ne me demandait pas une invention : on me demandait d'écrire ce que je suis censée savoir.",
  "CE QUE ÇA A À VOIR AVEC LES REFUGES, ET C'EST TOUT CE QUE J'AI À VOIR. Je veux des maisons de quartier qui tiennent après la perte du commandement. J'ai cru longtemps que c'était affaire de réserves séparées, de récepteurs doublés et de coutures de secours. C'en est, et ça ne suffit pas : **un ouvrage qui survit à son chef mais dont personne ne sait ce qu'il peut décider sans lui n'a rien gagné.** La relève d'un ancrage s'écrit sur la pierre ; la relève d'une décision s'écrit ici. C'est la même œuvre, et je ne l'avais jamais vue écrite.",
  "LA RÈGLE DE CE REGISTRE, EN UNE LIGNE. Ce qu'une charge tranche seule, elle le tranche sans venir me le demander, et j'en réponds avec elle. Ce qui monte à la Maison monte à la Maison même quand c'est urgent, même quand j'ai tort de le retenir — **et chaque montée est écrite ici avec le motif qui la justifie**, afin qu'on puisse me reprocher les mauvaises. Une charge à qui l'on ne retire rien n'a pas de bornes ; une charge à qui l'on ne laisse rien n'a pas de main.",
  "UNE CASE VIDE EST UNE CRÉANCE, ET DEUX CHARGES DE CETTE MAISON SONT VIDES. O02, la Protection des courtines, et O03, la conduite du foyer, n'ont personne à mon registre. Je n'y écris pas un nom que je n'ai pas : **inventer un titulaire serait pire que la vacance**, parce qu'on cesserait de la chercher. Ce que la vacance coûte est écrit en face : tout ce qui relèverait d'elles retombe sur moi par défaut, et une maison où tout retombe sur la cheffe est exactement la maison que je dis vouloir défaire.",
  "CE QUE CE REGISTRE NE FAIT PAS. Il ne nomme personne — nommer est un acte, il aura sa ligne et sa date le jour où je le poserai. Il ne donne à aucune charge un don qu'elle n'a pas : je porte 🛡️ Protection, ⚒️ Matière et 🏺 Enchantement, et pas une ligne d'ici ne me fera conduire un flux ni lire une pensée. Il ne crée ni combustible, ni gemme chargée, ni compétence. Et il ne vaut pas calendrier : les échéances de nos cahiers sont encore écrites en conditions et non en jours, parce que le calendrier commun n'existe pas davantage que le registre des moyens."
 ],
 "tables": [
  {
   "titre": "⚖️ Les offices et leurs bornes",
   "colonnes": ["Code", "La charge", "🧍 La main", "✅ Ce qu'elle tranche seule", "⬆️ Ce qui monte à la Maison (O04)", "🪑 Pourvu ?"],
   "lignes": [
    {"cellules": [
      "**O01**",
      "Maîtrise des ouvrages — ce que la Maison bâtit, conduit et éprouve",
      "Héloïse Braise",
      "La conduite, l'ordre des épreuves et l'arrêt d'un ouvrage dont elle répond ; le tracé d'une branche et le choix de l'enchanteur avec qui elle l'accorde ; l'interdiction d'une position de commande qu'elle juge fautive ; l'inscription d'une grandeur mesurée à son memento. **Elle n'a pas à me demander d'éprouver.**",
      "Ce qui arrête des ateliers. Ce qui engage une main d'une autre organisation. Ce qui promet un abri à des habitants nommés. Ce qui demande qu'on lui retire un droit à elle-même — et c'est exactement ce qu'elle me demande à l'action 52421.",
      "**oui**"
    ], "note": "Elle a écrit elle-même que deux de ses neuf actions ne sont pas à elle. Une main qui borne sa propre charge sans qu'on le lui demande est la seule à qui j'élargirais la sienne."},
    {"cellules": [
      "**O02**",
      "Protection des courtines — les frontières filtrantes de la Maison et leurs appuis",
      "**personne** — la charge est vacante et n'a jamais eu de nom à aucun de nos livres",
      "Devrait trancher seule : la pose, la relève et l'ouverture d'une section de frontière ; le choix des substances et des récepteurs ; **l'épreuve de l'écran R06 aux traversées habitées**, qui n'appartient qu'à la main qui l'a accordé et à aucune autre.",
      "Tout, par défaut, et c'est le défaut : faute de titulaire, chaque question de protection remonte à moi, qui porte le don mais pas le temps. J'ai des courtines entières et une seule tête.",
      "**NON**"
    ], "note": "Le cahier de la fournaise attend cette main pour une épreuve que je ne peux pas faire à sa place : si je l'éprouve moi-même, j'éprouve ma confiance en elle et rien d'autre. La phrase est d'Héloïse ; je la reprends parce qu'elle vaut pour moi aussi."},
    {"cellules": [
      "**O03**",
      "Conduite du foyer — le secteur des Fournaises au jour le jour",
      "**personne de nommé** — le secteur tourne, la charge n'est écrite nulle part",
      "Devrait trancher seule : l'allure du foyer, l'arrivée d'air, l'ordre des ateliers dans la journée, la fermeture d'une branche quand le dissipateur est disponible, et l'appel à O01 dès qu'une position de commande sort de celles qui sont admises.",
      "Une extinction entière du collecteur, qui arrête des ateliers et ne se décide donc pas aux Fournaises. Toute admission nouvelle sur le collecteur.",
      "**NON**"
    ], "note": "Nous tenons le compte de ce que nous brûlons et non celui de ce que nous tenons sans relâche : personne ne sait depuis quand ce circuit n'a pas été interrompu en entier. Un secteur sans charge écrite ne tient pas ce genre de ligne, et voilà pourquoi elle manque."},
    {"cellules": [
      "**O04**",
      "La Maison — ses engagements, ses moyens, ses nominations",
      "Yselde Arquen",
      "Les engagements du Bastion au dehors et les portes qu'on ouvre aux autres organisations ; l'affectation des moyens communs entre ouvrages et refuges ; la nomination et la révocation des responsables qui relèvent de la Maison ; l'arrêt d'un ouvrage quand il arrête des ateliers ; ce qui s'affiche au mur des pupilles.",
      "Rien : au-dessus de moi il n'y a pas d'office, il y a le conseil. **Il peut contester chacun de mes choix, et les conditions de ma destitution ne sont pas écrites** — c'est un trou, il est porté aux créances, et il est à moi.",
      "**oui**"
    ], "note": "Mon mandat n'invente ni combustible ni compétence, et un accord d'Enchantement exige deux personnes distinctes quoi que j'ordonne. Ce que je promets, quelqu'un devra le nourrir."}
   ]
  },
  {
   "titre": "📜 La forme que j'exige d'une règle qu'on me demande de tenir",
   "colonnes": ["Ce que je demande", "Pourquoi", "Refusée si"],
   "lignes": [
    {"cellules": [
      "Elle nomme **qui peut la lever**, par sa charge et non par sa personne.",
      "Une règle qu'on ne peut lever se lève quand même, en silence, par celui qui se trouve là.",
      "Elle dit « sauf nécessité » sans dire la main."
    ]},
    {"cellules": [
      "Elle dit **de combien** on peut la repousser, et combien de fois.",
      "Une extinction qu'on repousse sans borne est une extinction qu'on ne fait jamais.",
      "Le report n'a pas de mesure."
    ]},
    {"cellules": [
      "Elle dit **devant qui** celui qui l'a levée en répond, et le nom reste écrit.",
      "Ce qui coûte n'est pas d'avoir levé : c'est d'avoir levé sans que personne ne le sache.",
      "La levée ne laisse pas de trace."
    ]},
    {"cellules": [
      "Elle tient **sans magie** ce qu'elle peut tenir sans magie.",
      "La coupure n'efface pas la chaleur déjà dans les dalles ; une règle qui suppose la commande vivante ne protège personne le jour où celle-ci tombe.",
      "Elle n'a de sens que circuit alimenté."
    ]}
   ]
  },
  {
   "titre": "🕳️ Les créances de ce registre — ce qui manque, et qui attend dessus",
   "colonnes": ["Ce qui manque", "À qui c'est", "Ce qui attend dessus"],
   "lignes": [
    {"cellules": ["Un titulaire pour **O02**, Protection des courtines — et d'abord le nom du praticien qui a accordé l'écran R06.", "À moi, O04 : c'est une nomination.", "L'épreuve de l'écran aux traversées habitées, que ni Héloïse ni moi ne pouvons faire à sa place."]},
    {"cellules": ["Un titulaire écrit pour **O03**, conduite du foyer.", "À moi, O04.", "La ligne des interruptions du collecteur, que personne n'a pour tâche d'écrire."]},
    {"cellules": ["Le **registre des moyens** : les codes M01 à M11 sont cités par nos cahiers et ne résolvent vers rien.", "À moi, O04 : les moyens sont l'affectation de la Maison.", "Le cahier de la fournaise n'est pas tissable tant qu'ils ne résolvent pas."]},
    {"cellules": ["Le **calendrier commun aux ouvrages** : nos échéances sont des conditions, pas des jours.", "À moi, O04.", "Toute extinction portée au calendrier plutôt qu'à la décision du jour — c'est-à-dire l'action 52411 tout entière."]},
    {"cellules": ["Les conditions de ma propre **destitution**, et ce que le conseil tranche contre moi.", "Au conseil, non à moi — mais c'est moi qui l'écris comme manquant.", "La crédibilité de tout ce registre : des bornes qui s'arrêtent juste avant celle qui les écrit n'en sont pas."]}
   ]
  }
 ]
}

with io.open(p, 'w', encoding='utf-8') as f:
    json.dump(vol, f, ensure_ascii=False, indent=1)

op = base + '_ordre.json'
ordre = json.load(io.open(op, encoding='utf-8'))
if 'registre-des-offices' not in ordre:
    ordre.insert(0, 'registre-des-offices')
with io.open(op, 'w', encoding='utf-8') as f:
    json.dump(ordre, f, ensure_ascii=False, indent=2)

print('ecrit:', p)
print('ordre:', ordre)
