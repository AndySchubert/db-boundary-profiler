from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .metrics import RunStats


def stats_to_dict(stats: RunStats) -> dict[str, Any]:
    d = asdict(stats)
    d["latency_ms"] = {"p50": d.pop("p50_ms"), "p95": d.pop("p95_ms"), "p99": d.pop("p99_ms")}
    return d


def write_json(stats: RunStats, path: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        json.dumps(
            stats_to_dict(stats),
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
