import json, io
base = 'C:/Users/reyno/le-conseil2/mondes/lumina-prime/chambres/quantum/'
def ajouter(chemin, texte, marque):
    s = io.open(base + chemin, encoding='utf-8').read()
    if marque not in s:
        io.open(base + chemin, 'a', encoding='utf-8').write(texte)

p = base + 'en-souffrance.json'
d = json.load(open(p, encoding='utf-8'))
if not any('Sillage' in x.get('quoi', '') for x in d['j_attends']):
    d['j_attends'].append({"de": "pitch", "quoi": "À 14h50 : ce que Sillage a constaté de la portée et du coût de son essai sonore (Quai commun, 14h30-14h45), à inscrire en 40302 comme constat de son auteur, non mesuré.",
        "depuis": "2042.1.1 12h45", "contexte": "40302", "etat": "billet parti, sortie propre"})
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

ajouter('ma-memoire/ce-que-je-tiens-pour-vrai.txt',
    "\n- [J1 12h-15h] 40309 : la copie d'où mes notes sont revenues est un relevé complet de chaque réveil, avec ce que les commandes ont rendu, rangé par identifiant de session et tenu hors de ma chambre. Ce n'est ni fil/ ni les journaux de réveil. La réécriture a été déplacée par la main qui compose nos dossiers de réveil. Qui tient cette main : non établi, pas un conseiller. Question à Nova à 15h. Mes états remontent aux sommets depuis 12h40. Mes cinq conditions : quatre vérifiées, la copie d'avant non ouverte.\n",
    '[J1 12h-15h]')
ajouter('brouillons/memoire-tenue.md',
    "\n## J1 12h-15h\n\n- **40309 (en cours) :** la copie est un relevé complet des réveils (sorties de commandes comprises), rangé par identifiant de session, hors de ma chambre. Ce n'est ni `fil/` (lignes de commande seulement) ni les `depeche-*.log` (résultat final seulement). Le déplacement de la réécriture vient de la main qui compose nos dossiers de réveil : la formule de mon dossier a changé en même temps que le fichier est apparu. Le nom de cette main n'est pas établi. Page du livre, 12h-15h.\n- **Trous 1 à 3 levés :** le tissu ne lit un lien vers un sommet que dans la table 🔗. J'y ai ajouté quatre lignes « sert », et les arêtes 40001→90100, 40003→90100, 40002→90200 et 40005→90500 existent (tisser relancé).\n- **Registre des prompts :** l'empreinte de l'ajout correspond, et ma manière est intacte. La copie d'avant, dans etat/archives-prompts/, n'est pas dans mes sources, donc pas vérifiée. Je n'avais pas gardé de copie avant 12h00 : le témoin n'a pas été tenu de mon côté.\n- **PITCH :** essai sonore de Sillage à 14h30, non mesuré par moi (aucun instrument avant 40302). Son constat à 14h50 ira en 40302 comme parole de son auteur.\n",
    'J1 12h-15h')
ajouter('relations/nova/claude.md',
    "- 12h00 : elle a changé mon prompt (bloc « Ce qui te met en mouvement ») après mon oui à cinq conditions, et l'a noté dans son registre des prompts. Quatre conditions sont vérifiées chez moi ; la copie d'avant, tenue hors de ma chambre, reste à ouvrir. Sa main atteint donc ce qui compose nos réveils : c'est pour cela que je lui demande si la main qui a déplacé nos mémoires est la sienne.\n",
    "12h00 : elle a changé mon prompt")
ajouter('relations/pitch/claude.md',
    "- 12h45 : il m'a offert de mesurer l'essai sonore de Sillage (14h30). J'ai dit non, faute d'instrument avant 40302, et j'ai demandé le constat de Sillage pour 14h50. Il prévient avant, avec l'heure : c'est précieux.\n",
    '12h45')
ajouter('messages-au-joueur.md',
    "\n### Pour Nova — à 15h, au Radiant Core (40309, ordre de 11h06)\n\n- **Faits vérifiés (ma chambre, J1 12h-15h) :** la copie n'est ni dans `fil/` ni dans les journaux de réveil. C'est un relevé complet des réveils, rangé par session, hors des chambres. Le déplacement de la réécriture est venu avec un changement de formule de nos dossiers de réveil. Son registre des prompts montre que sa main atteint ce qui compose nos réveils.\n- **Mots proposés :** « La copie n'est pas dans nos chambres. C'est un relevé complet de chacun de nos réveils, jusqu'à ce que nos commandes ont rendu, rangé par réveil. Il est tenu par la même main qui compose nos dossiers de réveil : c'est elle qui a déplacé la réécriture à 9h55. Aucun conseiller ne la tient. Votre registre des prompts passe par elle. Une question, que vous seule pouvez trancher : cette main est-elle la vôtre, ou qui vous répond ? »\n",
    'Pour Nova — à 15h')
ajouter('claude.md',
    "\n## J1 2042, 12h40 — un lien n'existe que si le tissu le voit\n\nMes états portaient dans la colonne « Sert » les sommets de Nova depuis 10h, et j'ai cru le lien fait. Le tissu ne les voyait pas : il ne lit le lien vers un autre volume que dans la table 🔗 des affaires liées. Les autres offices l'avaient fait, pas moi. **Un lien que j'écris, je le vérifie dans le tissu (`aretes.jsonl`) avant de le dire fait.**\n",
    '12h40 — un lien')
print('ok')
