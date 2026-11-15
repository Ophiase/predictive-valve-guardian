# Infrastructure

The application engineer knows the services best, so he ships their CI:
high-level recipes, split further when a pipeline needs it.

## CI

```sh
infra/pipeline/bootstrap.sh     # the only step outside the recipes
just ci <registry>              # checks, then images at the commit's tag
```

- Needs: Docker with buildx, the registry's secret
  (`REGISTRY_USERNAME`, `REGISTRY_PASSWORD`).
- An image already in the registry is not rebuilt.
- Finer steps: `just check`, `just publish`, `just image::push`.

## Deploy

```sh
just kubernetes::deploy <registry> <tag>    # helm upgrade --install, current context
```

No CD here: config, secrets and environments are left to whoever deploys.

## Compose and Kubernetes

- Compose for development, Kubernetes for a platform.
- The chart is bjw-s app-template: values only, one concern per file.
- `just infra::parity` compares them, on demand.

## Checks

- On commit: compose and values smells, YAML depth.
- In `just check`: yamllint, kubeconform, kube-linter, hadolint.
- Rules: [infrastructure](../.agents/rules/infrastructure.md).

## Folders

- [build](build/README.md): the images.
- [compose](compose/README.md): both services on one machine.
- [kubernetes](kubernetes/README.md): both services on a cluster.
- [terraform](terraform/README.md): the 1.3.0 Cloud Run deployment, frozen.
