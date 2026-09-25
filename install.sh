#!/bin/bash
# Install the headwork skill into ~/.claude/skills/ as a live symlink install.
#
# headwork is instructions, not a program - there is nothing to compile, no
# dependency to install and no credential to store. The directory is symlinked
# whole, so every edit to SKILL.md is immediately live.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_ROOT="$HOME/.claude/skills"

echo "=== headwork skill installer (Claude Code) ==="
echo

mkdir -p "$SKILLS_ROOT"
for src in "$SCRIPT_DIR"/skills/*/; do
  src="${src%/}"
  name="$(basename "$src")"
  target="$SKILLS_ROOT/$name"
  echo "Installing '$name' -> $target"
  rm -rf "$target"
  ln -sfn "$src" "$target"
done

echo
echo "Installed as a directory symlink - all edits are live."
echo
echo "headwork stores nothing. No credentials, no config, no state directory,"
echo "no run log. To uninstall, delete the symlink:"
echo "  rm $SKILLS_ROOT/headwork"
echo
echo "It fires on its own when you are stuck between options or cannot decide."
echo "You can also call it directly with /headwork."
echo
