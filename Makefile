IMAGE_NAME=chimera-governor
CONTAINER_NAME=chimera-governor-test

.PHONY: setup build test lint spec-check clean

## Build Docker image
setup:
	docker build -t $(IMAGE_NAME) .

## Alias for setup (CI-friendly)
build: setup

## Run tests inside Docker (expected to FAIL for now)
test:
	docker run --rm $(IMAGE_NAME)

## Run linting (Ruff) inside Docker
lint:
	docker run --rm $(IMAGE_NAME) ruff check .

## Optional: verify spec structure exists
spec-check:
	@test -d specs || (echo " specs/ directory missing" && exit 1)
	@test -f specs/technical.md || (echo " specs/technical.md missing" && exit 1)
	@echo " Spec structure checks passed"

## Cleanup local docker artifacts
clean:
	docker rmi $(IMAGE_NAME) || true
