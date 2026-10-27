# -*- coding: utf-8 -*-
"""Les racines : ou vit l'etat, et l'accord des deux langues.

CE QUE CE BANC GARDE, ET POURQUOI IL EXISTE.

Le depot execute son monde dans deux langues. Aucune ne peut demander a l'autre
ou lire — ce serait un `spawn` par requete sur le chemin le plus chaud du
serveur. Elles doivent donc tomber sur le meme dossier PAR CONSTRUCTION, et
c'est la seule chose qu'une lecture ne peut pas garantir : deux fichiers qui se
ressemblent aujourd'hui divergent dans six semaines, et personne ne le voit.

Le precedent est dans le depot et il a deja coute : `noyau/diffusion.py` et
`serveur/domaine/regie.js` lisent un seul `diffusion.json` PARCE QUE les deux
implementations avaient silencieusement diverge. Ici l'enjeu est plus grave
qu'une constante — deux racines qui ne s'accordent pas, c'est le brouillard d'un
monde servi dans un autre.

Le banc compare donc les DEUX SORTIES, pas les deux textes.
"""
import os as _os, sys as _sys  # le chemin des freres : scripts/ et scripts/noyau/
_d = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_d) != "scripts" and _os.path.dirname(_d) != _d:
    _d = _os.path.dirname(_d)
for _p in (_d, _os.path.join(_d, "noyau")):
    if _p not in _sys.path:
        _sys.path.insert(0, _p)

import json
import os
import shutil
import subprocess
import tempfile
import unittest

import racines


def _sans(*noms):
    """L'environnement prive des variables de monde — un banc part toujours
    d'une ardoise, sinon il mesure la machine de celui qui le lance."""
    e = dict(os.environ)
    for n in noms:
        e.pop(n, None)
    return e


class Disposition(unittest.TestCase):
    def setUp(self):
        self._avant = {k: os.environ.get(k)
                       for k in ("CONSEIL_MONDE", "CONSEIL_RACINE")}
        for k in self._avant:
            os.environ.pop(k, None)

    def tearDown(self):
        for k, v in self._avant.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def test_heritee_est_le_defaut(self):
        """Sans variable, on rend exactement ce qu'on rendait avant ce module.

        C'est ce qui fait de ce lot un lot ADDITIF : rien ne bouge tant que
        personne ne nomme un monde. Si cette epreuve tombe, une partie en cours
        vient de perdre son etat."""
        self.assertEqual(racines.racine(), racines.DEPOT)
        self.assertEqual(racines.etat(), os.path.join(racines.DEPOT, "etat"))
        self.assertIsNone(racines.courant())

    def test_monde_nomme_deplace_l_etat_et_pas_le_depot(self):
        """La racine du DEPOT ne suit JAMAIS le monde.

        Le piege a failli se refermer deux fois pendant l'ecriture du lot : le
        `--verifier` de `tables.py` balaie les `*.py` suivis par git, et le
        serveur sert `ecrans/jeu.html` — les deux depuis une variable nommee
        `RACINE`. Pointer un monde y ferait chercher du CODE dans un dossier de
        DONNEES."""
        with tempfile.TemporaryDirectory() as tmp:
            faux = os.path.join(racines.MONDES, "_banc-%s" % os.path.basename(tmp))
            os.makedirs(os.path.join(faux, "etat"))
            try:
                os.environ["CONSEIL_MONDE"] = os.path.basename(faux)
                self.assertEqual(racines.racine(), faux)
                self.assertEqual(racines.etat(), os.path.join(faux, "etat"))
                self.assertEqual(racines.DEPOT,
                                 os.path.dirname(racines.MONDES))
            finally:
                shutil.rmtree(faux, ignore_errors=True)

    def test_monde_inconnu_plante(self):
        """On ne sert JAMAIS le monde d'a cote parce qu'on a mal tape un nom.

        Meme raison que la porte des tables devant un JSON abime : la faute la
        plus couteuse est celle qui ne se voit pas."""
        os.environ["CONSEIL_MONDE"] = "ce-monde-n-existe-pas"
        with self.assertRaises(racines.MondeInconnu):
            racines.racine()

    def test_racine_explicite_prime(self):
        """`CONSEIL_RACINE` est le contrat des tests du serveur depuis toujours :
        un chemin absolu qui CONTIENT `etat/`. On ne le change pas."""
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["CONSEIL_RACINE"] = tmp
            self.assertEqual(racines.racine(), os.path.abspath(tmp))
            self.assertEqual(racines.etat(), os.path.join(os.path.abspath(tmp), "etat"))

    def test_monde_de_service_cache_du_menu_jamais_de_la_machine(self):
        """`_epreuve` ne doit pas s'offrir au joueur, et doit rester nommable.

        Un diagnostic qui tairait les mondes de service mentirait sur ce qui est
        la — c'est ce qui a rendu un message d'erreur faux pendant une heure."""
        tous = racines.mondes(tous=True)
        offerts = racines.mondes()
        for m in tous:
            if m.startswith("_"):
                self.assertNotIn(m, offerts)


