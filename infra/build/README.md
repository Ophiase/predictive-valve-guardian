# Build

The images, built with `docker buildx bake`; a service's `Containerfile` only
knows how to build itself.

- [variables.hcl](variables.hcl): the tag, the version and the pinned base
  images.
- [contexts.hcl](contexts.hcl): where each library and service lives.
- [build.hcl](build.hcl): the `api` and `web` targets, and their releases.

`just image::build`, `just image::release`, `just image::print`.
