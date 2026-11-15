#!/usr/bin/env bash
# Usage: diagrams.sh <markdown>...
# Renders every Mermaid block of the files into build/diagrams/, as PNG to
# look at and SVG to measure, and prints each one's natural width. A preview
# scales a diagram to the page: past 1350 px its text shrinks past reading,
# under 1100 px it is blown up past the headings. Exits 1 if any diagram is
# either, or fails to render. Installs mermaid-cli and a browser into the
# user's cache on first run: run it on demand.
set -euo pipefail

mermaid_cli=@mermaid-js/mermaid-cli@11.4.2
narrowest=1100
widest=1350
cache=${XDG_CACHE_HOME:-$HOME/.cache}/agents-diagrams
mmdc=$cache/node_modules/.bin/mmdc
[[ -x $mmdc ]] || npm install --silent --prefix "$cache" "$mermaid_cli" >/dev/null
root=$(git rev-parse --show-toplevel)
out=$root/build/diagrams
mkdir -p "$out"
puppeteer=$(mktemp --suffix=.json)
trap 'rm -f "$puppeteer"' EXIT
echo '{"args":["--no-sandbox"]}' >"$puppeteer"

status=0
for markdown in "$@"; do
  name=$(realpath --relative-to="$root" "$markdown" | tr '/' '-')
  name=${name%.md}
  awk -v prefix="$out/$name" '
    /^```mermaid/ { count++; file = prefix "-" count ".mmd"; next }
    /^```$/ { file = ""; next }
    file { print > file }
  ' "$markdown"
  for source in "$out/$name"-*.mmd; do
    [[ -e $source ]] || continue
    image=${source%.mmd}
    if ! "$mmdc" -q -i "$source" -o "$image.svg" -w 4000 -p "$puppeteer" >/dev/null 2>&1 ||
      ! "$mmdc" -q -i "$source" -o "$image.png" -s 2 -b '#f4efe6' -p "$puppeteer" >/dev/null 2>&1; then
      printf '%s: does not render\n' "${source#"$root"/}"
      status=1
      continue
    fi
    read -r width height < <(grep -o 'viewBox="[^"]*"' "$image.svg" | head -1 | tr -d '"' | awk '{ printf "%d %d\n", $3, $4 }')
    verdict=fits
    if ((width > widest)); then
      verdict="too wide: shrunk past reading"
    elif ((width < narrowest)); then
      verdict="too narrow: blown up past the headings"
    fi
    [[ $verdict == fits ]] || status=1
    printf '%-60s %5d x %-5d %s\n' "${image#"$root"/}.png" "$width" "$height" "$verdict"
  done
done
exit "$status"
