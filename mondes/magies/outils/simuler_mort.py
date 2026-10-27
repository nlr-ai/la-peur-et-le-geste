#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Moteur de simulation pour l'école de la Mort (Affaire 🎯 57000)
Maison du Bastion — Univers Magies

Modélise les 28 pratiques (⚔️ 57020 à ⚔️ 57047), les deux verrous (🔒 57001 et 🔒 57002),
les mécanismes signal/bruit, le risque de contamination cognitive et la création de Remontés.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
import json
import random

# Définition des 28 actions avec leur désignation officielle
ACTIONS_CATALOGUE = {
    "⚔️ 57020": {"nom": "La litanie", "clef": "🗝️ 57010", "moyens": ["🧰 M70"]},
    "⚔️ 57021": {"nom": "Le nom d'usage", "clef": "🗝️ 57010", "moyens": ["🧰 M70"]},
    "⚔️ 57022": {"nom": "Les appellations propres", "clef": "🗝️ 57010", "moyens": ["🧰 M70"]},
    "⚔️ 57023": {"nom": "La relique portée", "clef": "🗝️ 57011", "moyens": ["🧰 M71"]},
    "⚔️ 57024": {"nom": "La chose qu'il avait choisie", "clef": "🗝️ 57011", "moyens": ["🧰 M71"]},
    "⚔️ 57025": {"nom": "La purge des objets tiers", "clef": "🗝️ 57011", "moyens": ["🧰 M71"]},
    "⚔️ 57026": {"nom": "La séance au seuil", "clef": "🗝️ 57012", "moyens": ["🧰 M75"]},
    "⚔️ 57027": {"nom": "L'heure de son habitude", "clef": "🗝️ 57012", "moyens": ["🧰 M75"]},
    "⚔️ 57028": {"nom": "Le chemin refait", "clef": "🗝️ 57012", "moyens": ["🧰 M75"]},
    "⚔️ 57029": {"nom": "L'adresse liturgique", "clef": "🗝️ 57013", "moyens": ["🧰 M73"]},
    "⚔️ 57030": {"nom": "La chapelle usée", "clef": "🗝️ 57013", "moyens": ["🧰 M73"]},
    "⚔️ 57031": {"nom": "La coupe posée", "clef": "🗝️ 57014", "moyens": ["🧰 M72"]},
    "⚔️ 57032": {"nom": "Le choix de la matière", "clef": "🗝️ 57014", "moyens": ["🧰 M72"]},
    "⚔️ 57033": {"nom": "Le vase neuf", "clef": "🗝️ 57014", "moyens": ["🧰 M72"]},
    "⚔️ 57034": {"nom": "Le retournement", "clef": "🗝️ 57014", "moyens": ["🧰 M72"]},
    "⚔️ 57035": {"nom": "Le psaume d'ouverture", "clef": "🗝️ 57015", "moyens": ["🧰 M70", "🧰 M73"]},
    "⚔️ 57036": {"nom": "Une question à la fois", "clef": "🗝️ 57015", "moyens": ["🧰 M70"]},
    "⚔️ 57037": {"nom": "Le silence tenu", "clef": "🗝️ 57015", "moyens": ["🧰 M70"]},
    "⚔️ 57038": {"nom": "Le congé", "clef": "🗝️ 57015", "moyens": ["🧰 M70", "🧰 M73"]},
    "⚔️ 57039": {"nom": "La conduite sans vase", "clef": "🗝️ 57016", "moyens": ["🧰 M70"]},
    "⚔️ 57040": {"nom": "La consignation d'avant", "clef": "🗝️ 57016", "moyens": ["🧰 M72"]},
    "⚔️ 57041": {"nom": "Le second témoin", "clef": "🗝️ 57016", "moyens": ["🧰 M70"]},
    "⚔️ 57042": {"nom": "La consultation", "clef": "🗝️ 57017", "moyens": ["🧰 M71", "🧰 M74"]},
    "⚔️ 57043": {"nom": "Le vidage de la salle", "clef": "🗝️ 57017", "moyens": ["🧰 M74"]},
    "⚔️ 57044": {"nom": "Le silence du visiteur", "clef": "🗝️ 57017", "moyens": ["🧰 M74"]},
    "⚔️ 57045": {"nom": "L'enquête sur le mort", "clef": "🗝️ 57018", "moyens": ["🧰 M75"]},
    "⚔️ 57046": {"nom": "La fiche du mort", "clef": "🗝️ 57018", "moyens": ["🧰 M75"]},
    "⚔️ 57047": {"nom": "Le nom le plus propre", "clef": "🗝️ 57019", "moyens": ["🧰 M70"]},
}

