# Results

This page is generated from JSON files in `experiments/`.

## Summary

| file | workload | mode | conc | pool_max | n | rps | p50(ms) | p95(ms) | p99(ms) | ctx(vol) | ctx(inv) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| async.json | - | - | - | - | 2000 | 20151.43 | 8.76 | 12.77 | 13.06 | 70 | 1 |
| oracle-seq.json | oracle | seq | 10 | 0 | 200 | 1534.36 | 0.45 | 0.54 | 0.64 | 402 | 2 |
| oracle-threads.json | oracle | threads | 20 | 0 | 500 | 1116.27 | 13.51 | 41.14 | 60.37 | 1903 | 0 |
| seq.json | - | - | - | - | 500 | 124.61 | 8.08 | 12.07 | 12.08 | 500 | 0 |
| test.json | oracle | threads | 100 | 5 | 1000 | 450.21 | 215.83 | 261.13 | 325.96 | 4720 | 0 |
| threads.json | - | - | - | - | 1000 | 5526.97 | 8.30 | 12.33 | 12.49 | 1362 | 0 |

## Oracle breakdown

| file | acquire p50 | acquire p95 | acquire p99 | query p50 | query p95 | query p99 |
|---|---:|---:|---:|---:|---:|---:|
| oracle-seq.json | 0.03 | 0.04 | 0.09 | 0.42 | 0.51 | 0.61 |
| oracle-threads.json | 10.12 | 39.88 | 59.36 | 2.83 | 4.32 | 5.32 |
| test.json | 207.08 | 253.52 | 316.43 | 8.22 | 11.28 | 14.30 |

