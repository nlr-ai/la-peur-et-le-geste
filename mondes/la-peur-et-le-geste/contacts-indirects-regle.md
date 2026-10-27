# Contacts indirects dans Les gens

Projection de deux liens dirigés : intermédiaire → joueur et intermédiaire → cible.
Chaque confiance doit atteindre 40/100 ; leur produit divisé par 100 doit atteindre 25.
Les seuils se règlent dans manifeste.json, gens.contacts_indirects.

Les opinions courantes de etat/relations.json priment, converties par (opinion + 100) / 2. Sinon, les liens proviennent des exports datés sous sources/modern-front/contacts-freres et postes-niort, projetés dans contacts-indirects.json. Ces instantanés ne sont pas une lecture en direct de la simulation. Aucune valeur manquante n'est inventée.

Les contacts déjà directs ne sont pas dupliqués ; les morts sont exclus. Aucune expansion au troisième degré. Les petites cartes ne transmettent que l'identité et les critères d'accès, jamais les traits, intentions ou secrets. Une présentation reste à obtenir ; cette projection ne crée pas de rencontre ni de relation canonique. Les personnes non intégrées au monde gardent un identifiant sim-contact et une silhouette.

Vérification : test_contacts_indirects.js contrôle le sens des liens, la baisse de confiance sur chacun des deux liens, les doublons, la profondeur et la non-transmission des secrets.
