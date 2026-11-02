"""Coverage depends on graph content rather than Mermaid source wrapping."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_visual_coverage import diagram_stats, is_substantive_diagram


class VisualCoverageTests(unittest.TestCase):
    def test_compact_and_expanded_graphs_have_same_coverage(self):
        nodes = 'A["Observe"]; B["Forecast"]; C{"Admit?"}; D["Plan"]; E["Attempt"]; F["Residual"]; G["Review"]'
        edges = 'A --> B --> C; C -- eligible --> D --> E --> F; C -- refuse --> G; F -- material --> G; G --> A'
        compact = "flowchart TD\n" + nodes + "\n" + edges
        expanded = compact.replace("; ", "\n")
        self.assertEqual(diagram_stats(compact)[1:], diagram_stats(expanded)[1:])
        self.assertEqual((8, 7, 3), diagram_stats(compact)[1:])
        self.assertTrue(is_substantive_diagram(compact))
        self.assertTrue(is_substantive_diagram(expanded))

    def test_unlabeled_chains_do_not_count_as_labels(self):
        self.assertEqual(0, diagram_stats('flowchart TD\nA --> B --> C\nB -.-> D')[3])
        self.assertFalse(is_substantive_diagram('flowchart TD\nA["A"] --> B["B"]'))

    def test_existing_label_syntaxes_remain_supported(self):
        for edge in ('A -- "review" --> B', 'A -->|review| B', 'A --|review|--> B', 'A->>B: review'):
            with self.subTest(edge=edge):
                self.assertEqual(1, diagram_stats(edge)[3])


if __name__ == "__main__":
    unittest.main()
