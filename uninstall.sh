#!/usr/bin/env bash
set -euo pipefail

die() { printf 'Error: %s\n' "$*" >&2; exit 1; }
usage() { printf 'Usage: bash uninstall.sh [--target-dir SKILLS_ROOT] [--force] [--legacy]\n'; }
target_dir="$HOME/.claude/skills"
force=false
legacy=false
while [ "$#" -gt 0 ]; do
  case "$1" in
    --target-dir) [ "$#" -ge 2 ] || die '--target-dir needs a directory'; target_dir="$2"; shift 2 ;;
    --force|-f) force=true; shift ;;
    --legacy) legacy=true; shift ;;
    --help|-h) usage; exit 0 ;;
    *) die "Unknown option: $1" ;;
  esac
done
[ -n "$target_dir" ] || die 'Target directory must not be empty'
if command -v cygpath >/dev/null 2>&1; then target_dir="$(cygpath -u "$target_dir")"; fi
case "$target_dir" in /*) ;; *) target_dir="$PWD/$target_dir" ;; esac
case "$target_dir/" in */../*) die 'Use a path without .. components' ;; esac
target_dir="${target_dir%/}"
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
if [ "$legacy" = true ]; then
  legacy_path="$target_dir/deal-inspector-SKILL.md"
  check_path "$legacy_path"
  if [ ! -e "$legacy_path" ]; then printf 'Legacy file is not installed in the selected directory.\n'; exit 0; fi
  [ -f "$legacy_path" ] || die 'Legacy path is not a file'
  [ "$force" = true ] || die 'Legacy ownership cannot be verified. Use --legacy --force to explicitly remove only deal-inspector-SKILL.md'
  rm -f -- "$legacy_path"
  printf 'Removed legacy file: %s\n' "$legacy_path"
  exit 0
fi
destination="$target_dir/deal-inspector"
marker="$destination/.deal-inspector-owned"
check_path "$destination"
if [ ! -e "$destination" ]; then printf 'Deal Inspector is not installed in the selected directory.\n'; exit 0; fi
[ -d "$destination" ] || die 'Install destination is not a directory'
check_path "$marker"
[ -f "$marker" ] || die 'No ownership marker; refusing to remove files'
[ "$(wc -l < "$marker" | tr -d ' ')" = 3 ] || die 'Invalid ownership marker'
[ "$(sed -n '1p' "$marker")" = deal-inspector-v2 ] || die 'Invalid ownership marker'
skill_line="$(sed -n '2p' "$marker")"
license_line="$(sed -n '3p' "$marker")"
[[ "$skill_line" =~ ^[a-f0-9]{64}\ \ SKILL\.md$ ]] || die 'Invalid ownership marker'
[[ "$license_line" =~ ^[a-f0-9]{64}\ \ LICENSE$ ]] || die 'Invalid ownership marker'
# Validate every file before removing any. Unknown files are never touched.
for name in SKILL.md LICENSE; do
  owned="$destination/$name"
  check_path "$owned"
  if [ -e "$owned" ]; then
    [ -f "$owned" ] || die "Owned path is not a file: $name"
    expected="${skill_line:0:64}"
    [ "$name" != LICENSE ] || expected="${license_line:0:64}"
    if [ "$force" = false ] && [ "$(hash_file "$owned")" != "$expected" ]; then die "$name has local changes. Use --force to remove the owned files anyway"; fi
  fi
done
rm -f -- "$destination/SKILL.md" "$destination/LICENSE" "$marker"
if ! rmdir -- "$destination" 2>/dev/null; then printf 'Other files remain in the installation folder and were preserved.\n'; fi
printf 'Uninstalled Deal Inspector from %s\n' "$destination"
