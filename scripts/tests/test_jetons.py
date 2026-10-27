# -*- coding: utf-8 -*-
"""La forme commune des jetons, pour les trois fournisseurs."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.jetons import jetons


class Jetons(unittest.TestCase):
    def test_codex_retire_le_cache_de_l_entree(self):
        c = jetons({"usage": {"input_tokens": 1000, "cached_input_tokens": 800,
                              "output_tokens": 50,
                              "reasoning_output_tokens": 20}})
        self.assertEqual(c, {"entree": 200, "cache_lue": 800,
                             "cache_ecrite": 0, "sortie": 50,
                             "raisonnement": 20})

    def test_claude_garde_son_cout(self):
        c = jetons({"total_cost_usd": 0.12,
                    "usage": {"input_tokens": 10, "output_tokens": 300,
                              "cache_read_input_tokens": 9000,
                              "cache_creation_input_tokens": 400}})
        self.assertEqual(c["entree"], 10)
        self.assertEqual(c["cache_ecrite"], 400)
        self.assertEqual(c["cout_usd"], 0.12)

    def test_gemini(self):
        c = jetons({"usageMetadata": {"promptTokenCount": 500,
                                      "cachedContentTokenCount": 100,
                                      "candidatesTokenCount": 40,
                                      "thoughtsTokenCount": 7}})
        self.assertEqual((c["entree"], c["cache_lue"], c["sortie"],
                          c["raisonnement"]), (400, 100, 40, 7))

    def test_rien_dit_rien_invente(self):
        self.assertIsNone(jetons(None))
        self.assertIsNone(jetons({"usage": {}}))
        self.assertIsNone(jetons({"total_cost_usd": 0.0, "result": "x"}))


if __name__ == "__main__":
    unittest.main()
