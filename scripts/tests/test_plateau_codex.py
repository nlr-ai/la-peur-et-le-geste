import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agents.plateau import commande_codex,lire_codex,contrat_mission,CONTRACT

class PlateauCodexTest(unittest.TestCase):
    def test_controls_follow_target_not_action_context(self):
        self.assertEqual(contrat_mission('40301', {'mission': {'target': '40002'}}), CONTRACT)
        self.assertNotEqual(contrat_mission('40002', {'mission': {'target': '40004'}}), CONTRACT)
        self.assertEqual(contrat_mission('40002', {}), CONTRACT)

    def test_model_and_isolation(self):
        command=commande_codex(Path('system.md'))
        self.assertEqual(command[command.index('--model')+1],'gpt-5.5')
        self.assertIn('--ignore-user-config',command)
        self.assertIn('read-only',command)
        self.assertIn('shell_tool',command)

    def test_final_message_and_usage(self):
        text,usage=lire_codex([{'type':'item.completed','item':{'type':'agent_message','text':'{"ok":true}'}},{'type':'turn.completed','usage':{'output_tokens':4}}])
        self.assertEqual(text,'{"ok":true}')
        self.assertEqual(usage['output_tokens'],4)

    def test_tool_call_rejected(self):
        with self.assertRaisesRegex(RuntimeError,'outil_inattendu'):
            lire_codex([{'type':'item.completed','item':{'type':'command_execution'}}])

if __name__=='__main__':unittest.main()
