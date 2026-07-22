#!/usr/bin/env bash
set -euo pipefail

FOUND=false
for path in \
  "$HOME/.claude/skills/deal-inspector-SKILL.md" \
  "$HOME/.config/opencode/skills/deal-inspector-SKILL.md" \
  "$HOME/.local/share/claude/skills/deal-inspector-SKILL.md"; do
  if [ -f "$path" ]; then
    rm "$path"
    echo "Removed $path"
    FOUND=true
  fi
done

if [ "$FOUND" = false ]; then
  echo "Deal Inspector is not installed."
  exit 1
fi

echo "Deal Inspector uninstalled."
