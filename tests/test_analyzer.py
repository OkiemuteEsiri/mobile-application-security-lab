from pathlib import Path
import unittest

from src.analyzer import analyze_manifest

ROOT = Path(__file__).resolve().parents[1]


class AnalyzerTests(unittest.TestCase):
    def test_insecure_manifest_generates_expected_findings(self):
        _, findings, score = analyze_manifest(ROOT / "data" / "synthetic_insecure_manifest.xml")
        ids = {finding.control_id for finding in findings}
        self.assertTrue({"MOB-001", "MOB-002", "MOB-003", "MOB-004", "MOB-005", "MOB-006", "MOB-007"}.issubset(ids))
        self.assertGreater(score, 0)

    def test_hardened_manifest_passes_baseline(self):
        _, findings, score = analyze_manifest(ROOT / "data" / "synthetic_hardened_manifest.xml")
        self.assertEqual(findings, [])
        self.assertEqual(score, 0)


if __name__ == "__main__":
    unittest.main()
