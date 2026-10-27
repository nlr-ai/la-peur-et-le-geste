import contextlib
import os
import sys
import unittest
import tempfile
import json
from pathlib import Path
from unittest import mock

SCRIPTS=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0]=[SCRIPTS,os.path.join(SCRIPTS,'noyau')]
from agents import runtime

class PlateauAdmissionTest(unittest.TestCase):
    def test_unavailable_slot_returns_waiting_without_model_call(self):
        from agents import plateau
        from agents.expose import depeche
        from agents.depeche import brief, manuel
        with tempfile.TemporaryDirectory() as tmp, \
             mock.patch.dict(os.environ, {'CONSEIL_MONDE':'lumina-prime'}), \
             mock.patch.object(runtime, 'RACINE', tmp), \
             mock.patch.object(runtime, '_essayer_reserver', return_value=None), \
             mock.patch.object(runtime, '_executer_flux') as call, \
             mock.patch.object(brief, 'les_pj', return_value=[]), \
             mock.patch.object(brief, 'brief_de', return_value={}), \
             mock.patch.object(brief, 'dossier_journee', return_value={'personnage':{'id':'quantum'}}), \
             mock.patch.object(manuel, 'manuel_de', return_value=''), \
             mock.patch.object(manuel, 'contexte_message', return_value=''), \
             mock.patch.object(plateau.work_identity, 'admettre', return_value={'attempt_id':'fixture'}), \
             mock.patch.object(plateau.work_identity, 'terminer_attempt') as finish:
            result=plateau.decision('quantum','40305',{'mission':{'id':'fixture','target':'40004'}})
            self.assertIn('waiting',result)
            self.assertEqual(finish.call_args.args[2], 'failed')
            self.assertFalse(finish.call_args.kwargs['term'])
            call.assert_not_called()

    def reserve(self, current, existing):
        with mock.patch.dict(os.environ,{'CONSEIL_MONDE':'lumina-prime','LE_CONSEIL_MODE':current}), \
             mock.patch.object(runtime,'_verrou_activites',return_value=contextlib.nullcontext()), \
             mock.patch.object(runtime,'_marqueurs_vivants',return_value=[('x',existing)]), \
             mock.patch.object(runtime,'_ecrire_json') as write:
            result=runtime._essayer_reserver('quantum','session')
            return result,write.called
    def test_plateau_waits_for_existing_day(self):
        self.assertEqual(self.reserve('plateau',{'homme':'quantum','monde':'lumina-prime','mode':'journee'}),(None,False))
    def test_day_waits_for_plateau(self):
        self.assertEqual(self.reserve('journee',{'homme':'quantum','monde':'lumina-prime','mode':'plateau'}),(None,False))
    def test_legacy_marker_is_conservative(self):
        self.assertEqual(self.reserve('plateau',{'homme':'quantum'}),(None,False))
    def test_other_person_can_work(self):
        self.assertTrue(self.reserve('plateau',{'homme':'gaia','monde':'lumina-prime'})[1])
    def test_delivery_uses_durable_reference_and_readback_without_sending(self):
        from agents import plateau, chambre
        with tempfile.TemporaryDirectory() as tmp:
            file=Path(tmp)/'discussion.json'
            file.write_text(json.dumps({'entrees':[{'de':'quantum','ref':'fixture-ref','texte':'Fixture'}]}),encoding='utf8')
            with mock.patch.dict(os.environ,{'CONSEIL_MONDE':'lumina-prime'}), \
                 mock.patch.object(chambre,'canal',return_value=str(file)), \
                 mock.patch.object(plateau.subprocess,'run',return_value=mock.Mock(returncode=0,stderr='',stdout='')) as run:
                result=plateau.deliver('quantum',{'delivery':{'recipient':'gaia','context':'40002','ref':'fixture-ref','text':'Fixture'}})
                self.assertTrue(result['deposited'])
                self.assertIn('--ref',run.call_args.args[0])
                self.assertIn('fixture-ref',run.call_args.args[0])

if __name__=='__main__':unittest.main()
