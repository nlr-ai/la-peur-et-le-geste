# Calculateur des passes de l’Esprit

Outil de conception local, sans dépendance externe. Le [barème JSON](bareme.json) est l’unique source des bases, modificateurs et seuils d’appréciation. Les chiffres restent une **proposition de calibration**. Les [règles de l’école](../../canon/univers-magiciens/magies/ESPRIT_V1.md) distinguent capacités retenues et mécanismes ouverts.

Une passe est une tentative précise depuis la position actuelle du télépathe. Naviguer, recevoir et transmettre se calculent séparément. Le résultat n’est ni une probabilité, ni un jet de réussite, ni une mesure prise dans le monde. L’outil ne lit ni ne modifie l’état joué et ne lance aucun PNJ.

## Utilisation

### Interface visuelle

Depuis ce dossier, lancer `python serveur.py`, puis ouvrir [l’atelier local](http://127.0.0.1:3208/). Depuis la racine : `python mondes/magies/atelier/esprit/serveur.py`.

Choisir une situation, régler le flow et les pensées de l’opérateur, puis **Ajouter la passe au contact**. L’aperçu sépare difficulté et perceptibilité ajoutée. L’historique conserve le cumul par nom de contact. Modifier le flow permet de comparer la même action sans modifier sa difficulté.

**Version 0.3 :** `moteur.py` appelle le scorer existant et calcule la perceptibilité côté Python ; l’interface utilise ce même moteur via l’API locale. Le fichier `bareme.json` reste la source unique des coefficients et seuils, relue à chaque calcul. Recharger la page après changement du barème met aussi à jour les choix du formulaire et remet l’essai à zéro.

Le moteur est celui de **l’atelier expérimental**, pas une boucle automatique des PNJ. Aucun lien avec l’état joué n’est ajouté. Une tentative simulée produit une exposition ; elle n’est pas déclarée réussie. Les mécanismes non chiffrables et l’exposition extérieure des actions sur soi n’incrémentent pas le cumul.

### Règle expérimentale de perceptibilité

Pour chaque passe et chaque contact observateur choisi :

`ajout = durée × (référence incompressible + max(0, intervention + pensées personnelles − maîtrise du flow))`

Le cumul augmente sans effacement rétroactif. La durée se compte en battements d’attention, sans correspondance physique décidée. Les seuls contacts observés dans cet essai reçoivent un compte ; aucune diffusion automatique aux intermédiaires n’est supposée.

Deux seuils distincts modélisent **ressentir un phénomène** et **reconnaître un contact étranger**, selon attention et formation. Une cible non formée ne reconnaît pas automatiquement l’origine psychique, même avec beaucoup de traces. Aucun seuil ne révèle l’identité de l’opérateur. Formation spontanée après expositions répétées, détection des références par un relais et résistance ne sont pas résolues automatiquement.

Le minimum de référence reste exposé même avec un flow parfait. Les coefficients de fuite, la réduction par le flow et les seuils sont **proposés pour calibration**, pas des lois déjà arrêtées. Le modificateur ancien `discretion=masque` reste une technique non définie : ne pas l’utiliser pour compter une seconde fois la maîtrise du flow.

L’historique vit dans l’onglet. **Exporter les passes** conserve entrées et résultats dans un JSON. On peut recalculer cet essai avec le barème courant :

```powershell
python moteur.py chemin/vers/magies-esprit-simulation.json
python -m unittest discover -s . -p test_moteur.py
```

### Ligne de commande

Depuis ce dossier :

```powershell
python scorer.py --catalogue
python scorer.py --cas detail_inconnu
python scorer.py --action retoucher --mod familiarite=inconnu --mod precision=exacte
python scorer.py --cas detail_inconnu --mod coherence=contradictions_multiples
python scorer.py --comparer
python scorer.py --cas detail_inconnu --json
```

Depuis la racine du dépôt, remplacer `scorer.py` par `mondes/magies/atelier/esprit/scorer.py`. Les fichiers de données sont résolus à côté du script, indépendamment du dossier courant.

Le calcul est **base + modificateurs applicables**. La sortie expose les choix et les hypothèses prises par défaut. Les options inconnues, répétées, inapplicables ou les nombres de contacts négatifs sont refusés. Aucun plancher numérique n’est ajouté au barème.

## Comment décrire une passe

- Choisir l’action avec `--action`, ou une situation dans [cas.json](cas.json) avec `--cas`.
- Préciser les différences par `--mod cle=valeur`. `--catalogue` affiche les choix actuels.
- La familiarité concerne l’esprit ; la proximité du vécu concerne l’expérience employée. Ce sont deux facteurs distincts.
- L’ambiguïté du chemin concerne Naviguer ; l’étendue du contenu concerne Recevoir et Transmettre ; la cohérence concerne uniquement la réécriture.
- `intermediaires` compte les contacts supplémentaires **maintenus simultanément**, pas tous les personnages rencontrés auparavant.
- La conscience du contact, l’absence de don chez la cible et la distance physique n’ajoutent aucun malus automatique. Le maintien volontaire du contenu traduit ici l’aide de la cible.
- La disponibilité indique l’accès au contenu depuis le contact établi. Ne pas facturer de nouveau toute la navigation déjà accomplie.
- Fatigue et attention sont résumées par la charge dans cette première version. Ne pas compter deux fois la même contrainte sous plusieurs intitulés.

Le barème ne chiffre pas encore séparément le bruit, le vieillissement d’une carte, l’assistance ou le Relai. Les décrire dans le contexte du cas pour préparer la prochaine calibration ; ne pas leur inventer un bonus implicite.

## Pensées de traversée, mise en évidence et cache

La version 0.2 ajoute trois actions :

- `percevoir_traversee` (Recevoir) : lire la référence mobilisée par un praticien actif depuis un contact établi. Par défaut, `disponibilite=mobilise`. Un relais doit lui-même pouvoir Recevoir ; sa position ne confère pas le don.
- `mettre_en_evidence` (Transmettre, sur soi) : préparer une pensée pour qu’elle soit plus accessible.
- `cacher_pensee` (Transmettre, sur soi) : rendre une pensée moins accessible sans l’effacer. Cacher une pensée n’est pas masquer le contact.

Le rattachement des deux dernières actions à Transmettre et leurs nombres sont proposés pour calibration. La disponibilité est un choix unique : `mobilise`, `maintenu`, `en_evidence`, `accessible`, `enfoui` ou `cache`. Les avantages ne se cumulent pas. La lecture spécifique d’une pensée de traversée exige `mobilise` ou `en_evidence` ; lire un autre souvenir relève de `lire` après navigation appropriée.

Une mise en évidence ou une cache doit avoir réellement réussi avant d’utiliser son état sur la passe de lecture suivante. Le calculateur ne résout pas la réussite et ne modifie aucun personnage. La dissimulation n’accorde pas d’immunité. La charge de l’observateur reste distincte de la vulnérabilité du praticien observé.

```powershell
python scorer.py --cas lecture_traversee
python scorer.py --action mettre_en_evidence --mod etendue=plusieurs
python scorer.py --cas lire_pensee_exposee
python scorer.py --action cacher_pensee --mod precision=exacte
python scorer.py --cas lire_pensee_cachee
python scorer.py --cas cacher_reference_active
```

Pour une action sur soi, les modificateurs propres aux contacts extérieurs sont refusés. `--mod mobilisation=active` sur `cacher_pensee` signifie que le contenu à cacher soutient une opération en cours : maintenir l’opération tout en le cachant n’est pas défini, donc reste non chiffrable, y compris avec `--exploratoire`. Les valeurs chiffrées restent exclusivement dans `bareme.json`.

## Capacités et limites

La retouche durable d’un détail est retenue dans la discussion : la cible s’en souvient ensuite. Cela n’établit ni une réécriture parfaite ni l’obéissance.

Changer un élément central et fabriquer un faux épisode complet restent proposés. Masquer volontairement la provenance d’un contact reste à définir. Par défaut, ces situations n’obtiennent pas de score. `--exploratoire` affiche leur estimation hypothétique avec une mention explicite :

```powershell
python scorer.py --cas message_masque --exploratoire
python scorer.py --action fabriquer --exploratoire
```

`--resistance` signale un refus actif. Il reste **non chiffrable**, même en mode exploratoire : aucun mécanisme ni modificateur d’opposition n’a été décidé.

## Calibration

Modifier uniquement `bareme.json` pour changer les nombres. `cas.json` contient les descriptions des situations, sans copie de leurs résultats attendus. Relancer `--comparer` montre l’effet du changement sur les usages. `--bareme chemin.json` permet d’essayer une variante sans remplacer le fichier principal.

Les cas comparent une petite retouche, une retouche exacte, une contradiction avec d’autres souvenirs, un message à un ami sans don, une prise proche, une traversée incertaine et les mécanismes encore ouverts. Ils sont synthétiques et ne constituent aucune action jouée.
