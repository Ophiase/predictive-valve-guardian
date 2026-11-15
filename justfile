mod agent
mod image "infra/build/justfile"
mod stack "infra/compose/justfile"
mod kubernetes "infra/kubernetes/justfile"
mod infra ".agents/infra.just"
mod terraform "infra/terraform/justfile"

export MLFLOW_DISABLE_TELEMETRY := "true"
export DO_NOT_TRACK := "true"
mlflow_version := "3.18.0"

default:
    @just --list

[group("run")]
[doc("Build both images and start the API on localhost:8000 and the page on localhost:8080")]
run: image::build stack::up

[group("run")]
[doc("Stop the stack started by just run")]
stop: stack::down

[group("install")]
[doc("Create the uv environment for Python 3.14, MLflow client included")]
install:
    uv sync

[group("install")]
[doc("The same environment without the optional MLflow client")]
install-minimal:
    uv sync --no-group tracking

[group("delivery")]
[doc("The tag of every image: the commit it is built from")]
image-tag:
    @git rev-parse --short=8 HEAD

[group("delivery")]
[doc("The whole CI: every check, then every image pushed to a registry at the commit's tag")]
ci registry: check
    just publish {{ registry }} "$(just image-tag)"

[group("delivery")]
[doc("Push every image at a tag unless the registry holds them; REGISTRY_USERNAME and REGISTRY_PASSWORD log in")]
[script("bash")]
publish registry tag rebuild="false":
    set -euo pipefail
    registry="{{ registry }}"
    [[ $registry == */ ]] || registry+=/
    if [[ -n ${REGISTRY_USERNAME:-} ]]; then
        DOCKER_CONFIG="$(mktemp -d)"
        export DOCKER_CONFIG
        trap 'rm -rf "$DOCKER_CONFIG"' EXIT
        printf '%s' "${REGISTRY_PASSWORD:?REGISTRY_PASSWORD goes with REGISTRY_USERNAME}" |
            docker login "${registry%%/*}" --username "$REGISTRY_USERNAME" --password-stdin
    fi
    published() {
        for image in api web; do
            docker buildx imagetools inspect "${registry}valve-guardian-$image:{{ tag }}" >/dev/null 2>&1 || return 1
        done
    }
    if [[ {{ rebuild }} != true ]] && published; then
        echo "every image is already in ${registry} at {{ tag }}"
        exit 0
    fi
    just image::push "$registry" "{{ tag }}"

[group("serve")]
[doc("Serve the API on localhost:8000; docs at /docs")]
api:
    uv run valve-guardian-api

[group("serve")]
[doc("Serve the page on localhost:8080, against the API on localhost:8000")]
web:
    VALVE_GUARDIAN_WEB_API_URL=http://127.0.0.1:8000 uv run valve-guardian-web

[group("serve")]
[doc("Serve the API and the page together; Ctrl-C stops both")]
[script("bash")]
serve:
    set -euo pipefail
    uv run valve-guardian-api &
    trap 'kill $!' EXIT
    VALVE_GUARDIAN_WEB_API_URL=http://127.0.0.1:8000 uv run valve-guardian-web

[group("model")]
[doc("Download the UCI hydraulic dataset into data/hydraulic")]
data:
    uv run valve-guardian-training data

[group("model")]
[doc("Every model on every representation, cross-validated, into docs/benchmark.md")]
benchmark:
    uv run valve-guardian-training benchmark

[group("model")]
[doc("Select, fit and export the model; tracked in runs/, or in MLflow when MLFLOW_TRACKING_URI is set")]
train:
    uv run valve-guardian-training train

[group("model")]
[doc("A local MLflow server on localhost:5000, stored in runs/mlflow; then MLFLOW_TRACKING_URI=http://127.0.0.1:5000 just train")]
mlflow:
    mkdir -p runs/mlflow
    uvx --from mlflow=={{ mlflow_version }} mlflow server --host 127.0.0.1 --port 5000 --backend-store-uri sqlite:///runs/mlflow/mlflow.db --artifacts-destination runs/mlflow/artifacts

[group("dev")]
[doc("Rewrite the code with ruff, then type-check it with ty")]
precommit:
    uv run ruff check . --fix
    uv run ruff format .
    uv run ty check .

[group("dev")]
[doc("Report style and typing defects without changing the code")]
lint:
    uv run ruff check .
    uv run ruff format --check .
    uv run ty check .

[group("dev")]
[doc("Run the tests of every library and service")]
test:
    uv run pytest

[group("dev")]
[doc("The lock is current and no locked dependency has a known vulnerability; asks the network")]
audit:
    uv lock --check
    uv audit

[group("dev")]
[doc("No locked dependency under a copyleft licence; asks the network")]
audit-licenses:
    uv run --with pip-licenses pip-licenses --partial-match --fail-on "GPL;AGPL;SSPL"

[group("dev")]
[doc("Everything that must pass before declaring work done")]
check: lint test rumdl infra::all

[group("dev")]
[doc("Check the markdown of the repository")]
rumdl:
    rumdl check .

[group("dev")]
[doc("Run the project's and the portable checks over every changed file")]
[script("bash")]
guards:
    status=0
    for check in markdown french comment-slop compose-smell kubernetes-values no-suppression no-module-docstring one-class no-protocol callable-alias hardcoded-url portable folder-size yaml-extension config-format file-length version; do
        just _guard "$check" || status=1
    done
    exit $status

_guard check:
    @.agents/portable/checks/changed-files.sh | xargs -r -d '\n' .agents/checks/run.sh {{ check }}
