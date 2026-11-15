set positional-arguments := true

import ".agents/portable/just/harness.just"

[group("gate")]
[doc("The full local gate: check, then guards.")]
[script("bash")]
ci:
    set -euo pipefail
    just check
    just guards

[group("code")]
[doc("The longest files of code, tests left out: just agent::longest 20; green to 100 lines, yellow to 200, red past")]
[script("bash")]
longest count="20":
    set -euo pipefail
    [[ $1 =~ ^[0-9]+$ ]] || { echo "a count of files" >&2; exit 1; }
    git ls-files -- '*.py' '*.sh' ':!tests/*' ':!.agents/*' | while IFS= read -r file; do
        [[ -f $file ]] || continue
        awk 'END { print NR + 0 }' "$file" | sed "s|\$| $file|"
    done | sort -rn | head -n "$1" | while read -r lines file; do
        if ((lines > 200)); then colour=31; elif ((lines > 100)); then colour=33; else colour=32; fi
        printf '\e[%sm%5d\e[0m  %s\n' "$colour" "$lines" "$file"
    done
