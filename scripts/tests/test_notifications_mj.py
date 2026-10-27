"""Les réponses techniques réveillent la session destinataire, jamais le PNJ."""
import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scenes


class NotificationsMjTests(unittest.TestCase):
    def executer(self, operation, pret=False, sans_reveil=False):
        arguments = ["scenes.py", operation, "--de", "bob", "--id", "relais",
                     "--message", "nouvelle contrainte"]
        if pret:
            arguments.append("--pret")
        if sans_reveil:
            arguments.append("--sans-reveil")
        registre = mock.Mock()
        resultat = {"id": "relais", "de": "alice", "a": "bob"}
        getattr(registre, operation).return_value = resultat
        with mock.patch.object(sys, "argv", arguments), \
                mock.patch.object(scenes, "Scenes", return_value=registre), \
                mock.patch.object(scenes, "notifier", return_value=42) as notifier, \
                contextlib.redirect_stdout(io.StringIO()):
            scenes.main()
        return notifier

    def test_reponse_reveille_le_mj_emetteur(self):
        appel = self.executer("repondre")
        self.assertEqual(appel.call_args.args[1:3], ("alice", "relais"))
        self.assertIn("nouvelle contrainte", appel.call_args.args[3])

    def test_accuse_et_complement_reveillent_la_source(self):
        for pret in (True, False):
            with self.subTest(pret=pret):
                appel = self.executer("recevoir", pret=pret)
                self.assertEqual(appel.call_args.args[1], "alice")

    def test_sans_reveil_reste_explicite(self):
        for operation in ("repondre", "recevoir"):
            self.executer(operation, sans_reveil=True).assert_not_called()


if __name__ == "__main__":
    unittest.main()
