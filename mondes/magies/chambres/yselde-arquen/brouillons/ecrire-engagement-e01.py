# -*- coding: utf-8 -*-
# De ma main, le 1.1.1 au soir — O05 ouverte, et le registre des engagements.
import json, io
base = 'C:/Users/reyno/le-conseil2/mondes/magies/etat/maisons/bastion/documents/books/'

# ---- 1. O05 : la charge de l'accueil, ouverte et vacante, au registre des offices
p = base + 'registre-des-offices.json'
d = json.load(io.open(p, encoding='utf-8'))
off = d['tables'][0]
if not any(l['cellules'][0].strip('*') == 'O05' for l in off['lignes']):
    off['lignes'].append({"cellules": [
        "**O05**",
        "L'accueil des arrivées — ce qui entre dans la ville par la Station des passages et par les portes",
        "**personne** — charge ouverte le 1.1.1 au soir, et **tenue par moi par défaut** jusqu'à nomination",
        "Devrait trancher seule, et à la porte : arrêter l'accueil quand la salle d'arrivée n'a plus de sortie franche, quand la main qui reçoit n'a pas de relève nommée pour la veille suivante, ou quand ce qui est entré ne peut plus s'asseoir, manger et ressortir. **L'arrêt se prononce avant une arrivée, jamais sur des gens en cours de traversée.**",
        "La reprise après un arrêt, qui n'appartient qu'à moi et se fait par écrit. L'ouverture d'une liaison, qui est un engagement au dehors et non un accueil. Toute promesse de chiffre.",
        "**NON**"
    ], "note": "Ouverte le soir où Oren Sangle, président du conseil fédéral des stations, m'a demandé par écrit trois lignes : qui reçoit, où exactement, à quelle condition l'accueil cesse. Je ne pouvais répondre à la première qu'en écrivant mon propre nom, faute de titulaire — et une maison où tout retombe sur la cheffe est celle que je dis vouloir défaire. La charge est donc écrite avant d'être pourvue, pour qu'on puisse me la retirer."})