class AccordDesDeuxLangues(unittest.TestCase):
    """Le seul banc qui compte vraiment : Python et Node sur le meme dossier."""

    def _node(self, quoi, monde=None):
        env = _sans("CONSEIL_MONDE", "CONSEIL_RACINE")
        if monde:
            env["CONSEIL_MONDE"] = monde
        return subprocess.check_output(
            ["node", "-e", "console.log(require('./serveur/racines').%s())" % quoi],
            cwd=racines.DEPOT, env=env).decode("utf-8").strip()

    def _python(self, quoi, monde=None):
        env = _sans("CONSEIL_MONDE", "CONSEIL_RACINE")
        if monde:
            env["CONSEIL_MONDE"] = monde
        code = ("import sys;sys.path.insert(0,'scripts');"
                "sys.path.insert(1,'scripts/noyau');import racines;"
                "print(racines.%s())" % quoi)
        return subprocess.check_output(
            [_sys.executable, "-c", code],
            cwd=racines.DEPOT, env=env).decode("utf-8").strip()

    def _accord(self, quoi, monde=None):
        try:
            n = self._node(quoi, monde)
        except (OSError, subprocess.CalledProcessError) as e:
            raise unittest.SkipTest("node indisponible : %s" % e)
        self.assertEqual(self._python(quoi, monde), n,
                         "python et node ne tombent pas sur le meme %s "
                         "(monde=%r) — le brouillard d'un monde s'ouvrirait "
                         "dans l'autre" % (quoi, monde))

    def test_accord_en_disposition_heritee(self):
        self._accord("etat")
        self._accord("racine")

    def test_accord_sur_un_monde_nomme(self):
        nom = "_banc-accord"
        faux = os.path.join(racines.MONDES, nom)
        os.makedirs(os.path.join(faux, "etat"), exist_ok=True)
        try:
            self._accord("etat", nom)
            self._accord("chambres", nom)
        finally:
            shutil.rmtree(faux, ignore_errors=True)

    def test_accord_sur_le_depot(self):
        """`DEPOT` est la seule chose que les deux deduisent de leur position.
        Elles partent de dossiers differents (`scripts/noyau/`, `serveur/`) :
        c'est exactement le genre d'arithmetique de chemins qui se casse au
        premier deplacement, et que personne ne relit."""
        try:
            n = subprocess.check_output(
                ["node", "-e", "console.log(require('./serveur/racines').DEPOT)"],
                cwd=racines.DEPOT).decode("utf-8").strip()
        except (OSError, subprocess.CalledProcessError) as e:
            raise unittest.SkipTest("node indisponible : %s" % e)
        self.assertEqual(os.path.normpath(racines.DEPOT), os.path.normpath(n))


