from __future__ import annotations

import random
import time


def simulated_work(latency_ms: int = 5, jitter_ms: int = 3, error_rate: float = 0.0) -> None:
    """
    Placeholder "boundary work" until we plug in real DB calls.
    Simulates waiting (like network/DB roundtrip) and occasional failure.
    """
    if error_rate > 0 and random.random() < error_rate:
        raise RuntimeError("simulated error")

    sleep_ms = max(0, latency_ms + random.randint(-jitter_ms, jitter_ms))
    time.sleep(sleep_ms / 1000.0)
