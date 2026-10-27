# -*- coding: utf-8 -*-
import os
import sys
import unittest

SCRIPTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

from agents.expose import reveiller_main  # noqa: E402,F401 — ordre de la porte
from agents import mj  # noqa: E402
from agents.sections_mode import filtrer  # noqa: E402
from unittest import mock  # noqa: E402


def _spectacle_mj():
    with open(mj.MJ_SPECTACLE_MD, encoding="utf-8") as f:
        return f.read()


TEXTE = """# Manuel
tronc
<!-- modes: run -->
## Laisser faire
corps run
### detail run
<!-- modes: meta -->
## Coulisses
corps meta
## Ton
toujours
<!-- modes: jump, run -->
### Jump
corps jump"""


class SectionsModeTests(unittest.TestCase):
    def test_sans_mode_seul_le_tronc_reste(self):
        sortie = filtrer(TEXTE, [])
        for present in ("tronc", "## Ton", "toujours"):
            self.assertIn(present, sortie)
        for absent in ("corps run", "detail run", "corps meta", "corps jump",
                       "<!--"):
            self.assertNotIn(absent, sortie)

    def test_la_marque_suivante_appartient_a_la_section_suivante(self):
        # Garder « Laisser faire » ne doit pas avaler la marque de Coulisses.
        sortie = filtrer(TEXTE, ["run"])
        self.assertIn("detail run", sortie)
        self.assertIn("corps jump", sortie)
        self.assertNotIn("corps meta", sortie)

    def test_plusieurs_modes_sur_une_marque(self):
        self.assertIn("corps jump", filtrer(TEXTE, ["jump"]))
        self.assertNotIn("corps run", filtrer(TEXTE, ["jump"]))


class ReveilRunTests(unittest.TestCase):
    def test_message_run_porte_le_mode_et_le_systeme_sa_garde(self):
        with mock.patch.object(mj, "date_du_monde",
                               return_value=(129, 4, 4)):
            message = mj._message(
                "rhaenyra", "je viens d'agir", "JOUEUR", modes=["run"])
        self.assertIn("MODES DU TOUR : run", message)
        self.assertNotIn("RUN ACTIF", message)

        avec = filtrer(_spectacle_mj(), ["run"])
        sans = filtrer(_spectacle_mj(), ["dire"])
        self.assertIn("Quand le mode `run` est actif", avec)
        self.assertIn("il n'est jamais requis", avec)
        self.assertIn("Le garde mécanique porte sur le contenu, jamais sur `suites`",
                      avec)
        self.assertNotIn("Quand le mode `run` est actif", sans)
        self.assertNotIn("« Laisser faire » — le MJ tient", sans)
        self.assertNotIn("Le dernier item d'un « laisser faire » est un", avec)


if __name__ == "__main__":
    unittest.main()
