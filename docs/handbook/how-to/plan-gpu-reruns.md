---
title: "Plan GPU speed and order reruns"
description: "Review workload, arguments and output gaps before requesting a new measurement."
kind: "how-to"
source_ref: ["benchmarks/speed.py#L1-L79", "benchmarks/order.py#L1-L84", "benchmarks/report.py#L196-L210", "BENCHMARKS.md#L120-L154", "CONTEXT.md"]
---

# Plan GPU speed and order reruns

These scripts load real models and use CUDA. They are not documentation checks and were **not run** here. Obtain explicit evaluation/GPU approval and review model paths, environment, raw-evidence permissions and write destinations first.

## Speed

`python benchmarks/speed.py --stock PATH [--dex PATH] [--out PATH]` requires a stock-Laya directory. Dex defaults to repository `model`; output defaults to `benchmarks/results/speed-rerun.json`.

It queries GPU name/memory, loads Dex via adapter `load`, times short/long states with 1, 3, 5, 10 and 15 yes/no questions, then loads stock Laya on CUDA. Each cell uses three warmups and fifteen timed calls. Output contains GPU name, model-file sizes, GPU allocations and `[median_ms,p95_index_ms]` cells.

Current `main` has no HTTP/Jev timing loop despite its module docstring. A rerun does not recreate published `jev_api` cells. No actual path placeholders are copied as runnable commands in this guide.

## Answer order

`python benchmarks/order.py --stock PATH [--n N] [--out PATH]` defaults N=400 and output `benchmarks/results/order-rerun.json`. It has no `--dex`: Dex model path is fixed by code.

It reads A/B choice questions with at least three options, shuffles seed 3 and takes the first N. Each model answers original/reversed criteria order with keys/text preserved. Null choices are skipped. It reports question count, flip rate and accuracy in each order. No positivity guard on N; no accepted questions can cause division by zero.

Only Dex/stock are rerun. Saved published `order.json` also contains Jev; that collector is absent here.

## Promotion is separate

The report reads fixed `speed.json` and `order.json`. Neither script promotes reruns or updates report prose. Confirm exactly which saved results a future comparison uses; do not relabel a partial rerun as the published full methodology. Refer to [command defaults](../reference/commands.md) and [evidence method](../reference/evidence-schemas-and-scoring.md).

A failed GPU/model/write operation is not an instruction to repair drivers, install packages, change dtype or restart a service. Preserve minimal redacted evidence; let the owner decide recovery and cleanup under the measurement task.
