# Configuration files

A configuration file is read by someone looking for one value. Indentation
is how they find it: nesting shows on the page, not inside braces.

- **YAML**: block style for the structure, a leaf mapping inline
  (`{ cpu: 50m, memory: 128Mi }`) and a flow list for a few short scalars,
  so nothing nests past twelve spaces; split a deeper value into its own
  file. yamllint runs strict with [yamllint.yaml](../checks/yamllint.yaml).
- **TOML**: `taplo fmt`, with [taplo.toml](../../taplo.toml): an array that
  does not fit is expanded, one item per line, and never collapsed back.
- **Nix**: `nixfmt` (the RFC 166 style): an argument set or a list of more
  than two items goes one per line.
- **JSON**: two spaces, one key per line, as `jq .` writes it.

[config-format.sh](../checks/config-format.sh) checks the YAML depth, TOML and Nix; a
formatter that is not installed is skipped with a note.
