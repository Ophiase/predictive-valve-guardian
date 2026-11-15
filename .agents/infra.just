root := source_directory() / ".."
checks := root / ".agents/checks"
kubeconform := "ghcr.io/yannh/kubeconform:v0.7.0"
kube_linter := "stackrox/kube-linter:v0.7.4"
hadolint := "hadolint/hadolint:v2.14.0"
yamllint_version := "1.37.1"
kubernetes_version := "1.34.0"

[doc("Every infrastructure check over the whole repository: YAML, compose, Kubernetes, Containerfiles")]
all: yaml compose kubernetes containerfiles

[doc("yamllint, strict, over every YAML file outside .agents")]
yaml:
    cd {{ root }} && git ls-files -z '*.yaml' ':!.agents/*' | xargs -0 uvx --quiet yamllint@{{ yamllint_version }} --strict --config-file {{ checks }}/yamllint.yaml

[doc("The compose specification, then the compose smells")]
compose:
    cd {{ root }} && docker compose --file infra/compose/compose.yaml config --quiet
    cd {{ root }} && {{ checks }}/compose-smell.sh infra/compose/compose.yaml

[doc("The values smells; the rendered manifests through kubeconform and kube-linter")]
[script("bash")]
kubernetes:
    set -euo pipefail
    cd {{ root }}
    find infra/kubernetes/values -name '*.yaml' -print0 | sort -z | xargs -0 {{ checks }}/kubernetes-values.sh
    manifests="$(mktemp)"
    trap 'rm -f "$manifests"' EXIT
    just kubernetes::template registry.invalid/ 0123abcd 2>/dev/null > "$manifests"
    docker run --rm -i {{ kubeconform }} -strict -summary -kubernetes-version {{ kubernetes_version }} < "$manifests"
    docker run --rm -v "$manifests:/manifests.yaml:ro" -v "{{ checks }}/kube-linter.yaml:/config.yaml:ro" \
        {{ kube_linter }} lint --config /config.yaml /manifests.yaml

[doc("hadolint over every Containerfile")]
[script("bash")]
containerfiles:
    set -euo pipefail
    cd {{ root }}
    git ls-files '*Containerfile' | while IFS= read -r file; do
        docker run --rm -i -v "{{ checks }}/hadolint.yaml:/config.yaml:ro" {{ hadolint }} hadolint --config /config.yaml - < "$file"
    done

[doc("On demand, never in the gate: does the chart still run what compose runs?")]
[script("bash")]
parity:
    set -euo pipefail
    cd {{ root }}
    manifests="$(mktemp)"
    trap 'rm -f "$manifests"' EXIT
    just kubernetes::template registry.invalid/ 0123abcd 2>/dev/null > "$manifests"
    uv run --quiet python {{ checks }}/compose_parity.py infra/compose/compose.yaml "$manifests"
