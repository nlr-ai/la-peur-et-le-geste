import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'noyau'))
from instructions_monde import blocs_locaux, constitution_mj


class InstructionsMondeTests(unittest.TestCase):
    def test_monde_neuf_ne_recoit_pas_westeros(self):
        with tempfile.TemporaryDirectory() as tmp:
            depot = Path(tmp)
            world = depot / 'mondes' / 'neuf'
            world.mkdir(parents=True)
            (world / 'manuel.md').write_text('MANUEL LOCAL', encoding='utf-8')
            (world / 'AGENTS.md').write_text('REGLES LOCALES', encoding='utf-8')
            paths = []
            def reader(path):
                paths.append(Path(path))
                return 'SOCLE' if Path(path).name == 'mj-socle.md' else None
            self.assertEqual(constitution_mj(world, depot, reader), 'SOCLE')
            self.assertNotIn(depot / 'CLAUDE.md', paths)
            self.assertIn('MANUEL LOCAL', '\n'.join(blocs_locaux(world, 'mj')))
            self.assertNotIn('MANUEL LOCAL', '\n'.join(blocs_locaux(world, 'pnj')))
            self.assertIn('REGLES LOCALES', '\n'.join(blocs_locaux(world, 'pnj')))

    def test_prompt_explicite_et_heritage_conserves(self):
        with tempfile.TemporaryDirectory() as tmp:
            depot = Path(tmp)
            world = depot / 'mondes' / 'ancien'
            world.mkdir(parents=True)
            def reader(path):
                path = Path(path)
                return path.read_text(encoding='utf-8') if path.is_file() else None
            (depot / 'CLAUDE.md').write_text('HERITAGE', encoding='utf-8')
            self.assertEqual(constitution_mj(world, depot, reader), 'HERITAGE')
            self.assertEqual(constitution_mj(depot, depot, reader), 'HERITAGE')
            (world / 'prompts').mkdir()
            (world / 'prompts' / 'mj.md').write_text('EXPLICITE', encoding='utf-8')
            (world / 'manuel.md').write_text('LOCAL', encoding='utf-8')
            self.assertEqual(constitution_mj(world, depot, reader), 'EXPLICITE')

    def test_instructions_relues_et_aucun_canon_injecte(self):
        with tempfile.TemporaryDirectory() as tmp:
            world = Path(tmp)
            (world / 'canon').mkdir()
            (world / 'canon' / 'secret.md').write_text('SECRET', encoding='utf-8')
            file = world / 'manuel.md'
            file.write_text('VERSION 1', encoding='utf-8')
            self.assertIn('VERSION 1', '\n'.join(blocs_locaux(world, 'mj')))
            file.write_text('VERSION 2', encoding='utf-8')
            result = '\n'.join(blocs_locaux(world, 'mj'))
            self.assertIn('VERSION 2', result)
            self.assertNotIn('SECRET', result)


if __name__ == '__main__':
    unittest.main()
