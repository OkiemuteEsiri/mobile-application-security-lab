from pathlib import Path
import unittest

from src.manifest_parser import parse_manifest

ROOT = Path(__file__).resolve().parents[1]


class ManifestParserTests(unittest.TestCase):
    def test_insecure_manifest_is_parsed(self):
        profile = parse_manifest(ROOT / "data" / "synthetic_insecure_manifest.xml")
        self.assertEqual(profile.package, "com.example.synthetic")
        self.assertTrue(profile.debuggable)
        self.assertTrue(profile.allow_backup)
        self.assertTrue(profile.uses_cleartext_traffic)
        self.assertEqual(profile.target_sdk, 30)
        self.assertIn("android.permission.RECORD_AUDIO", profile.permissions)
        self.assertTrue(any(c.exported is True for c in profile.components))

    def test_hardened_manifest_is_parsed(self):
        profile = parse_manifest(ROOT / "data" / "synthetic_hardened_manifest.xml")
        self.assertFalse(profile.debuggable)
        self.assertFalse(profile.allow_backup)
        self.assertFalse(profile.uses_cleartext_traffic)
        self.assertEqual(profile.target_sdk, 35)
        self.assertIsNotNone(profile.network_security_config)


if __name__ == "__main__":
    unittest.main()
