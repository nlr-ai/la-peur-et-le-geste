# -*- coding: utf-8 -*-
"""Le mode session-claude-guetteur : billet déposé, rendu par la session."""
import os
import sys
import threading
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "noyau"))

from agents import guichet_mj  # noqa: E402


def test_billet_rendu_et_flux_constate(tmp_path):
    flux = tmp_path / "etat" / "flux.jsonl"
    flux.parent.mkdir()
    flux.write_text("", encoding="utf-8")
    d = guichet_mj.dossier(str(tmp_path))

    def session():
        while not guichet_mj.en_souffrance(d):
            time.sleep(0.05)
        ident = guichet_mj.en_souffrance(d)[0]
        texte = guichet_mj.lire(d, ident)
        assert "MANUEL DU MJ CHANGE" in texte and "[JOUEUR]" in texte
        assert 'LE_CONSEIL_REF="r1"' in texte
        flux.write_text('{"type":"recit"}\n', encoding="utf-8")
        guichet_mj.rendre(d, ident, "fait", ["parloir.py"])

    t = threading.Thread(target=session)
    t.start()
    rep = guichet_mj.appeler("# manuel", "[JOUEUR] x", "sid",
                             {"LE_CONSEIL_REF": "r1"}, str(flux),
                             timeout=10, monde=str(tmp_path))
    t.join()
    assert rep["result"] == "fait"
    assert rep["provider"] == guichet_mj.MODE
    assert set(rep["gestes"]) == {"parloir.py", "append_flux.py"}
    assert guichet_mj.en_souffrance(d) == []


def test_mode_par_env(monkeypatch):
    monkeypatch.setenv("LE_CONSEIL_MJ_FOURNISSEUR", "session")
    assert guichet_mj.mode_mj() == guichet_mj.MODE
    monkeypatch.setenv("LE_CONSEIL_MJ_FOURNISSEUR", "defaut")
    assert guichet_mj.mode_mj() is None
