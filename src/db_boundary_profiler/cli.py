from __future__ import annotations

import argparse
import time

from .metrics import RunStats, Timer, capture_process_snapshot, summarize_latencies_ms
from .report import write_json
from .workload import simulated_work


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="dbbp",
        description="DB Boundary Profiler (starter)",
    )

    parser.add_argument(
        "--requests",
        type=int,
        default=200,
        help="number of requests",
    )
    parser.add_argument(
        "--latency-ms",
        type=int,
        default=5,
        help="simulated per-request latency (ms)",
    )
    parser.add_argument(
        "--jitter-ms",
        type=int,
        default=3,
        help="random +/- jitter (ms)",
    )
    parser.add_argument(
        "--error-rate",
        type=float,
        default=0.0,
        help="simulated error rate [0..1]",
    )
    parser.add_argument(
        "--json",
        default="",
        help="write results to a JSON file (e.g. experiments/baseline.json)",
    )

    args = parser.parse_args()

    cpu_user0, cpu_sys0, _ = capture_process_snapshot()
    latencies_ms: list[float] = []
    errors = 0

    with Timer() as t:
        for _ in range(args.requests):
            t0 = time.perf_counter()
            try:
                simulated_work(args.latency_ms, args.jitter_ms, args.error_rate)
            except Exception:
                errors += 1
            finally:
                latencies_ms.append((time.perf_counter() - t0) * 1000.0)

    cpu_user1, cpu_sys1, rss1 = capture_process_snapshot()

    p50, p95, p99 = summarize_latencies_ms(latencies_ms)
    duration = t.elapsed_s
    rps = args.requests / duration if duration > 0 else 0.0

    stats = RunStats(
        n=args.requests,
        errors=errors,
        duration_s=duration,
        rps=rps,
        p50_ms=p50,
        p95_ms=p95,
        p99_ms=p99,
        cpu_user_s=max(0.0, cpu_user1 - cpu_user0),
        cpu_system_s=max(0.0, cpu_sys1 - cpu_sys0),
        rss_mb=rss1,
    )

    print(stats.to_text())

    if args.json:
        write_json(stats, args.json)
        print(f"Wrote JSON report to: {args.json}")
