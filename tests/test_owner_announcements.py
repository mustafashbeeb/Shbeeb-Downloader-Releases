"""Owner-controlled announcement publishing checks; no GitHub token or Android Push."""
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from scripts.owner_announcements import make_message, disable_message

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "owner_announcements.py"
FIXED = datetime(2026, 11, 20, 7, 0, tzinfo=timezone.utc)


class OwnerAnnouncementPublisherTests(unittest.TestCase):
    def message(self, **values):
        args = dict(title="رسالة من شبيب", body="أهلاً بكم في تطبيق شبيب.",
                    audience="beta", category="general", duration_days=7, now=FIXED)
        args.update(values)
        return make_message(**args)

    def test_valid_message_matches_android_contract(self):
        notice = self.message()
        self.assertEqual(set(notice), {"schema", "enabled", "messageId", "audience",
                      "category", "title", "body", "startsAt", "expiresAt"})
        self.assertEqual(notice["schema"], 1)
        self.assertEqual(notice["audience"], "beta")
        self.assertLessEqual(len(notice["title"]), 80)
        self.assertLessEqual(len(notice["body"]), 500)
        self.assertLessEqual(len(notice["messageId"]), 64)
        self.assertEqual(notice["expiresAt"] - notice["startsAt"], 7 * 86400)
        self.assertTrue(notice["enabled"])

    def test_multiline_text_is_safe_but_title_must_be_single_line(self):
        notice = self.message(body="السطر الأول\nالسطر الثاني")
        self.assertEqual(notice["body"], "السطر الأول\nالسطر الثاني")
        with self.assertRaises(ValueError):
            self.message(title="عنوان\nمزيف")
        with self.assertRaises(ValueError):
            self.message(body="نص\x01غير آمن")

    def test_new_publish_has_new_id_even_in_same_second(self):
        a, b = self.message(), self.message()
        self.assertNotEqual(a["messageId"], b["messageId"])

    def test_rejects_invalid_text_categories_and_duration(self):
        for kwargs in (
            {"title": ""}, {"title": "a" * 81},
            {"body": "a" * 501}, {"body": "\x00unsafe"},
            {"audience": "all-users-except-someone"}, {"category": "security"},
            {"duration_days": 0}, {"duration_days": 91},
            {"duration_days": 1.2}, {"duration_days": True},
            {"now": datetime(2026, 11, 20)},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.message(**kwargs)

    def test_disable_keeps_id_and_payload_but_turns_off(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "announcements.json"
            before = self.message()
            path.write_text(json.dumps(before, ensure_ascii=False), encoding="utf-8")
            after = disable_message(path)
            self.assertFalse(after["enabled"])
            for key, value in before.items():
                if key != "enabled":
                    self.assertEqual(after[key], value)

    def test_disable_requires_real_prior_publication(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "announcements.json"
            with self.assertRaisesRegex(ValueError, "No previously"):
                disable_message(path)
            path.write_text('{"schema":1,"enabled":true}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "invalid"):
                disable_message(path)

    def run_cli(self, cwd, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args], cwd=cwd,
            capture_output=True, text=True, check=False,
        )

    def test_public_preview_cannot_write_or_collect_messages(self):
        root = Path(__file__).resolve().parents[1]
        script = (root / "admin" / "preview.js").read_text(encoding="utf-8")
        page = (root / "admin" / "preview.html").read_text(encoding="utf-8")
        self.assertIn("textContent", script)
        self.assertNotIn("fetch(", script)
        self.assertNotIn("XMLHttpRequest(", script)
        self.assertNotIn("localStorage", script)
        self.assertIn("connect-src 'none'", page)
        self.assertNotIn("ghp_", page)

    def test_only_owner_can_publish_using_manual_workflow(self):
        root = Path(__file__).resolve().parents[1]
        wf = (root / ".github" / "workflows" / "owner-announcements.yml").read_text(
            encoding="utf-8")
        self.assertIn("github.actor == 'mustafashbeeb'", wf)
        self.assertIn("github.ref == 'refs/heads/main'", wf)
        self.assertIn("permissions:\n  contents: read", wf)
        self.assertIn("if: inputs.mode == 'publish' || inputs.mode == 'disable'", wf)
        self.assertIn("git add -- announcements.json", wf)

    def test_preview_has_no_persistent_side_effects(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli(tmp, "--mode", "preview", "--title", "مرحباً",
                                  "--body", "هذا اختبار", "--audience", "beta")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("NO changes", result.stdout)
            self.assertNotIn("هذا اختبار", result.stdout)
            self.assertFalse((Path(tmp) / "announcements.json").exists())

    def test_publish_requires_explicit_confirmation(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = ("--mode", "publish", "--title", "مرحباً",
                    "--body", "هذه رسالة من إدارة شبيب")
            no = self.run_cli(tmp, *args)
            self.assertNotEqual(no.returncode, 0)
            self.assertFalse((Path(tmp) / "announcements.json").exists())
            yes = self.run_cli(tmp, *args, "--confirm", "PUBLISH")
            self.assertEqual(yes.returncode, 0, yes.stderr)
            self.assertEqual(
                json.loads((Path(tmp) / "announcements.json").read_text(encoding="utf-8"))["audience"],
                "beta"
            )
            disable_without = self.run_cli(tmp, "--mode", "disable")
            self.assertNotEqual(disable_without.returncode, 0)
            disable_yes = self.run_cli(tmp, "--mode", "disable", "--confirm", "DISABLE")
            self.assertEqual(disable_yes.returncode, 0, disable_yes.stderr)
            self.assertFalse(
                json.loads((Path(tmp) / "announcements.json").read_text(encoding="utf-8"))["enabled"]
            )


if __name__ == "__main__":
    unittest.main()
