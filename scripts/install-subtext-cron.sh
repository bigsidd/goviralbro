#!/usr/bin/env bash
#
# Install (or uninstall) the Subtext weekly-fetch launchd job.
# Runs scripts/subtext-weekly-fetch.sh every Sunday at 8:00 AM local (Pacific).
#
# Usage:
#   ./scripts/install-subtext-cron.sh            # install + load
#   ./scripts/install-subtext-cron.sh --uninstall
#   ./scripts/install-subtext-cron.sh --dry-run

set -euo pipefail

LABEL="com.goviralbro.subtext-fetch"
PIPELINE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SRC_PLIST="$PIPELINE_DIR/cron/$LABEL.plist"
DEST_PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

mode="install"
[[ "${1:-}" == "--uninstall" ]] && mode="uninstall"
[[ "${1:-}" == "--dry-run" ]] && mode="dry-run"

if [[ "$mode" == "uninstall" ]]; then
  launchctl unload "$DEST_PLIST" 2>/dev/null || true
  rm -f "$DEST_PLIST"
  echo "Uninstalled $LABEL"
  exit 0
fi

if [[ ! -f "$SRC_PLIST" ]]; then
  echo "FATAL: $SRC_PLIST not found"; exit 1
fi

echo "Pipeline dir : $PIPELINE_DIR"
echo "Plist source : $SRC_PLIST"
echo "Plist dest   : $DEST_PLIST"

if [[ "$mode" == "dry-run" ]]; then
  echo "(dry-run) would substitute __PIPELINE_DIR__ and load into launchd"
  exit 0
fi

mkdir -p "$HOME/Library/LaunchAgents" "$PIPELINE_DIR/logs"
sed "s|__PIPELINE_DIR__|$PIPELINE_DIR|g" "$SRC_PLIST" > "$DEST_PLIST"
launchctl unload "$DEST_PLIST" 2>/dev/null || true
launchctl load "$DEST_PLIST"
echo "Loaded $LABEL — runs Sundays 8:00 AM Pacific."
launchctl list | grep "$LABEL" || echo "(note: not shown in launchctl list until next agent refresh)"
