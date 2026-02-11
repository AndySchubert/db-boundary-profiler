from __future__ import annotations

import math
import os
import time
from collections.abc import Iterable
from dataclasses import dataclass

import psutil


def _percentile(sorted_vals: list[float], p: float) -> float:
    if not sorted_vals:
        return float("nan")
    if p <= 0:
        return sorted_vals[0]
    if p >= 100:
        return sorted_vals[-1]
    k = (len(sorted_vals) - 1) * (p / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_vals[int(k)]
    d0 = sorted_vals[f] * (c - k)
    d1 = sorted_vals[c] * (k - f)
    return d0 + d1


@dataclass
class RunStats:
    n: int
    errors: int
    duration_s: float
    rps: float
    p50_ms: float
    p95_ms: float
    p99_ms: float
    cpu_user_s: float
    cpu_system_s: float
    rss_mb: float
    ctx_switch_voluntary: int
    ctx_switch_involuntary: int

    def to_text(self) -> str:
        return (
            f"Requests: {self.n} | Errors: {self.errors}\n"
            f"Duration: {self.duration_s:.3f}s | Throughput: {self.rps:.2f} req/s\n"
            f"Latency (ms): "
            f"p50={self.p50_ms:.2f} "
            f"p95={self.p95_ms:.2f} "
            f"p99={self.p99_ms:.2f}\n"
            f"Process CPU time (s): "
            f"user={self.cpu_user_s:.2f} "
            f"system={self.cpu_system_s:.2f}\n"
            f"Process RSS: {self.rss_mb:.1f} MB\n"
            f"Context switches: "
            f"voluntary={self.ctx_switch_voluntary} "
            f"involuntary={self.ctx_switch_involuntary}\n"
        )


def summarize_latencies_ms(lat_ms: Iterable[float]) -> tuple[float, float, float]:
    vals = sorted(float(x) for x in lat_ms)
    return (_percentile(vals, 50), _percentile(vals, 95), _percentile(vals, 99))


def capture_process_snapshot(pid: int | None = None) -> tuple[float, float, float, int, int]:
    pid = pid or os.getpid()
    p = psutil.Process(pid)
    ct = p.cpu_times()
    rss = p.memory_info().rss / (1024 * 1024)
    cs = p.num_ctx_switches()
    return (ct.user, ct.system, rss, cs.voluntary, cs.involuntary)


class Timer:
    def __enter__(self):
        self.t0 = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.t1 = time.perf_counter()

    @property
    def elapsed_s(self) -> float:
        return self.t1 - self.t0
