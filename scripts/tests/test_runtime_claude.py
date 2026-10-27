# -*- coding: utf-8 -*-
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

from agents import runtime  # noqa: E402


def _sortie(stdout, code=0):
    return mock.Mock(returncode=code, stdout=stdout.encode("utf-8"), stderr=b"")


class OrdreDesEssaisClaudeTests(unittest.TestCase):
    """Session connue : reprise d'abord (creer puis se faire refuser
    « already in use » coutait un lancement par reveil). Seuls les refus
    d'ouverture changent d'essai : un autre echec a pu agir."""

    def _appeler(self, entree, sorties):
        lancees = []

        def run(commande, **_):
            lancees.append(commande)
            return sorties.pop(0)

        with tempfile.TemporaryDirectory() as dossier, \
                mock.patch.object(runtime, "_entree_session", return_value=entree), \
                mock.patch.object(runtime, "_poser_empreinte_manuel"), \
                mock.patch.object(runtime.subprocess, "run", side_effect=run):
            runtime._appel_claude("MANUEL", "msg", "sid-1", None, None, None,
                                  dossier, [], [], None, None, {}, None, None,
                                  None, None)
        return lancees

    def test_session_connue_reprise_d_abord_un_seul_lancement(self):
        lancees = self._appeler({"manuel_sha256_claude": "x"},
                                [_sortie(json.dumps({"result": "ok"}))])
        self.assertEqual(len(lancees), 1)
        self.assertIn("--resume", lancees[0])
        self.assertIn("--system-prompt-file", lancees[0])

    def test_session_connue_mais_absente_on_la_cree(self):
        lancees = self._appeler(
            {"manuel_sha256_claude": "x"},
            [_sortie("No conversation found with session ID: sid-1"),
             _sortie(json.dumps({"result": "ok"}))])
        self.assertIn("--resume", lancees[0])
        self.assertIn("--session-id", lancees[1])

    def test_session_inconnue_creation_d_abord(self):
        lancees = self._appeler({}, [_sortie(json.dumps({"result": "ok"}))])
        self.assertEqual(len(lancees), 1)
        self.assertIn("--session-id", lancees[0])

    def test_un_autre_echec_ne_relance_pas(self):
        with self.assertRaises(RuntimeError):
            self._appeler({"manuel_sha256_claude": "x"},
                          [_sortie("boom", code=1), _sortie("{}")])


if __name__ == "__main__":
    unittest.main()
