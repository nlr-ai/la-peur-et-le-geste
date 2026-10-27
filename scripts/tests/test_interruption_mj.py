"""Vrais processus locaux : arrêt entre les outils et reprise du même thread."""
import json
import os
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from agents.expose import runtime
from agents import file_mj, mj


class InterruptionMjTests(unittest.TestCase):
    def test_arret_attend_la_fin_de_l_operation_et_conserve_le_transcript(self):
        with tempfile.TemporaryDirectory() as dossier:
            termine = os.path.join(dossier, "ecriture-terminee")
            transcript = os.path.join(dossier, "transcript.jsonl")
            code = """
import json,sys,time,pathlib
def event(type,item=None,**kw):
 print(json.dumps(dict(type=type,item=item,**kw)),flush=True)
event('thread.started',thread_id='thread-continu')
event('item.started',dict(id='outil',type='command_execution'))
time.sleep(.3)
pathlib.Path(sys.argv[1]).write_text('commis')
event('item.completed',dict(id='outil',type='command_execution',status='completed'))
time.sleep(10)
"""
            demande = threading.Event()
            def evenement(ev):
                if ev.get("type") == "item.started":
                    demande.set()  # le nouveau message arrive pendant l'écriture
            debut = time.monotonic()
            with mock.patch.object(file_mj, "plus_recent", side_effect=lambda _: demande.is_set()):
                with self.assertRaises(file_mj.Interrompu):
                    runtime._executer_flux([sys.executable, "-u", "-c", code, termine],
                        "ancien message", dossier, dict(os.environ, LE_CONSEIL_MJ_TICKET="ticket"),
                        15, on_event=evenement, transcript=transcript)
            self.assertLess(time.monotonic() - debut, 5)
            self.assertEqual(Path(termine).read_text(), "commis")
            evs = [json.loads(l) for l in Path(transcript).read_text().splitlines()]
            self.assertTrue(any(e.get("type") == "item.completed" for e in evs))

    def test_thread_preserve_meme_si_interruption_au_premier_tour(self):
        with tempfile.TemporaryDirectory() as dossier:
            interruption = file_mj.Interrompu([{"type": "thread.started", "thread_id": "meme-thread"}])
            with mock.patch.object(runtime, "SESSIONS", os.path.join(dossier, "sessions.json")), \
                    mock.patch.object(runtime, "_executer_flux", side_effect=interruption):
                with self.assertRaises(file_mj.Interrompu):
                    runtime._appel_codex("manuel", "message", "logique", "modele", "low", 15,
                        dossier, [], None, {}, None, None, None, None)
                self.assertEqual(runtime._entree_session("logique")["codex_thread_id"], "meme-thread")

    def test_reprise_regroupe_les_refs_et_reste_sur_la_meme_session(self):
        with tempfile.TemporaryDirectory() as dossier:
            os.makedirs(os.path.join(dossier, "etat", "inbox", "alice"))
            for i, ref in enumerate(("ancien", "nouveau")):
                with open(os.path.join(dossier,"etat/inbox/alice/action-%s.json" % i), "w") as f:
                    json.dump({"ref": ref, "mode": "dire", "texte": ref}, f)
            with mock.patch.object(mj, "ETAT", os.path.join(dossier,"etat")), \
                    mock.patch.object(runtime, "DOSSIER_RUNTIME", dossier), \
                    mock.patch.object(mj, "_appeler_mj", return_value="reponse") as appel:
                mj.appeler_mj("alice", "", "JOUEUR", refs=["nouveau"], routage={"decision":"direct"})
            self.assertEqual(appel.call_args.args[5], ["ancien", "nouveau"])
            self.assertEqual(len(appel.call_args.args[6]["messages_joueur"]), 2)
            self.assertTrue(appel.call_args.kwargs["ticket"])


if __name__ == "__main__":
    unittest.main()
