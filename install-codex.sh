#!/bin/bash
# Install the headwork skill for Codex.
#
# Codex does not substitute ${CLAUDE_SKILL_DIR}, so SKILL.md is rewritten with
# the real installed path and the subdirectories are symlinked alongside it.
#
# Codex has no question-box tool. headwork ships a specified text fallback for
# exactly this case - the same five parts in a fixed block, one decision per
# turn. See "The text fallback" in SKILL.md.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_ROOT="${CODEX_SKILLS_DIR:-$HOME/.codex/skills}"

echo "=== headwork skill installer (Codex) ==="
echo

mkdir -p "$SKILLS_ROOT"
for src in "$SCRIPT_DIR"/skills/*/; do
  src="${src%/}"
  name="$(basename "$src")"
  target="$SKILLS_ROOT/$name"
  echo "Installing '$name' -> $target"
  mkdir -p "$target"
  # Clear what a previous install symlinked, so a directory removed upstream
  # does not survive as a dangling link that still looks installed. Only
  # symlinks are removed, so a real SKILL.md is never at risk.
  find "$target" -mindepth 1 -maxdepth 1 -type l -exec rm -f {} +
  for sub in references tests; do
    [ -d "$src/$sub" ] && ln -sfn "$src/$sub" "$target/$sub"
  done
  sed "s#\${CLAUDE_SKILL_DIR}#$target#g" "$src/SKILL.md" > "$target/SKILL.md"
done

echo
echo "Installed for Codex."
echo
echo "Codex has no question box, so headwork uses its text fallback: the same"
echo "explainer, the same justified options, the recommendation named first,"
echo "one decision per turn."
echo
echo "headwork stores nothing - no credentials, no config, no state directory."
echo
