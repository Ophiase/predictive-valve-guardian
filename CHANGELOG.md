# Changelog

## 1.3.0

The 2026 modernization. The model and its features are unchanged: the
deployed trees are the same, converted from a pickle to XGBoost's own format.

- A uv workspace on Python 3.14: `libraries/valve-guardian` holds the
  dataset, the features, the model and the training; `services/dashboard`
  holds the Streamlit page.
- `infra/build` holds the image build as `docker buildx bake` files;
  `services/dashboard/Containerfile` only knows how to build itself.
- `infra/terraform` moved from `terraform/`; its `.tf` files are unchanged,
  its Makefile removed.
- The image runs as a non-root user, without uv, with a health check, and
  depends on `xgboost-cpu` instead of the CUDA build.
- The dashboard sends no usage statistics and no longer looks up the public
  IP address of the machine it runs on.
- The model is stored with `save_model` instead of `joblib`: loading it no
  longer runs code, and it survives an XGBoost upgrade.
- The Kanon agent layer: `AGENTS.md`, `.agents/`, the `just agent gate`.
- `taskipy`, the pre-commit configuration (black, isort) and the Makefiles
  are gone; `just` and ruff replace them.

## Before 1.3.0

The entries as they were written, numbering included; the package said
0.2.0 and the last tag was v1.1.0.

- v0.1.1: a justfile release mechanism, the Dockerfile cache, a lighter base
  image.
- v0.1.0: the task runner moved to `just`, the packaging to hatchling, the
  linter to ruff.
- v1.0.0: the first release, written in 2025 as a time-boxed assignment.
