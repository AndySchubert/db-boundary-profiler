from __future__ import annotations

import os
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


def ping(pool: oracledb.ConnectionPool) -> None:
    with pool.acquire() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM dual")
            cur.fetchone()
