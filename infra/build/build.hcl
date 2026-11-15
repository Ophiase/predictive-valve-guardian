group "default" {
  targets = ["dashboard"]
}

target "dashboard" {
  context    = "."
  dockerfile = "${CONTEXT_DASHBOARD}/Containerfile"
  target     = "runtime"

  args = {
    BASE_IMAGE = PYTHON_IMAGE
    UV_IMAGE   = UV_IMAGE
  }

  contexts = {
    library = CONTEXT_LIBRARY
    service = CONTEXT_DASHBOARD
  }

  labels = {
    "org.opencontainers.image.title"    = "valve-guardian-dashboard"
    "org.opencontainers.image.version"  = VERSION
    "org.opencontainers.image.licenses" = "Apache-2.0"
  }

  tags   = ["valve-guardian-dashboard:${TAG}"]
  output = ["type=docker"]
}

target "dashboard-release" {
  inherits = ["dashboard"]
  tags = [
    "valve-guardian-dashboard:${VERSION}",
    "valve-guardian-dashboard:latest",
  ]
}
