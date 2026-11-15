#!/usr/bin/env bash
# Usage: compose-smell.sh <file>...
# Reports what .agents/rules/infrastructure.md asks of every compose service,
# over the compose files among the given ones.
set -uo pipefail

checks=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
files=()
for file in "$@"; do
  [[ -f $file && $(basename "$file") =~ ^compose.*\.yaml$ ]] && files+=("$file")
done
((${#files[@]})) || exit 0
exec uv run --quiet python "$checks/compose_smells.py" "${files[@]}"
