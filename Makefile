IMAGE_NAME=chimera-governor
CONTAINER_NAME=chimera-governor-test

.PHONY: setup build test spec-check clean

setup:
	docker build -t $(IMAGE_NAME) .

build: setup

test:
	docker run --rm $(IMAGE_NAME)

spec-check:
	@test -d specs || (echo " specs/ directory missing" && exit 1)
	@test -f specs/technical.md || (echo " specs/technical.md missing" && exit 1)
	@echo " Spec structure checks passed"

clean:
	docker rmi $(IMAGE_NAME) || true
