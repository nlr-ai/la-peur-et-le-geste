# Lyon 1943 — le manuel de ce monde

Ce fichier est la moitié « décor » du manuel du meneur. La doctrine — la Règle
Zéro, les boucles, le brouillard, la montre, l'interdiction des menus — vit à la
racine du dépôt et ne change pas. Ici, on ne dit que ce qui est vrai **de
celui-ci**. Le pitch d'origine : `docs/pitch-lyon-1943.md`. Les sources de la
chronologie : `docs/recherche-lyon-1943/`.

---

## Ce que c'est

Lyon, mars 1943. Les Allemands occupent la zone sud depuis le 11 novembre 1942.
La Gestapo de Lyon — la section IV du SD, que dirige Klaus Barbie — s'installe
dans la ville. La loi du 16 février 1943 appelle au Service du travail
obligatoire les jeunes gens nés en 1920, 1921 et 1922 ; le premier convoi part
de la gare des Brotteaux le dimanche 7 mars. Les trois grands mouvements de zone
sud — Combat, Libération-Sud, Franc-Tireur — se sont unis en janvier dans les
MUR. L'envoyé de De Gaulle qui les a unis, « Rex », est à Londres jusqu'à la
fin mars.

Le joueur est **Marcel Rivoire**, vingt et un ans, ouvrier typographe à
l'imprimerie Chabert, sur les pentes de la Croix-Rousse. Il vit chez ses
parents sur le plateau. Il est de la classe 1921.

**La partie s'ouvre le vendredi 5 mars 1943, vers dix-huit heures trente, à
l'imprimerie Chabert.** Le patron vient de poser sa feuille de route sur le
marbre, devant l'atelier : départ dimanche, gare des Brotteaux.

## Le but, et contre qui

- **Le but de Marcel**, en une phrase : *ne pas partir, puis devenir assez utile
  au groupe pour porter des plis de plus en plus haut — sans tomber, et sans
  faire tomber les autres.* Acte II : trouver qui a vendu le groupe.
- **Au-dehors** : Klaus Barbie, ses hommes et ses indicateurs — Jean Multon, qui
  ne viendra à Lyon que le 24 mai. La police de Vichy et la Milice, qui
  connaissent les visages du quartier.
- **Au-dedans** : Étienne Marchal, « Bastien », le recruteur. Il est sincère au
  départ. Sa tête porte l'horloge de sa chute : arrêté en mai, relâché, il
  donnera. Le joueur ne le sait pas, Marchal non plus avant que ça arrive.

## Le joueur sait la date de Caluire — et c'est assumé

Mêmes règles que Navarre :

1. **Marcel n'agit que sur ce qu'il peut justifier.** Un agent de liaison qui
   dit « on va arrêter Max à Caluire » sans source devient le suspect : on le
   met au vert, on coupe le contact, on se demande d'où il le sait. Ce qui porte,
   c'est ce qu'il a VU : un camarade relâché trop vite, une traction noire
   devant une boîte aux lettres, un rendez-vous où quelqu'un est arrivé trop tôt.
2. **Le canon dévie dès qu'il bouge.** Les têtes de Barbie, de Multon, de Moog
   et de Marchal portent des horloges et des déclencheurs. Un rendez-vous déplacé,
   un indicateur grillé, une boîte changée : Barbie attend autre chose ailleurs.
   Ne remets jamais le rail en place.
3. **Le cloisonnement protège le canon.** Marcel ne connaît pas Max, ni Didot, ni
   Vidal. Il lui faut des semaines de confiance pour approcher le niveau où
   Caluire se décide. Ne raccourcis pas ce chemin.

## Les horloges du canon

Dans `etat/evenements.json`, avec leurs conditions de déviation et leurs
sources. Ce qui dépend d'une **décision de Marcel** n'y est pas : partir ou non,
entrer dans le groupe, prendre une arme, dénoncer quelqu'un.

**Ce que le jeu ne tranche pas.** La culpabilité de René Hardy à Caluire n'est
pas établie : acquitté en 1947, puis à la minorité de faveur en 1950. Sa tête
porte une vérité privée ; on ne la présente jamais comme un fait historique, ni
au joueur, ni dans un récit, ni dans une annale.

## Ce qui est histoire, ce qui est inventé

- **Histoire** : Barbie, Moog, Multon, Moulin, les Aubrac, Hardy, leurs dates ;
  la loi STO, les convois des Brotteaux ; Montluc réquisitionnée le 17 février ;
  le Terminus puis l'avenue Berthelot ; la rafle de la rue Sainte-Catherine
  (9 février) ; les couvre-feux et les attentats datés dans
  `docs/recherche-lyon-1943/`.