@dataclass
class Defunt:
    """Représente le réseau mnésique d'une vie révolue."""
    nom_registre: str
    nom_usage: str
    nom_intime: str
    sedentarite_score: float  # 0.0 à 1.0 (sillon des habitudes)
    densite_objets: float     # 0.0 à 1.0 (qualité des reliques)
    attachement_seuil: bool   # Existence d'un pas de porte fréquenté 30 ans
    secrets_ou_actes: List[str] = field(default_factory=list)

@dataclass
class ConfigurationSeance:
    """Paramètres et actions engagées pour la séance."""
    actions_retenues: Set[str] = field(default_factory=set)
    matiere_vase: str = "métal"  # "eau", "métal", "sel"
    vase_neuf: bool = True
    vivants_parlent_dans_la_piece: bool = False
    paroles_des_vivants: List[str] = field(default_factory=list)
    questions_posees: List[str] = field(default_factory=list)

@dataclass
class ResultatSeance:
    """Indicateurs et journal calculés par la simulation."""
    reussite_cible_🎯57000: bool
    verrou_🔒57001_leve: bool  # La Venue
    verrou_🔒57002_leve: bool  # La Matérialisation
    signal_authentique: float  # 0.0 à 100.0 %
    bruit_homonymes: float     # 0.0 à 100.0 %
    auto_illusion_vivants: float  # 0.0 à 100.0 %
    contamination_mental: float   # 0.0 à 100.0 %
    risque_remonte_lieu: float    # 0.0 à 100.0 %
    journal_seance: List[str] = field(default_factory=list)
    verdict: str = ""

