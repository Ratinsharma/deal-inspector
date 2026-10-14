#!/usr/bin/env bash
set -euo pipefail

die() { printf 'Error: %s\n' "$*" >&2; exit 1; }
usage() { printf 'Usage: bash install.sh [--target-dir SKILLS_ROOT] [--force]\n'; }
target_dir="$HOME/.claude/skills"
force=false
while [ "$#" -gt 0 ]; do
  case "$1" in
    --target-dir) [ "$#" -ge 2 ] || die '--target-dir needs a directory'; target_dir="$2"; shift 2 ;;
    --force|-f) force=true; shift ;;
    --help|-h) usage; exit 0 ;;
    *) die "Unknown option: $1" ;;
  esac
done
[ -n "$target_dir" ] || die 'Target directory must not be empty'
if command -v cygpath >/dev/null 2>&1; then target_dir="$(cygpath -u "$target_dir")"; fi
case "$target_dir" in /*) ;; *) target_dir="$PWD/$target_dir" ;; esac
case "$target_dir/" in */../*) die 'Use a path without .. components' ;; esac
target_dir="${target_dir%/}"
destination="$target_dir/deal-inspector"
marker="$destination/.deal-inspector-owned"
script_dir="$(cd -- "$(dirname -- "$0")" && pwd -P)"

check_path() {
  local current="$1"
  while [ -n "$current" ]; do
    [ ! -L "$current" ] || die "Linked paths are not supported: $current"
    [ "$current" != / ] || break
    current="$(dirname -- "$current")"
  done
}
hash_file() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then shasum -a 256 "$1" | awk '{print $1}'
  else die 'A SHA-256 tool (sha256sum or shasum) is required'; fi
}
check_marker() {
  [ -f "$marker" ] || die 'Existing directory has no ownership marker; refusing to overwrite it'
  [ "$(wc -l < "$marker" | tr -d ' ')" = 3 ] || die 'Invalid ownership marker'
  [ "$(sed -n '1p' "$marker")" = deal-inspector-v2 ] || die 'Invalid ownership marker'
  local skill_line license_line
  skill_line="$(sed -n '2p' "$marker")"
  license_line="$(sed -n '3p' "$marker")"
  [[ "$skill_line" =~ ^[a-f0-9]{64}\ \ SKILL\.md$ ]] || die 'Invalid ownership marker'
  [[ "$license_line" =~ ^[a-f0-9]{64}\ \ LICENSE$ ]] || die 'Invalid ownership marker'
}

check_path "$destination"
for name in SKILL.md LICENSE; do [ -f "$script_dir/$name" ] || die "$name is missing beside the installer"; done
if [ -e "$destination" ]; then
  [ -d "$destination" ] || die 'Install destination is not a directory'
  check_path "$marker"
  check_marker
  for name in SKILL.md LICENSE; do
    check_path "$destination/$name"
    if [ -e "$destination/$name" ] && [ ! -f "$destination/$name" ]; then die "Owned path is not a file: $name"; fi
  done
  [ "$force" = true ] || die 'Already installed. Use --force to replace the two owned files; local edits will be overwritten'
fi
# Check the hash tool before creating or overwriting an installation.
hash_file "$script_dir/SKILL.md" >/dev/null
mkdir -p -- "$destination"
# Stage files, then rename them, so replacing an owned file never edits a hard-linked neighbour.
stage="$(mktemp -d "$destination/.install.XXXXXX")"
trap 'rm -f -- "$stage/SKILL.md" "$stage/LICENSE" "$stage/.deal-inspector-owned"; rmdir -- "$stage" 2>/dev/null || true' EXIT
cp -- "$script_dir/SKILL.md" "$stage/SKILL.md"
cp -- "$script_dir/LICENSE" "$stage/LICENSE"
{
  printf 'deal-inspector-v2\n'
  printf '%s  SKILL.md\n' "$(hash_file "$stage/SKILL.md")"
  printf '%s  LICENSE\n' "$(hash_file "$stage/LICENSE")"
} > "$stage/.deal-inspector-owned"
for name in SKILL.md LICENSE .deal-inspector-owned; do mv -f -- "$stage/$name" "$destination/$name"; done
printf 'Installed Deal Inspector in %s\n' "$destination"
printf 'Start a new Claude Code session and invoke /deal-inspector.\n'
printf 'An old deal-inspector-SKILL.md is untouched; use uninstall.sh --legacy --force with the same target directory to remove it explicitly.\n'
