define USAGE
Super awesome hand-crafted build system ⚙️

Commands:
	setup     Install dependencies, dev included
	lock      Generate requirements.txt
	test      Run tests
	lint      Run linting tests
	release   Build and publish docker image to registry.int.deskcrash.com
endef

export USAGE
.EXPORT_ALL_VARIABLES:
VERSION := $(shell git describe --tags)
BUILD := $(shell git rev-parse --short HEAD)
PROJECTNAME := $(shell basename "$(PWD)")
PACKAGE_DIR = $(shell basename "$(PWD)")

help:
	@echo "$$USAGE"

.PHONY: startenv
startenv:
	poetry shell
	docker-compose start 
	alembic upgrade head

lock:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

.PHONY: lint
lint:
	echo "Running pylint...\n"
	pylint --disable=R,C,W $(PACKAGE_DIR)
	# echo "Running isort...\n"
	# isort --check $(PACKAGE_DIR)
	# echo "Running mypy...\n"
	# mypy $(PACKAGE_DIR)

.PHONY: test
test:
	PYTHONPATH=$(PWD) pytest tests/

.PHONY: db
db:
	PYTHONPATH=${PWD} alembic upgrade head

.PHONY: setup
setup:
	poetry install --dev

.PHONY: run
run:
	docker run --rm -p 127.0.0.1:8000:8000 --env-file=.env nuxion/${PROJECTNAME}

.PHONY: docker
docker:
	docker build -t nuxion/${PROJECTNAME} .

.PHONY: release
release: lint docker 
	docker tag nuxion/${PROJECTNAME} registry.int.deskcrash.com/nuxion/${PROJECTNAME}:$(VERSION)
	docker push registry.int.deskcrash.com/nuxion/$(PROJECTNAME):$(VERSION)

.PHONY: registry
registry:
	# curl http://registry.int.deskcrash.com/v2/_catalog | jq
	curl http://registry.int.deskcrash.com/v2/nuxion/$(PROJECTNAME)/tags/list 

.PHONY: redis-cli
redis-cli:
	docker-compose exec redis redis-cli

.PHONY: tag
tag:
	#poetry version prealese
	git tag -a $(shell poetry version --short) -m "$(shell git log -1 --pretty=%B | head -n 1)"