class SimulateurMort:
    """Moteur de calcul et d'exécution d'une séance."""

    def simuler(self, defunt: Defunt, config: ConfigurationSeance) -> ResultatSeance:
        journal = []
        actions = config.actions_retenues

        # 1. Vérification de la phase d'enquête amont (🗝️ 57018)
        enquete_faite = "⚔️ 57045" in actions
        fiche_faite = "⚔️ 57046" in actions
        if enquete_faite:
            journal.append("📋 [Enquête préalable ⚔️ 57045] Réalisée auprès des proches : le réseau du mort est cartographié.")
        if fiche_faite:
            journal.append("📜 [Fiche du mort ⚔️ 57046] Consignée au registre du conseil : les repères sont fixés pour les séances futures.")

        # Si consultation de Remonté (🗝️ 57017)
        if "⚔️ 57042" in actions:
            return self._simuler_consultation_remonte(defunt, config, journal)

        # 2. Résolution du Verrou 🔒 57001 : LA VENUE
        force_venue = 0.0
        facteur_bruit_venue = 50.0

        # Effet du nom invoqué
        if "⚔️ 57047" in actions and defunt.nom_intime:
            journal.append(f"🗣️ [Appellation ⚔️ 57047] Invocateur appelle par le nom le plus propre : « {defunt.nom_intime} ».")
            force_venue += 40.0
            facteur_bruit_venue = 5.0
        elif "⚔️ 57022" in actions:
            journal.append(f"🗣️ [Appellation ⚔️ 57022] Invocateur emploie les sobriquets et surnoms d'usage.")
            force_venue += 30.0
            facteur_bruit_venue = 15.0
        elif "⚔️ 57021" in actions:
            journal.append(f"🗣️ [Appellation ⚔️ 57021] Invocateur emploie le nom d'usage : « {defunt.nom_usage} ».")
            force_venue += 20.0
            facteur_bruit_venue = 30.0
        elif "⚔️ 57020" in actions:
            journal.append(f"🗣️ [Litanie ⚔️ 57020] Récitation brute du nom officiel : « {defunt.nom_registre} ».")
            force_venue += 15.0
            facteur_bruit_venue = 60.0
        else:
            journal.append("⚠️ Aucun appel nominal structuré : les mémoires ne sont pas mises en phase.")

        # Effet des reliques
        if "⚔️ 57024" in actions and defunt.densite_objets > 0.3:
            journal.append("💍 [Relique choisie ⚔️ 57024] L'objet personnel choisi et réparé par le mort est posé au centre.")
            force_venue += 45.0 * defunt.densite_objets
            facteur_bruit_venue *= 0.6
        elif "⚔️ 57023" in actions and defunt.densite_objets > 0.1:
            journal.append("🗝️ [Relique portée ⚔️ 57023] Un objet ordinaire du défunt est apporté dans la pièce.")
            force_venue += 30.0 * defunt.densite_objets
            facteur_bruit_venue *= 0.8

        if "⚔️ 57025" in actions:
            journal.append("🧹 [Purge ⚔️ 57025] Les objets tiers sont sortis de la salle : suppression des nœuds parasites.")
            facteur_bruit_venue *= 0.3

        # Effet du lieu
        if "⚔️ 57026" in actions and defunt.attachement_seuil:
            journal.append("🚪 [Séance au seuil ⚔️ 57026] La séance se tient sur le pas de porte familier du mort.")
            force_venue += 35.0 * defunt.sedentarite_score
            if "⚔️ 57027" in actions:
                journal.append("⏰ [Heure d'habitude ⚔️ 57027] Pratique à l'heure exacte de son passage quotidien (+15% résonance).")
                force_venue += 15.0
            if "⚔️ 57028" in actions:
                journal.append("🚶 [Chemin refait ⚔️ 57028] Son itinéraire habituel a été parcouru au préalable.")
                force_venue += 10.0

        # Appui liturgique
        if "⚔️ 57029" in actions:
            journal.append("🕯️ [Liturgie ⚔️ 57029] Appel ancré sur le nœud public de Némareth.")
            force_venue += 20.0

        risque_remonte = 0.0
        if "⚔️ 57030" in actions:
            journal.append("⛪ [Chapelle usée ⚔️ 57030] Rite tenu dans un lieu ancien où l'on récite depuis des siècles.")
            force_venue += 40.0
            risque_remonte += 35.0

        verrou_1_leve = force_venue >= 30.0
        if verrou_1_leve:
            journal.append(f"🔓 [Verrou 🔒 57001 LEVÉ] Les mémoires sont arrivées dans la pièce (Intensité de venue : {force_venue:.1f}/100).")
        else:
            journal.append(f"🔒 [Verrou 🔒 57001 BLOQUÉ] Trop peu de nœuds ralliés ({force_venue:.1f}/100) : la pièce reste vide.")

        # 3. Résolution du Verrou 🔒 57002 : LA MATÉRIALISATION / LA VOIX
        verrou_2_leve = False
        contamination_mental = 0.0

        conduite_sans_vase = "⚔️ 57039" in actions or "⚔️ 57031" not in actions
        coupe_posee = "⚔️ 57031" in actions and not ("⚔️ 57039" in actions)

        if coupe_posee:
            journal.append(f"🏺 [Coupe posée ⚔️ 57031] Récipient posé, ouverture vers le haut (Matière : {config.matiere_vase}).")
            verrou_2_leve = True
            if not config.vase_neuf or "⚔️ 57033" not in actions:
                journal.append("⚠️ [Vase ancien] Le récipient a déjà servi : rémanence de fragments antérieurs.")
                facteur_bruit_venue += 20.0
            else:
                journal.append("✨ [Vase neuf ⚔️ 57033] Récipient vierge : aucune rémanence.")

            if "⚔️ 57034" in actions:
                journal.append("🔄 [Retournement ⚔️ 57034] La coupe est retournée à la fin : dispersion des fragments résiduels.")
            else:
                journal.append("⚠️ [Coupe non retournée] Le lieu reste chaud : persistance de fragments dans la salle.")
                risque_remonte += 25.0

        elif conduite_sans_vase:
            journal.append("🧠 [Conduite sans vase ⚔️ 57039] Aucun récepteur matériel : l'opérateur PREND LA VOIX !")
            verrou_2_leve = True
            contamination_mental = 85.0
            if "⚔️ 57040" in actions:
                journal.append("✍️ [Consignation ⚔️ 57040] L'opérateur avait écrit ses connaissances : comparaison possible a posteriori.")
                contamination_mental -= 30.0
            if "⚔️ 57041" in actions:
                journal.append("👥 [Second témoin ⚔️ 57041] Un témoin note les paroles en direct pour l'opérateur.")
                contamination_mental -= 25.0

        # Protocole d'interlocution
        auto_illusion = 0.0
        if config.vivants_parlent_dans_la_piece and "⚔️ 57037" not in actions:
            journal.append("🗣️ [Bavardage des vivants] Des paroles sont prononcées pour aider : elles forment des nœuds frais immédiats !")
            auto_illusion = 65.0
        elif "⚔️ 57037" in actions:
            journal.append("🤫 [Silence tenu ⚔️ 57037] Règle du silence absolu : aucune suggestion n'alimente le rassemblement.")
            auto_illusion = 0.0

        if "⚔️ 57035" in actions:
            journal.append("📖 [Psaume ⚔️ 57035] Formule d'ouverture imposant une syntaxe d'interlocuteur.")
        else:
            journal.append("⚠️ Pas de formule d'ouverture : les réponses fusent sans structure.")

        if "⚔️ 57038" in actions:
            journal.append("🔔 [Congé ⚔️ 57038] Formule finale prononcée et clochette sonnée : clôture de phase.")
        else:
            journal.append("⚠️ Pas de congé officiel : le contact traîne et fatigue l'opérateur.")

        # 4. Calcul des pourcentages finaux
        if not verrou_1_leve or not verrou_2_leve:
            signal_auth = 0.0
            bruit = facteur_bruit_venue if verrou_1_leve else 0.0
            reussite = False
            verdict = "Échec de la séance : impossible d'extraire un fragment exploitable."
        else:
            ratio_signal = max(10.0, min(95.0, force_venue - facteur_bruit_venue - auto_illusion))
            bruit = min(100.0 - ratio_signal, facteur_bruit_venue)
            signal_auth = max(5.0, 100.0 - bruit - auto_illusion)

            reussite = signal_auth >= 45.0 and contamination_mental < 60.0
            if reussite:
                verdict = "Succès de l'état cible 🎯 57000 : un fragment authentique et exploitable a été recueilli."
            elif auto_illusion > 40.0:
                verdict = "Échec (Auto-illusion) : le mort a simplement répété ce que les vivants ont murmuré."
            elif contamination_mental >= 60.0:
                verdict = "Désastre cognitif : l'opérateur a absorbé les fragments et a perdu son propre discernement."
            else:
                verdict = "Incertain : le bruit des homonymes noie le message."

        # Questions/Réponses simulées
        if verrou_1_leve and verrou_2_leve:
            journal.append("\n--- DÉROULEMENT DU DIALOGUE ---")
            questions = config.questions_posees or ["Où est caché le registre ?", "Qui a signé le pacte ?"]
            for idx, q in enumerate(questions):
                journal.append(f"❓ Question {idx+1} : « {q} »")
                if "⚔️ 57036" in actions:
                    journal.append("🪨 [Caillou déposé ⚔️ 57036] Temps de pause respecté jusqu'à fin d'émission.")

                if auto_illusion > 45.0:
                    rep = f"« ...{config.paroles_des_vivants[0] if config.paroles_des_vivants else 'ce que vous venez de dire'}... » (Écho des vivants)"
                elif signal_auth > 50.0:
                    fragment = defunt.secrets_ou_actes[idx % len(defunt.secrets_ou_actes)] if defunt.secrets_ou_actes else "un atelier froid, l'odeur du suif et du chêne"
                    rep = f"« ...{fragment}... » (Authentique)"
                else:
                    rep = "« ...qui m'appelle... quel atelier... nous étions trois... » (Parasitage/Homonyme)"

                canal = "dans la coupe" if coupe_posee else "dans l'esprit de l'opérateur"
                journal.append(f"💬 Réponse perçue {canal} : {rep}")

        return ResultatSeance(
            reussite_cible_🎯57000=reussite,
            verrou_🔒57001_leve=verrou_1_leve,
            verrou_🔒57002_leve=verrou_2_leve,
            signal_authentique=round(signal_auth, 1),
            bruit_homonymes=round(bruit, 1),
            auto_illusion_vivants=round(auto_illusion, 1),
            contamination_mental=round(contamination_mental, 1),
            risque_remonte_lieu=round(risque_remonte, 1),
            journal_seance=journal,
            verdict=verdict
        )

    def _simuler_consultation_remonte(self, defunt: Defunt, config: ConfigurationSeance, journal: List[str]) -> ResultatSeance:
        journal.append("🧟 [Consultation Remonté ⚔️ 57042] Audience devant la créature. Le verrou 🔒 57002 est levé d'office.")
        relique_presente = "⚔️ 57023" in config.actions_retenues or "⚔️ 57024" in config.actions_retenues
        silence_visiteur = "⚔️ 57044" in config.actions_retenues
        salle_videe = "⚔️ 57043" in config.actions_retenues

        bruit = 10.0 if salle_videe else 40.0
        if not salle_videe:
            journal.append("⚠️ Salle encombrée d'objets d'autres consultants : interférence par d'autres mémoires.")

        auto_illusion = 0.0 if silence_visiteur else 70.0
        if not silence_visiteur:
            journal.append("🗣️ Le visiteur a parlé de son affaire devant la créature : elle lui renvoie son propre récit !")
        else:
            journal.append("🤫 [Silence du visiteur ⚔️ 57044] Le visiteur s'est tu : la créature ne peut pas tricher.")

        if relique_presente:
            journal.append("🗝️ Relique présentée à la créature : ancrage réussi sur le mort.")
            signal = max(10.0, 100.0 - bruit - auto_illusion)
            verrou_1 = True
            reussite = signal > 40.0
            verdict = "Consultation aboutie : le Remonté a articulé les mémoires de la relique." if reussite else "Le Remonté n'a fait que flatter le visiteur avec ses propres paroles."
        else:
            journal.append("❌ Aucune relique présentée : le Remonté bavarde dans le vide.")
            signal = 0.0
            verrou_1 = False
            reussite = False
            verdict = "Échec : sans relique, le Remonté n'a rien à quoi s'accrocher."

        return ResultatSeance(
            reussite_cible_🎯57000=reussite,
            verrou_🔒57001_leve=verrou_1,
            verrou_🔒57002_leve=True,
            signal_authentique=round(signal, 1),
            bruit_homonymes=round(bruit, 1),
            auto_illusion_vivants=round(auto_illusion, 1),
            contamination_mental=0.0,
            risque_remonte_lieu=0.0,
            journal_seance=journal,
            verdict=verdict
        )

