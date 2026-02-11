# db-boundary-profiler

A small profiling tool to measure latency, throughput, and *boundary costs* between an application and a database.

The goal of this project is to make system bottlenecks visible — especially the cost of:

- Crossing process boundaries
- Connection pool contention
- Thread scheduling overhead
- Network round-trips
- Database execution time

---

## Features

- Sequential, threaded, and asyncio modes
  (async is intended for non-blocking workloads)

- Oracle workload (Docker-based) using a connection pool

- Metrics:
  - p50 / p95 / p99 latency
  - Throughput (requests per second)
  - CPU time (user/system)
  - RSS memory usage
  - Context switches

- Oracle latency breakdown:
  - Pool acquire time
  - Query execution time

---

## Quickstart

Install dependencies:

```bash
poetry install
```

Run Oracle workload (sequential):

```bash
make oracle-seq
```

Run Oracle workload (threaded):

```bash
make oracle-threads
```

See [Experiments](experiments.md) for detailed experiment setups.

See [Results](results.md) for rendered summaries generated from JSON output.