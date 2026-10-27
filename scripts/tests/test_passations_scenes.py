import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
sys.path.insert(0, str(Path(__file__).parents[1] / "noyau"))
from scenes_partagees import Scenes


def partie(tmp_path):
    etat = tmp_path / "etat"
    etat.mkdir()
    date = {"annee": 1743, "lune": 5, "jour": 4, "minute": 805}
    for nom, valeur in {
        "joueurs": [{"personnage_id": p, "occupe": True} for p in ["a", "b"]],
        "presence": {"presence": {p: {"salle": "ferme", "date": date} for p in ["a", "b"]}},
        "horloges": {p: date for p in ["a", "b"]},
        "monde": {"date": date}, "personnages": [], "corps": {"affectations": {}},
    }.items():
        (etat / (nom + ".json")).write_text(json.dumps(valeur), encoding="utf-8")
    (etat / "flux.jsonl").write_text('', encoding="utf-8")
    s = Scenes(tmp_path)
    s.activer()
    r = s.proposer("a", "b", {"faits": [], "actions_en_attente": [],
        "savoirs_par_joueur": {"a": ["initial-a"], "b": ["initial-b"]}, "contraintes": []})
    s.repondre(r["id"], "b", True, "accord")
    vecu = [{"type": "recit", "texte": "fait commun", "pour": ["a", "b"]},
            {"type": "pensee", "texte": "secret-a", "pour": "a"},
            {"type": "pensee", "texte": "secret-b", "pour": "b"}]
    (etat / "flux.jsonl").write_text('\n'.join(json.dumps(x) for x in vecu) + '\n', encoding="utf-8")
    for joueur in ("a", "b"):
        dossier = etat / "inbox" / joueur
        dossier.mkdir(parents=True)
        (dossier / "action-1.json").write_text(json.dumps({"joueur_id": joueur, "ref": joueur + "-action"}))
    return s, r


def test_passation_privee_conserve_sources_et_ack_independants(tmp_path, monkeypatch):
    s, r = partie(tmp_path)
    avant = (tmp_path / "etat/horloges.json").read_bytes()
    passages = s.separer(r["id"], "b choisit une autre route", {"a": {"bilan": "pour a"}, "b": {"bilan": "pour b"}})
    assert len(passages) == 2
    for joueur, autre in (("a", "b"), ("b", "a")):
        brief = s.brief(joueur)
        assert len(brief["passations_privees"]) == 1
        texte = json.dumps(brief)
        assert "secret-" + joueur in texte
        assert "secret-" + autre not in texte
        assert "initial-" + autre not in texte
        dossier = brief["passations_privees"][0]["dossier"]
        assert dossier["actions_en_attente"][0]["ref"] == joueur + "-action"
        assert dossier["horloge"]["minute"] == 805
    assert (tmp_path / "etat/horloges.json").read_bytes() == avant
    b = passages[1]
    monkeypatch.setenv("LE_CONSEIL_SCENE", "a")
    with pytest.raises(ValueError):
        s.recevoir(b["id"], "b", True, "faux accusé")
    monkeypatch.setenv("LE_CONSEIL_SCENE", "b")
    s.recevoir(b["id"], "b", False, "Il manque le dernier engagement")
    assert s.passations_non_recues("b")[0]["statut"] == "a_completer"
    monkeypatch.setenv("LE_CONSEIL_SCENE", "a")
    s.completer(b["id"], "a", {"engagement": "bilan sourcé"})
    monkeypatch.setenv("LE_CONSEIL_SCENE", "b")
    rep = s.recevoir(b["id"], "b", True, "Sources et engagement lus")
    assert s.recevoir(b["id"], "b", True, "retry") == rep
    assert not s.passations_non_recues("b")
    assert s.passations_non_recues("a")  # l'accord de b ne vaut pas pour a
    trace = s.brief("b")["passations_privees"][-1]
    assert trace["statut"] == "recue" and "dossier" not in trace  # reçue : plus recopiée


def test_plume_interdit_reprise_avant_accuse(tmp_path):
    s, r = partie(tmp_path)
    passages = s.separer(r["id"], "Séparation explicite")
    depot = Path(__file__).parents[2]
    env = dict(os.environ, CONSEIL_RACINE=str(tmp_path), PYTHONUTF8="1", LE_CONSEIL_SCENE="b")
    commande = [sys.executable, str(depot / "scripts/append_flux.py"),
                json.dumps({"type": "recit", "texte": "reprise fixture", "duree": 1}), "--pour", "b"]
    avant = (tmp_path / "etat/flux.jsonl").read_bytes()
    rep = subprocess.run(commande, env=env, capture_output=True, text=True, encoding="utf-8")
    assert rep.returncode != 0 and "passation" in rep.stderr
    assert (tmp_path / "etat/flux.jsonl").read_bytes() == avant
    s.recevoir(passages[1]["id"], "b", True, "Dossier lu")
    rep = subprocess.run(commande, env=env, capture_output=True, text=True, encoding="utf-8")
    assert rep.returncode == 0, rep.stderr
    h = json.loads((tmp_path / "etat/horloges.json").read_text())
    assert h["b"]["minute"] == 806 and h["a"]["minute"] == 805


def test_cli_depose_puis_recoit_sans_rejouer_scene(tmp_path):
    s, r = partie(tmp_path)
    depot = Path(__file__).parents[2]
    env = dict(os.environ, CONSEIL_RACINE=str(tmp_path), PYTHONUTF8="1", LE_CONSEIL_SCENE="a")
    commande = [sys.executable, str(depot / "scripts/scenes.py")]
    rep = subprocess.run(commande + ["separer", "--id", r["id"], "--raison", "choix explicite", "--sans-reveil"],
                         env=env, capture_output=True, text=True, encoding="utf-8")
    assert rep.returncode == 0, rep.stderr
    passages = json.loads(rep.stdout)
    env["LE_CONSEIL_SCENE"] = "b"
    rep = subprocess.run(commande + ["recevoir", "--de", "b", "--id", passages[1]["id"],
        "--pret", "--message", "dossier lu"], env=env, capture_output=True, text=True, encoding="utf-8")
    assert rep.returncode == 0, rep.stderr
    assert json.loads(rep.stdout)["statut"] == "recue"
