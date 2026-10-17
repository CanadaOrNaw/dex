"""Tests for documentation-only offline examples, not the Dex integration suite."""
import unittest
from offline_examples import shape_example, scoring_example


class OfflineExamples(unittest.TestCase):
    def test_shape_uses_real_filter_and_preserves_input(self):
        result = shape_example()
        self.assertEqual(result, {"types": ["choice", "noul", "score"],
                                  "runtime_only_removed": True, "input_unchanged": True})

    def test_scoring_matches_human_labels_and_rejects_missing_answer(self):
        result = scoring_example()
        self.assertEqual(result, {"predictions": ["refund", 2, True, None],
                                  "correct": 3, "scored": 3})


if __name__ == "__main__":
    unittest.main()