class Manifeste(unittest.TestCase):
    # L'ARDOISE, COMME `Disposition`. Sans ce menage, `CONSEIL_MONDE` restait
    # pose pour tout le reste de la suite : les epreuves qui lancent un
    # sous-processus heritaient d'un monde jetable deja efface, et plantaient
    # trois fichiers plus loin sur un `MondeInconnu`.
    def setUp(self):
        self._avant = {k: os.environ.get(k)
                       for k in ("CONSEIL_MONDE", "CONSEIL_RACINE")}
        for k in self._avant:
            os.environ.pop(k, None)

    def tearDown(self):
        for k, v in self._avant.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def test_absent_rend_vide_et_ne_plante_pas(self):
        """Un monde sans manifeste rend vide, et le defaut du code s'applique.

        L'epreuve visait d'abord le monde reel, qui n'avait pas de manifeste ;
        il en a un depuis le lot 4, et l'epreuve est tombee. Elle avait raison
        de tomber — mais son INTENTION reste juste et vaut d'etre gardee : un
        monde neuf, ou un monde qui ne declare rien, ne doit pas planter. On la
        pose donc sur un monde jetable, ou l'absence est vraie pour de bon."""
        nom = "_banc-sans-manifeste"
        faux = os.path.join(racines.MONDES, nom)
        os.makedirs(os.path.join(faux, "etat"), exist_ok=True)
        try:
            os.environ["CONSEIL_MONDE"] = nom
            self.assertEqual(racines.manifeste(), {})
            self.assertIsNone(racines.dit("monnaie"))
            self.assertEqual(racines.dit("monnaie", "defaut"), "defaut")
        finally:
            shutil.rmtree(faux, ignore_errors=True)

    def test_le_monde_d_epreuve_declare_ce_qu_il_faut(self):
        """Le monde d'epreuve est le gabarit : ce qu'il declare est ce qu'un
        monde DOIT declarer pour que le lot 4 ait ou verser."""
        p = os.path.join(racines.MONDES, "_epreuve", "manifeste.json")
        if not os.path.exists(p):
            raise unittest.SkipTest("mondes/_epreuve absent")
        with open(p, encoding="utf-8") as f:
            m = json.load(f)
        for cle in ("id", "nom", "calendrier", "monnaie", "titres",
                    "unites", "canaux", "offices", "signes", "depart"):
            self.assertIn(cle, m, "le gabarit doit porter %r" % cle)


class LeMoteurNeConnaitPlusLeDecor(unittest.TestCase):
    """Lot 4 : la monnaie et les titres viennent du monde, plus du code.

    DEUX EPREUVES, ET IL FAUT LES DEUX. Prouver que la valeur du monde arrive
    ne suffit pas : il faut aussi prouver que SANS monde, rien n'a bouge — sinon
    on a deplace une declaration ET casse une partie en cours. Et prouver que
    rien n'a bouge ne suffit pas non plus : un manifeste purement ignore
    donnerait exactement le meme vert.

    On lance les deux dans des PROCESSUS separes, parce que ces tables se
    calculent une seule fois, au chargement du module : les comparer dans la
    meme session ne mesurerait que l'ordre des imports.
    """

    SONDE = (
        "import sys;sys.path.insert(0,'scripts');sys.path.insert(1,'scripts/noyau');"
        "import plan.expose;"                    # LA PORTE : entrer par elle resout le cycle
        "import chiffrer;"
        "from plan.criticite import hommes;"
        "print(list(chiffrer.MONNAIE));print(hommes.TITRES.pattern)")

    def _sonde(self, monde=None):
        env = _sans("CONSEIL_MONDE", "CONSEIL_RACINE")
        if monde:
            env["CONSEIL_MONDE"] = monde
        return subprocess.check_output(
            [_sys.executable, "-c", self.SONDE],
            cwd=racines.DEPOT, env=env).decode("utf-8").strip()

    def test_le_monde_reel_ne_bouge_pas(self):
        """Le manifeste du monde reel redit mot pour mot les defauts du code."""
        sortie = self._sonde()
        self.assertIn("dragon", sortie)
        self.assertIn("mestre", sortie)

    def test_un_autre_monde_change_la_monnaie_et_les_titres(self):
        """Sans ceci, un manifeste ignore rendrait le meme vert que l'autre
        epreuve. C'est celle-la qui prouve que le moteur a lache le decor."""
        if not os.path.isdir(os.path.join(racines.MONDES, "_epreuve")):
            raise unittest.SkipTest("mondes/_epreuve absent")
        sortie = self._sonde("_epreuve")
        self.assertIn("piece", sortie)
        self.assertIn("sieur", sortie)
        self.assertNotIn("dragon", sortie)
        self.assertNotIn("mestre", sortie)


if __name__ == "__main__":
    unittest.main()
