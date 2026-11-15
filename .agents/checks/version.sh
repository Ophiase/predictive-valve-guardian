#!/usr/bin/env bash
# Usage: version.sh <file>...
# Reports a VERSION that differs from any other file that carries the version:
# Cargo.toml, pyproject.toml, CITATION.cff. It also reports a VERSION with no
# section in CHANGELOG.md. A file that is absent is a project that does not
# use it, not a failure. Runs whatever files it is given.
set -uo pipefail

root=$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)
[[ -f $root/VERSION ]] || exit 0
version=$(tr -d '[:space:]' <"$root/VERSION")

status=0
if [[ -f $root/Cargo.toml ]]; then
  cargo=$(awk '/^\[workspace.package\]/ { inside = 1; next } /^\[/ { inside = 0 } inside && /^version/ { gsub(/[" ]/, "", $0); split($0, parts, "="); print parts[2]; exit }' "$root/Cargo.toml")
  if [[ -n $cargo && $version != "$cargo" ]]; then
    printf 'VERSION says %s, Cargo.toml says %s: bump both together.\n' "$version" "$cargo"
    status=1
  fi
fi

if [[ -f $root/pyproject.toml ]]; then
  pyproject=$(awk '/^version[[:space:]]*=/ { gsub(/[" ]/, "", $0); split($0, parts, "="); print parts[2]; exit }' "$root/pyproject.toml")
  if [[ -n $pyproject && $version != "$pyproject" ]]; then
    printf 'VERSION says %s, pyproject.toml says %s: bump both together.\n' "$version" "$pyproject"
    status=1
  fi
fi

if [[ -f $root/CITATION.cff ]]; then
  citation=$(awk '/^version:/ { print $2; exit }' "$root/CITATION.cff")
  if [[ -n $citation && $version != "$citation" ]]; then
    printf 'VERSION says %s, CITATION.cff says %s: bump both together.\n' "$version" "$citation"
    status=1
  fi
fi

if [[ -f $root/CHANGELOG.md ]] && ! grep -qE "^## ${version//./\\.}([[:space:]]|\$)" "$root/CHANGELOG.md"; then
  printf 'CHANGELOG.md has no section for %s.\n' "$version"
  status=1
fi
exit $status
