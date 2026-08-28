#!/usr/bin/env bash
set -euo pipefail

REPOSITORY="Catmint103/xilehui-brand-agent"
SKILL_NAMES=("create-xilehui-brand-poster" "xilehui-header-footer-template")
FORCE=0
TEMP_DIR=""
VERIFY_DIR=""

for argument in "$@"; do
  case "$argument" in
    --force) FORCE=1 ;;
    -h|--help)
      echo "Usage: ./install.sh [--force]"
      echo "Install the Xilehui brand and header/footer template skills into \${CODEX_HOME:-\$HOME/.codex}/skills."
      exit 0
      ;;
    *)
      echo "Unknown argument: $argument" >&2
      exit 2
      ;;
  esac
done

cleanup() {
  if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
  fi
  if [ -n "$VERIFY_DIR" ] && [ -d "$VERIFY_DIR" ]; then
    rm -rf "$VERIFY_DIR"
  fi
}
trap cleanup EXIT

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"
REPOSITORY_ROOT="${SCRIPT_DIR}"
if [ ! -f "${REPOSITORY_ROOT}/skills/create-xilehui-brand-poster/SKILL.md" ]; then
  command -v curl >/dev/null 2>&1 || { echo "curl is required" >&2; exit 1; }
  command -v tar >/dev/null 2>&1 || { echo "tar is required" >&2; exit 1; }
  TEMP_DIR="$(mktemp -d)"
  ARCHIVE="${TEMP_DIR}/repository.tar.gz"
  echo "Downloading https://github.com/${REPOSITORY} ..."
  curl -fsSL "https://github.com/${REPOSITORY}/archive/refs/heads/main.tar.gz" -o "$ARCHIVE"
  tar -xzf "$ARCHIVE" -C "$TEMP_DIR"
  SOURCE_MARKER="$(find "$TEMP_DIR" -type f -path "*/skills/create-xilehui-brand-poster/SKILL.md" -print -quit)"
  REPOSITORY_ROOT="$(dirname "$(dirname "$(dirname "$SOURCE_MARKER")")")"
fi

if [ -z "${CODEX_HOME:-}" ]; then
  if [ -z "${HOME:-}" ]; then
    echo "Neither CODEX_HOME nor HOME is available." >&2
    exit 1
  fi
  CODEX_ROOT="${HOME}/.codex"
else
  CODEX_ROOT="${CODEX_HOME}"
fi

SKILLS_ROOT="${CODEX_ROOT}/skills"
mkdir -p "$SKILLS_ROOT"

for SKILL_NAME in "${SKILL_NAMES[@]}"; do
  SOURCE_SKILL="${REPOSITORY_ROOT}/skills/${SKILL_NAME}"
  DESTINATION="${SKILLS_ROOT}/${SKILL_NAME}"
  if [ ! -f "${SOURCE_SKILL}/SKILL.md" ]; then
    echo "Skill source is missing: ${SOURCE_SKILL}" >&2
    exit 1
  fi

  if [ -e "$DESTINATION" ]; then
    if [ "$FORCE" -ne 1 ]; then
      echo "Skill already exists: $DESTINATION" >&2
      echo "Run again with --force to back up installed skills and install this version." >&2
      exit 2
    fi
    BACKUP="${DESTINATION}.backup-$(date +%Y%m%d-%H%M%S)"
    mv "$DESTINATION" "$BACKUP"
    echo "Previous installation backed up to: $BACKUP"
  fi

  mkdir -p "$DESTINATION"
  cp -R "${SOURCE_SKILL}/." "$DESTINATION/"
  echo "Installed ${SKILL_NAME} -> ${DESTINATION}"
done

if command -v python3 >/dev/null 2>&1 && python3 -c "from PIL import Image" >/dev/null 2>&1; then
  python3 "${SKILLS_ROOT}/create-xilehui-brand-poster/scripts/brand_assets.py" verify
  VERIFY_DIR="$(mktemp -d)"
  python3 "${SKILLS_ROOT}/xilehui-header-footer-template/scripts/render_template.py" \
    --output-dir "$VERIFY_DIR" \
    --set output.prefix=install-verification >/dev/null
else
  echo "Optional verification dependency missing. Run: python3 -m pip install Pillow"
fi
echo "Start a new Codex task, then invoke \$create-xilehui-brand-poster or \$xilehui-header-footer-template."
