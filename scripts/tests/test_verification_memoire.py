import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agents.verification_memoire import run

class MemoryExecutionTest(unittest.TestCase):
    def test_real_comparator_and_ordered_diff_preserve_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);chamber=root/'chamber'
            (chamber/'ma-memoire').mkdir(parents=True)
            (chamber/'brouillons').mkdir()
            (chamber/'ma-memoire/ce-que-je-tiens-pour-vrai.txt').write_text('B\nA\nA\n',encoding='utf8')
            (chamber/'brouillons/temoin-memoire.txt').write_text('A\nB\n',encoding='utf8')
            result=run(chamber,Path(__file__).parent/'fixtures/juris-comparator.py',root/'evidence')
            self.assertTrue(result['ok'])
            comparison=result['comparisons'][0]
            self.assertNotEqual(comparison['before'],comparison['after'])
            self.assertIn('+A',comparison['diff'])
            self.assertEqual(result['script_result'][0]['ecarts'],[])
            self.assertIsNone(result['comparisons'][1]['diff'])
            self.assertTrue((root/'evidence/report.json').is_file())
            self.assertEqual((chamber/'ma-memoire/ce-que-je-tiens-pour-vrai.txt').read_text(),'B\nA\nA\n')

    def test_unreviewed_script_is_not_executed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);script=root/'other.py';script.write_text('raise Exception("executed")')
            with self.assertRaisesRegex(ValueError,'version_non'):
                run(root,script,root/'evidence')
            self.assertFalse((root/'evidence').exists())

if __name__=='__main__':unittest.main()
