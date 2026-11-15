# Predictive Valve Guardian

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![Python 3.14](https://img.shields.io/badge/Python-3.14-yellow.svg)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-workspace-brightgreen.svg)](https://docs.astral.sh/uv/)
[![Justfile](https://img.shields.io/badge/just-available-brightgreen.svg)](https://just.systems/man/en/)
[![Kanon](https://img.shields.io/badge/%3C%3E-Kanon-blueviolet.svg)](.agents/kanon.md)

Predict, cycle by cycle, whether the valve of a hydraulic system is in optimal
condition, from its pressure and flow sensors.

> [!NOTE]
> Written in 2025 as a time-boxed assignment, modernized in 2026. The original
> choices are kept on purpose; reasonable then, they would not be mine today,
> in the agentic era:
>
> - **Streamlit** made sense for a page written by hand under a deadline. With
>   an agent, a typed API (FastAPI, pydantic) and a thin page in front cost
>   little more and keep the model apart from the UI.
> - **XGBoost** was picked among models that all score 1.0 on 205 test cycles,
>   which cannot rank them; a cross-validated evaluation should come first.
> - **The Terraform** in [infra/terraform](infra/terraform/README.md) was
>   tested and deployed in 2025; its GCP project is gone, so it is kept as it
>   was and can no longer evolve.

<div align="center">
  <img src="./resources/dashboard/dashboard_preview_00.png" width="800">
</div>

## Quickstart

[uv](https://docs.astral.sh/uv/getting-started/installation/) and
[just](https://just.systems/man/en/) are the prerequisites; Docker with buildx
for the image.

```sh
just install
just dashboard          # http://localhost:8501
```

Or in a container:

```sh
just image::build
just image::run         # http://localhost:8501
```

The model:

```sh
just data               # download the UCI dataset into data/hydraulic
just demo               # check the deployed model on the 205 test cycles
just benchmark          # every candidate model on every representation
just train              # retrain and overwrite the deployed model
```

`just` alone lists every recipe.

## Layout

```text
libraries/valve-guardian/   the dataset, the features, the model, the training
services/dashboard/         the Streamlit page and its Containerfile
infra/build/                the bake files: images, contexts, tags
infra/terraform/            the Cloud Run deployment
```

A service knows how to build itself and nothing else: its `Containerfile`
receives its base images as arguments and its sources as named contexts.
What to tag, from which base, lives in `infra/build`; where to deploy, in
`infra/terraform`.

## Problem statement

The data comes from the UCI
[Condition monitoring of hydraulic systems](https://archive.ics.uci.edu/dataset/447/condition+monitoring+of+hydraulic+systems)
dataset.

A cycle is one complete operation of the system. There are $C = 2205$
cycles, and each cycle $i < C$ holds:

- $PS2_i$: pressure sensor 2, in bar, at 100 Hz: 6 000 values.
- $FS1_i$: flow sensor 1, in litres per minute, at 10 Hz: 600 values.
- $Profile_i$: cooler, valve, pump, accumulator and stable flag, where the
  valve condition $z_i \in \{73, 80, 90, 100\}$.

We estimate whether $z_i = 100$, that is, we learn

$$f_\theta : \mathbb{R}^{6000} \times \mathbb{R}^{600} \to \{0, 1\}$$

on the first 2 000 cycles and test it on the last 205.

## Solution

The target is one category of a categorical variable: a binary
classification. The inputs are time series of fixed length that oscillate,
so classical models on engineered features are the first thing to try:

- **Raw**: every sample is a feature.
- **Statistics**: mean, standard deviation, minimum, maximum, 10th and 90th
  percentiles and energy, on the signal (order 0), its first difference
  (order 1) and its second difference (order 2).
- **Fourier**: the magnitudes of the first 20 coefficients of the FFT.

The models are a logistic regression, a random forest and XGBoost. A 1D CNN or
an LSTM was planned only if those failed; they did not.

### Results

| Features | Order | Fourier | Model | Accuracy | F1 | Total time (s) |
| --- | --- | --- | --- | --- | --- | --- |
| raw | 0 | no | XGBoost | 1.000 | 1.000 | 0.856 |
| raw | 0 | no | LogisticRegression | 1.000 | 1.000 | 0.863 |
| raw | 0 | no | RandomForest | 1.000 | 1.000 | 0.870 |
| statistics | 0 | yes | LogisticRegression | 1.000 | 1.000 | 1.149 |
| statistics | 0 | yes | XGBoost | 1.000 | 1.000 | 1.150 |
| statistics | 0 | yes | RandomForest | 1.000 | 1.000 | 1.162 |
| statistics | 2 | yes | LogisticRegression | 1.000 | 1.000 | 1.841 |
| statistics | 2 | yes | XGBoost | 1.000 | 1.000 | 1.842 |
| statistics | 2 | yes | RandomForest | 1.000 | 1.000 | 1.854 |
| statistics | 1 | no | XGBoost | 0.951 | 0.934 | 1.464 |
| statistics | 1 | no | RandomForest | 0.937 | 0.918 | 1.477 |
| statistics | 2 | no | XGBoost | 0.937 | 0.918 | 1.790 |
| statistics | 2 | no | RandomForest | 0.937 | 0.918 | 1.803 |
| statistics | 2 | no | LogisticRegression | 0.605 | 0.643 | 1.789 |
| statistics | 1 | no | LogisticRegression | 0.580 | 0.629 | 1.463 |

The total time is the feature extraction plus the prediction, in seconds, on
the 2025 machine.

## Conclusion

The raw signals and the Fourier features both reach a perfect accuracy and F1
score. The raw model is set aside for its dimension: 6 600 features invite
overfitting and cost more to run.

The deployed model is XGBoost on the order-0 statistics and the Fourier
magnitudes: 54 features. The note at the top says what I would weigh
differently today.

## Contributors

- Ophiase — author: the 2025 model, the dashboard and the deployment.
- Claude Code — the 2026 modernization, under the author's review.
