import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import joueur_pnj as pilote


class JourneeTest(unittest.TestCase):
    def executer(self, budget, retour=True, apercu=False, initial=None):
        with tempfile.TemporaryDirectory() as dossier, contextlib.ExitStack() as stack:
            chambre = Path(dossier) / "chambres" / "tiers"
            chambre.mkdir(parents=True)
            (chambre / "joueur.md").write_text("Je suis un employé prudent.", encoding="utf-8")
            args = ["joueur_pnj", "--qui", "tiers", "--port", "3212", "--journee", "--messages", str(budget), "--fournisseur", "claude"]
            if apercu: args.append("--voir")
            stack.enter_context(patch.object(sys, "argv", args))
            stack.enter_context(patch.object(pilote, "base_monde", return_value=dossier))
            stack.enter_context(patch.object(pilote, "siege", return_value={"jeton": "test"}))
            stack.enter_context(patch.object(pilote, "get", return_value={"items": initial if initial is not None else [{"type": "recit", "texte": "Matin."}]}))
            stack.enter_context(patch.object(pilote, "noms", return_value={"tiers": "Employé"}))
            stack.enter_context(patch.object(pilote, "prendre_verrou", return_value=str(Path(dossier)/"lock")))
            stack.enter_context(patch.object(pilote, "lire_boite", return_value=[]))
            attente = stack.enter_context(patch.object(pilote, "attendre_reponse", return_value=[{"type":"recit", "texte":"Résultat."}] if retour else None))
            modele = stack.enter_context(patch.object(pilote, "appeler_claude", return_value=({"mode":"agir", "texte":"Je vérifie les livraisons.", "pourquoi":"Mon travail.", "a_qui":""}, "test")))
            envoi = stack.enter_context(patch.object(pilote, "post", return_value={"ref":"test"}))
            stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            resultat = pilote.main()
            return resultat, modele, envoi, attente

    def test_budget_et_canal(self):
        for budget in (1, 2):
            with self.subTest(budget=budget):
                resultat, modele, envoi, attente = self.executer(budget)
                self.assertEqual(resultat, 0)
                self.assertEqual(envoi.call_count, budget)
                self.assertEqual(attente.call_count, budget)
                for call in envoi.call_args_list:
                    self.assertEqual(call.args[2]["mode"], "agir")
                    self.assertEqual(call.args[2]["pilote_mode"], "pnjpj-journee")
                self.assertIn("une journée hors scène", modele.call_args.args[0])
                self.assertNotIn("Tu joues au niveau d'un souverain", modele.call_args.args[0])
                self.assertIn("Dernier message disponible", modele.call_args.args[1])
                if budget == 2:
                    self.assertIn("Résultat.", modele.call_args.args[1])
                    self.assertIn("ajuste le reste", modele.call_args.args[1])

    def test_fil_vide_demarre_depuis_la_tete(self):
        for budget in (1, 2):
            resultat, modele, envoi, attente = self.executer(budget, initial=[])
            self.assertEqual(resultat, 0)
            self.assertEqual(envoi.call_count, budget)
            self.assertEqual(attente.call_count, budget)
            self.assertIn("Je suis un employé prudent.", modele.call_args.args[0])

    def test_action_en_attente_ne_doit_pas_etre_rejouee(self):
        resultat, modele, envoi, _ = self.executer(2, retour=False,
            initial=[{"type":"vous", "joueur_id":"tiers", "texte":"Je vérifie."}])
        self.assertEqual(resultat, 1)
        modele.assert_not_called()
        envoi.assert_not_called()

    def test_apercu_sans_envoi(self):
        resultat, modele, envoi, _ = self.executer(2, apercu=True)
        self.assertEqual(resultat, 0)
        modele.assert_not_called()
        envoi.assert_not_called()

    def test_pas_de_fausse_fin(self):
        resultat, _, envoi, _ = self.executer(1, retour=False)
        self.assertEqual(resultat, 1)
        self.assertEqual(envoi.call_count, 1)


if __name__ == "__main__":
    unittest.main()
