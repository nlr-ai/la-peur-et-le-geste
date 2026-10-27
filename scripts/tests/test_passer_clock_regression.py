import sys, json, tempfile, pathlib, unittest
from unittest import mock
sys.path.insert(0,str(pathlib.Path('scripts').resolve()))
from agents import expose, mj
class ClockRegression(unittest.TestCase):
 def test_canonical_action_and_real_progress(self):
  with tempfile.TemporaryDirectory() as td:
   p=pathlib.Path(td);(p/'inbox/michel').mkdir(parents=True)
   start={'annee':1940,'lune':6,'jour':15,'minute':754};end=dict(start,minute=1217)
   (p/'inbox/michel/action-1.json').write_text(json.dumps({'mode':'jump','ref':'wanted','joueur_id':'michel','date_atteinte':start}),encoding='utf-8')
   route={'ref':'wanted','jump':{'version':'passer/1','depart':dict(start,jour=18),'joueurs':['michel','raymond-moreau']}}
   with mock.patch.object(mj,'ETAT',td),mock.patch.object(mj,'_items_flux_depuis',return_value=[{'type':'replique','date':end}]):
    (p/'monde.json').write_text(json.dumps({'date':end}),encoding='utf-8')
    self.assertEqual([],mj._manques_jump(route,0))
    (p/'monde.json').write_text(json.dumps({'date':start}),encoding='utf-8')
    self.assertIn('date du monde non avancée',mj._manques_jump(route,0))
    route['ref']='unrelated'
    self.assertEqual(2,len(mj._manques_jump(route,0)))
 def test_scene_still_required(self):
  route={'jump':{'version':'passer/1','depart':{'annee':1940,'lune':6,'jour':15,'minute':754}}}
  with mock.patch.object(mj,'_items_flux_depuis',return_value=[]),mock.patch.object(mj,'_lire_json',return_value={'date':{'annee':1940,'lune':6,'jour':15,'minute':1217}}):
   self.assertEqual(['prochaine scène absente du flux ou date non avancée'],mj._manques_jump(route,0))
if __name__ == '__main__':
 unittest.main()
