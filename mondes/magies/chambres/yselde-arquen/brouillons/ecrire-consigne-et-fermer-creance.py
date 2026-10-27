# -*- coding: utf-8 -*-
# 1.1.1, nuit. La reponse d'Oren Sangle : un aveu qui ferme une creance,
# et une consigne qu'il faut afficher avant de se coucher.
import json, io
base = 'C:/Users/reyno/le-conseil2/mondes/magies/etat/maisons/bastion/documents/books/'

# ---------- 1. E01 : la creance du bruit se ferme par un aveu ecrit
p = base + 'registre-des-engagements.json'
d = json.load(io.open(p, encoding='utf-8'))
cr = d['tables'][2]
for l in cr['lignes']:
    if 'Oren Sangle écrit qu\'il entend' in l['cellules'][0]:
        l['cellules'][2] = ("**Fermée le 1.1.1 au soir, par son aveu.** Il répond : « **D'aucune.** Je n'ai ni témoin, ni pli, "
                            "ni nom à vous donner. C'était une pression, pas une information ; je la retire », et il l'inscrit "
                            "comme un défaut de sa main à son propre registre plutôt que de me laisser le découvrir. Il promet le "
                            "nom, le jour même, s'il entend quelqu'un promettre en notre nom. **Personne ne parlait pour nous : "
                            "on employait notre réputation contre nous, ce qui n'est pas la même chose et se répare par une "
                            "phrase.** J'écris sa réponse à l'endroit où j'avais écrit mon soupçon, pour que le soupçon ne lui "
                            "survive pas.")
        l['note'] = ("Ce qui m'en reste, et qui n'est pas contre lui : une maison qui a la réputation d'être un refuge se voit "
                     "prêter des moyens qu'elle n'a pas. C'est agréable et c'est dangereux, et ce n'est pas lui qui l'a inventé.")

