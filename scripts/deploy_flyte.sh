#!/usr/bin/env bash
# Build container and register Flyte workflows
set -euo pipefail

IMAGE_NAME=${IMAGE_NAME:-agent-ai:latest}

# Build Docker image containing the Flyte tasks
docker build -t "$IMAGE_NAME" -f Dockerfile .

# Register all workflows using pyflyte
pyflyte --pkgs flyte,services.workflow register --image "$IMAGE_NAME"
