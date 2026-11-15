#!/usr/bin/env bash
# Usage: config-format.sh <file>...
# Reports configuration files whose layout hides what a reader looks for
# (.agents/rules/config-format.md): YAML nested past six levels, a TOML file
# taplo would change, a Nix file nixfmt would change. A formatter that is
# not installed is skipped with a note, never failed.
set -uo pipefail

status=0
missing=()
for file in "$@"; do
  [[ -f $file ]] || continue
  case $file in
    *.yaml)
      if awk -v limit=12 '{ match($0, /^ */) } RLENGTH > limit { printf "%s:%d: nested deeper than %d spaces; inline the leaf as { ... } or split the file.\n", FILENAME, FNR, limit; found = 1 } END { exit !found }' "$file"; then
        status=1
      fi
      ;;
    *.toml)
      if ! command -v taplo >/dev/null; then
        missing+=(taplo)
      elif ! taplo fmt --check "$file" >/dev/null 2>&1; then
        printf '%s: not formatted; run taplo fmt %s.\n' "$file" "$file"
        status=1
      fi
      ;;
    *.nix)
      if ! command -v nixfmt >/dev/null; then
        missing+=(nixfmt)
      elif ! nixfmt --check "$file" >/dev/null 2>&1; then
        printf '%s: not formatted; run nixfmt %s.\n' "$file" "$file"
        status=1
      fi
      ;;
  esac
done
if ((${#missing[@]})); then
  printf 'note: %s not installed, skipped (the nix shell has it).\n' "$(printf '%s\n' "${missing[@]}" | sort -u | paste -sd' ')"
fi
exit $status