# Archétypes préconfigurés pour démonstration
ARCHETYPES = {
    "charpentier": Defunt(
        nom_registre="Aldon Merin",
        nom_usage="Le père Aldon",
        nom_intime="Aldonnet",
        sedentarite_score=0.9,
        densite_objets=0.8,
        attachement_seuil=True,
        secrets_ou_actes=["La poutre maîtresse sous l'abside est fissurée", "J'ai caché dix pièces d'argent sous l'établi"]
    ),
    "messager": Defunt(
        nom_registre="Joran de Val-Brume",
        nom_usage="Joran le Rouge",
        nom_intime="Mon petit loup",
        sedentarite_score=0.15,
        densite_objets=0.2,
        attachement_seuil=False,
        secrets_ou_actes=["Le gué de Sombreval était inondé la veille"]
    )
}

if __name__ == "__main__":
    sim = SimulateurMort()
    defunt = ARCHETYPES["charpentier"]

    # Exemple 1 : Séance rigoureuse dans les règles de l'art
    config_expert = ConfigurationSeance(
        actions_retenues={
            "⚔️ 57045", "⚔️ 57046", "⚔️ 57047", "⚔️ 57024", "⚔️ 57025",
            "⚔️ 57031", "⚔️ 57032", "⚔️ 57033", "⚔️ 57034", "⚔️ 57035",
            "⚔️ 57036", "⚔️ 57037", "⚔️ 57038"
        },
        matiere_vase="métal",
        vase_neuf=True,
        vivants_parlent_dans_la_piece=False,
        questions_posees=["Où sont les dix pièces ?", "Où est le point faible du mur ?"]
    )

    res = sim.simuler(defunt, config_expert)
    print("=" * 60)
    print("SIMULATION EXPERTE (RÈGLE DU SILENCE ET COUPE NEUVE)")
    print("=" * 60)
    for l in res.journal_seance:
        print(l)
    print(f"\n📊 Signal authentique: {res.signal_authentique}% | Bruit: {res.bruit_homonymes}% | Illusion: {res.auto_illusion_vivants}%")
    print(f"🎯 Verdict: {res.verdict}")
