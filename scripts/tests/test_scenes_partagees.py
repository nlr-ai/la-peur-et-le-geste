import json
import sys
import os
import socket
import subprocess
import time
import urllib.request
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parents[1] / "noyau"))
from scenes_partagees import Scenes


def monde(tmp_path):
    etat = tmp_path / "etat"
    etat.mkdir()
    date = {"annee": 1743, "lune": 5, "jour": 4, "minute": 632}
    for nom, valeur in {
        "joueurs": [{"personnage_id": p, "occupe": True} for p in ["a", "b"]],
        "presence": {"presence": {p: {"salle": "ferme"} for p in ["a", "b", "isobel"]}},
        "horloges": {p: date.copy() for p in ["a", "b"]},
    }.items():
        (etat / (nom + ".json")).write_text(json.dumps(valeur))
    scenes = Scenes(tmp_path)
    scenes.activer()
    return scenes


def dossier():
    return {"faits": ["Deux joueurs"], "actions_en_attente": [],
            "savoirs_par_joueur": {"a": ["secret"], "b": []}, "contraintes": []}


def test_accord_exige_destinataire_et_heure(tmp_path):
    scenes = monde(tmp_path)
    r = scenes.proposer("a", "b", dossier())
    assert scenes.responsable("b") == "b"
    with pytest.raises(ValueError):
        scenes.repondre(r["id"], "a", True, "faux accord")
    path = tmp_path / "etat" / "horloges.json"
    h = json.loads(path.read_text())
    h["b"]["minute"] += 161
    path.write_text(json.dumps(h))
    avant = scenes.etat()
    with pytest.raises(ValueError, match="horloges"):
        scenes.repondre(r["id"], "b", True, "prêt")
    assert scenes.etat() == avant
    assert json.loads(path.read_text()) == h
    scenes.repondre(r["id"], "b", False, "rattrapage nécessaire")
    h["a"] = h["b"].copy()
    path.write_text(json.dumps(h))
    scenes.repondre(r["id"], "b", True, "rattrapage joué")
    assert scenes.responsable("b") == "a"
    scenes.separer(r["id"], "b décide explicitement de rester")
    assert scenes.responsable("b") == "b"


def test_duo_change_de_salle_sans_nouveau_relais(tmp_path):
    scenes = monde(tmp_path)
    r = scenes.proposer("a", "b", dossier())
    scenes.repondre(r["id"], "b", True, "prêt")
    with pytest.raises(ValueError, match="team"):
        scenes.separer(r["id"])
    presence = json.loads((tmp_path / "etat" / "presence.json").read_text())
    for p in ("a", "b"):
        presence["presence"][p]["salle"] = "route"
    (tmp_path / "etat" / "presence.json").write_text(json.dumps(presence))
    scenes.suivre_mouvement(["a", "b"], "route")
    assert scenes.responsable("b") == "a"
    assert scenes.audience("b") == ["a", "b"]
    assert scenes.etat()["communes"][0]["id"] == r["id"]


def test_reponse_pnj_suit_parole_commune_question_reste_privee(tmp_path):
    scenes = monde(tmp_path)
    r = scenes.proposer("a", "b", dossier())
    scenes.repondre(r["id"], "b", True, "prêt")
    (tmp_path / "etat" / "flux.jsonl").write_text(
        '\n'.join(json.dumps(x) for x in [
            {"type": "vous", "ref": "public", "pour": ["a", "b"]},
            {"type": "question", "ref": "prive"}]))
    assert scenes.audience("a", "isobel", "public") == ["a", "b"]
    assert scenes.audience("a", "isobel", "prive") == "a"
    assert scenes.audience("a", "absent", "public") == "a"


def test_verrou_empeche_double_tour(tmp_path):
    scenes = monde(tmp_path)
    with scenes.verrou("tour"):
        with pytest.raises(RuntimeError):
            with scenes.verrou("tour", timeout=0):
                pass
    assert not (scenes.dossier / "tour.lock").exists()


