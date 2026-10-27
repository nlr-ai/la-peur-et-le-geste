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

# La porte charge les paquets dans leur ordre canonique ; importer mj
# directement court-circuite cet ordre et cree une fausse boucle depeche/expose.
from agents.expose import reveiller_main  # noqa: F401
from agents import mj, portage


def _spectacle():
    with open(mj.MJ_SPECTACLE_MD, encoding="utf-8") as f:
        return f.read()


class MessageJoueurTests(unittest.TestCase):
    def test_premiere_tranche_demandee_avant_les_appels_pnj(self):
        from agents.expose import runtime
        from scenes_partagees import Scenes
        with mock.patch.object(Scenes, "__init__", return_value=None), \
                mock.patch.object(Scenes, "active", new_callable=mock.PropertyMock, return_value=False), \
                mock.patch.object(mj.chambre, "ouvrir", return_value="chambre-test"), \
                mock.patch.object(mj, "_manuel", return_value="manuel"), \
                mock.patch.object(mj, "_message", return_value="message joueur"), \
                mock.patch.object(mj, "_retours_parloir_non_lus", return_value=([], 0)), \
                mock.patch.object(mj, "_marquer_retours_parloir_lus"), \
                mock.patch("agents.mj_generation.compter_tour"), \
                mock.patch.object(mj, "_types_flux_depuis", return_value=["recit"]), \
                mock.patch.object(runtime, "appeler", return_value={"result": "fait"}) as appel:
            mj._appeler_mj("rhaenyra", "Bonjour", "POST")
        message = appel.call_args.kwargs["message"]
        self.assertNotIn("PREMIERE REPONSE", message)
        self.assertNotIn("GARDE CONTRE LES BOUCLES", message)
        reveil = _spectacle()
        self.assertIn("Ouvre le tour par un premier item visible", reveil)
        self.assertIn("Cette tranche ne termine pas le tour", reveil)
        self.assertIn("Garde contre les boucles", reveil)

    def test_le_monde_peut_remplacer_constitution_et_spectacle(self):
        monde = os.path.dirname(mj.ETAT)
        manuel = self._manuel_avec({
            os.path.join(monde, "prompts", "mj.md"): "CONSTITUTION LOCALE",
            os.path.join(monde, "prompts", "mj-spectacle.md"): "SCENE LOCALE",
            mj.MANUEL_MJ_RACINE: "CONSTITUTION VOISINE",
            mj.MJ_SPECTACLE_MD: "SCENE VOISINE",
        }, partie=None)
        self.assertIn("CONSTITUTION LOCALE", manuel)
        self.assertIn("SCENE LOCALE", manuel)
        self.assertNotIn("VOISINE", manuel)

    def test_message_joueur_n_est_pas_un_arbitrage(self):
        brief = ("== BRIEF MESSAGE JOUEUR — rhaenyra\n"
                 "ACTION C:\\inbox\\action-1.json · ref abc\n"
                 "FIL CANONIQUE DU PJ : C:\\etat\\flux.jsonl\n"
                 "  L42 · 13h07 · intervention · - | recommencons")
        with mock.patch.object(mj, "date_du_monde",
                               return_value=(129, 4, 4)):
            message = mj._message(
                "rhaenyra", brief, "JOUEUR")

        self.assertIn("[JOUEUR]", message)
        self.assertIn("FIL CANONIQUE DU PJ", message)
        self.assertIn("L42", message)
        self.assertIn("--pour rhaenyra", message)
        self.assertNotIn("CADRE DU TOUR PJ", message)
        self.assertNotIn("Tu es l'arbitre", message)
        reveil = _spectacle()
        self.assertIn("jamais par billet ni parloir", reveil)
        self.assertIn("Ferme le tour par un SECOND item visible", reveil)
        self.assertIn("plusieurs poussées par tour sont normales", reveil)
        self.assertIn("Un item refusé se lit", reveil)

    def test_brief_joueur_pointe_inbox_et_lignes_du_fil(self):
        with tempfile.TemporaryDirectory() as dossier:
            inbox = os.path.join(dossier, "etat", "inbox", "rhaenyra")
            os.makedirs(inbox)
            action = os.path.join(inbox, "action-1.json")
            with open(action, "w", encoding="utf-8") as f:
                json.dump({"mode": "question", "ref": "ref-42",
                           "recu_a": "maintenant",
                           "texte": "Le texte exact"}, f)
            flux = os.path.join(dossier, "etat", "flux.jsonl")
            with open(flux, "w", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps({"type": "recit", "pour": "daemon",
                                    "texte": "cache"}) + "\n")
                for i in range(10):
                    f.write(json.dumps({"type": "recit",
                                        "pour": "rhaenyra",
                                        "ref": ("ref-42" if i == 9 else None),
                                        "texte": ("Le texte exact" if i == 9
                                                  else "item-%d" % i)}) + "\n")
            with mock.patch.object(portage, "ETAT", os.path.join(dossier, "etat")), \
                    mock.patch.object(portage, "FLUX", flux), \
                    mock.patch.object(portage, "matiere_du_message",
                                      return_value="\nREGISTRE CIBLE\n"):
                brief = portage.brief_message_joueur("rhaenyra")

            self.assertIn(os.path.abspath(action), brief)
            self.assertIn("ref ref-42", brief)
            self.assertIn("TEXTE EXACT : Le texte exact", brief)
            self.assertIn("DANS LE FLUX : L11", brief)
            self.assertIn(os.path.abspath(flux), brief)
            self.assertIn("L4", brief)
            self.assertIn("L11", brief)
            self.assertNotIn("item-0", brief)
            self.assertNotIn("cache", brief)
            self.assertIn("REGISTRE CIBLE", brief)

    def test_message_du_front_joueur_reste_un_arbitrage(self):
        with mock.patch.object(mj, "date_du_monde",
                               return_value=(129, 4, 4)):
            message = mj._message("daemon", "mon rapport", "POST")

        self.assertIn("[POST] daemon te reveille", message)
        self.assertIn("mon rapport", message)
        self.assertNotIn("[JOUEUR]", message)
        self.assertIn("Un billet paie son péage", _spectacle())

    def test_le_lanceur_constate_les_items_pousses_directement(self):
        with tempfile.TemporaryDirectory() as dossier:
            flux = os.path.join(dossier, "flux.jsonl")
            with open(flux, "w", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps({"type": "question"}) + "\n")
            with mock.patch.object(mj, "FLUX", flux):
                position = mj._position_flux()
                with open(flux, "a", encoding="utf-8", newline="\n") as f:
                    f.write(json.dumps({"type": "recit"}) + "\n")
                    f.write(json.dumps({"type": "replique"}) + "\n")
                self.assertEqual(["recit", "replique"],
                                 mj._types_flux_depuis(position))

    def test_le_lanceur_reconnait_l_appel_direct_a_la_porte(self):
        self.assertTrue(mj._a_pousse_flux({
            "gestes": ["command_execution python scripts/append_flux.py {...}"]
        }))
        self.assertFalse(mj._a_pousse_flux({"gestes": []}))

    def test_retirer_actions_ne_touche_que_l_instantane(self):
        with tempfile.TemporaryDirectory() as dossier:
            anciens = [os.path.join(dossier, "action-1.json"),
                       os.path.join(dossier, "action-2.json")]
            nouveau = os.path.join(dossier, "action-3.json")
            for chemin in anciens + [nouveau]:
                with open(chemin, "w", encoding="utf-8") as f:
                    f.write("{}")

            mj._retirer_actions(anciens)

            self.assertFalse(any(os.path.exists(p) for p in anciens))
            self.assertTrue(os.path.exists(nouveau))

    def test_un_run_de_rapport_exige_une_replique(self):
        with tempfile.TemporaryDirectory() as dossier:
            action = os.path.join(dossier, "action-1.json")
            with open(action, "w", encoding="utf-8") as f:
                json.dump({"mode": "run",
                           "texte": "obtiens le rapport reel d'Alys"}, f)
            self.assertTrue(mj._actions_exigent_replique([action]))
            self.assertFalse(mj._actions_exigent_replique([]))

    def test_un_parloir_dans_les_gestes_exige_une_replique(self):
        self.assertTrue(mj._a_interroge_un_pnj({
            "gestes": ["command_execution python scripts/parloir.py --dire"]}))
        self.assertFalse(mj._a_interroge_un_pnj({"gestes": []}))

    def _manuel_avec(self, contenus, partie="reine-des-enfers"):
        with mock.patch.object(mj, "lire",
                               side_effect=lambda p: contenus.get(p)), \
                mock.patch.object(mj, "_partie_active", return_value=partie), \
                mock.patch.object(mj.chambre, "chemin",
                                  return_value="C:\\chambre-mj"):
            return mj._manuel()

    def test_le_mj_principal_recoit_le_claude_racine_en_premier(self):
        manuel = self._manuel_avec({
            mj.MANUEL_MJ_RACINE: "CONSTITUTION RACINE",
            mj.MJ_SPECTACLE_MD: "MANUEL SPECTACLE",
            mj.MJ_PARTIE_MD: "MANUEL DE L'ARBITRE",
            mj.REGLES_PARTIE_MD: "LIVRE DE REGLES",
        })
        self.assertLess(manuel.index("CONSTITUTION RACINE"),
                        manuel.index("MANUEL SPECTACLE"))
        self.assertLess(manuel.index("MANUEL SPECTACLE"),
                        manuel.index("MANUEL DE L'ARBITRE"))
        self.assertLess(manuel.index("MANUEL DE L'ARBITRE"),
                        manuel.index("LIVRE DE REGLES"))
        self.assertIn("# Le livre de règles de la partie", manuel)

    def test_le_mj_a_les_regles_de_la_partie_quand_elle_est_active(self):
        """Le 3.9, le MJ etait reveille sur un coup du conseil de guerre sans
        avoir jamais lu mj-partie.md, et il repartait faire autre chose. Un
        arbitre a qui l'on ne donne pas les regles n'arbitre pas : le manuel
        REFUSE de se monter sans elles — le manuel de l'arbitre ET le livre
        de regles (audit du 7.9, C1 : le manuel cite les regles par adresse
        sans en porter le texte)."""
        with self.assertRaises(SystemExit):
            self._manuel_avec({
                mj.MANUEL_MJ_RACINE: "CONSTITUTION RACINE",
                mj.MJ_SPECTACLE_MD: "MANUEL SPECTACLE",
            })
        with self.assertRaises(SystemExit):
            self._manuel_avec({
                mj.MANUEL_MJ_RACINE: "CONSTITUTION RACINE",
                mj.MJ_SPECTACLE_MD: "MANUEL SPECTACLE",
                mj.MJ_PARTIE_MD: "MANUEL DE L'ARBITRE",
            })

    def test_sans_partie_active_le_mj_ne_recoit_rien_de_la_partie(self):
        """Audit du 7.9, C1 : un reveil ordinaire n'a rien a faire d'un
        wargame — ni le manuel de l'arbitre ni le livre de regles ne se
        chargent quand `_courante.json` ne nomme aucune partie vivante, et
        leur absence sur disque n'est alors pas une faute."""
        manuel = self._manuel_avec({
            mj.MANUEL_MJ_RACINE: "CONSTITUTION RACINE",
            mj.MJ_SPECTACLE_MD: "MANUEL SPECTACLE",
            mj.MJ_PARTIE_MD: "MANUEL DE L'ARBITRE",
            mj.REGLES_PARTIE_MD: "LIVRE DE REGLES",
        }, partie=None)
        self.assertIn("CONSTITUTION RACINE", manuel)
        self.assertNotIn("MANUEL DE L'ARBITRE", manuel)
        self.assertNotIn("LIVRE DE REGLES", manuel)
        self.assertEqual(manuel, self._manuel_avec({
            mj.MANUEL_MJ_RACINE: "CONSTITUTION RACINE",
            mj.MJ_SPECTACLE_MD: "MANUEL SPECTACLE",
        }, partie=None))


if __name__ == "__main__":
    unittest.main()
