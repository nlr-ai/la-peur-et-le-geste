"""Le relevé technique rejette un PID vivant dont la naissance ne correspond pas."""
import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from agents.expose import runtime


class ActiviteRuntimeTest(unittest.TestCase):
    def test_identite_et_lecture_seule(self):
        with tempfile.TemporaryDirectory() as dossier:
            base = {"homme": "mj", "pid": os.getpid(),
                    "processus": runtime._identite_processus(os.getpid()),
                    "racine": dossier, "pour": ["alice", "bob"]}
            for nom, d in (("bon", base),
                           ("recycle", dict(base, processus="autre-naissance")),
                           ("reserve", dict(base, reserve=True)),
                           ("mort", dict(base, pid=2147483647))):
                with open(os.path.join(dossier, nom + ".json"), "w") as f:
                    json.dump(d, f)
            with open(os.path.join(dossier, "incomplet.json"), "w") as f:
                f.write("{")
            with patch.object(runtime, "ACTIVITES", dossier):
                actifs = runtime.activites_vivantes()
            self.assertEqual(len(actifs), 1)
            self.assertEqual(actifs[0]["pour"], ["alice", "bob"])
            self.assertEqual(len(os.listdir(dossier)), 5)


if __name__ == "__main__":
    unittest.main()
