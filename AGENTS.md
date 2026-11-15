# AGENTS.md

Instructions for any coding agent in this repository. Claude Code reads them
through `.claude/CLAUDE.md`.

## What this project is

A binary classifier that says, cycle by cycle, whether the valve of a
hydraulic test rig is in optimal condition, from its pressure (PS2) and flow
(FS1) signals; a typed API that serves it; a page that uses the API like any
other client. The 2025 version, written for an assignment, is the `v1.3.0`
tag.

## Language

English everywhere: code, comments, markdown, commits. The author may write to
you in French; answer in French, write files in English.

## Before working

Read the reference projects whose paths are in
`.agents/local/projects.yaml` (gitignored; template:
[.agents/local.example.yaml](.agents/local.example.yaml)), only those marked
`granted` and only within their `scope`, and the Python rules in
[.agents/portable/rules/python.md](.agents/portable/rules/python.md).

## Toolchain

- Python 3.14, managed by `uv` as a workspace: the root `pyproject.toml`
  lists the members, `uv.lock` pins them all. Never `pip install`.
- `just install` syncs it, MLflow client included; `just install-minimal`
  leaves MLflow out. `just serve` runs the API and the page.
- `just lint` is `ruff check`, `ruff format --check` and `ty check`.
  `just precommit` fixes what it can.
- `just agent gate` is the one command to declare work done: `just check`
  (lint, tests, markdown) then `just guards`.
- `just data`, `just benchmark` and `just train` download the UCI dataset if
  absent: a network call, so never in the gate. `just audit` and
  `just audit-licenses` ask the network too.
- `just run` builds both images and starts them with compose.
- `just ci <registry>` is the CI; a pipeline runs
  `infra/pipeline/bootstrap.sh` then only that ([infra/README.md](infra/README.md)).
- `just infra::all` holds compose, the Kubernetes values and the
  Containerfiles to [infrastructure](.agents/rules/infrastructure.md); it
  runs inside `just check`.
- CI exists and runs by hand only; activating it is the author's consent.

## Layout

- [libraries/valve-guardian-contract](libraries/valve-guardian-contract/README.md):
  pydantic models shared by every side.
- [libraries/valve-guardian](libraries/valve-guardian/README.md): features,
  ONNX inference, the deployed model.
- [libraries/valve-guardian-training](libraries/valve-guardian-training/README.md):
  evaluation, selection, export, tracking.
- [services/api](services/api/README.md): FastAPI, `/predictions`, `/model`,
  `/health`.
- [services/web](services/web/README.md): the page, an HTTP client of the API.
- [infra](infra/README.md): build, compose, Kubernetes, the frozen Terraform,
  and the delivery recipes.

The boundaries are the point of the layout:

- `services/web` depends on the contract only, never on `valve_guardian`:
  the page is a client of the API, and could run anywhere.
- `services/api` depends on the contract and the core, never on training:
  no scikit-learn, XGBoost or MLflow in the serving image.
- The model card is the contract between training and serving: the API
  rebuilds the features from it, so the two cannot drift.
- A service knows how to build itself and nothing else: its `Containerfile`
  takes its base images as arguments and its sources as named contexts.

One concept per file, seven entries per folder, two hundred lines per file
([layout](.agents/rules/layout.md)).

## Python

Follow [.agents/portable/rules/python.md](.agents/portable/rules/python.md)
and this project's [.agents/rules/python.md](.agents/rules/python.md):
type annotations everywhere, the array aliases of `valve_guardian.arrays`,
names that say what a value means, short functions, one concern per file. A
comment records a **why** the code cannot express
([comments](.agents/portable/rules/comments.md)).

`MlflowTracker` imports `mlflow` inside `record`: MLflow is an optional
extra, and nothing else may import it.

## The model

`just train` overwrites `libraries/valve-guardian/src/valve_guardian/artifact/`.
Commit a new model only with its card, after `just benchmark` refreshed
`docs/benchmark.md`, and say in the commit what changed in the card.

## Infrastructure

`infra/terraform/` deployed the 1.3.0 dashboard image to a GCP project that no
longer exists, so a change there cannot be tested. Do not edit the `.tf`
files without the author's explicit request, and never run `terraform` or
`gcloud` unasked.

## Rules and checks

`.agents/portable/` is copied as is and stays project-agnostic
(`.agents/checks/portable.sh` guards it). Project rules and checks go to
`.agents/rules/` and `.agents/checks/`. `.agents/checks/run.sh <check>
<file>...` runs one; `just guards` runs them all over the changed files.

[.agents/rules/infrastructure.md](.agents/rules/infrastructure.md) is the
compose and Kubernetes rule: `compose-smell` and `kubernetes-values`
guard it on a commit, `just infra::all` over everything, `just infra::parity`
on demand.

The canon is [.agents/kanon.md](.agents/kanon.md); the `<>` in the README is
its sign.

## Done

A topic is done when `just agent gate` passes. Commit then, on its
`dev/<topic>` branch; never push, and never merge into `main` without the
author's review. The policy is recorded in
[.agents/project.yaml](.agents/project.yaml).

## Never

- A network call the person did not ask for: no telemetry, no update check,
  no lookup of the machine's public address. MLflow runs with its telemetry
  off.
- The name of a company, client or professional project in a tracked file or
  a commit.
- Commit or push without being asked.
