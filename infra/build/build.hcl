group "default" {
  targets = ["api", "web"]
}

group "release" {
  targets = ["api-release", "web-release"]
}

target "service" {
  context = "."
  target  = "runtime"
  output  = ["type=docker"]

  args = {
    BASE_IMAGE = PYTHON_IMAGE
    UV_IMAGE   = UV_IMAGE
  }

  labels = {
    "org.opencontainers.image.version"  = VERSION
    "org.opencontainers.image.licenses" = "Apache-2.0"
  }
}

target "api" {
  inherits   = ["service"]
  dockerfile = "${CONTEXT_API}/Containerfile"

  contexts = {
    contract = CONTEXT_CONTRACT
    core     = CONTEXT_CORE
    service  = CONTEXT_API
  }

  tags = ["valve-guardian-api:${TAG}"]
}

target "web" {
  inherits   = ["service"]
  dockerfile = "${CONTEXT_WEB}/Containerfile"

  contexts = {
    contract = CONTEXT_CONTRACT
    service  = CONTEXT_WEB
  }

  tags = ["valve-guardian-web:${TAG}"]
}

target "api-release" {
  inherits = ["api"]
  tags = [
    "valve-guardian-api:${VERSION}",
    "valve-guardian-api:latest",
  ]
}

target "web-release" {
  inherits = ["web"]
  tags = [
    "valve-guardian-web:${VERSION}",
    "valve-guardian-web:latest",
  ]
}
