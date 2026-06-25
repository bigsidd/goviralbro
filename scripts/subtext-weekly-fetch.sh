#!/usr/bin/env bash
#
# Subtext weekly fetch — pulls TBOY candidate stories for the week's issue.
# Invoked by launchd (cron/com.goviralbro.subtext-fetch.plist), Sundays 8am PT.
# The lens + review stay manual: this only fills data/subtext/candidates/.
#
# Usage: subtext-weekly-fetch.sh [PIPELINE_DIR]
#   PIPELINE_DIR defaults to the repo root inferred from this script's location.

set -uo pipefail

PIPELINE_DIR="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
cd "$PIPELINE_DIR" || { echo "FATAL: cannot cd to $PIPELINE_DIR"; exit 1; }

# launchd runs with a bare PATH — add the user pip bin so yt-dlp resolves.
export PATH="/Users/siddharthshah/Library/Python/3.9/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

mkdir -p logs
{
  echo "[$(date '+%F %T %Z')] subtext fetch starting (dir=$PIPELINE_DIR)"
  /usr/bin/python3 scripts/subtext_fetch.py --count 8
  rc=$?
  echo "[$(date '+%F %T %Z')] subtext fetch done (exit $rc)"
} >> logs/subtext-fetch.log 2>&1
