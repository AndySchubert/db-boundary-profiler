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

threads:
	poetry run dbbp --mode threads --concurrency 50 --requests 1000 --latency-ms 8 --jitter-ms 4

async:
	poetry run dbbp --mode async --concurrency 200 --requests 2000 --latency-ms 8 --jitter-ms 4

seq-json:
	poetry run dbbp --mode seq --requests 500 --latency-ms 8 --jitter-ms 4 --json experiments/seq.json

threads-json:
	poetry run dbbp --mode threads --concurrency 50 --requests 1000 --latency-ms 8 --jitter-ms 4 --json experiments/threads.json

async-json:
	poetry run dbbp --mode async --concurrency 200 --requests 2000 --latency-ms 8 --jitter-ms 4 --json experiments/async.json

oracle-seq:
	poetry run dbbp --workload oracle --mode seq --requests 200 --json experiments/oracle-seq.json

oracle-threads:
	poetry run dbbp --workload oracle --mode threads --concurrency 20 --requests 500 --json experiments/oracle-threads.json

docs-render:
	poetry run python scripts/render_results.py

docs-serve: docs-render
	poetry run mkdocs serve

docs-build: docs-render
	poetry run mkdocs build