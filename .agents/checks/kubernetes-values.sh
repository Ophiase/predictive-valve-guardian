#!/usr/bin/env bash
# Usage: kubernetes-values.sh <file>...
# Reports what .agents/rules/infrastructure.md asks of the app-template values,
# over the files of infra/kubernetes/values among the given ones.
set -uo pipefail

checks=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
files=()
for file in "$@"; do
  [[ -f $file && $file == infra/kubernetes/values/*.yaml ]] && files+=("$file")
done
((${#files[@]})) || exit 0
exec uv run --quiet python "$checks/kubernetes_values.py" "${files[@]}"
