SHELL := /bin/bash

.PHONY: help setup install run fmt lint test clean

help:
	@echo "Targets:"
	@echo "  make setup   - install deps via Poetry"
	@echo "  make run     - run a sample benchmark"
	@echo "  make fmt     - format/lint (ruff)"
	@echo "  make lint    - strict lint (ruff)"
	@echo "  make test    - run tests"
	@echo "  make clean   - remove caches"

setup: install

install:
	poetry install

run:
	poetry run dbbp --requests 300 --latency-ms 8 --jitter-ms 4

fmt:
	poetry run ruff check --fix .
	poetry run ruff format .

lint:
	poetry run ruff check .
	poetry run ruff format --check .

test:
	poetry run pytest -q

clean:
	rm -rf .pytest_cache .ruff_cache __pycache__ **/__pycache__

baseline:
	poetry run dbbp --requests 500 --latency-ms 8 --jitter-ms 4 --json experiments/baseline.json
