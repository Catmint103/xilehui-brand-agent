#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: scripts/create-workspace.sh <target-directory>" >&2
  exit 2
fi

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPOSITORY_ROOT="$(dirname "$SCRIPT_DIR")"
TARGET="$1"

if [ -e "$TARGET" ] && [ "$(find "$TARGET" -mindepth 1 -maxdepth 1 -print -quit 2>/dev/null)" ]; then
  echo "Target must not exist or must be empty: $TARGET" >&2
  exit 2
fi

mkdir -p "$TARGET/inputs" "$TARGET/outputs"
cp "$REPOSITORY_ROOT/AGENTS.md" "$TARGET/AGENTS.md"
touch "$TARGET/inputs/.gitkeep" "$TARGET/outputs/.gitkeep"

echo "Created JoyBrand workspace: $TARGET"
echo "Install the skill with: $REPOSITORY_ROOT/install.sh"
echo "Then start Codex with: codex --cd \"$TARGET\""