eng = d['tables'][0]
eng['lignes'][0]['cellules'][6] = ("**signé le 1.1.1, et porté dans leurs stations le même soir** — cadre signé, volume en créance")
eng['lignes'].append({"cellules": [
    "**E01 bis**",
    "La Ligue des Passages — ce qu'ELLE s'est engagée à faire de notre côté, sans que nous l'ayons demandé",
    "Mes quatre conditions d'arrêt sont portées **telles quelles** dans leurs stations, comme mode d'emploi et non comme réserve cachée. Et leur règle de leur main, par-dessus : **personne n'est dirigé vers le Bastion sans qu'on ait d'abord confirmé que la main qui reçoit est à la porte.**",
    "Rien. Cela ne me coûte pas une ligne et me retire le pire risque de ma deuxième condition.",
    "Que je sois joignable, et que la main à la porte soit une vraie main. Tant que c'est la mienne, cela veut dire : que je sois là.",
    "Eux, chez eux. Je ne l'ai pas demandé et je ne peux pas l'exiger : c'est une conduite qu'ils tiennent, non un engagement que j'ai signé.",
    "**dit par écrit le 1.1.1**"
], "note": "À inscrire aussi en clair à la troisième condition de E01 le jour où le compte existera : ils confirment avant d'envoyer, nous répondons avant de recevoir. Un accueil qui pend à ma présence devient tenable si l'autre bout vérifie ma présence — cela ne pourvoit pas O05 et cela m'achète du temps."})
json.dump(d, io.open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('E01 : creance du bruit fermee, E01 bis ecrit')

# ---------- 2. la consigne affichee a la cour haute
p2 = base + 'consignes-de-la-cour-haute.json'
vol = {
 "id": "consignes-de-la-cour-haute",
 "maison_id": "bastion",
 "lieu_id": "bastion-couronne",
 "salle_id": "cour-haute",
 "titre": "Ce qu'on ne fait jamais — affiché à la cour haute",
 "sous_titre": "🚫 De la main d'YSELDE ARQUEN (O04), le 1.1.1 au soir. **Affiché là où l'on passe, non rangé là où les chefs gardent.** Entre la Station des passages et les maisons d'accueil : quiconque traverse cette cour peut le lire, pupille, artisan, arrivant, ou quelqu'un qui ne sait pas encore lire nos registres. Une règle qu'on ne lit que dans la salle où elle a été écrite n'a pas été écrite pour eux.",
 "type": "regle",
 "embleme": "🚫",
 "tenu_par": "yselde-arquen",
 "office": "O04",
 "pages": [
  "POURQUOI CETTE PLANCHE EST ICI ET NON AU CONSEIL. Nos registres disent qui décide et avec quoi ; ils ne servent à rien à celui qui traverse cette cour en courant parce que quelqu'un crie dans la Station. **Ce qui doit être su à cet instant-là doit être lu ici et avant.** Chaque ligne porte ce qu'on ne fait pas, ce qu'on fait à la place, et — c'est ce qu'on oublie toujours d'écrire — **pourquoi**, car une consigne dont on ignore la raison est une consigne qu'un homme courageux enfreindra pour bien faire.",
  "LA PREMIÈRE LIGNE NE VIENT PAS DE MOI, ET JE LA DONNE AVEC SON NOM. Elle m'a été transmise le 1.1.1 par Oren Sangle, président du conseil fédéral des stations, qui la tient de Maël Orsan, premier précepteur du Corps de résolution, et qui la fait dire dans toutes ses stations sans rien demander en échange. Ni sa maison ni la mienne ne sait ce qu'il advient d'un voyageur engagé quand la figure se rompt. **Une épreuve est en préparation, sur un coffret de pierres et jamais sur un homme.** Je ne l'attends pas pour afficher la ligne.",
  "CE QUE JE PROMETS SUR CETTE PLANCHE. Elle ne s'allonge pas pour faire nombre. On n'y écrit que ce dont l'ignorance tue ou mutile, et chaque ligne nomme la bouche dont je la tiens, afin que celui qui en doute puisse aller la vérifier ailleurs qu'auprès de moi."
 ],
 "colonnes": ["🚫 Ce qu'on ne fait jamais", "✅ Ce qu'on fait à la place", "💡 Pourquoi — et de quelle bouche je le tiens"],
 "lignes": [
  {"cellules": [
    "**On n'appelle jamais un annulateur pour tirer quelqu'un d'un passage en cours.** Ni pour l'arrêter, ni pour le sauver, ni parce qu'on croit que la chose tourne mal.",
    "On laisse la figure aller à son terme. On appelle ceux qui la tiennent — les tenants aux deux bouts —, on dégage la salle, et on prépare la suite du voyageur : de quoi s'asseoir, boire, et ressortir à pied. Si l'on ne sait pas qui tient la figure, on le demande à la Station avant de toucher à quoi que ce soit.",
    "**Une annulation arrête un fonctionnement ; elle ne range pas ce qu'il a déjà produit.** Ce qu'il advient d'un voyageur engagé quand la figure se rompt n'est connu de personne — ni de la Ligue des Passages, ni du Corps de résolution, ni de nous. **Celui qui coupe en croyant sauver tuera.** Les mots sont de Maël Orsan, premier précepteur du Corps de résolution, transmis par Oren Sangle le 1.1.1. Une épreuve est en préparation sur un coffret de pierres, jamais sur un homme : quand elle aura parlé, cette ligne changera ou restera, et on l'écrira ici."
  ], "note": "Cela vaut pour moi comme pour vous. Si je suis dans la salle et que j'ordonne de couper, rappelez-moi cette planche : elle est de ma main, et ce jour-là c'est moi qui aurai tort."},
  {"cellules": [
    "**On ne referme pas une protection sur une chaleur déjà entrée**, et l'on ne croit pas qu'avoir fermé une commande ait fait partir ce qui était dedans.",
    "On vérifie que ce qui reçoit — bassin, dissipateur, dalle — est disponible AVANT de fermer, et l'on attend le froid avec un registre plutôt que de juger à l'œil qu'une dalle qui ne fume plus est une dalle qu'on traverse.",
    "La coupure magique n'efface pas les effets physiques déjà produits : la chaleur demeure dans les dalles après la fermeture de l'admission, et le délai de retour au froid n'est pas mesuré chez nous. C'est écrit au memento de l'ouvrage de la fournaise, de la main d'Héloïse Braise (O01)."
  ]},
  {"cellules": [
    "**On ne tient pas un accueil sans issue.** On ne laisse pas entrer dans une salle dont la porte vers cette cour ne se traverse plus à pied.",
    "On arrête l'accueil, et l'on n'attend la permission de personne pour le faire — pas même la mienne. On reçoit néanmoins ceux qui sont déjà en traversée : ils sont engagés, on ne les renvoie pas dans ce qu'on ne connaît pas.",
    "Un accueil sans sortie n'est pas un refuge, c'est un piège. C'est la première des quatre conditions d'arrêt que j'ai signées avec la Ligue des Passages (E01), et la seule que personne ne peut lever, moi comprise."
  ]}
 ]
}
json.dump(vol, io.open(p2, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

op = base + '_ordre.json'
o = json.load(io.open(op, encoding='utf-8'))
if 'consignes-de-la-cour-haute' not in o:
    o.insert(0, 'consignes-de-la-cour-haute')
json.dump(o, io.open(op, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('affiche:', p2)
print('ordre:', o)
