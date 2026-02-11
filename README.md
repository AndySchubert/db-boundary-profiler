# db-boundary-profiler

A systems-oriented profiling tool for measuring boundary costs between application code and a database.

This project explores how latency and throughput are affected by:

- Connection pool contention
- Thread scheduling overhead
- Context switching
- Blocking I/O boundaries
- Database execution time

It is designed as an investigation tool, not just a benchmark.

---

## Why This Exists

In real systems, performance bottlenecks rarely live purely in “application code”.

They appear at boundaries:

Application thread  
→ Driver  
→ Connection pool  
→ Network  
→ Database engine  

This tool makes those boundary costs visible.

---

## Features

- Sequential and threaded execution modes
- Async mode for non-blocking workloads
- Oracle workload using Docker (`gvenzl/oracle-free`)
- Connection pool size control (`--pool-max`)
- High-resolution latency measurement (p50 / p95 / p99)
- Throughput (requests/sec)
- CPU user/system time
- RSS memory usage
- Voluntary / involuntary context switches
- Oracle latency breakdown:
  - Pool acquire time
  - Query execution time

---

## Quickstart

Install dependencies:

    poetry install

Start Oracle in Docker:

    bash scripts/run_docker.sh

Export DB connection variables:

    export DB_USER=system
    export DB_PASSWORD='YourStrongPass1'
    export DB_HOST=127.0.0.1
    export DB_PORT=1521
    export DB_SERVICE=FREEPDB1

Run sequential workload:

    make oracle-seq

Run threaded workload:

    make oracle-threads

---

## Example: Pool Contention at High Concurrency

### Concurrency = 100, pool-max = 100

Throughput: ~1018 req/s  
Latency p50: ~82 ms  
Acquire p50: ~69 ms  
Query p50: ~13 ms  

### Concurrency = 100, pool-max = 5

Throughput: ~451 req/s  
Latency p50: ~220 ms  
Acquire p50: ~210 ms  
Query p50: ~8 ms  

Observation:

Tail latency is dominated by connection acquisition time, not query execution time.  
Reducing pool size creates queuing and increases context switching and system CPU usage.

---

## JSON Output

Each run can produce structured JSON output:

    --json experiments/run.json

JSON includes:

- Run metadata (workload, mode, concurrency, pool-max)
- Latency percentiles
- Throughput
- CPU usage
- Context switches
- Oracle breakdown (acquire vs query)

Example structure:

{
  "meta": { ... },
  "latency_ms": { "p50": ..., "p95": ..., "p99": ... },
  "oracle": {
    "acquire_ms": { ... },
    "query_ms": { ... }
  }
}

---

## Documentation

Documentation is built with MkDocs.

Render locally:

    make docs-render
    make docs-serve

---

## Future Work

- Network latency injection (tc netem)
- Syscall profiling via strace
- perf CPU analysis
- Compare Docker vs host networking
- Async driver comparison
- Visualization (charts from JSON)

---

## License

MIT