d['tables'][2]['lignes'].append({"cellules": [
    "Un titulaire pour **O05**, l'accueil des arrivées — et une relève pour la veille suivante.",
    "À moi, O04 : c'est une nomination. Tant qu'elle n'est pas faite, l'accueil du Bastion s'arrête chaque fois que je quitte la porte, ce qui est exactement l'inverse d'un refuge qui tient sans commandement.",
    "L'accord d'accueil signé avec la Ligue des Passages le 1.1.1, dont la deuxième condition d'arrêt est ma propre absence."
]})
json.dump(d, io.open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('O05 portee au registre des offices')

# ---- 2. le registre des engagements de la Maison
p2 = base + 'registre-des-engagements.json'
vol = {
 "id": "registre-des-engagements",
 "maison_id": "bastion",
 "lieu_id": "bastion-couronne",
 "salle_id": "conseil-couronne",
 "titre": "Les engagements du Bastion au dehors — ce que nous avons promis, et à quelle condition cela cesse",
 "sous_titre": "🤝 Ouvert le 1.1.1 au soir, de la main d'YSELDE ARQUEN (O04), le jour même où l'on m'a demandé ma première signature. Une ligne par engagement : à qui, quoi, ce que cela coûte aujourd'hui, ce que cela coûtera, qui peut l'arrêter et devant qui il en répond. Ce qui n'est pas ici n'a pas été promis par la Maison.",
 "type": "regle",
 "embleme": "🤝",
 "tenu_par": "yselde-arquen",
 "office": "O04",
 "pages": [
  "POURQUOI CE TROISIÈME REGISTRE, LE MÊME JOUR QUE LES DEUX AUTRES. Les offices disent qui tranche, les moyens disent avec quoi. Il manquait ce que nous avons promis à des gens qui ne vivent pas sous ce toit — et c'est la seule des trois choses qu'on ne peut pas reconstituer après coup, parce qu'elle vit dans la mémoire de deux parties qui ne se souviennent jamais pareil. **Un engagement non écrit n'est pas un engagement modeste : c'est un engagement dont l'autre décidera seul de l'étendue.**",
  "CE QUI M'A FAIT L'OUVRIR CE SOIR. Oren Sangle, président du conseil fédéral des stations, m'a écrit pour une signature et non pour un service : trois lignes de ma main — qui reçoit, où exactement, et à quelle condition l'accueil cesse. Et il a ajouté la phrase qui m'a décidée : « un accueil dont la fin n'est pas écrite d'avance n'est pas un accueil généreux ; c'est un accueil qu'on retire au pire moment, parce que personne n'a convenu de ce qui était trop. » C'est, mot pour mot, la forme que j'ai exigée d'Héloïse Braise ce matin pour sa règle d'extinction. On me demande le soir la discipline que j'imposais à midi : je ne vais pas me faire prier.",
  "LA RÈGLE DE CE REGISTRE. Je signe volontiers un **cadre** ; je ne signe jamais un **nombre** que je n'ai pas compté. Un engagement dont le volume est écrit comme créance datée reste un engagement — il a une porte, un détenteur et une fin. Un engagement dont le volume est inventé pour faire bonne figure est un mensonge à retardement, et c'est toujours celui qui arrive qui le paie.",
  "CE QUE JE N'ENGAGE JAMAIS ICI. Les moyens d'un autre. Une équipe que je n'ai pas — une liaison d'Espace demande des gens capables de tenir une posture aux deux bouts, et le Bastion n'en déclare aucune à sa Station. Le don d'un praticien qui n'est pas de mon office. Et la mémoire ou le vécu de l'un des nôtres, qui n'entre pas à mon registre des moyens et n'entrera pas davantage dans un traité."
 ],
 "tables": [
  {
   "titre": "🤝 Les engagements en cours",
   "colonnes": ["N°", "Avec qui", "Ce que la Maison promet", "💰 Ce que cela coûte aujourd'hui", "⚠️ Ce que cela coûtera", "🛑 Qui l'arrête, et devant qui il en répond", "⏳ État"],
   "lignes": [
    {"cellules": [
     "**E01**",
     "La Ligue des Passages, par Oren Sangle, président du conseil fédéral des stations",
     "**Un accueil, non une liaison.** Trois lignes : *(1) Qui reçoit* — l'office O05, l'accueil des arrivées, ouvert ce jour et tenu par Yselde Arquen elle-même faute de titulaire. *(2) Où* — la **Station des passages de la ville haute**, et nulle part ailleurs ; elle donne sur la cour haute à trois minutes de marche, et les **maisons d'accueil sont sur cette même cour**, à deux minutes de sa porte. *(3) À quelle condition cela cesse* — les quatre conditions de la table suivante.",
     "**Rien** : ni un homme, ni une pierre, ni une gemme. Une signature et une charge écrite.",
     "Ce que je ne sais pas encore : mes réserves ne sont pas vérifiées. **Le compte d'accueil est une case vide, donc une créance, jamais une permission.** Je l'écrirai ici après ma tournée, et pas avant.",
     "L'office O05 à la porte — aujourd'hui moi. La **reprise** après un arrêt n'appartient qu'à moi, par écrit, et j'en réponds devant le conseil du Bastion.",
     "**signé le 1.1.1** — cadre signé, volume en créance"
    ], "note": "Ce qu'il ne m'a pas demandé et que je n'ai pas promis : hommes, réserves, priorité sur nos ouvrages, et l'équipe d'Espace qu'il faudrait à notre bout. Il l'a dit avant que j'aie à le refuser ; je le note pour qu'on se souvienne qu'il l'a dit."}
   ]
  },
  {
   "titre": "🛑 Les quatre conditions d'arrêt de E01 — écrites d'avance, et constatables à l'œil",
   "colonnes": ["", "La condition", "Ce qu'on regarde pour la constater", "Qui peut la lever"],
   "lignes": [
    {"cellules": ["**1**", "**La sortie franche.** L'accueil cesse quand la salle d'arrivée n'a plus d'issue matérielle praticable à pied pour ceux qui y sont déjà.", "La porte de la Station vers la cour haute : on la traverse à pied, sans magie, sans permission. Si elle ne se traverse pas, l'accueil est clos, quoi qu'il en coûte au dehors.", "Personne. Celle-là ne se lève pas : un accueil sans sortie n'est pas un refuge, c'est un piège, et je n'en signerai pas un."]},
    {"cellules": ["**2**", "**La relève nommée.** L'accueil cesse quand la main qui reçoit n'a pas de relève nommée pour la veille suivante.", "Le nom de la veille suivante, écrit. Aujourd'hui il n'y en a aucun : **l'accueil du Bastion s'arrête donc chaque fois que je quitte la porte**, et c'est écrit ici pour que la honte en soit publique et brève.", "Moi, en pourvoyant O05 — c'est-à-dire en cessant d'être la seule main. C'est la créance que ce registre me met sur le dos."]},
    {"cellules": ["**3**", "**Le compte.** L'accueil cesse quand ce qui est entré ne peut plus s'asseoir, manger et ressortir.", "Ce que la main à la porte voit dans la salle et aux maisons d'accueil de la même cour. Le chiffre n'existe pas encore et je n'en invente pas : jusqu'à ma tournée, la mesure est ce que l'œil constate, une veille à la fois.", "Moi, par écrit, et seulement après avoir écrit le chiffre à ce registre. Une reprise sans chiffre écrit est une faute de ma main."]},
    {"cellules": ["**4**", "**L'arrêt se prononce avant une arrivée, jamais pendant.** Ce qui est en cours de traversée est reçu, même si l'arrêt est décidé dans la minute.", "L'heure de l'arrêt et l'heure de l'arrivée, notées toutes deux à la porte.", "Personne, et celle-là est pour eux et non pour moi : c'est le débordement borné que j'accepte de payer pour qu'un accord signé vaille mieux qu'une promesse verbale."]}
   ]
  },
  {
   "titre": "🕳️ Les créances de ce registre",
   "colonnes": ["Ce qui manque", "Pourquoi ça compte", "Ce qui le remplira"],
   "lignes": [
    {"cellules": ["Le compte d'accueil de E01 : combien d'âmes la Station et les maisons de la cour haute tiennent sans toucher une réserve non vérifiée.", "Sans lui, la troisième condition d'arrêt dépend d'un œil et non d'une règle — donc de ma présence, donc du commandement.", "Ma tournée des réserves, de mes propres yeux, portée d'abord au registre des moyens puis ici."]},
    {"cellules": ["Un titulaire pour O05, et une relève pour la veille suivante.", "La deuxième condition d'arrêt de E01 est ma propre absence. C'est intenable et c'est écrit.", "Une nomination de ma main, qui est mon office et que rien ne bloque sinon que je n'ai personne à nommer."]},
    {"cellules": ["Ce qui se dit de nous au dehors : Oren Sangle écrit qu'il entend que cette ville se prépare à recevoir plus de monde qu'elle n'en a jamais logé.", "Je ne sais pas de quelle bouche il le tient, et c'est une chose qu'on dit de ma maison sans moi. Un engagement se négocie mal quand l'autre sait de vous ce que vous ne savez pas qu'il sait.", "Le lui demander — je l'ai fait le soir même. Sa réponse, ou son silence, ira ici."]}
   ]
  }
 ]
}
json.dump(vol, io.open(p2, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

op = base + '_ordre.json'
o = json.load(io.open(op, encoding='utf-8'))
if 'registre-des-engagements' not in o:
    i = o.index('registre-des-moyens') + 1 if 'registre-des-moyens' in o else 0
    o.insert(i, 'registre-des-engagements')
json.dump(o, io.open(op, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('ecrit:', p2)
print('ordre:', o)
