"""Preuves de bout en bout du pilote, en depot et registre jetables."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from agents import work_identity
from agents.atelier import catalogue
from agents.atelier.essais import essayer, comparer, verifier_sortie
from agents.atelier.processus import executer, verrou


def mesure(variante="temoin"):
    return {"version": "resultat-ralliement/1", "variante": variante,
            "effectif_demande": 30, "effectif_observe": 30,
            "duree_demandee_s": 1, "duree_simulee_s": 1, "graine": 7,
            "etat_initial_sha256": "initial",
            "donnees": {"plan": {"status": 200, "sha256": "plan"}},
            "appels_arbitre": 0 if variante == "temoin" else 12,
            "appels_ralliement": 0, "decisions_ralliement": 0,
            "ralliements": 0, "morts": 0, "blesses": 0, "fuyards": 0}


class AtelierTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.racine = Path(self.tmp.name)
        for cible, valeur in (("RACINE", self.racine), ("RUNTIME", self.racine / "runtime")):
            patch = mock.patch.object(catalogue, cible, valeur)
            patch.start()
            self.addCleanup(patch.stop)
        patch = mock.patch.object(work_identity, "REGISTRE", str(self.racine / "work.sqlite3"))
        patch.start()
        self.addCleanup(patch.stop)
        self.cahier = self.racine / "etat/maisons/_sans-maison/documents/books" / (catalogue.AFFAIRE + ".json")
        self.cahier.parent.mkdir(parents=True)
        self.cahier.write_text(json.dumps({"id": catalogue.AFFAIRE, "titre": "Bataille",
            "tables": [{"titre": "Actions", "lignes": [{"cellules": ["**90312**", "Ralliement"]}]}]}))
        source = self.racine / catalogue.SOURCE / "ecrans/modules"
        source.mkdir(parents=True)
        (source / "moteur.js").write_text("// sources de test\n")
        self.banc = self.racine / catalogue.BANC
        self.faux_banc()
        subprocess.run(["git", "init", "-q", str(self.racine)], check=True, capture_output=True)
        subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                        "-c", "commit.gpgsign=false", "commit", "--allow-empty", "-qm", "initial"],
                       cwd=self.racine, check=True, capture_output=True)

    def faux_banc(self, suffixe=""):
        self.banc.write_text("const args=process.argv.slice(2);\n"
            "const variante=args.find(x=>x.startsWith('--variante=')).split('=')[1];\n"
            "const r=" + json.dumps(mesure()) + ";\n"
            "r.variante=variante; r.appels_arbitre=variante==='arbitre'?12:0;\n"
            + suffixe + "\nprocess.stdout.write(JSON.stringify(r));\n", encoding="utf-8")

    def essai(self, **kwargs):
        return essayer(annoncer=lambda _: None, **kwargs)

    def test_deux_variantes_archivees_et_retry_sans_ecrasement(self):
        avant = self.cahier.read_bytes()
        a = self.essai()
        b = self.essai()
        self.assertEqual("mesure_obtenue", a["statut"])
        self.assertFalse(a["ralliement_exerce"])
        self.assertIn("Non concluant", a["conclusion"])
        self.assertEqual(["temoin", "arbitre"], list(a["variantes"]))
        self.assertEqual(avant, self.cahier.read_bytes())
        self.assertNotEqual(a["dossier_essai"], b["dossier_essai"])
        ia, ib = a["demande"]["identite_travail"], b["demande"]["identite_travail"]
        self.assertEqual(ia["work_id"], ib["work_id"])
        self.assertEqual(ia["attempt_number"] + 1, ib["attempt_number"])
        self.assertEqual(2, len(work_identity.observer(ia["work_id"])["attempts"]))
        self.assertTrue((Path(a["dossier_essai"]) / "resultat.json").exists())
        self.assertIn("--relire-donnees", b["variantes"]["arbitre"]["commande"])
        self.assertEqual(b["dossier_essai"], catalogue.dernier()["dossier_essai"])

    def test_sortie_vide_ne_vaut_pas_succes(self):
        self.banc.write_text("// silence\n")
        r = self.essai()
        self.assertEqual("echec", r["statut"])
        self.assertEqual(["temoin"], list(r["variantes"]))
        self.assertEqual("failed", work_identity.observer(r["demande"]["identite_travail"]["work_id"])["term"]["state"])
        self.assertTrue((Path(r["dossier_essai"]) / "temoin.json").exists())

    def test_timeout_conserve_progression_et_resultat(self):
        self.banc.write_text("console.error(JSON.stringify({etape:'simulation',secondes_simulees:0.5})); setTimeout(()=>{},30000);")
        r = self.essai(limite=0.7)
        self.assertEqual("delai_depasse", r["statut"])
        self.assertIn("0.5 s simulees", r["conclusion"])
        self.assertTrue((Path(r["dossier_essai"]) / "resultat.json").exists())

    def test_sources_modifiees_par_essai_refusees(self):
        self.faux_banc("const fs=require('fs'); const p=require('path');"
            "fs.appendFileSync(p.join(args.find(x=>x.startsWith('--source=')).slice(9),'ecrans/modules/moteur.js'),'change');")
        r = self.essai()
        self.assertEqual("echec", r["statut"])
        self.assertIn("sources a change", r["conclusion"])

    def test_collision_affaire_refusee_avant_execution(self):
        d = json.loads(self.cahier.read_text())
        d["tables"][0]["lignes"] *= 2
        self.cahier.write_text(json.dumps(d))
        with self.assertRaisesRegex(ValueError, "une seule source"):
            self.essai()

    def test_criteres_rejettent_simulation_incomplete_arbitre_inactif_nan(self):
        for cle, valeur in (("duree_simulee_s", 0.5), ("appels_arbitre", 0),
                            ("morts", float("nan")), ("donnees", {})):
            r = mesure("arbitre")
            r[cle] = valeur
            with self.subTest(cle=cle), self.assertRaises(ValueError):
                verifier_sortie(r, "arbitre", 30, 1)

    def test_comparaison_refuse_donnees_ou_depart_differents(self):
        t, a = mesure(), mesure("arbitre")
        for cle in ("etat_initial_sha256", "donnees", "graine"):
            b = copy.deepcopy(a)
            b[cle] = "autre"
            with self.subTest(cle=cle), self.assertRaisesRegex(ValueError, "non comparables"):
                comparer(t, b)

    def test_verrou_interprocessus_refuse_second_lancement(self):
        script = self.racine / "concurrent.py"
        script.write_text("import sys\nfrom pathlib import Path\nsys.path.insert(0," + repr(str(SCRIPTS)) + ")\n"
            "from agents.atelier.processus import verrou\nwith verrou(Path(sys.argv[1])): print('acquis')\n")
        fichier = self.racine / "banc.lock"
        with verrou(fichier):
            autre = subprocess.run([sys.executable, str(script), str(fichier)], capture_output=True, text=True, timeout=10)
        self.assertNotEqual(0, autre.returncode)
        self.assertIn("occupe deja", autre.stderr)
        with verrou(fichier):
            pass

    def test_noms_et_consigne_limites_a_equipe_et_affaire(self):
        self.assertIn("Développeuse", catalogue.consignes("ygga-main-de-pierre", "90312"))
        self.assertEqual("", catalogue.consignes("ygga-main-de-pierre", "91020"))
        self.assertEqual("", catalogue.consignes("rhaenyra-targaryen"))

    def test_validation_avant_admission(self):
        for kwargs in ({"duree": 0}, {"limite": float("nan")}, {"effectif": -1}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.essai(**kwargs)
        self.assertFalse(Path(work_identity.REGISTRE).exists())

    def test_brief_reel_retrouve_la_preuve_sans_reveil(self):
        from agents.depeche import manuel
        r = self.essai()
        with mock.patch.object(manuel, "_cahier_amende", return_value=True):
            texte = manuel.memoire_du_jour({"personnage": {"id": "ygga-main-de-pierre"},
                                           "contexte_affaire": {"id": "90312"}})
        self.assertIn("Ygga — Développeuse", texte)
        self.assertIn(r["dossier_essai"], texte)
        self.assertIn("Non concluant", texte)

    def test_enfant_survivant_bloque_nouvelle_admission(self):
        from agents import runtime
        kwargs = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
        p = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"], **kwargs)
        try:
            dossier = catalogue.RUNTIME / "90312/ancien"
            dossier.mkdir(parents=True)
            (dossier / "processus.json").write_text(json.dumps({"pid": p.pid,
                "naissance": runtime._identite_processus(p.pid)}))
            with self.assertRaisesRegex(RuntimeError, "encore vivant"):
                self.essai()
            self.assertFalse(Path(work_identity.REGISTRE).exists())
        finally:
            p.terminate()
            p.wait(timeout=5)


if __name__ == "__main__":
    unittest.main()
