SHELL := /bin/bash

# Variables definitions
# -----------------------------------------------------------------------------

ifeq ($(TIMEOUT),)
TIMEOUT := 60
endif

# Target section and Global definitions
# -----------------------------------------------------------------------------

.PHONY: all clean install run deploy down logs

all: clean install run deploy down logs

install: generate_dot_env
	pip install --upgrade pip
	pip install -r requirements.txt

run:
	docker-compose up -d --build

logs:
	docker-compose logs -f

deploy: generate_dot_env
	docker-compose -f docker-compose.prod.yml build
	docker-compose -f docker-compose.prod.yml up -d

down:
	docker-compose -f docker-compose.prod.yml down

generate_dot_env:
	@if [[ ! -e .env ]]; then \
		cp .env.dist .env; \
	fi

clean:
	@find . -name '*.pyc' -exec rm -rf {} \;
	@find . -name '__pycache__' -exec rm -rf {} \;
	@find . -name 'Thumbs.db' -exec rm -rf {} \;
	@find . -name '*~' -exec rm -rf {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build
