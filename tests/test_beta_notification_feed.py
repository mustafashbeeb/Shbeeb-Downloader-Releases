"""Strict public metadata-only Beta31 acceptance tests."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEED = ROOT / "beta" / "android.json"
PAGE = ROOT / "beta" / "index.html"
SUMS = ROOT / "beta" / "SHA256SUMS.txt"

class BetaNotificationOnlyTests(unittest.TestCase):
    def test_signed_beta31_feed_and_trusted_page(self):
        data = json.loads(FEED.read_text(encoding="utf-8"))
        self.assertEqual(set(data), {"packageId","versionCode","versionName","minSdk","notesAr","downloadPageUrl","urgency"})
        self.assertEqual(data["packageId"], "com.shbeeb.downloader.beta")
        self.assertIs(type(data["versionCode"]), int)
        self.assertEqual(data["versionCode"], 31)
        self.assertEqual(data["versionName"], "0.3.10-beta")
        self.assertEqual(data["minSdk"], 29)
        self.assertEqual(data["urgency"], "normal")
        self.assertEqual(data["downloadPageUrl"], "https://mustafashbeeb.github.io/Shbeeb-Downloader-Releases/beta/")
        self.assertTrue(data["notesAr"])

    def test_no_public_apk_or_executable_links(self):
        data = FEED.read_text(encoding="utf-8")
        page = PAGE.read_text(encoding="utf-8")
        self.assertNotRegex(data.lower(), r'apkurl|apkbytes|apksha256|releases/download')
        self.assertNotRegex(page.lower(), r'<script|<iframe|<form|<a\s|href\s*=|releases/download')
        self.assertIn("لا", page)
        self.assertNotIn('class="download"', page)
        self.assertIn("0.3.10-beta", page)
        self.assertIn("default-src 'none'", page)

    def test_signed_hash_is_a_manifest_not_an_apk(self):
        line = SUMS.read_text(encoding="utf-8").strip()
        self.assertRegex(line, r'^[0-9a-f]{64}  Shbeeb-BETA-v31\.apk$')
        self.assertTrue(line.startswith("c60c5e2cf4d85e4836f5e24d5df36a5dba11acf2313892cbe492b3dae9815531"))
        self.assertFalse(any(ROOT.rglob("*.apk")))

if __name__ == "__main__":
    unittest.main()
