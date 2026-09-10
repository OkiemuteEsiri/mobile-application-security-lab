import unittest
from unittest.mock import patch
from datetime import date

from src.risk_register import RiskItem, render_markdown, summarize


class RiskRegisterTests(unittest.TestCase):
    def item(self, **overrides):
        values = dict(
            control_id="MASVS-STORAGE-1",
            title="Sensitive data stored insecurely",
            severity="high",
            component="local-storage",
            owner="Mobile Engineering",
            status="open",
            due_date=None,
            evidence="Synthetic static-analysis observation",
            remediation="Use platform-backed protected storage.",
            validation="Confirm sensitive values are absent from unprotected storage.",
        )
        values.update(overrides)
        return RiskItem(**values)

    def test_finding_id_is_deterministic(self):
        self.assertEqual(self.item().finding_id, self.item().finding_id)

    def test_invalid_severity_is_rejected(self):
        with self.assertRaises(ValueError):
            self.item(severity="urgent")

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            self.item(status="done")

    def test_closed_item_requires_validation_evidence(self):
        with self.assertRaises(ValueError):
            self.item(status="validated_closed", validation="")

    def test_summary_excludes_validated_closed_from_open_risk(self):
        items = [self.item(), self.item(component="network", status="validated_closed")]
        metrics = summarize(items)
        self.assertEqual(metrics["open"], 1)
        self.assertEqual(metrics["validated_closed"], 1)
        self.assertEqual(metrics["by_severity"]["high"], 1)

    def test_exposure_score_is_bounded(self):
        metrics = summarize([self.item(severity="critical"), self.item(component="network", severity="low")])
        self.assertGreaterEqual(metrics["exposure_score"], 0)
        self.assertLessEqual(metrics["exposure_score"], 100)

    def test_markdown_contains_governance_fields(self):
        report = render_markdown([self.item()])
        self.assertIn("Mobile Security Risk Register", report)
        self.assertIn("Mobile Engineering", report)
        self.assertIn("Revalidation", report)
        self.assertIn("Synthetic assessment output", report)

    def test_bad_due_date_is_rejected(self):
        with self.assertRaises(ValueError):
            self.item(due_date="10-09-2026")


if __name__ == "__main__":
    unittest.main()
