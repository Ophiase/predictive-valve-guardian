# Infrastructure

Compose for development, Kubernetes for a platform. Strict where it is cheap,
loose where it slows a developer down.

## Checked on commit

- Compose: an explicit image tag, never `latest`; ports bound to
  `127.0.0.1`; no `privileged` or host namespace
  ([compose-smell.sh](../checks/compose-smell.sh)).
- Values: one concern per file; the image from `global.registry` at
  `global.imageTag`; no Ingress
  ([kubernetes-values.sh](../checks/kubernetes-values.sh)).
- YAML nested twelve spaces at most ([config-format.sh](../checks/config-format.sh)).

## Checked by `just check`

- yamllint, strict ([yamllint.yaml](../checks/yamllint.yaml)).
- The rendered chart through kubeconform and kube-linter
  ([kube-linter.yaml](../checks/kube-linter.yaml)).
- The Containerfiles through hadolint ([hadolint.yaml](../checks/hadolint.yaml)).

## Conventions, not checked

- The chart is bjw-s app-template: values only, a leaf mapping inline.
- Exposure is a Gateway API route, off; the platform names the Gateway.
- `just infra::parity` compares compose and the chart, on demand.

## What kube-linter skips

| Check | Why |
| --- | --- |
| `dnsconfig-options`, `no-node-affinity` | the platform's |
| `minimum-three-replicas` | sizing is the platform's; `web` keeps analyses in memory |
| `no-anti-affinity` | `api` spreads with `topologySpreadConstraints` |
| `required-annotation-email`, `required-label-owner` | the organisation's |

hadolint skips `DL3022`: a `COPY --from` names a bake context.
