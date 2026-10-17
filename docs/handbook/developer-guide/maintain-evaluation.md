---
title: Maintain evaluation evidence
description: Change report consumers and rerun methods without confusing regenerated
  tables with new measurements.
kind: developer
source_ref:
- benchmarks/report.py#L11-L216
- benchmarks/speed.py#L22-L79
- benchmarks/order.py#L22-L84
- BENCHMARKS.md#L3-L11
- BENCHMARKS.md#L120-L154
- DATA_CARD.md#L3-L30
---

# Maintain evaluation evidence

## Know which operation you need

| Need | Existing tool | What it does not do |
|---|---|---|
| Rebuild tables/charts from retained evidence | `benchmarks/report.py` | No model/Jev request; no `BENCHMARKS.md` or Decision Index rewrite |
| New local latency/memory measurements | `benchmarks/speed.py --stock ...` | No HTTP/Jev speed loop in current `main`, despite docstring/import |
| New original/reversed-choice check | `benchmarks/order.py --stock ...` | No Jev collector; no `--dex`; Dex root/model fixed |
| Train/release model or recollect A/B/C/Jev/Index | No complete authored pipeline in this tree | Do not invent a working command |

All new measurements and raw-evidence changes require the root contract's evaluation approval. Raw benchmark rows can include public personal data and licence restrictions; do not copy them into docs.

## Add or change a report system/suite

Read `SYS`, `NAME`, `load_results`, `collect`, `score_items` and `main` as one flow. A/B/C consumers have different qid/gold shapes. Missing result files are silently absent from `load_results`, but downstream tables can still assume required systems exist. Review both joins and table code.

A new system needs compatible row-ID keyed answers, labels/cohort provenance, naming/chart decisions and every relevant table/denominator. A new suite needs a real collector or supplied evidence owner, not just a new heading. Keep Jev aggregate injection and local per-item scoring distinct.

See the exhaustive [schema/method reference](../reference/evidence-schemas-and-scoring.md). Missing/error local answers currently do not increment the scored denominator. Changing that policy changes meaning, not just formatting.

## Report outputs and prose

The script writes `benchmarks/results/tables.md`, headline-only `tables.json`, `charts/usecases.svg` and `charts/exam.svg`. It reads fixed published `speed.json` and `order.json`. Reruns default to `speed-rerun.json` and `order-rerun.json`; there is no automatic promotion step.

Updating published data is an explicit evidence decision. Update measurement date, methods, scope/coverage, README/card headline claims and benchmark prose after source/evidence review. The report does not rewrite those owning records or reproduce the self-run Index.

## Rerun-method details that affect interpretation

- Speed uses three warmups and fifteen timed calls per short/long × 1/3/5/10/15 question cell. Its p95 is a specific sorted-index expression, not a generic quantile library call. GPU memory is process allocation at measurement time.
- Order uses A/B choice questions with at least three options, seed-3 shuffle, first N rows and original/reversed dict order. It skips null choices. Zero accepted questions can divide by zero; N has integer parsing but no positivity validation.
- Both scripts load Dex then stock Laya. Their current outputs omit Jev, while published saved summaries contain it.

## Verify and contribute honestly

Run the [offline scoring tutorial](../tutorials/trace-saved-evidence.md) for a safe concept check. Use [report regeneration](../how-to/rebuild-saved-report.md) or [GPU rerun planning](../how-to/plan-gpu-reruns.md) only for an authorized evidence task. Record what was actually rerun, never infer fresh accuracy from regenerated SVGs or a source fingerprint.