def test_parloir_serveur_reponse_visible_aux_deux_apres_accord(tmp_path):
    """POST réel -> ref -> plume du parloir -> GET /scene de chaque siège."""
    scenes = monde(tmp_path)
    etat = tmp_path / "etat"
    joueurs = json.loads((etat / "joueurs.json").read_text())
    for joueur in joueurs:
        joueur["jeton"] = joueur["personnage_id"]
        joueur["depuis"] = 0
    (etat / "joueurs.json").write_text(json.dumps(joueurs))
    h = json.loads((etat / "horloges.json").read_text())
    (etat / "monde.json").write_text(json.dumps({"date": h["a"]}))
    (etat / "personnages.json").write_text('[]')
    (etat / "corps.json").write_text('{"affectations": {}}')
    (etat / "flux.jsonl").write_text('')
    depot = Path(__file__).parents[2]
    env = dict(os.environ, CONSEIL_RACINE=str(tmp_path), CONSEIL_SANS_REVEIL="1", PYTHONUTF8="1")
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        env["PORT"] = str(sock.getsockname()[1])
    server = subprocess.Popen(["node", str(depot / "serveur" / "serveur.js")],
                              env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    base = "http://127.0.0.1:" + env["PORT"]

    def requete(route, joueur, data=None):
        req = urllib.request.Request(base + route, data=json.dumps(data).encode() if data else None,
            headers={"Cookie": "jeton=" + joueur, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as rep:
            return json.load(rep)

    try:
        for _ in range(50):
            try:
                requete("/scene", "a")
                break
            except OSError:
                time.sleep(.1)
        requete("/action", "a", {"type": "libre", "mode": "dire", "texte": "fixture privée"})
        assert not requete("/scene", "b")["items"]
        r = scenes.proposer("a", "b", dossier())
        scenes.repondre(r["id"], "b", True, "accord de test")
        requete("/action", "a", {"type": "libre", "mode": "dire", "texte": "fixture publique"})
        flux = [json.loads(l) for l in (etat / "flux.jsonl").read_text().splitlines()]
        ref = flux[-1]["ref"]
        code = ("import sys;sys.path[:0]=[sys.argv[1],sys.argv[1]+'/noyau'];"
                "import agents.expose;from agents import parloir;"
                "parloir._pousser_au_flux_web('isobel','a','réponse fixture',ref=sys.argv[2])")
        result = subprocess.run([sys.executable, "-c", code, str(depot / "scripts"), ref],
                                env=env, capture_output=True, text=True, encoding="utf-8")
        assert result.returncode == 0, result.stderr
        for joueur in ("a", "b"):
            reponses = [it for it in requete("/scene", joueur)["items"] if it["type"] == "reponse"]
            assert len(reponses) == 1
            assert reponses[0]["texte"] == "réponse fixture"
            assert reponses[0]["pour"] == ["a", "b"]
        assert json.loads((etat / "horloges.json").read_text()) == h
        # Un mouvement adressé à un seul PJ entraîne sa team, sans nouvel accord.
        mouvement = {"type": "salle", "salle": "route", "lieu": "Route fixture",
                     "presents": ["a"], "duree": 2}
        result = subprocess.run([sys.executable, str(depot / "scripts" / "append_flux.py"),
            json.dumps(mouvement), "--pour", "a"], env=env, capture_output=True,
            text=True, encoding="utf-8")
        assert result.returncode == 0, result.stderr
        presence = json.loads((etat / "presence.json").read_text())["presence"]
        assert presence["a"]["salle"] == presence["b"]["salle"] == "route"
        avancees = json.loads((etat / "horloges.json").read_text())
        assert avancees["a"] == avancees["b"]
        assert avancees["a"]["minute"] == h["a"]["minute"] + 2
        assert scenes.etat()["communes"][0]["id"] == r["id"]
        assert scenes.etat()["communes"][0]["salle"] == "route"
        requete("/action", "b", {"type": "libre", "mode": "dire", "texte": "après déplacement"})
        for joueur in ("a", "b"):
            assert requete("/scene", joueur)["items"][-1]["texte"] == "après déplacement"
        explication = {"type": "reparation", "texte": "régie fixture", "duree": 0}
        result = subprocess.run([sys.executable, str(depot / "scripts" / "append_flux.py"),
            json.dumps(explication), "--pour", "b"], env=env, capture_output=True,
            text=True, encoding="utf-8")
        assert result.returncode == 0, result.stderr
        for joueur in ("a", "b"):
            assert requete("/scene", joueur)["items"][-1]["texte"] == "régie fixture"
    finally:
        server.terminate()
        server.wait(timeout=10)

