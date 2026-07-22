#!/usr/bin/env bash
set -euo pipefail

SKILL_FILE="$(dirname "$0")/SKILL.md"

if [ ! -f "$SKILL_FILE" ]; then
  echo "Error: SKILL.md not found next to this script." >&2
  exit 1
fi

# Detect target directory
TARGET_DIR=""
for dir in \
  "$HOME/.claude/skills" \
  "$HOME/.config/opencode/skills" \
  "$HOME/.local/share/claude/skills"; do
  if [ -d "$dir" ]; then
    TARGET_DIR="$dir"
    break
  fi
done

if [ -z "$TARGET_DIR" ]; then
  TARGET_DIR="$HOME/.claude/skills"
fi

mkdir -p "$TARGET_DIR"
TARGET_PATH="$TARGET_DIR/deal-inspector-SKILL.md"

if [ -f "$TARGET_PATH" ] && [ "${1:-}" != "--force" ] && [ "${1:-}" != "-f" ]; then
  read -p "$TARGET_PATH already exists. Overwrite? [y/N] " -r
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Install cancelled."
    exit 1
  fi
fi

cp "$SKILL_FILE" "$TARGET_PATH"
echo "Installed Deal Inspector to $TARGET_PATH"
echo ""
echo "Load it in Claude Code:  /skill deal-inspector"
