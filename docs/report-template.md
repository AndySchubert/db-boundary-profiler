# Experiment Report

## Title

Short descriptive title.
Example:
"Oracle Connection Pool Contention at High Concurrency"

---

## 1. Objective

What question are we trying to answer?

Examples:
- Does increasing thread concurrency improve throughput?
- How does pool-max affect tail latency?
- Is latency dominated by pool acquisition or query execution?

Be specific.

---

## 2. Environment

### Hardware
- CPU:
- RAM:
- OS:
- Kernel version:

### Database
- Oracle version:
- Running in Docker? (yes/no)
- Host networking or bridge?

### Profiler Version
- Git commit hash:
- Branch:
- Timestamp:

---

## 3. Configuration

Command used:

    poetry run dbbp \
      --workload oracle \
      --mode threads \
      --concurrency 100 \
      --pool-max 5 \
      --requests 2000 \
      --json experiments/pool5.json

Parameters:

- workload:
- mode:
- concurrency:
- pool-max:
- requests:

---

## 4. Results Summary

### Throughput
- Requests per second:

### Latency (ms)
- p50:
- p95:
- p99:

### CPU
- User time:
- System time:

### Context Switches
- Voluntary:
- Involuntary:

---

## 5. Oracle Breakdown

### Acquire Time (ms)
- p50:
- p95:
- p99:

### Query Time (ms)
- p50:
- p95:
- p99:

---

## 6. Observations

What stands out?

Examples:
- Acquire time dominates total latency.
- Increasing concurrency beyond 20 does not increase throughput.
- Small pool-max creates queuing behavior.
- System CPU increases significantly under contention.

---

## 7. Interpretation

What does this mean?

Example:
"At concurrency 100 with pool-max 5, throughput drops by ~55% and p50 latency increases 2.7x. The majority of the increase is due to pool acquire wait, not query execution. This suggests the boundary bottleneck is client-side resource contention rather than database processing time."

---

## 8. Conclusion

Clear final statement answering the Objective.

Example:
"Under high concurrency, connection pool size acts as a hard throughput cap. Tail latency is dominated by pool acquisition delay, not query execution time."

---

## 9. Follow-up Experiments

- Test with larger pool sizes (10, 20, 50)
- Add artificial network latency (tc netem)
- Compare Docker vs host networking
- Measure syscall counts using strace
- Profile CPU with perf

---

## Appendix

Link to raw JSON:

- experiments/<file>.json
