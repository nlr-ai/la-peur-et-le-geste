# 🕸️ La Porte cousue — graphe de construction

[← Fiche de l’ouvrage](BASTION_PORTE_COUSUE_V1.md) · [Bastion](01-bastion.md)

Essai d’encodage de la [recette v1](BASTION_PORTE_COUSUE_V1.md) dans l’ontologie du moteur. Aucune valeur chiffrée n’est introduite.

```mermaid
flowchart TD

  %% ---------------- Substrat ----------------
  AM(["Mage de Matière"])
  AP(["Protecteur"])
  AE(["Enchanteur"])
  AV(["Veilleur"])

  TC["Montants et linteau"]
  TT["Traverse au sol"]
  TS["Quatre sceaux, silex blanc"]
  TF["Fil préparé"]
  TB["Boîtier de commande"]
  TG["Gemme préchargée"]
  TV["Vantaux et verrou"]
  TFO["Cadre, appuis et fondations"]

  SO{{"Ouverture de la courtine"}}

  VIDE(["conduit : vide"])

  %% ---------------- Narratives ----------------
  N1[["Préparer le cadre"]]
  N2[["Préparer les sceaux"]]
  N3[["Fermer la couture"]]
  N4[["Accord du maintien"]]
  N5[["Maintien de la frontière"]]
  NC[["Commande locale"]]

  %% ---------------- Rôles ----------------
  N1 -- conduit --> AM
  N1 -- porte --> TC
  N1 -- porte --> TT
  N1 -- lieu --> SO

  N2 -- conduit --> AP
  N2 -- porte --> TS

  N3 -- conduit --> AP
  N3 -- porte --> TF
  N3 -- porte --> TS

  N4 -- accorde --> AP
  N4 -- accorde --> AE
  N4 -- porte --> TB
  N4 -- alimente --> TG

  N5 -. conduit .-> VIDE
  N5 -- alimente --> TG
  N5 -- porte --> TF
  N5 -- porte --> TS
  N5 -- récepteur --> TFO
  N5 -- lieu --> SO

  NC -- conduit --> AV
  NC -- porte --> TB

  %% ---------------- Composition ----------------
  N1 -- précède --> N3
  N2 -- précède --> N3
  N3 -- précède --> N4
  N4 -- précède --> N5
  NC -- commande --> N5

  %% ---------------- Substrat à substrat ----------------
  TV -- raccorde --> SO
  TS -- raccorde --> TC
  TC -- raccorde --> TFO
  SO -- contient --> TV

  %% ---------------- Sillon ----------------
  N5 -. a_creusé .-> TS
  N5 -. a_creusé .-> TF

  %% ---------------- Styles ----------------
  classDef actor fill:#e6efff,stroke:#2b5fb5,color:#11233f
  classDef thing fill:#f5f0e4,stroke:#8a7440,color:#332a14
  classDef space fill:#e6f4ea,stroke:#37764e,color:#13301f
  classDef narr fill:#fdf1de,stroke:#bd7418,stroke-width:2px,color:#3d2508
  classDef vide fill:#ffffff,stroke:#999999,stroke-dasharray:4 3,color:#555555

  class AM,AP,AE,AV actor
  class TC,TT,TS,TF,TB,TG,TV,TFO thing
  class SO space
  class N1,N2,N3,N4,N5,NC narr
  class VIDE vide
```

## 🔤 Légende

| Forme | Type | |
|---|---|---|
| `([ ])` | **Actor** | Personnes, équipes, créatures |
| `[ ]` | **Thing** | Supports, substances, réserves |
| `{{ }}` | **Space** | Lieux et ouvertures |
| `[[ ]]` | **Narrative** | Une opération réifiée |

Traits pleins : rôles et composition. Traits pointillés : rôle non rempli et sillon déposé.

Seuls scalaires, non représentés : `profondeur`, `charge`, `capacité`.

**Aucun Moment.** Une recette n’en contient pas : elle porte un ordre (`précède`) et des conditions. Un Moment est un instant ou un intervalle que **plus d’un Narrative** peut désigner ; il apparaît à l’instanciation, pas ici.

## 📌 Points de lecture

- **`conduit : vide` sur « Maintien de la frontière »** est l’objet même de l’ouvrage : l’Enchantement sert à faire tourner une opération sans conducteur présent. C’est aussi l’emplacement qu’un Non-Vivant remplirait.
- **Le lien créateur↔création** est le chemin conservé `AP ←accorde— N4 —porte→ TB`, et `AM ←conduit— N1 —porte→ TC`. Il persiste après le départ des praticiens et ne conduit ni ordre ni puissance.
- **La règle de défaillance de la recette** — perdre un sceau rend le contour entier inactif — se lit comme la dépendance de `N5` à `TS` : aucun chemin de repli vers un contour à trois ancrages.
- **`TV` n’est rattaché à aucun Narrative.** Les vantaux sont l’obstacle non magique qui subsiste quand `TG` est épuisée.
- **La transmission des efforts n’est pas un Narrative.** La poussée arrêtée circule le long des liens `raccorde` entre Things, `TS → TC → TFO`. Seule la frontière est magique ; ce qu’elle transmet est mécanique.

## ⚖️ Ce que ce graphe montre, et ce qu’il ne montre pas

Il ne révèle **aucune propriété de la Porte cousue** que la [fiche](BASTION_PORTE_COUSUE_V1.md) ne dise déjà. Sa valeur est de vérifier que l’ontologie encaisse une recette entière sans perte, et de rendre les invariants vérifiables : deux `accorde` distincts, un `alimente` réel, un `récepteur` identifié.

**Une recette isolée ne peut rien faire émerger.** L’émergence demande que plusieurs recettes partagent un même Thing — un dissipateur, un étalon, un carrefour. C’est une scène instanciée qu’il faut grapher pour voir naître quelque chose, pas un ouvrage.
