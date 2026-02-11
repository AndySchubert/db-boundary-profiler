from __future__ import annotations

import json
from pathlib import Path


EXPERIMENTS_DIR = Path("experiments")
OUTPUT_MD = Path("docs/results.md")


def load_json_files() -> list[tuple[str, dict]]:
    if not EXPERIMENTS_DIR.exists():
        return []

    items: list[tuple[str, dict]] = []
    for p in sorted(EXPERIMENTS_DIR.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            items.append((p.name, data))
        except Exception:
            # Skip invalid JSON files
            continue
    return items


def fmt(x, nd=2):
    if isinstance(x, (int, float)):
        return f"{x:.{nd}f}"
    return str(x)


def main() -> None:
    rows = load_json_files()

    lines: list[str] = []
    lines.append("# Results")
    lines.append("")
    lines.append("This page is generated from JSON files in `experiments/`.")
    lines.append("")

    if not rows:
        lines.append("> No JSON results found. Run an experiment with `--json experiments/<name>.json`.")
        lines.append("")
        OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return

    lines.append("## Summary")
    lines.append("")
    lines.append(
        "| file | workload | mode | conc | pool_max | n | rps | p50(ms) | p95(ms) | p99(ms) | ctx(vol) | ctx(inv) |"
    )
    lines.append(
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"
    )

    for fname, d in rows:
        meta = d.get("meta", {})
        latency = d.get("latency_ms", {})

        lines.append(
            "| {file} | {workload} | {mode} | {conc} | {pool} | {n} | {rps} | {p50} | {p95} | {p99} | {cv} | {ci} |".format(
                file=fname,
                workload=meta.get("workload", "-"),
                mode=meta.get("mode", "-"),
                conc=meta.get("concurrency", "-"),
                pool=meta.get("pool_max", "-"),
                n=d.get("n", "-"),
                rps=fmt(d.get("rps", "-")),
                p50=fmt(latency.get("p50", "-")),
                p95=fmt(latency.get("p95", "-")),
                p99=fmt(latency.get("p99", "-")),
                cv=d.get("ctx_switch_voluntary", "-"),
                ci=d.get("ctx_switch_involuntary", "-"),
            )
        )

    # Oracle breakdown section
    oracle_rows = [(f, d) for f, d in rows if "oracle" in d]
    if oracle_rows:
        lines.append("")
        lines.append("## Oracle breakdown")
        lines.append("")
        lines.append("| file | acquire p50 | acquire p95 | acquire p99 | query p50 | query p95 | query p99 |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")

        for fname, d in oracle_rows:
            o = d.get("oracle", {})
            a = o.get("acquire_ms", {})
            q = o.get("query_ms", {})
            lines.append(
                "| {file} | {a50} | {a95} | {a99} | {q50} | {q95} | {q99} |".format(
                    file=fname,
                    a50=fmt(a.get("p50", "-")),
                    a95=fmt(a.get("p95", "-")),
                    a99=fmt(a.get("p99", "-")),
                    q50=fmt(q.get("p50", "-")),
                    q95=fmt(q.get("p95", "-")),
                    q99=fmt(q.get("p99", "-")),
                )
            )

    lines.append("")
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
