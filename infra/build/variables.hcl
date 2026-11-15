variable "TAG" {
  default = "dev"
}

variable "VERSION" {
  default = "dev"
}

variable "PYTHON_IMAGE" {
  default = "docker.io/library/python:3.14-slim-bookworm"
}

variable "UV_IMAGE" {
  default = "ghcr.io/astral-sh/uv:0.11.3"
}
