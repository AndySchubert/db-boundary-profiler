from __future__ import annotations

import argparse
import asyncio
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait

from .metrics import RunStats, Timer, capture_process_snapshot, summarize_latencies_ms
from .report import write_json
from .workload import simulated_work, simulated_work_async


def run_sequential(
    n: int,
    latency_ms: int,
    jitter_ms: int,
    error_rate: float,
) -> tuple[list[float], int]:
    latencies_ms: list[float] = []
    errors = 0

    for _ in range(n):
        t0 = time.perf_counter()
        try:
            simulated_work(latency_ms, jitter_ms, error_rate)
        except Exception:
            errors += 1
        finally:
            latencies_ms.append((time.perf_counter() - t0) * 1000.0)

    return latencies_ms, errors


def run_threads(
    n: int,
    concurrency: int,
    latency_ms: int,
    jitter_ms: int,
    error_rate: float,
) -> tuple[list[float], int]:
    latencies_ms: list[float] = []
    errors = 0

    def _one() -> None:
        simulated_work(latency_ms, jitter_ms, error_rate)

    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        in_flight: dict[object, float] = {}

        def submit_one() -> None:
            fut = ex.submit(_one)
            in_flight[fut] = time.perf_counter()

        # Fill the pipeline
        initial = min(concurrency, n)
        for _ in range(initial):
            submit_one()

        submitted = initial
        completed = 0

        while completed < n:
            done, _ = wait(in_flight.keys(), return_when=FIRST_COMPLETED)

            for fut in done:
                t0 = in_flight.pop(fut)
                try:
                    fut.result()
                except Exception:
                    errors += 1
                finally:
                    latencies_ms.append((time.perf_counter() - t0) * 1000.0)
                    completed += 1

                if submitted < n:
                    submit_one()
                    submitted += 1

    return latencies_ms, errors


async def run_asyncio(
    n: int,
    concurrency: int,
    latency_ms: int,
    jitter_ms: int,
    error_rate: float,
) -> tuple[list[float], int]:
    sem = asyncio.Semaphore(concurrency)
    latencies_ms: list[float] = []
    errors = 0

    async def _one() -> float:
        async with sem:
            t0 = time.perf_counter()
            await simulated_work_async(latency_ms, jitter_ms, error_rate)
            return (time.perf_counter() - t0) * 1000.0

    tasks = [asyncio.create_task(_one()) for _ in range(n)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for r in results:
        if isinstance(r, Exception):
            errors += 1
        else:
            latencies_ms.append(float(r))

    return latencies_ms, errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dbbp",
        description="DB Boundary Profiler",
    )

    parser.add_argument(
        "--mode",
        choices=["seq", "threads", "async"],
        default="seq",
        help="execution mode",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=10,
        help="in-flight operations (threads/async)",
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

    return parser


def main() -> None:
    args = build_parser().parse_args()

    cpu_user0, cpu_sys0, _, v0, iv0 = capture_process_snapshot()

    with Timer() as t:
        if args.mode == "seq":
            latencies_ms, errors = run_sequential(
                args.requests,
                args.latency_ms,
                args.jitter_ms,
                args.error_rate,
            )
        elif args.mode == "threads":
            latencies_ms, errors = run_threads(
                args.requests,
                args.concurrency,
                args.latency_ms,
                args.jitter_ms,
                args.error_rate,
            )
        else:
            latencies_ms, errors = asyncio.run(
                run_asyncio(
                    args.requests,
                    args.concurrency,
                    args.latency_ms,
                    args.jitter_ms,
                    args.error_rate,
                )
            )

    cpu_user1, cpu_sys1, rss1, v1, iv1 = capture_process_snapshot()

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
        ctx_switch_voluntary=max(0, v1 - v0),
        ctx_switch_involuntary=max(0, iv1 - iv0),
    )

    print(stats.to_text())

    if args.json:
        write_json(stats, args.json)
        print(f"Wrote JSON report to: {args.json}")
