import json
import sys
from pathlib import Path
import pytest
sys.path[:0] = [str(Path(__file__).parents[1]), str(Path(__file__).parents[1] / "noyau")]
import agents.expose
from agents.volontes_pj import Volontes

def suivi(tmp_path):
    (tmp_path / "etat").mkdir()
    items = [{"type": "vous", "joueur_id": "a", "texte": "Aller à Inverness", "ref": "aller"},
             {"type": "vous", "joueur_id": "b", "texte": "Je reste", "ref": "rester"},
             {"type": "vous", "joueur_id": "a", "texte": "Je renonce au trajet", "ref": "renoncer"}]
    (tmp_path / "etat/flux.jsonl").write_text('\n'.join(json.dumps(x) for x in items))
    return Volontes(tmp_path)

def test_stagnation_par_scene_et_progression_concrete(tmp_path):
    v = suivi(tmp_path)
    v.poser("a", "aller", "Rejoindre Inverness")
    v.debut_tour(["b"])
    assert not v.debut_tour(["a"])["a_debloquer"]
    assert v.debut_tour(["a"])["a_debloquer"] == ["aller"]
    v.actualiser("aller", "bloquee", "Raccord manquant")
    assert v.brief(["a"])["a_debloquer"] == ["aller"]
    v.actualiser("aller", "active", "Un embranchement utilisable a été trouvé")
    assert not v.brief(["a"])["a_debloquer"]
    v.actualiser("aller", "attente_joueur", "Choisir entre le pont et le gué")
    for _ in range(3):
        assert not v.debut_tour(["a"])["a_debloquer"]

def test_pas_de_volonte_inventee_ni_abandon_par_un_autre(tmp_path):
    v = suivi(tmp_path)
    with pytest.raises(ValueError):
        v.poser("a", "rester", "Rester")
    v.poser("a", "aller", "Rejoindre Inverness")
    with pytest.raises(ValueError):
        v.actualiser("aller", "abandonnee", "Il renonce", "rester")
    with pytest.raises(ValueError):
        v.actualiser("aller", "abandonnee", "Il renonce", "aller")
    v.actualiser("aller", "abandonnee", "Renoncement explicite", "renoncer")
    assert not v.brief(["a"])["volontes"]
