# Kubernetes

Both services through the bjw-s
[app-template](https://bjw-s-labs.github.io/helm-charts/docs/app-template/)
chart, 5.3.0. There is no template of our own: every file of
[values/](values) is passed to Helm, one concern each.

- [stack.yaml](values/stack.yaml): what every pod shares; the registry and
  the tag come from the command line.
- `api/`, `web/`: `deployment`, `service`, `network-policy`, `expose`, and
  `placement` or `uploads` where a service needs one.

## Deploy

```sh
just kubernetes::template ghcr.io/me 1a2b3c4d   # the manifests, nothing applied
just kubernetes::deploy ghcr.io/me 1a2b3c4d     # on the current kubectl context
```

## Try it

```sh
just image::build
just kubernetes::kind          # kind cluster, images loaded, release installed
just kubernetes::open          # the page on localhost:8080
just kubernetes::kind-delete
```

## Expose

Each service has a Gateway API route in its `expose.yaml`, off. The platform
turns it on and names the Gateway and the hostnames. The `api` network policy
admits only `web`; exposing the API adds the Gateway's namespace to it.
