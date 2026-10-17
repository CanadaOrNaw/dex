---
title: Understand scoring without a benchmark rerun
description: Use the real prediction function with synthetic answers, then trace how
  historical reports consume evidence.
kind: tutorial
source_ref:
- benchmarks/report.py#L17-L107
- benchmarks/report.py#L135-L216
- benchmarks/results/tables.json#L1-L7
- BENCHMARKS.md#L128-L154
- docs/verification/examples/offline_examples.py
- docs/verification/examples/test_offline_examples.py
---

# Understand scoring without a benchmark rerun

You will call the real report `pred` function on synthetic answers and identify the report's missing-answer rule. This is not `benchmarks/report.py` execution and does not read retained prompts, gold labels or per-item results.

## Prerequisites

Use the existing project interpreter from the repository root. Read `docs/verification/examples/offline_examples.py`. It AST-selects only `pred`, which uses no model or external dependency. Do not run the report builder on the audited tree: the builder writes published tables/charts and reads retained payloads.

## 1. Predict labels from synthetic answers

```bash
.venv/bin/python -B docs/verification/examples/offline_examples.py scoring
```

Expected exact output:

```json
{"correct": 3, "predictions": ["refund", 2, true, null], "scored": 3}
```

The four invented cases show:

1. `choice` returns the answer's choice key (`refund`).
2. `score` chooses the maximum probability key and converts it to integer level `2`; it does not grade the returned `score` value.
3. `noul` at exactly `0.5` predicts `true`.
4. A missing answer returns `null`/Python `None` and is excluded from the example denominator.

The three accepted predictions match this fixture's invented labels. “Correct: 3” is **not model accuracy**.

## 2. Trace the real saved-report join

Read `collect`, `score_items` and `main` in `benchmarks/report.py`. A has a single question per row; B uses qid `q`; C looks up gold by `row_id|qid`. Per-system results join by row ID. `score_items` skips absent/empty system-result mappings and missing qids, then skips only when `pred` returns None before incrementing the denominator. None/error answers cause that prediction result; malformed typed answers, including an empty per-question noul object, can still raise.

Jev results come from an aggregate summary, not per-request answers in the local report. The saved headline JSON contains only overall rates. This documentation reviewed saved aggregates and consuming code; it did not independently reproduce the original requests or scores.

## 3. Keep two methods separate

This `score_items` denominator excludes prediction-None results; it does not guarantee the full report skips every malformed/missing answer. The separate calibration loop eagerly calls `conf`, which has no None/error guard and can fail before its later value check. See the [calibration failure caveat](../reference/evidence-schemas-and-scoring.md#predictions-confidence-and-statistics). The Decision Index narrative says unsupported requests count wrong and records a self-run, not official-board result. A percentage is meaningful only with its cohort and denominator. See [evidence schemas](../reference/evidence-schemas-and-scoring.md).

## 4. Know what would change files

A separately authorized `python benchmarks/report.py` writes `tables.md`, `tables.json` and two SVG charts. It does not rerun a model, rewrite `BENCHMARKS.md` or regenerate the Decision Index narrative. Speed/order reruns write different filenames that the report does not consume by default.

## Failure, recovery and next step

A missing function or changed prediction contract fails this fixture; review source, expected values and prose together. Do not read raw rows to “repair” a docs-only check. No cleanup is needed: the example reads source text, uses synthetic dictionaries and writes nothing.

Next, read [evaluation maintenance](../developer-guide/maintain-evaluation.md) before an approved evidence change. The [fixture test command](read-a-decision-offline.md#4-recheck-the-fixture) tests both offline examples.
