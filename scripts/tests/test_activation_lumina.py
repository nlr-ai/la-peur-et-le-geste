import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agents import expose
from agents.activation.taches import mettre_a_jour_energie_graphe, amorcer_sources_energie


def test_attente_recharge_sans_avancer_la_fiction():
    etat = {}
    noeuds = {'pers:a': {'genre': 'personne'}}
    horloge = {'present_secondes': 0, 'energie_mur_s': 1000}
    with patch('agents.activation.taches.appliquer_polarites_horloge', side_effect=lambda c, *_: c):
        mettre_a_jour_energie_graphe(etat, horloge, {'pers:a': 0}, noeuds, {}, {}, front='lumina-prime')
        horloge['energie_mur_s'] += 300
        energie = mettre_a_jour_energie_graphe(etat, horloge, {'pers:a': 1}, noeuds, {}, {}, front='lumina-prime')
    assert energie['pers:a'] == 50
    assert horloge['present_secondes'] == 0


def test_impulsion_unique_meme_apres_depense():
    etat, energies = {}, {'pers:a': 0}
    amorcer_sources_energie(etat, energies, ['a'], 'lumina-prime', 0, minimum=100)
    assert energies['pers:a'] == 100
    energies['pers:a'] = 2
    amorcer_sources_energie(etat, energies, ['a'], 'lumina-prime', 0, minimum=100)
    assert energies['pers:a'] == 2
