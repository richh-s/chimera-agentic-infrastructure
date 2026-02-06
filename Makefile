IMAGE_NAME=chimera-governor
CONTAINER_NAME=chimera-governor-test

.PHONY: setup test spec-check clean

## Build Docker image
setup:
	docker build -t $(IMAGE_NAME) .

## Run tests inside Docker (expected to FAIL for now)
test:
	docker run --rm $(IMAGE_NAME)

## Optional: verify spec structure exists
spec-check:
	@test -d specs || (echo " specs/ directory missing" && exit 1)
	@test -f specs/technical.md || (echo " specs/technical.md missing" && exit 1)
	@echo " Spec structure checks passed"

## Cleanup local docker artifacts
clean:
	docker rmi $(IMAGE_NAME) || true
