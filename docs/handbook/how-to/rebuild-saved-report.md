---
title: Rebuild a saved benchmark report
description: Understand the read/write boundary and exact outputs before an approved
  report regeneration.
kind: how-to
source_ref:
- benchmarks/report.py#L1-L216
- benchmarks/CONTEXT.md#L18-L30
- DATA_CARD.md#L9-L30
- README.md#L84-L87
---

# Rebuild a saved benchmark report

Report regeneration does not run a model or spend API credit, but it **does read retained prompt/label/result payloads and overwrite output files**. It was not run in this documentation task. The [synthetic scoring tutorial](../tutorials/trace-saved-evidence.md) is the read-only alternative.

## Preconditions

Use an authorized evidence-maintenance task, reviewed retained input set, existing interpreter and approved output scope. Respect dataset licences and public-personal-data limits. Preserve unrelated changes in existing table/chart outputs; the script has no dry-run or output-directory flag.

## Existing command and effects

```bash
.venv/bin/python benchmarks/report.py
```

It reads A/B/C prompt/gold/result consumers, Jev summary, saved speed and saved answer-order summaries. It writes:

| Output | Content |
|---|---|
| `benchmarks/results/tables.md` | Accuracy, per-group results, disagreement/calibration, ablation, speed/order tables |
| `benchmarks/results/tables.json` | Only overall headline rates |
| `benchmarks/charts/usecases.svg` | Saved A per-use-case grouped bars |
| `benchmarks/charts/exam.svg` | Saved C per-dataset grouped bars |

The script creates charts directory if needed and prints table Markdown. It does **not** rewrite `BENCHMARKS.md`, README/card claims or the Decision Index section. It reads `speed.json`/`order.json`, not `*-rerun.json`.

## Verify the result

Expect normal exit 0 only if required files, schemas and denominators are valid. File/JSON/schema/math exceptions are uncaught. Inspect changed counts, cohorts, missing-answer behavior, units and chart values before accepting output. Regeneration is not proof that original measurements were valid or fresh.

Review owning prose separately with the evidence date/method. Do not “fix” missing results by inventing rows or silently changing scoring. See [evaluation maintenance](../developer-guide/maintain-evaluation.md) and [evidence reference](../reference/evidence-schemas-and-scoring.md).

## Recovery and cleanup

If it fails or changes unexpected outputs, preserve redacted evidence and stop for owner review. Do not reset/clean a shared working tree. Cleanup/promotion of regenerated files belongs to the approved maintenance task, not this handbook.
