#!/usr/bin/env python3
"""Owner-only GitHub Actions helper for a read-only in-app announcement feed.

This never distributes APKs, sends push notifications or collects users' data.
Preview does not write or print message text to public action logs.
"""
import argparse
import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

REQUIRED_KEYS = {
    "schema", "enabled", "messageId", "audience", "category",
    "title", "body", "startsAt", "expiresAt",
}
TARGET_FILE = Path("announcements.json")


def clean(value: str, max_length: int, name: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > max_length:
        raise ValueError(f"Invalid {name}: expected nonempty text of at most {max_length} chars")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        raise ValueError(f"Invalid {name}: control characters are not allowed")
    return value.strip()


def make_message(title, body, audience, category, duration_days, now=None):
    title = clean(title, 80, "title")
    body = clean(body, 500, "body")
    if audience not in {"all", "beta", "production"}:
        raise ValueError("Unrecognized audience")
    if category not in {"general", "maintenance", "apps"}:
        raise ValueError("Unrecognized announcement category")
    if isinstance(duration_days, bool) or not isinstance(duration_days, int) or not 1 <= duration_days <= 90:
        raise ValueError("Duration must be 1–90 whole days")
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("Clock must be timezone-aware")
    stamp = now.astimezone(timezone.utc)
    code = hashlib.sha256((title + "\n" + body).encode("utf-8")).hexdigest()[:8]
    message_id = "owner-" + stamp.strftime("%Y%m%dT%H%M%S") + "-" + code
    return {
        "schema": 1,
        "enabled": True,
        "messageId": message_id,
        "audience": audience,
        "category": category,
        "title": title,
        "body": body,
        "startsAt": int(stamp.timestamp()),
        "expiresAt": int((stamp + timedelta(days=duration_days)).timestamp()),
    }


def disable_message(path=TARGET_FILE):
    if not path.is_file():
        raise ValueError("No previously published announcement exists to disable")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) != REQUIRED_KEYS or data.get("schema") != 1:
        raise ValueError("Existing announcement is invalid")
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", data.get("messageId", "")):
        raise ValueError("Existing messageId is invalid")
    data["enabled"] = False
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["preview", "publish", "disable"], default="preview")
    parser.add_argument("--title", default="")
    parser.add_argument("--body", default="")
    parser.add_argument("--audience", default="beta")
    parser.add_argument("--category", default="general")
    parser.add_argument("--duration-days", type=int, default=7)
    parser.add_argument("--confirm", default="")
    args = parser.parse_args()
    if args.mode == "disable":
        if args.confirm != "DISABLE":
            raise SystemExit("Refusing disable without exact DISABLE confirmation")
        message = disable_message()
    else:
        message = make_message(
            args.title, args.body, args.audience, args.category, args.duration_days
        )
        if args.mode == "publish" and args.confirm != "PUBLISH":
            raise SystemExit("Refusing publication without exact PUBLISH confirmation")

    if args.mode == "preview":
        print("Preview validation successful. NO changes or messages published.")
        print("Audience:", message["audience"])
        print("Category:", message["category"])
        print("Title characters:", len(message["title"]))
        print("Body characters:", len(message["body"]))
        print("Use the local-only dashboard preview for visual checking.")
        return

    TARGET_FILE.write_text(json.dumps(message, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print("Owner publication file prepared:", TARGET_FILE)
    print("Mode:", args.mode)
    print("Message ID:", message["messageId"])


if __name__ == "__main__":
    main()
