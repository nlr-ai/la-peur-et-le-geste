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

from agents import expose  # noqa: F401 — lie la porte avant les dépendances tardives
from agents import billet, jump, mj, parloir, portage, routeur_message as routeur


class RouteurMessageTests(unittest.TestCase):
    def test_journee_transmet_le_mj_commun_meme_pour_une_parole(self):
        for mode in ("agir", "dire"):
            with self.subTest(mode=mode), mock.patch.object(mj, "appeler_mj", return_value="ok") as appel:
                routeur._router_mj("tiers", "ref-test", {
                    "mode": mode, "texte": "Je vérifie les livraisons.",
                    "pilote_mode": "pnjpj-journee"})
                self.assertTrue(appel.call_args.kwargs["routage"]["mj_commun_journee"])
                self.assertEqual(appel.call_args.kwargs["refs"], ["ref-test"])
        with mock.patch.object(mj, "appeler_mj", return_value="ok") as appel:
            routeur._router_mj("tiers", "ref-test", {"mode":"agir", "texte":"Je marche."})
            self.assertNotIn("mj_commun_journee", appel.call_args.kwargs["routage"])

    def test_la_piece_route_directement_vers_les_habitants_presents(self):
        positions = {
            "nlr": {"salle": "archives", "etat": "arrete"},
            "filippo": {"salle": "archives", "etat": "arrete"},
            "autre-joueur": {"salle": "archives", "etat": "arrete"},
            "marcheur": {"salle": "archives", "etat": "en-chemin"},
            "ailleurs": {"salle": "quai", "etat": "arrete"},
        }
        with mock.patch("agents.routeur_message.chambre.existe",
                        return_value=True):
            presents = routeur.gens_presents(
                "nlr", positions=positions,
                joueurs={"nlr", "autre-joueur"})
        self.assertEqual(["filippo"], presents)

    def test_une_parole_va_une_fois_au_narrateur_et_laisse_un_recu(self):
        with tempfile.TemporaryDirectory() as dossier:
            inbox = os.path.join(dossier, "action.json")
            with open(inbox, "w", encoding="utf-8") as flux:
                json.dump({"ref": "r1", "mode": "dire", "texte": "Bonjour"}, flux)
            with mock.patch.object(routeur, "action_par_ref",
                                   return_value=(inbox, {"ref": "r1", "mode": "dire",
                                                        "texte": "Bonjour"})), \
                    mock.patch.object(routeur, "SORTIES", dossier), \
                    mock.patch.object(routeur, "_router_mj", return_value={
                        "mode": "dire", "mj": {"appele": True}}) as narrateur, \
                    mock.patch.object(billet, "ecrire") as ecrire:
                document = routeur.router_ref("nlr", "r1")
            narrateur.assert_called_once()
            ecrire.assert_not_called()
            self.assertTrue(os.path.exists(inbox))
            self.assertTrue(os.path.exists(os.path.join(dossier, "nlr", "r1.json")))
            self.assertEqual("routage-presence/1", document["version"])

    def test_reponse_ciblee_et_modes_normaux_sans_multiplexage(self):
        with tempfile.TemporaryDirectory() as dossier:
            for mode in ("dire", "parler", "agir", "question", "commenter", "penser"):
                action = {"ref": mode, "mode": mode, "texte": "Bonjour",
                          "destinataire_id": "filippo"}
                with mock.patch.object(routeur, "action_par_ref", return_value=("action.json", action)), \
                        mock.patch.object(routeur, "SORTIES", dossier), \
                        mock.patch.object(mj, "appeler_mj", return_value="fait") as narrateur, \
                        mock.patch.object(billet, "ecrire") as ecrire:
                    routeur.router_ref("nlr", mode)
                narrateur.assert_called_once()
                ecrire.assert_not_called()
                self.assertEqual("filippo", narrateur.call_args.kwargs["routage"]["destinataire_id"])

    def test_un_geste_va_directement_au_mj(self):
        action = {"ref": "r-geste", "type": "libre", "mode": "agir",
                  "texte": "Je retourne la pièce."}
        with mock.patch.object(mj, "appeler_mj", return_value="fait") as appeler:
            resultat = routeur._router_mj("rhaenyra", "r-geste", action)
        self.assertEqual(["r-geste"], appeler.call_args.kwargs["refs"])
        self.assertEqual("direct", appeler.call_args.kwargs["routage"]["decision"])
        self.assertTrue(resultat["mj"]["appele"])
        self.assertNotIn("transmission_pnj", appeler.call_args.kwargs["routage"])

    def test_narrateur_recoit_la_parole_exacte_a_transmettre(self):
        action = {"mode": "dire", "texte": "Vous avez dit non ?", "destinataire_id": "filippo"}
        with mock.patch.object(mj, "appeler_mj", return_value="fait") as appeler:
            routeur._router_mj("nlr", "ref-dialogue", action)
        routage = appeler.call_args.kwargs["routage"]
        self.assertEqual(routage["transmission_pnj"], {
            "de": "nlr", "ref": "ref-dialogue", "texte_exact": "Vous avez dit non ?",
            "destinataire_id": "filippo"})
        self.assertIn("premiere tranche visible", routage["consigne"])
        self.assertIn("reveil", routage["consigne"])
        self.assertIn("joue directement la reponse", routage["consigne"])
        self.assertIn("Respecte destinataire_id", routage["consigne"])
        self.assertNotIn("scripts/parloir.py --dire", routage["consigne"])

    def test_jump_garde_sa_preparation_dediee(self):
        action = {"ref": "r-jump", "type": "libre", "mode": "jump",
                  "texte": ""}
        preparation = {"version": "passer/1", "evenements": []}
        with mock.patch.object(jump, "preparer_scene",
                               return_value=preparation), \
                mock.patch.object(routeur, "_joueurs", return_value={"rhaenyra"}), \
                mock.patch.object(mj, "appeler_mj",
                                  return_value="scène jouée") as appeler:
            resultat = routeur._router_jump("rhaenyra", "r-jump", action)
        routage = appeler.call_args.kwargs["routage"]
        self.assertEqual("jump", routage["decision"])
        self.assertEqual("passer/1", routage["jump"]["version"])
        self.assertIn("première décision du joueur", routage["consigne"])
        self.assertTrue(resultat["mj"]["appele"])

    def test_un_retour_au_joueur_va_au_web_et_au_flux_mj(self):
        faux_canal = os.path.join("chambres", "canal.json")
        with mock.patch("agents.billet.deposer",
                        return_value=(faux_canal, True)) as deposer, \
                mock.patch.object(parloir, "_pousser_au_flux_web") as web, \
                mock.patch.object(mj, "deposer_retour_parloir",
                                  return_value={"id": "retour-1"}) as flux_mj, \
                mock.patch("agents.chambre.marquer_lu") as marquer:
            canal, retour = parloir.rendre_au_joueur(
                "gerardys", "rhaenyra", "Voici le chiffre.", "23030",
                "r-parole")
        deposer.assert_called_once_with("gerardys", "rhaenyra",
                                        "Voici le chiffre.",
                                        contexte_id="23030", ref="r-parole",
                                        statut=True)
        web.assert_called_once_with("gerardys", "rhaenyra",
                                    "Voici le chiffre.",
                                    contexte_id="23030", ref="r-parole")
        flux_mj.assert_called_once_with(
            "gerardys", "rhaenyra", "Voici le chiffre.",
            contexte_id="23030", ref="r-parole")
        marquer.assert_called_once_with("rhaenyra", "gerardys")
        self.assertEqual(faux_canal, canal)
        self.assertEqual("retour-1", retour["id"])

    def test_un_retour_duplique_ne_repart_ni_au_web_ni_au_mj(self):
        with mock.patch("agents.billet.deposer",
                        return_value=("canal.json", False)), \
                mock.patch.object(parloir, "_pousser_au_flux_web") as web, \
                mock.patch.object(mj, "deposer_retour_parloir") as flux_mj:
            _, retour = parloir.rendre_au_joueur(
                "gerardys", "rhaenyra", "Voici.", "23030", "r-parole")
        self.assertTrue(retour["duplicate"])
        web.assert_not_called()
        flux_mj.assert_not_called()

    def test_flux_mj_append_only_garde_les_arrivees_pendant_un_reveil(self):
        with tempfile.TemporaryDirectory() as dossier, \
                mock.patch.object(mj, "FLUX_RETOURS_PARLOIR",
                                  os.path.join(dossier, "retours.jsonl")), \
                mock.patch.object(mj, "CURSEUR_RETOURS_PARLOIR",
                                  os.path.join(dossier, "retours.lu")):
            mj.deposer_retour_parloir(
                "gerardys", "rhaenyra", "premier", "23030", "r1")
            premiers, position = mj._retours_parloir_non_lus()
            mj.deposer_retour_parloir(
                "gunthor-darklyn", "rhaenyra", "second", "20100", "r2")
            mj._marquer_retours_parloir_lus(position)
            suivants, _ = mj._retours_parloir_non_lus()
        self.assertEqual(["premier"], [x["texte"] for x in premiers])
        self.assertEqual(["r1"], [x["ref"] for x in premiers])
        self.assertEqual(["second"], [x["texte"] for x in suivants])
        self.assertEqual(["r2"], [x["ref"] for x in suivants])

    def test_le_payload_web_conserve_contexte_et_ref(self):
        with mock.patch.object(parloir, "_nom_de", return_value="Gerardys"), \
                mock.patch.object(parloir.subprocess, "run") as lancer:
            parloir._pousser_au_flux_web(
                "gerardys", "rhaenyra", "Voici.", "23030", "r-parole")
        commande = lancer.call_args.args[0]
        item = json.loads(commande[2])
        self.assertEqual("23030", item["contexte_id"])
        self.assertEqual("r-parole", item["ref"])

    def test_le_brief_mj_isole_la_ref_routee(self):
        with tempfile.TemporaryDirectory() as dossier:
            inbox = os.path.join(dossier, "etat", "inbox", "rhaenyra")
            os.makedirs(inbox)
            chemins = []
            for i, ref in enumerate(("r1", "r2")):
                chemin = os.path.join(inbox, "action-%d.json" % i)
                with open(chemin, "w", encoding="utf-8") as f:
                    json.dump({"ref": ref, "mode": "dire",
                               "texte": "texte-%s" % ref}, f)
                chemins.append(chemin)
            with mock.patch.object(portage, "ETAT", os.path.join(dossier, "etat")), \
                    mock.patch.object(portage, "FLUX",
                                      os.path.join(dossier, "etat", "flux.jsonl")):
                brief = portage.brief_message_joueur("rhaenyra", refs=["r2"])
            self.assertIn("texte-r2", brief)
            self.assertNotIn("texte-r1", brief)
            self.assertEqual([chemins[1]], mj._filtrer_actions_refs(
                chemins, ["r2"]))


if __name__ == "__main__":
    unittest.main()
