# -*- coding: utf-8 -*-
import os
import sys
import tempfile
import unittest

SCRIPTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

from agents import runtime  # noqa: E402


class RuntimeGeminiTests(unittest.TestCase):
    def test_atelier_monetaire_restreint_sans_repli_non_restreint(self):
        from unittest import mock
        from agents import runtime_gemini
        for monde in ('argent-intelligent', 'frontieres-du-vivant'):
            with self.subTest(monde=monde), tempfile.TemporaryDirectory() as dossier, \
                    mock.patch.object(runtime_gemini.subprocess, 'run') as run:
                run.return_value = mock.Mock(returncode=1, stdout=b'', stderr=b'permission denied')
                with self.assertRaises(RuntimeError):
                    runtime_gemini.appeler('M', 'msg', 'test', 'm', None, 5,
                                          dossier, [], ['WebSearch'], None, False,
                                          {'CONSEIL_MONDE': monde})
                self.assertEqual(run.call_count, 1)
                cmd = run.call_args.args[0]
                self.assertEqual('--sandbox' in cmd, monde == 'argent-intelligent')
                self.assertEqual('--dangerously-skip-permissions' in cmd,
                                 monde != 'argent-intelligent')

    def test_recherche_conserve_sortie_sans_inventer_trace_outil(self):
        from unittest import mock
        from agents import runtime_gemini
        import json
        commandes = []

        def faux_run(cmd, **kw):
            commandes.append(cmd)
            return mock.Mock(returncode=0, stdout=b'{"response":"declaration"}', stderr=b'')

        with tempfile.TemporaryDirectory() as dossier, \
                mock.patch.object(runtime_gemini.subprocess, 'run', faux_run), \
                mock.patch.object(runtime_gemini._rt, '_poser_empreinte_manuel'):
            result = runtime_gemini.appeler('M', 'msg', 'audit', 'm', None, 5,
                                            dossier, [], ['WebSearch'], None, False, {})
            self.assertIn('--log-file', commandes[0])
            with open(result['transcript_path'], encoding='utf-8') as f:
                self.assertEqual(json.load(f)['response'], 'declaration')
            self.assertIsNone(result['research_log_path'])
            self.assertNotIn('gestes', result)

    def test_gemini_pose_le_manuel_en_agents_md_sans_add_dir(self):
        from agents import runtime_gemini
        with tempfile.TemporaryDirectory() as dossier:
            self.assertTrue(runtime_gemini._poser_agents_md("MANUEL", dossier))
            with open(os.path.join(dossier, "AGENTS.md"), encoding="utf-8") as f:
                self.assertEqual(f.read(), "MANUEL")
        self.assertFalse(runtime_gemini._poser_agents_md(
            "MANUEL", os.path.join(runtime.RACINE, "scripts")))
        commande = runtime_gemini.commande("m", "sid", True)
        self.assertNotIn("--add-dir", commande)
        self.assertEqual(commande[-2:], ["--conversation", "sid"])

    def test_gemini_reprend_par_l_id_que_agy_a_rendu(self):
        """agy reprend par SON conversation_id, jamais par notre id logique."""
        from unittest import mock
        from agents import runtime_gemini
        appels = []

        def faux_run(cmd, **kw):
            appels.append(cmd)
            sortie = '{"conversation_id":"agy-42","status":"SUCCESS","response":"ok"}'
            return mock.Mock(returncode=0, stdout=sortie.encode(), stderr=b"")

        with tempfile.TemporaryDirectory() as dossier,                 mock.patch.object(runtime_gemini, "_TABLE", os.path.join(dossier, "t.json")),                 mock.patch.object(runtime_gemini.subprocess, "run", faux_run):
            for reprendre in (None, None, False):
                runtime_gemini.appeler("M", "msg", "logique-mj", "m", None, 5, dossier,
                                       [], None, None, reprendre, {})
        self.assertNotIn("--conversation", appels[0])          # rien de connu : neuve
        self.assertEqual(appels[1][-2:], ["--conversation", "agy-42"])  # reprise
        self.assertNotIn("--conversation", appels[2])          # neuve voulue


if __name__ == "__main__":
    unittest.main()
