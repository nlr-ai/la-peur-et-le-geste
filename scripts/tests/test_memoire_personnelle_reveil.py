import pathlib
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from agents.expose import depeche  # Initialise la porte avant les modules internes.
from agents.depeche import pas_de_tir


class MemoirePersonnelleTests(unittest.TestCase):
    def test_reveil_actualise_etat_sans_effacer_notes(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(pas_de_tir, '_pensees_de', return_value=[
                {'date': {'annee': 2042, 'lune': 1, 'jour': 1}, 'texte': 'Première lecture'}]):
            pas_de_tir.poser_la_memoire(tmp, 'aria', {'intention': {'croyances': ['Mandat initial']}})
            root = pathlib.Path(tmp) / 'ma-memoire'
            croyance = root / 'ce-que-je-tiens-pour-vrai.txt'
            pensee = root / 'ce-que-jai-appris.txt'
            croyance.write_text('Une connaissance personnelle sourcée.', encoding='utf-8')
            pensee.write_text('Un souvenir de la séance.', encoding='utf-8')
            pas_de_tir.poser_la_memoire(tmp, 'aria', {'intention': {'croyances': ['Mandat actualisé']}})
            self.assertEqual(croyance.read_text(encoding='utf-8'), 'Une connaissance personnelle sourcée.')
            self.assertEqual(pensee.read_text(encoding='utf-8'), 'Un souvenir de la séance.')
            self.assertIn('Mandat actualisé', (root / 'croyances-etat.txt').read_text(encoding='utf-8'))
            self.assertIn('Première lecture', (root / 'pensees-etat.txt').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
