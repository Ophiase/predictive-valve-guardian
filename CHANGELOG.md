# Changelog

## 2.0.0

The legacy choices of 2025 are dropped: the page, the model and the
evaluation are rebuilt.

- Streamlit is gone. `services/api` is a typed FastAPI service
  (`/predictions`, `/model`, `/health`, OpenAPI at `/docs`);
  `services/web` is a server-rendered page that only talks to it over HTTP.
- `libraries/valve-guardian-contract` holds the pydantic models both sides
  share; the page never imports the model, the API never imports the page.
- The model is selected by repeated stratified cross-validation and a
  parsimony rule, checked on the chronological holdout, and served as ONNX.
  The deployed model is a logistic regression on 54 features: 1.5 KB instead
  of a 147 KB XGBoost.
- Every model ships with a card: features, cross-validated and holdout
  metrics, dataset hash, library versions; its identifier is a content hash.
- Training is tracked locally in `runs/`, or in MLflow, model registry
  included, when `MLFLOW_TRACKING_URI` is set; MLflow is optional.
- `libraries/valve-guardian-training` keeps scikit-learn, XGBoost and the
  ONNX converters out of the serving images.
- Two images built by bake, `valve-guardian-api` and `valve-guardian-web`,
  a compose stack in `infra/compose` (`just run`), and bjw-s app-template
  values in `infra/kubernetes`, exposed through the Gateway API.
- `just audit` lists known vulnerabilities; `just audit-licenses` the
  licences.
- `just ci` runs from any pipeline after `infra/pipeline/bootstrap.sh`:
  every check, then the images at the commit's tag, skipped when published.
- `just infra::all` and the guards hold compose and the Kubernetes values to
  `.agents/rules/infrastructure.md`: yamllint, smells, kubeconform,
  kube-linter, hadolint; `just infra::parity` compares compose and the chart.

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
