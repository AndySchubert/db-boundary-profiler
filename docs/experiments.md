# Experiments

This project supports controlled experiments to analyze database boundary costs.

---

## 1. Start Oracle in Docker

This project uses `gvenzl/oracle-free`.

Start the container:

```bash
bash scripts/run_docker.sh
```

## 2. Export Environment Variables

Set database connection details:

```bash
export DB_USER=system
export DB_PASSWORD='YourStrongPass1'
export DB_HOST=127.0.0.1
export DB_PORT=1521
export DB_SERVICE=FREEPDB1
```

## 3. Run Experiments

### Sequential
```bash
make oracle-seq
```

### Threaded
```bash
make oracle-threads
```

### High Concurrency (Pool Contention Analysis)

**Small pool (contention):**

```bash
poetry run dbbp \
  --workload oracle \
  --mode threads \
  --concurrency 100 \
  --pool-max 5 \
  --requests 2000 \
  --json experiments/pool5.json
```

**Large pool (no artificial contention):**

```bash
poetry run dbbp \
  --workload oracle \
  --mode threads \
  --concurrency 100 \
  --pool-max 100 \
  --requests 2000 \
  --json experiments/pool100.json
```

## 4. Render Documentation Results

Generate the results page from experiment JSON:

```bash
make docs-render
```

Serve the documentation locally:

```bash
make docs-serve
```

Build static site:

```bash
make docs-build
```