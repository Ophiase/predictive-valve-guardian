# Compose

Both services on one machine: the API on `localhost:8000`, the page on
`localhost:8080`; read-only, non-root, every capability dropped.

```sh
just run      # build the images and start the stack
just stop
```

`just stack::logs` follows them. [compose.yaml](compose.yaml) is held to the
Kubernetes values by `just infra::kubernetes`: change one, and the check says
what the other must follow.
