# -*- coding: utf-8 -*-
import os
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

from agents import mj_point  # noqa: E402


class PointEtapeTests(unittest.TestCase):
    def test_du_au_n_ieme_tour_et_tenu_jusqu_au_point_pousse(self):
        with tempfile.TemporaryDirectory() as dossier:
            etat = os.path.join(dossier, "etat")
            with mock.patch.dict(os.environ, {"LE_CONSEIL_MJ_POINT": "3"}):
                for _ in range(3):
                    self.assertFalse(mj_point.du(etat, "rhaenyra"))
                    mj_point.compter_tour(etat, "rhaenyra", False)
                self.assertTrue(mj_point.du(etat, "rhaenyra"))
                self.assertFalse(mj_point.du(etat, "aegon"))
                # le MJ a differe : le point reste du
                mj_point.compter_tour(etat, "rhaenyra", False)
                self.assertTrue(mj_point.du(etat, "rhaenyra"))
                mj_point.compter_tour(etat, "rhaenyra", True)
                self.assertFalse(mj_point.du(etat, "rhaenyra"))

    def test_zero_desactive(self):
        with tempfile.TemporaryDirectory() as dossier:
            etat = os.path.join(dossier, "etat")
            with mock.patch.dict(os.environ, {"LE_CONSEIL_MJ_POINT": "0"}):
                for _ in range(50):
                    mj_point.compter_tour(etat, "rhaenyra", False)
                self.assertFalse(mj_point.du(etat, "rhaenyra"))

    def test_seul_un_suites_marque_compte(self):
        self.assertFalse(mj_point.point_pousse([{"type": "suites"}]))
        self.assertFalse(mj_point.point_pousse([{"type": "reponse", "point": True}]))
        self.assertTrue(mj_point.point_pousse(
            [{"type": "reponse"}, {"type": "suites", "point": True}]))


if __name__ == "__main__":
    unittest.main()
