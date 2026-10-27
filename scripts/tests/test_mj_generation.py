# -*- coding: utf-8 -*-
import os
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

from agents.expose import reveiller_main  # noqa: E402,F401 — ordre de la porte
from agents import mj, mj_generation  # noqa: E402


class RotationSessionMjTests(unittest.TestCase):
    def test_journee_partage_la_session_mais_pas_entre_mondes(self):
        routage = {"mj_commun_journee": True}
        with tempfile.TemporaryDirectory() as dossier:
            with mock.patch.object(mj, "ETAT", os.path.join(dossier, "monde-a", "etat")):
                a = mj.identifiant_de_session(mj.cle_session_routage("scene-a", routage))
                b = mj.identifiant_de_session(mj.cle_session_routage("scene-b", routage))
                normal = mj.identifiant_de_session(mj.cle_session_routage("scene-a"))
                self.assertEqual(a, b)
                self.assertNotEqual(a, normal)
            with mock.patch.object(mj, "ETAT", os.path.join(dossier, "monde-b", "etat")):
                self.assertNotEqual(a, mj.identifiant_de_session(mj.cle_session_routage("scene-a", routage)))

    def test_la_session_tourne_apres_n_tours_et_le_dit_une_fois(self):
        with tempfile.TemporaryDirectory() as dossier:
            etat = os.path.join(dossier, "etat")
            with mock.patch.object(mj, "ETAT", etat), \
                    mock.patch.dict(os.environ, {"LE_CONSEIL_MJ_TOURS": "3"}):
                historique = mj.identifiant_de_session("aurore")
                for _ in range(2):
                    self.assertFalse(mj_generation.compter_tour(etat, mj._base_de_session("aurore")))
                self.assertEqual(historique, mj.identifiant_de_session("aurore"))
                self.assertTrue(mj_generation.compter_tour(etat, mj._base_de_session("aurore")))
                nouvelle = mj.identifiant_de_session("aurore")
                self.assertNotEqual(historique, nouvelle)
                self.assertTrue(mj_generation.neuve(etat, mj._base_de_session("aurore")))
                mj_generation.compter_tour(etat, mj._base_de_session("aurore"))
                self.assertFalse(mj_generation.neuve(etat, mj._base_de_session("aurore")))
                # une autre scene garde sa propre session
                self.assertEqual(mj.identifiant_de_session("nicolas"),
                                 mj.identifiant_de_session("nicolas"))

    def test_zero_desactive_la_rotation(self):
        with tempfile.TemporaryDirectory() as dossier:
            etat = os.path.join(dossier, "etat")
            with mock.patch.dict(os.environ, {"LE_CONSEIL_MJ_TOURS": "0"}):
                for _ in range(50):
                    self.assertFalse(mj_generation.compter_tour(etat, "mj"))
            self.assertEqual(mj_generation.suffixe(etat, "mj"), "")


if __name__ == "__main__":
    unittest.main()
