mod agent
mod image "infra/build/justfile"
mod terraform "infra/terraform/justfile"

default:
    @just --list --list-submodules

[group("install")]
[doc("Create the uv environment for Python 3.14 and install the workspace")]
install:
    uv sync

[group("user")]
[doc("Open the dashboard on localhost:8501; extra arguments go to streamlit")]
dashboard *args:
    uv run valve-guardian-dashboard --server.port=8501 {{ args }}

[group("model")]
[doc("Download the UCI hydraulic dataset into data/hydraulic")]
data:
    uv run python -m valve_guardian.dataset

[group("model")]
[doc("Train the deployed model and overwrite its cached file")]
train:
    uv run python -m valve_guardian.training

[group("model")]
[doc("Every candidate model on every representation, best first")]
benchmark:
    uv run python -m valve_guardian.training.estimation

[group("model")]
[doc("Check the deployed model on the test cycles; downloads the dataset if absent")]
demo:
    uv run python libraries/valve-guardian/tests/demo/verify_model.py

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
[doc("Run the unit tests")]
test:
    uv run pytest

[group("dev")]
[doc("Check the lock, the known vulnerabilities and the licences; asks the network, so it stays out of the gate")]
audit:
    uv lock --check
    uv audit
    uv run --with pip-licenses pip-licenses --partial-match --fail-on "GPL;AGPL;SSPL"

[group("dev")]
[doc("Everything that must pass before declaring work done")]
check: lint test rumdl

[group("dev")]
[doc("Check the markdown of the repository")]
rumdl:
    rumdl check .

[group("dev")]
[doc("Run the project's and the portable checks over every changed file")]
[script("bash")]
guards:
    status=0
    for check in markdown french comment-slop no-suppression no-module-docstring one-class no-protocol callable-alias hardcoded-url portable folder-size yaml-extension config-format file-length version; do
        just _guard "$check" || status=1
    done
    exit $status

_guard check:
    @.agents/portable/checks/changed-files.sh | xargs -r -d '\n' .agents/checks/run.sh {{ check }}
