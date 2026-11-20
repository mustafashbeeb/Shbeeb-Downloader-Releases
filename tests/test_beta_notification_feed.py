"""Strict public metadata-only Beta32 acceptance tests and owner-private handoff."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEED = ROOT / "beta" / "android.json"
PAGE = ROOT / "beta" / "index.html"
SUMS = ROOT / "beta" / "SHA256SUMS.txt"

OWNER_PRIVATE_RELEASE = (
    "https://github.com/mustafashbeeb/Shbeeb-Downloader/"
    "releases/tag/untagged-2fc87efb09b13c838231"
)

class BetaNotificationOnlyTests(unittest.TestCase):
    def test_signed_beta32_feed_and_trusted_page(self):
        data = json.loads(FEED.read_text(encoding="utf-8"))
        self.assertEqual(set(data), {
            "packageId", "versionCode", "versionName", "minSdk",
            "notesAr", "downloadPageUrl", "urgency"
        })
        self.assertEqual(data["packageId"], "com.shbeeb.downloader.beta")
        self.assertIs(type(data["versionCode"]), int)
        self.assertEqual(data["versionCode"], 32)
        self.assertEqual(data["versionName"], "0.3.11-beta")
        self.assertEqual(data["minSdk"], 29)
        self.assertEqual(data["urgency"], "normal")
        self.assertEqual(
            data["downloadPageUrl"],
            "https://mustafashbeeb.github.io/Shbeeb-Downloader-Releases/beta/"
        )
        self.assertIn("قرّاء", data["notesAr"])

    def test_no_public_apk_binary_or_token_bearing_link(self):
        data = FEED.read_text(encoding="utf-8")
        page = PAGE.read_text(encoding="utf-8")
        self.assertNotRegex(data.lower(), r"apkurl|apkbytes|apksha256|releases/download")
        self.assertNotRegex(page.lower(), r"<script|<iframe|<form|releases/download")
        self.assertNotIn("github_pat_", page)
        self.assertNotIn("ghp_", page)
        self.assertNotIn("access_token", page.lower())
        self.assertIn("default-src 'none'", page)
        self.assertIn("noindex,nofollow", page)
        self.assertIn("0.3.11-beta", page)
        self.assertIn("لا تحذف", page)
        self.assertNotIn('class="download"', page)
        self.assertFalse(any(ROOT.rglob("*.apk")))

    def test_only_owner_private_draft_release_page_is_linked(self):
        page = PAGE.read_text(encoding="utf-8")
        urls = re.findall(r'<a\s+[^>]*href="([^"]+)"', page, flags=re.I)
        self.assertEqual(urls, [OWNER_PRIVATE_RELEASE])
        self.assertIn('rel="noopener noreferrer"', page)
        self.assertIn("المصرّح له", page)
        self.assertIn("التحميل العام لم يُفعّل", page)

    def test_signed_hash_is_manifest_not_an_apk(self):
        line = SUMS.read_text(encoding="utf-8").strip()
        self.assertRegex(line, r"^[0-9a-f]{64}  Shbeeb-BETA-v32\.apk$")
        self.assertTrue(line.startswith(
            "84e2ae1fd0e46a8a0b465f039812b199cddd31f49ba50fafcc9f7bb3369e7843"
        ))

if __name__ == "__main__":
    unittest.main()
