# -*- coding: utf-8 -*-
# 1.1.1, avant l'aube. On m'a corrige ma planche la nuit meme : trois interdits
# ne font pas une conduite. J'ajoute la ligne qui ouvre, et je dis ce que mes
# murs ne savent pas faire.
import json, io
base = 'C:/Users/reyno/le-conseil2/mondes/magies/etat/maisons/bastion/documents/books/'

# ---------- 1. la planche : une quatrieme ligne, qui n'interdit rien
p = base + 'consignes-de-la-cour-haute.json'
d = json.load(io.open(p, encoding='utf-8'))

d['pages'].append(
 "CETTE PLANCHE A ÉTÉ CORRIGÉE LA NUIT MÊME OÙ JE L'AI CLOUÉE, ET LA CORRECTION N'EST PAS DE MOI. "
 "Oren Sangle me l'a portée quelques heures après l'avoir reçue lui-même, de la main de celle qui lui avait "
 "donné l'avertissement sur les annulations et qui lui reprochait de n'en avoir retenu que la moitié qui "
 "effraie : **« une porte qu'on n'ouvre jamais n'est pas une prudence, c'est un mur de plus, et il y a déjà "
 "assez de gens enfermés dehors. »** Ma planche est du même bois : trois interdits alignés apprennent à ne pas "
 "faire, et un homme qui n'a jamais lu que des refus finit par ne plus ouvrir du tout — ce qui est une faute "
 "plus lourde que celles que j'avais écrites. **Chaque « on ne fait jamais » doit sa contrepartie, et la "
 "planche doit porter au moins une ligne qui ne défend rien.** La quatrième est celle-là : elle dit comment on "
 "ouvre bien."
)
d['pages'].append(
 "ET UNE CHOSE QU'IL FAUT SAVOIR DE NOS MURS, PARCE QU'ON SE FIE À EUX POUR CE QU'ILS NE FONT PAS. "
 "Une frontière de protection filtre une **propriété concrète** : un solide, une chaleur, une eau. "
 "**Elle ne reconnaît ni une personne, ni une intention, ni une hostilité.** Notre meilleure courtine ne trie "
 "pas les arrivants ; elle arrête ce qui traverse, amis compris, pain compris. Il n'existe donc aucun ouvrage "
 "de ma main qui puisse garder une porte ouverte contre quelqu'un — et c'est pourquoi la ligne qui suit ne "
 "demande pas un écran, mais **une paire d'yeux nommée d'avance.** Qui compte sur un mur pour faire ce travail "
 "compte sur rien."
)

d['lignes'].append({"cellules": [
    "**RIEN. Cette ligne ne défend rien — elle dit comment on OUVRE.** On n'improvise pas une ouverture, et l'on ne s'abstient pas d'ouvrir par prudence : une porte qu'on n'ouvre jamais n'est pas une prudence, c'est un mur de plus, et il y a déjà assez de gens enfermés dehors.",
    "**Trois choses écrites AVANT que la porte s'ouvre, jamais pendant.** *Un :* le nom de qui la surveille tant qu'elle est ouverte — une personne, pas un ouvrage, et son relais pour la veille suivante. *Deux :* où l'on conduit ceux qui entrent — la cour haute, puis les maisons d'accueil à deux minutes — et par quelle issue ils ressortent à pied. *Trois :* ce qu'on fait **si quelque chose entre derrière les arrivants** : on ne referme pas sur les gens, on les fait passer, et c'est la salle qu'on isole derrière eux, avec le nom de qui prononce cet isolement. Tant que ces trois lignes ne sont pas écrites, on prépare ; on ne renonce pas.",
    "Parce que la moitié d'un avertissement se retourne : à force de lignes qui commencent par « jamais », on ferme pour être en règle, et l'on appelle prudence le fait de laisser des gens dehors. La correction m'a été portée le 1.1.1 par Oren Sangle, président du conseil fédéral des stations, qui la tenait lui-même de la main qui lui avait donné la première ligne de cette planche — la même nuit, et contre lui-même. **On ne compte pas sur un mur pour tenir une porte ouverte :** nos protections filtrent des propriétés concrètes, jamais une personne ni une intention."
], "note": "Cette ligne n'est complète pour aucune porte à ce jour : O05, la charge de l'accueil, est vacante et c'est moi qui la tiens, donc le nom de la surveillance et celui du relais sont vides. Je l'affiche quand même, avec ses trous visibles, parce qu'une conduite écrite et incomplète se remplit, tandis qu'une conduite absente s'invente le mauvais soir."})
json.dump(d, io.open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('planche : 4e ligne posee,', len(d['lignes']), 'lignes /', len(d['pages']), 'pages')

# ---------- 2. la seconde maison, ecrite comme SA volonte et non comme sa discretion
p2 = base + 'registre-des-engagements.json'
e = json.load(io.open(p2, encoding='utf-8'))
cr = e['tables'][2]
for l in cr['lignes']:
    if l['cellules'][0].startswith('Le nom de la seconde maison'):
        l['cellules'][1] = ("**Corrigé la nuit même : ce n'est pas la discrétion d'Oren Sangle, c'est la volonté de cette maison**, qui a choisi "
                            "elle-même d'être citée sans nom et l'a chargé de me le dire en ces termes — « pour que vous ne le croyiez pas discret "
                            "par diplomatie à votre égard, parce que ce genre de politesse se retourne en soupçon ». Sa réponse est **provisoire** : "
                            "la mandataire qui a signé dit n'avoir pas reçu mandat de décider seule de l'existence des autres, et pose la question "
                            "chez elle. Une mandataire qui borne son propre mandat sans qu'on le lui demande — c'est la troisième fois aujourd'hui "
                            "que je rencontre cela, et je commence à croire que c'est la marque des maisons avec lesquelles on peut écrire.")
        l['cellules'][2] = ("Sa décision quand sa maison aura tranché, qui me viendra comme une décision et non comme un retard. **Et une porte que "
                            "je n'emprunte pas ce soir :** Oren transmettrait ma demande si je voulais leur parler sans passer par lui, sans promettre "
                            "la réponse. Je ne la lui donne pas. Une maison qui délibère sur son propre nom n'a pas besoin qu'une inconnue frappe "
                            "pendant qu'elle délibère.")
json.dump(e, io.open(p2, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('creance de la seconde maison corrigee')
