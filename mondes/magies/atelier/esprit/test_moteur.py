"""Contrats de simulation : cumul, flow, perception, limites et isolation."""
import unittest
from moteur import simuler
from scorer import lire, ICI


class Perceptibilite(unittest.TestCase):
    def setUp(self):
        self.b = lire(ICI / "bareme.json")
        self.p = {"action": "retoucher", "contact": "A", "flow": 0,
                  "pensees": "commentaires", "modificateurs": {
                      "familiarite": "inconnu", "precision": "exacte"}}

    def test_flow_ne_change_pas_la_difficulte_et_nefface_pas_le_passe(self):
        calme = dict(self.p, flow=4, pensees="dans_le_flow")
        r = simuler(self.b, [self.p, calme])
        self.assertEqual([p["difficulte"] for p in r["passes"]], [14, 14])
        self.assertEqual([p["perceptibilite"]["ajout"] for p in r["passes"]], [7, 1])
        self.assertEqual(r["contacts"]["A"]["cumul"], 8)

    def test_contacts_independants_et_reference_incompressible(self):
        calme = dict(self.p, contact="B", flow=4, pensees="dans_le_flow")
        r = simuler(self.b, [self.p, calme])
        self.assertEqual(r["contacts"]["A"]["cumul"], 7)
        self.assertEqual(r["contacts"]["B"]["cumul"], 1)

    def test_ressentir_ne_signifie_pas_reconnaitre(self):
        naive = simuler(self.b, [dict(self.p, duree=10)])["contacts"]["A"]
        self.assertTrue(naive["phenomene_percu"])
        self.assertFalse(naive["contact_reconnu"])
        forme = simuler(self.b, [dict(self.p, formation="forme", attention="vigilante")])["contacts"]["A"]
        self.assertTrue(forme["contact_reconnu"])

    def test_mecanismes_ouverts_et_actions_sur_soi_sans_cumul(self):
        for p in [dict(self.p, resistance=True), {"action": "cacher_pensee"},
                  {"action": "fabriquer"}, {"action": "message", "modificateurs": {"discretion": "masque"}}]:
            self.assertEqual(simuler(self.b, [p])["contacts"], {})

    def test_entrees_invalides(self):
        for p in [dict(self.p, flow=-1), dict(self.p, duree=0), dict(self.p, contact=""),
                  dict(self.p, formation="inconnue"), dict(self.p, resistance="non")]:
            with self.assertRaises(ValueError):
                simuler(self.b, [p])

    def test_bareme_unique(self):
        self.b["perceptibilite"]["reference_par_battement"] = 3
        calme = dict(self.p, flow=4, pensees="dans_le_flow")
        self.assertEqual(simuler(self.b, [calme])["contacts"]["A"]["cumul"], 3)


if __name__ == "__main__":
    unittest.main()