- **Inventé, et déclaré** : Marcel Rivoire et sa famille, l'imprimerie Chabert,
  le groupe des pentes et tous ses membres (Marchal, Dutreuil, Merle, Le Gall,
  la veuve Thivolet), l'inspecteur Mazet, le milicien Bouvard ; le café du Gros
  Caillou et la cave de Merle ; les minutes de marche de `chemins.json` ; les
  plans, croyances et déclencheurs de toutes les têtes, canon comprises.
- **Probable, à tenir comme tel** : ce qui vient de la chronologie compilée en
  ligne et n'est pas recoupé (marqué `probable` dans les événements).

## Le point de vue du joueur

- Marcel sait tout ce qu'un ouvrier lyonnais de vingt et un ans sait : les rues,
  les traboules, les trams, le prix du pain au marché noir, qui dans l'atelier
  est pour le Maréchal, ce que dit Radio Londres le soir chez le voisin. Il
  connaît son métier à fond : composer, imposer, tirer, plier. Ne le fais jamais
  découvrir une évidence de sa vie.
- Il ne sait rien de la Résistance organisée : ni les mouvements, ni les
  pseudonymes, ni les règles. Il les apprend scène après scène, par des gens.
- Il ne sait rien de la Gestapo au-delà de la rumeur : des noms de lieux qui
  font peur, des gens qui n'en reviennent pas.

## Le brouillard de ce monde

- **Personne ne sait tout, et c'est voulu.** Le cloisonnement est la loi du
  groupe. Ce que Marcel apprend lui vient de son chef de groupe, de la rue, de
  la BBC, ou de ce qu'il imprime lui-même.
- **La presse ment, mais elle informe.** *Le Nouvelliste* et la presse autorisée
  donnent les ordonnances, les rations, le couvre-feu et les affiches. Ce
  qu'elles disent des « terroristes » est de la propagande.
- **Un silence est une nouvelle.** Quelqu'un qui ne vient pas au rendez-vous est
  peut-être arrêté. On ne le sait jamais sûrement avant longtemps.
- **Les distances tranchent.** Monter des Terreaux au plateau, c'est vingt
  minutes de pentes ; passer le Rhône, c'est passer un pont, donc un contrôle
  possible. Le couvre-feu ferme la ville.

## Les contraintes dures

1. **Marcel ne commande personne.** Il obéit à un chef de groupe qu'il ne
   choisit pas. Ce qu'il fait de son propre chef, il le fait contre la règle.
2. **Un réfractaire n'a plus d'existence légale.** Sans faux papiers, pas de
   carte d'alimentation, pas de travail déclaré, pas de logement à son nom. Ses
   parents seront interrogés.
3. **Une arrestation ne se rattrape pas par une scène.** Ce qui se passe avenue
   Berthelot ne se joue pas en action. Un homme pris est perdu pour le groupe,
   et le groupe doit déménager.
4. **La violence est de l'Histoire, pas un spectacle.** La torture, la
   déportation et la rafle de la rue Sainte-Catherine se jouent à hauteur de
   Marcel : la peur avant, le silence après, celui qui revient changé, celui qui
   ne revient pas. Jamais de scène d'interrogatoire en spectacle. La persécution
   des Juifs n'est jamais une mission ni un obstacle.
5. **Les personnes réelles.** On s'en tient à ce qui est établi sur Barbie,
   Moulin, les Aubrac, Hardy, Multon et Moog. Leurs répliques passent par leur
   dépêche, comme celles de tout le monde.

## Les valeurs locales du schéma

- `allegeance_affichee` / `allegeance_reelle` des maisons : `resistant` |
  `collaborateur` | `attentiste` au lieu de noir / vert / neutre.
- `jours_de_pr` de `lieux.json` se lit **jours de route depuis Lyon** (train ou
  route en 1943, contrôles compris).

## Lyon, ce que le plan connaît

Les salles sont dans `etat/chemins.json` (minutes de marche) :

- **Le plateau de la Croix-Rousse** — le logement des Rivoire, la place de la
  Croix-Rousse, le café du Gros Caillou.
- **Les pentes** — la montée de la Grande-Côte, l'imprimerie Chabert, la cour
  des Voraces, la cave de Merle.
- **La presqu'île** — la place des Terreaux, la rue Sainte-Catherine, la place
  Bellecour, la gare de Perrache et l'hôtel Terminus.
- **Le Vieux-Lyon** — la rue Saint-Jean et ses traboules, la chambre de la veuve
  Thivolet à Saint-Georges.
- **La rive gauche** — le pont Morand, la gare des Brotteaux, l'avenue
  Berthelot, la prison Montluc.
- **Caluire** — la place Castellane.
