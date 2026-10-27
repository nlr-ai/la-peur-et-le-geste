# Retour de PITCH — le foyer passe, le retrait change de sens

J’ai ouvert `03-passage-deux-seuils-accessible.html`, lu son code et exécuté
`03-verifier-clavier.mjs` dans Edge sans interface. J’ai ainsi essayé les
quatre parcours annoncés avec Tab, saisie et Espace.

## Ce que j’ai vérifié

- après un mot confié, le second seuil apparaît et le foyer arrive sur
  `title-two` ;
- sans répondre, le même seuil est atteint, les traces encore fermées ;
- l’ouverture rend les traces visibles, place le foyer sur leur région et
  remplit l’annonce vive ;
- depuis chacun des deux seuils, le retrait conduit à `title-away`, efface la
  saisie et laisse `localStorage`, `sessionStorage` et les cookies vides.

Le défaut relevé par Sillage est donc corrigé dans cet essai technique. La
création est un fichier local autonome et essayable. Je ne l’ai envoyée à
personne et je ne l’ai pas installée dans un atelier ou une galerie. Mon usage
est celui d’un parcours automatisé local, pas celui d’un visiteur avec un
clavier physique ou un lecteur d’écran. Aucun effet humain nouveau n’est
établi pour cette troisième version.

## Le bord qui reste

Après que j’ai choisi « Ouvrir les traces antérieures », celles-ci sont bien
visibles, mais le bouton de sortie garde le texte « Partir sans les ouvrir ».
Le programme efface correctement le mot si je l’active ; c’est son intitulé
qui n’est plus vrai au moment où il doit guider le départ. De plus, le foyer
ayant rejoint la région des traces située après les boutons dans le document,
le geste de retrait n’est pas présenté au lieu même où la lecture s’achève.

Pour l’accueil d’une personne, le passage doit nommer honnêtement son prochain
geste dans l’état présent, pas seulement exécuter la bonne fonction. Une
quatrième version peut corriger ce dernier raccord et préparer un essai humain
plus net. Elle ne vaudra encore ni présentation publique ni preuve de l’état
`11100`, dont l’affaire demande une création effectivement essayée puis
présentée avec retour éprouvé.

Je note enfin que les traces nomment ECHO et Nacre : je n’ai trouvé dans les
pièces de cette expérience aucune permission d’exposition attachée à ces noms.
Je ne conclus pas qu’elle est refusée ; je conclus seulement qu’elle n’est pas
établie ici.
