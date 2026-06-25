#!/usr/bin/env python3
"""
Subtext — TBOY candidate-story fetcher.

Pulls recent episodes from The Best One Yet (TBOY) via yt-dlp. Each episode's
title + description becomes a candidate story for the Subtext editorial lens
(.claude/commands/viral-subtext.md).

Why no transcripts: as of 2025 YouTube walls automatic captions behind a PO
token, so yt-dlp can't fetch them without browser cookies. TBOY titles +
descriptions already carry the full story AND the hook DNA, so transcripts add
cost without adding signal. Format-DNA is derived from title/description
structure instead (see recon/format-dna.json).

Usage:
    python3 scripts/subtext_fetch.py
    python3 scripts/subtext_fetch.py --count 8
    python3 scripts/subtext_fetch.py --count 8 --no-descriptions   # fast, titles only
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

# ── Config ────────────────────────────────────────────────────────────────────
TBOY_CHANNEL_URL = "https://www.youtube.com/channel/UCly3md3CbnTFJP83lVUEcjw/videos"
TBOY_NAME = "The Best One Yet (TBOY)"
DEFAULT_COUNT = 8
DESC_MAX_CHARS = 700
LIST_TIMEOUT_S = 120
DESC_TIMEOUT_S = 60
REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "data" / "subtext" / "candidates"
# ──────────────────────────────────────────────────────────────────────────────


def _yt_dlp(args: List[str], timeout: int) -> Optional[str]:
    """Run yt-dlp, return stdout on success, None on any failure."""
    try:
        result = subprocess.run(
            ["yt-dlp", *args],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        print("ERROR: yt-dlp not found. Install with: pip install yt-dlp", file=sys.stderr)
        return None
    except subprocess.TimeoutExpired:
        print(f"WARN: yt-dlp timed out after {timeout}s", file=sys.stderr)
        return None
    if result.returncode != 0:
        print(f"WARN: yt-dlp exited {result.returncode}: {result.stderr[:200]}", file=sys.stderr)
        return None
    return result.stdout


def list_recent_episodes(count: int) -> List[Dict]:
    """Fetch recent episode id/title/url via flat-playlist (no PO token needed)."""
    out = _yt_dlp(
        [
            "--flat-playlist",
            "--print", "%(id)s\t%(title)s",
            "--playlist-end", str(count),
            "--no-warnings",
            "--quiet",
            TBOY_CHANNEL_URL,
        ],
        timeout=LIST_TIMEOUT_S,
    )
    if not out:
        return []
    episodes = []
    for line in out.strip().split("\n"):
        if "\t" not in line:
            continue
        vid, title = line.split("\t", 1)
        vid, title = vid.strip(), title.strip()
        if not vid or not title:
            continue
        episodes.append(
            {
                "video_id": vid,
                "title": title,
                "url": f"https://www.youtube.com/watch?v={vid}",
            }
        )
    return episodes


def fetch_description(video_id: str) -> str:
    """Fetch a single episode's description (full extract). Empty string on failure."""
    out = _yt_dlp(
        [
            "--skip-download",
            "--no-warnings",
            "--quiet",
            "--print", "%(description)s",
            f"https://www.youtube.com/watch?v={video_id}",
        ],
        timeout=DESC_TIMEOUT_S,
    )
    if not out:
        return ""
    desc = " ".join(out.strip().split())
    return desc[:DESC_MAX_CHARS]


def build_candidates(count: int, with_descriptions: bool) -> List[Dict]:
    """Assemble candidate stories. Descriptions are best-effort."""
    episodes = list_recent_episodes(count)
    if not episodes:
        return []
    fetched_at = datetime.now(timezone.utc).isoformat()
    for ep in episodes:
        ep["source"] = TBOY_NAME
        ep["description"] = fetch_description(ep["video_id"]) if with_descriptions else ""
        ep["fetched_at"] = fetched_at
    return episodes


def save_candidates(candidates: List[Dict]) -> Path:
    """Write candidates to data/subtext/candidates/{YYYY-MM-DD}-candidates.json."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = OUT_DIR / f"{date_str}-candidates.json"
    payload = {
        "source": TBOY_NAME,
        "channel_url": TBOY_CHANNEL_URL,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "count": len(candidates),
        "candidates": candidates,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch TBOY candidate stories for Subtext.")
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT, help="Episodes to fetch (default 8)")
    parser.add_argument("--no-descriptions", action="store_true", help="Titles only (fast)")
    args = parser.parse_args()

    candidates = build_candidates(args.count, with_descriptions=not args.no_descriptions)
    if not candidates:
        print("ERROR: fetched 0 candidates — check network or channel URL", file=sys.stderr)
        return 1

    out_path = save_candidates(candidates)
    print(f"OK: {len(candidates)} candidates → {out_path}")
    for c in candidates:
        has_desc = "desc" if c["description"] else "no-desc"
        print(f"  [{has_desc}] {c['video_id']}  {c['title'][:70]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
