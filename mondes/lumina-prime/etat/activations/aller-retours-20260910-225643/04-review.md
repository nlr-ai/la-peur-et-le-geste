# Retour de PITCH — essai du gabarit exact 2.1

## Ce que j’ai réellement ouvert et essayé

J’ai ouvert la présentation, le gabarit vierge, les deux SVG remplis et les deux aperçus PNG. J’ai relu le XML des trois SVG : ils sont bien formés et déclarent tous un A3 paysage de 420 × 297 mm avec une vue de 420 × 297.

Sur les aperçus, les valeurs occupent les champs existants du gabarit. Je ne vois pas de chevauchement qui empêche la lecture. Sur la feuille 2 prise seule, je retrouve sans explication orale : l’origine S0, « feuille 2 sur 2 », le raccord au point 4, le total de 11 pas, le repère V1, puis le point 5 à 14 pas et l’état NON OBSERVÉ. Le raccord demandé fonctionne donc dans cette maquette numérique.

J’ai aussi essayé un rendu neuf à 1680 × 1188 avec CairoSVG, puis copié la feuille 2 seule dans un autre dossier. Les deux SVG remplis appellent le gabarit par le lien relatif `13000-fiche-points-ecoute-v2.1.svg`. Dans mon rendu neuf, ce fond SVG externe n’a pas été composé, même lorsque le fichier voisin était présent : seules les valeurs ajoutées restaient. Dans le dossier isolé, la cible du lien était en plus absente. Ce test ne contredit pas les aperçus PNG fournis, que j’ai bien pu lire ; il établit que les SVG remplis ne sont pas des feuilles autonomes et que leur rendu complet dépend du voisinage des fichiers et du lecteur employé.

## Mon jugement depuis l’accueil et les usages

Mica a accompli la correction demandée au tour précédent. Elle a rempli deux copies aux dimensions et à la structure exactes du gabarit A3, sans recomposer une fiche A4, et la seconde conserve assez de repères pour reprendre la suite. C’est une création numérique réelle et une utilisation fictive effective du gabarit. La suite `ENTENDU → NON ENTENDU → ENTENDU → SEUIL INCERTAIN`, puis `NON OBSERVÉ`, reste clairement annoncée comme fictive ; elle ne fabrique aucun relevé du Quai.

Pour qu’un habitant ou un accompagnateur puisse recevoir une feuille remplie, il faut cependant savoir ce qu’on lui remet. Aujourd’hui, le PNG est autonome pour la lecture, mais il n’est pas le gabarit structuré ; le SVG conserve la structure et le texte, mais dépend d’un fichier externe et d’un lecteur qui sait le composer. Envoyer le SVG rempli seul peut donc retirer silencieusement tout le formulaire. Cette limite est maintenant éprouvée, pas supposée.

Je n’ai testé ni impression à taille réelle, ni écriture manuscrite, ni fabrication, ni découpe, ni pose, ni stabilité, ni relevé sonore. Je n’établis aucun accès au Quai ni droit de pose. L’objet a franchi une étape numérique utile ; son usage matériel et son utilité en situation restent ouverts.

## Prochain geste utile

Rendre une seule feuille remplie réellement transmissible : produire une variante autonome de la feuille 2, sans lien externe nécessaire, puis l’ouvrir depuis un dossier où le gabarit voisin n’existe pas. C’est le plus petit essai qui départage une feuille partageable d’un montage seulement lisible dans son dossier de fabrication.
