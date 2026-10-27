"""Concurrence réelle : ordre des messages et récupération après un crash."""
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class FileMjTests(unittest.TestCase):
    def worker(self, dossier, session="scene"):
        code = """
import os,sys
sys.path.insert(0, sys.argv[1])
from agents.expose import runtime
from agents import file_mj
runtime.DOSSIER_RUNTIME = sys.argv[2]
runtime.ACTIVITES = os.path.join(sys.argv[2], 'active')
ecrire = runtime._ecrire_json
def ticket(*args):
    ecrire(*args)
    print('ticket', flush=True)
runtime._ecrire_json = ticket
with file_mj.attendre(sys.argv[3]):
    print('entre', flush=True)
    sys.stdin.readline()
"""
        p = subprocess.Popen([sys.executable, "-c", code, SCRIPTS, dossier, session],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, text=True)
        self.addCleanup(self.nettoyer, p)
        self.assertEqual(p.stdout.readline().strip(), "ticket")
        return p

    @staticmethod
    def nettoyer(p):
        if p.poll() is None:
            p.kill()
        p.communicate(timeout=10)

    def finir(self, p):
        p.stdin.write("fin\n")
        p.stdin.flush()
        p.wait(timeout=10)
        self.assertEqual(p.returncode, 0, p.stderr.read())

    def test_fifo_et_scenes_independantes(self):
        with tempfile.TemporaryDirectory() as dossier:
            a = self.worker(dossier)
            self.assertEqual(a.stdout.readline().strip(), "entre")
            b = self.worker(dossier)
            c = self.worker(dossier)
            autre = self.worker(dossier, "autre-scene")
            self.assertEqual(autre.stdout.readline().strip(), "entre")
            self.finir(autre)
            self.finir(a)
            lu = b.stdout.readline().strip()
            self.assertEqual(lu, "entre", b.stderr.read() if not lu else "")
            self.finir(b)
            self.assertEqual(c.stdout.readline().strip(), "entre")
            self.finir(c)

    def test_crash_ne_bloque_pas_la_file(self):
        with tempfile.TemporaryDirectory() as dossier:
            a = self.worker(dossier)
            self.assertEqual(a.stdout.readline().strip(), "entre")
            b = self.worker(dossier)
            a.kill()
            a.wait(timeout=10)
            lu = b.stdout.readline().strip()
            self.assertEqual(lu, "entre", b.stderr.read() if not lu else "")
            self.finir(b)


if __name__ == "__main__":
    unittest.main()
