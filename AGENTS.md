# AGENTS.md

Instructions for any coding agent in this repository. Claude Code reads them
through `.claude/CLAUDE.md`.

## What this project is

A binary classifier that says, cycle by cycle, whether the valve of a
hydraulic test rig is in optimal condition, from its pressure (PS2) and flow
(FS1) signals, and a Streamlit page that runs it on uploaded files. It was
written in 2025 as a time-boxed assignment and modernized in 2026; the
original choices of format are kept on purpose (see the README).

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
- `just install` syncs it; `just dashboard` opens the page;
  `just test` runs pytest.
- `just lint` is `ruff check`, `ruff format --check` and `ty check`.
  `just precommit` fixes what it can.
- `just agent gate` is the one command to declare work done: `just check`
  (lint, tests, markdown) then `just guards`.
- `just data`, `just train`, `just benchmark` and `just demo` download the
  UCI dataset: a network call, so never in the gate.
- `just image::build` builds the container with `docker buildx bake`.
- CI exists and runs by hand only; activating it is the author's consent.

## Layout

```text
libraries/valve-guardian/   the dataset, the features, the model, the training
services/dashboard/         the Streamlit page and its Containerfile
infra/build/                the bake files: images, contexts, tags
infra/terraform/            the Cloud Run deployment
```

A service knows how to build itself and nothing else: its `Containerfile`
takes its base images as arguments and its sources as named contexts.
Tags, base images and targets live in `infra/build/`; deployment lives in
`infra/terraform/`.

One concept per file, seven entries per folder, two hundred lines per file
([layout](.agents/rules/layout.md)).

## Python

Follow [.agents/portable/rules/python.md](.agents/portable/rules/python.md)
and this project's [.agents/rules/python.md](.agents/rules/python.md):
type annotations everywhere, the array aliases of `valve_guardian.arrays`,
names that say what a value means, short functions, one concern per file. A
comment records a **why** the code cannot express
([comments](.agents/portable/rules/comments.md)).

`Classifier` is a Protocol on purpose: it is the seam with scikit-learn and
XGBoost estimators, which the project does not own.

## Infrastructure

`infra/terraform/` targets a GCP project that no longer exists, so a change
there cannot be tested. Do not edit the `.tf` files without the author's
explicit request, and never run `terraform` or `gcloud` unasked.

## Rules and checks

`.agents/portable/` is copied as is and stays project-agnostic
(`.agents/checks/portable.sh` guards it). Project rules and checks go to
`.agents/rules/` and `.agents/checks/`. `.agents/checks/run.sh <check>
<file>...` runs one; `just guards` runs them all over the changed files.

The canon is [.agents/kanon.md](.agents/kanon.md); the `<>` in the README is
its sign.

## Done

A topic is done when `just agent gate` passes. Commit then, on its
`dev/<topic>` branch; never push, and never merge into `main` without the
author's review. The policy is recorded in
[.agents/project.yaml](.agents/project.yaml).

## Never

- A network call the person did not ask for: no telemetry, no update check,
  no lookup of the machine's public address.
- The name of a company, client or professional project in a tracked file or
  a commit.
- Commit or push without being asked.
