from __future__ import annotations

import os
import time
from dataclasses import dataclass

import oracledb


@dataclass(frozen=True)
class OracleConfig:
    user: str
    password: str
    host: str
    port: int
    service: str

    @property
    def dsn(self) -> str:
        # Easy Connect: host:port/service
        return f"{self.host}:{self.port}/{self.service}"


def config_from_env() -> OracleConfig:
    return OracleConfig(
        user=os.environ.get("DB_USER", "system"),
        password=os.environ.get("DB_PASSWORD", ""),
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("DB_PORT", "1521")),
        service=os.environ.get("DB_SERVICE", "FREEPDB1"),
    )


def make_pool(cfg: OracleConfig, min_size: int, max_size: int) -> oracledb.ConnectionPool:
    if not cfg.password:
        raise RuntimeError("DB_PASSWORD is required (set env var)")
    return oracledb.create_pool(
        user=cfg.user,
        password=cfg.password,
        dsn=cfg.dsn,
        min=min_size,
        max=max_size,
        increment=1,
        timeout=60,
    )


def ping_timed(pool: oracledb.ConnectionPool) -> tuple[float, float]:
    """
    Returns (acquire_ms, query_ms).
    """
    t0 = time.perf_counter()
    with pool.acquire() as conn:
        t1 = time.perf_counter()
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM dual")
            cur.fetchone()
    t2 = time.perf_counter()

    acquire_ms = (t1 - t0) * 1000.0
    query_ms = (t2 - t1) * 1000.0
    return acquire_ms, query_ms
