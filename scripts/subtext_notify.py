#!/usr/bin/env python3
"""
Subtext — notifier. Fires after the weekly fetch to tell Sidd candidates are ready.

Three channels, each best-effort and independent (one failing never blocks the
others or the cron):
  1. macOS banner      — always on, zero setup (osascript)
  2. ntfy phone push    — on if SUBTEXT_NTFY_TOPIC is set
  3. email digest       — on if SUBTEXT_SMTP_USER + SUBTEXT_SMTP_PASS are set;
                          locked to send personal->personal only (Identity Gate safe)

Config comes from the repo .env (KEY=VALUE), loaded without external deps.

Usage:
    python3 scripts/subtext_notify.py [candidates.json]
    (defaults to the newest file in data/subtext/candidates/)
"""

import json
import os
import smtplib
import subprocess
import sys
import urllib.request
from email.message import EmailMessage
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANDIDATES_DIR = REPO_ROOT / "data" / "subtext" / "candidates"
ENV_PATH = REPO_ROOT / ".env"
NTFY_SERVER = "https://ntfy.sh"


def load_env() -> dict:
    """Parse KEY=VALUE lines from .env (no python-dotenv dependency)."""
    env = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            env[key.strip()] = val.strip().strip('"').strip("'")
    # Real environment overrides .env
    for k in ("SUBTEXT_NTFY_TOPIC", "SUBTEXT_SMTP_USER", "SUBTEXT_SMTP_PASS", "SUBTEXT_EMAIL_TO"):
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


def latest_candidates() -> Path:
    files = sorted(CANDIDATES_DIR.glob("*-candidates.json"))
    if not files:
        raise FileNotFoundError(f"no candidates files in {CANDIDATES_DIR}")
    return files[-1]


def load_summary(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    titles = [c["title"] for c in data.get("candidates", [])]
    return {"count": data.get("count", len(titles)), "titles": titles, "date": path.stem.replace("-candidates", "")}


def _sanitize(s: str) -> str:
    return s.replace('"', "'").replace("\\", "")


def notify_banner(summary: dict) -> str:
    body = f"{summary['count']} candidates ready — run /subtext-weekly"
    subtitle = _sanitize(summary["titles"][0]) if summary["titles"] else ""
    script = (
        f'display notification "{_sanitize(body)}" '
        f'with title "Subtext" subtitle "{subtitle}" sound name "Glass"'
    )
    subprocess.run(["osascript", "-e", script], check=True, capture_output=True, timeout=15)
    return "banner: sent"


def notify_ntfy(summary: dict, topic: str) -> str:
    lines = [f"• {t}" for t in summary["titles"][:6]]
    body = f"{summary['count']} candidates ready for {summary['date']}.\n" + "\n".join(lines)
    req = urllib.request.Request(
        f"{NTFY_SERVER}/{topic}",
        data=body.encode("utf-8"),
        headers={
            # HTTP headers must be latin-1 — keep the title ASCII (unicode lives in the body).
            "Title": "Subtext: candidates ready",
            "Priority": "default",
            "Tags": "newspaper",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return f"ntfy: {resp.status}"


def notify_email(summary: dict, user: str, password: str, to_addr: str) -> str:
    lines = [f"  • {t}" for t in summary["titles"]]
    body = (
        f"{summary['count']} TBOY candidates are ready for the {summary['date']} issue.\n\n"
        + "\n".join(lines)
        + "\n\nNext: run /subtext-weekly to draft, review, and approve."
    )
    msg = EmailMessage()
    msg["Subject"] = f"Subtext — {summary['count']} candidates ready ({summary['date']})"
    msg["From"] = user
    msg["To"] = to_addr
    msg.set_content(body)
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
        server.starttls()
        server.login(user, password)
        server.send_message(msg)
    return f"email: sent to {to_addr}"


def main() -> int:
    env = load_env()
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else latest_candidates()
    summary = load_summary(path)

    results = []
    # 1. Banner (always)
    try:
        results.append(notify_banner(summary))
    except Exception as e:
        results.append(f"banner: FAILED ({e})")

    # 2. ntfy push
    topic = env.get("SUBTEXT_NTFY_TOPIC")
    if topic:
        try:
            results.append(notify_ntfy(summary, topic))
        except Exception as e:
            results.append(f"ntfy: FAILED ({e})")
    else:
        results.append("ntfy: skipped (SUBTEXT_NTFY_TOPIC unset)")

    # 3. email — Identity Gate: from and to both default to the personal account
    user = env.get("SUBTEXT_SMTP_USER")
    password = env.get("SUBTEXT_SMTP_PASS")
    to_addr = env.get("SUBTEXT_EMAIL_TO", user or "")
    if user and password:
        try:
            results.append(notify_email(summary, user, password, to_addr))
        except Exception as e:
            results.append(f"email: FAILED ({e})")
    else:
        results.append("email: skipped (SUBTEXT_SMTP_USER/PASS unset)")

    print("notify | " + " | ".join(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
