#!/usr/bin/env bash
# Usage: bootstrap.sh
# The one step a pipeline runs before the recipes: uv, just and rumdl on the
# PATH, Docker with buildx and Helm checked. Everything after is `just ci` or
# `just cd`, the same as on a laptop.
set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
command -v just >/dev/null || uv tool install rust-just
command -v rumdl >/dev/null || uv tool install rumdl
docker buildx version >/dev/null
command -v helm >/dev/null || echo "helm missing: just cd needs it, or HELM_IMAGE" >&2
uv sync --frozen
