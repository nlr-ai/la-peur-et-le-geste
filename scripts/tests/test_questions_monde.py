import json
import sys
from pathlib import Path
from unittest.mock import patch
import pytest
sys.path[:0] = [str(Path(__file__).parents[1]), str(Path(__file__).parents[1] / "noyau")]
import agents.expose
from agents import questions_monde as q
from agents import runtime, billet
from scenes_partagees import Scenes


def fixture(tmp_path):
    (tmp_path / "etat").mkdir()
    (tmp_path / ".agents-runtime").mkdir()
    (tmp_path / ".agents-runtime/questions-monde.json").write_text('{"pnj_autorises": true}')
    (tmp_path / "etat/personnages.json").write_text('[{"id":"isobel","nom":"Isobel"},{"id":"a"}]')
    (tmp_path / "etat/joueurs.json").write_text('[{"personnage_id":"a","occupe":true}]')


def test_question_ne_bloque_pas_tour_et_retry_ne_double_pas_appel(tmp_path, monkeypatch):
    fixture(tmp_path)
    monkeypatch.delenv("LE_CONSEIL_QUI", raising=False)
    with patch.object(q, "racine", return_value=str(tmp_path)), \
            patch.object(billet, "deposer", return_value=("canal", True)) as depot, \
            patch.object(runtime, "appeler", return_value={"result":"Fait établi, source chemins.json."}) as appel:
        with Scenes(tmp_path).verrou("tour"):
            assert q.demander("isobel", "Où mène la route ?", ref="r") == "Fait établi, source chemins.json."
            assert q.demander("isobel", "Où mène la route ?", ref="r") == "Fait établi, source chemins.json."
        assert appel.call_count == 1
        assert depot.call_args_list[1].args[0:2] == ("mj", "isobel")
        assert "ne touche ni aux horloges" in appel.call_args.kwargs["manuel"]


def test_canal_refuse_usurpation_joueur_et_monde_non_active(tmp_path, monkeypatch):
    fixture(tmp_path)
    with patch.object(q, "racine", return_value=str(tmp_path)):
        monkeypatch.setenv("LE_CONSEIL_QUI", "autre-pnj")
        with pytest.raises(ValueError, match="autre PNJ"):
            q.demander("isobel", "route ?")
        monkeypatch.delenv("LE_CONSEIL_QUI")
        with pytest.raises(ValueError, match="joueur"):
            q.demander("a", "route ?")
        (tmp_path / ".agents-runtime/questions-monde.json").write_text('{}')
        with pytest.raises(ValueError, match="activées"):
            q.demander("isobel", "route ?")
