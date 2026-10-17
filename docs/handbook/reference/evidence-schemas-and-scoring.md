---
title: Evidence schemas and scoring
description: Consumer contracts, answerability denominators, statistical methods and
  historical reproduction limits.
kind: reference
source_ref:
- benchmarks/report.py#L11-L216
- benchmarks/order.py#L30-L79
- benchmarks/speed.py#L22-L75
- benchmarks/results/jev_summary.json#L1-L113
- benchmarks/results/speed.json#L1-L113
- benchmarks/results/order.json#L1-L20
- benchmarks/results/tables.json#L1-L7
- BENCHMARKS.md#L3-L11
- BENCHMARKS.md#L128-L154
- DATA_CARD.md#L9-L30
---

# Evidence schemas and scoring

The following row contracts are inferred from reviewed **consumer code**, not raw-row inspection. Retained prompt/gold/per-item bodies remain in place and are not exported to the site. Aggregates were read; accuracy was not independently recomputed here.

## Input joins

| Pool/input | Fields consumed | Result join / missing behavior |
|---|---|---|
| A usecases JSONL | id, suite, state, exactly one questions qid, gold[qid] | `A-<system>.json` row ID -> qid answer |
| B heldout JSONL | id, state, questions.q, gold.q | `B-<system>.json` row ID -> q answer |
| C exam JSONL + external gold JSON | id, dataset, questions; gold key `id\|qid` | `C-<system>.json` row ID -> qid answer; absent gold skipped |

`load_results` opens only existing system files. `collect` considers Dex, stock-Laya and two ablations; Jev is merged separately. `score_items` skips absent/empty system-result mappings or absent qids, then skips a `pred` result of None (including None/error answers) **before denominator increment**. Malformed typed answers can still raise; empty per-question noul answers are not normalized. This makes local report answerability different from an all-request failure rate.

## Predictions, confidence and statistics

| Type / method | Exact rule |
|---|---|
| choice prediction | Answer `choice` key |
| score prediction | Max `probabilities` key converted to int, or None if empty |
| noul prediction | float probability >=0.5 |
| None / answer with error | `pred` returns None; `score_items` skips it |
| noul confidence | max(p,1-p) |
| other confidence | Max probability value, or None if absent |
| Wilson interval | z=1.96; empty n returns NaN tuple; table cell renders n/a |
| ECE | 15 equal-width bins, weighted absolute confidence-vs-accuracy gap; upper bin edge inclusive |
| Sure subset | confidence >=0.9; reported share/accuracy over accepted predictions |

`score_items` counts at pool and pool+label level. The calibration loop in `main` is different: it guards absent/empty system-result mappings and missing qids, then evaluates both `pred` and `conf` before checking their returned values. `conf` has no None/error guard. None at an existing qid can fail during indexing or `.get`; a noul error/empty object can raise KeyError. A None prediction therefore does not guarantee the full report safely skips that answer. Other malformed typed answers and empty calibration/sure subsets can also fail rather than become a normalized missing result.

Reporting does not fit new runtime calibration. The [synthetic scoring tutorial](../tutorials/trace-saved-evidence.md) exercises `pred` and an invented denominator, not this calibration path. These are static control-flow limits from `benchmarks/report.py`, not freshly reproduced failures or reasons to change product code in a docs task.

## Aggregate summary contracts

- `jev_summary.json`: cells `A/B/C` and `pool|label` -> `[questions, correct]`; disagree counts by model/category; calibration accuracy/ece/sure_share/sure_accuracy. Main injects these counts instead of recollecting Jev. There are no per-request Jev answers in this local reporting contract.
- `tables.json`: `headline` rates only for jev/dex/stock-laya, not every table or original prediction.
- `speed.json`: GPU string, weights_mb, per-system gpu_gb and cells `short|long/k` -> `[median_ms,p95_ms]`. Published file additionally contains jev_api cells. Current rerun writes local models only.
- `order.json`: per-system questions/flip_rate/accuracy_as_written/accuracy_reversed. Published file includes Jev; current rerun does not.

## Rerun schema and method

Speed's short/long constants are synthetic support text. For each 1/3/5/10/15 question cell it performs3warmup+15timed calls, sorts milliseconds, returns median and `t[int(len(t)*0.95)-1]`. GPU allocation is process memory at measurement time, not guaranteed incremental model footprint; an unused `base` variable does not subtract it.

Order uses A/B >=3-option choice pool, seed3 shuffle and firstN, reverses criteria dict order without changing keys/text, skips null choices and reports flips/accuracy across accepted pairs. With no accepted pairs, division can fail. Data/schema failures are not caught or normalized.

## Outputs and reproducibility limits

Report writes tables Markdown, headline JSON and two grouped SVGs using fixed system palette/names. Text/chart labels are interpolated from trusted retained labels; it is not a general untrusted-SVG sanitization layer. It reads published speed/order filenames, not reruns, and does not rewrite README/cards/benchmark narrative.

October8–9 A/B/C saved results are not fresh measurements. The separate October9 Decision Index self-run counts unsupported requests wrong; its private-board comparison is explicitly approximate. The trainer, complete A/B/C/Jev collectors and Index harness are not authored in this repository. Do not manufacture a reproduction command for absent pieces.

See [evaluation maintenance](../developer-guide/maintain-evaluation.md), [report how-to](../how-to/rebuild-saved-report.md) and [capabilities](../capabilities-and-limits.md).
