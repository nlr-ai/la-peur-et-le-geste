"""Un billet déclenche une discussion ciblée, pas une nouvelle journée."""
import sys
import importlib
import unittest
from pathlib import Path
from unittest import mock
sys.path[:0] = [str(Path(__file__).resolve().parents[1]),
               str(Path(__file__).resolve().parents[1] / "noyau")]
from agents import expose
from agents import billet
from agents.depeche import brief, manuel
mission = importlib.import_module("agents.depeche.mission")

class BilletDiscussionTests(unittest.TestCase):
    def test_cast_transmet_le_mode_et_la_provenance(self):
        with mock.patch.object(billet, "date_du_monde", return_value=(2001, 10, 10)), \
                mock.patch.object(brief, "identifiant_de_session", return_value="session"), \
                mock.patch.object(brief, "brief_de", return_value="brief"), \
                mock.patch.object(brief, "dossier_journee", return_value={}), \
                mock.patch.object(manuel, "manuel_de", return_value="manuel") as systeme, \
                mock.patch.object(mission, "mission", return_value="mission") as texte, \
                mock.patch.object(mission, "appeler", return_value={"cast": True}) as appel, \
                mock.patch.object(billet.chambre, "marquer_lu"):
            billet._reveiller("courtier", de="malek", ref="origine")
        self.assertEqual(systeme.call_args.kwargs["mode"], "discussion")
        self.assertEqual(texte.call_args.kwargs["billet_de"], "malek")
        self.assertIn("une seule fois", texte.call_args.args[2])
        self.assertEqual(appel.call_args.kwargs["mode"], "discussion")
        self.assertEqual(appel.call_args.kwargs["ref"], "origine")

if __name__ == "__main__":
    unittest.main()
