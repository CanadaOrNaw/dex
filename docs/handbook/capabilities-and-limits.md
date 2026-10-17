---
title: Capabilities and limits
description: Decide whether typed output fits a task without overreading saved benchmark
  claims.
kind: concept
source_ref:
- README.md#L33-L82
- MODEL_CARD.md#L56-L67
- BENCHMARKS.md#L3-L11
- BENCHMARKS.md#L106-L154
- server/dex_server.py#L42-L45
---

# Capabilities and limits

## Shape is not correctness

The public examples use three question types: `choice`, `score` and `noul` (yes/no). The default adapter filters answer keys; it does not validate that every required field exists or that the answer is true. Laya owns scoring and detailed validation. Do not infer that wrong decisions, bias, unsafe choices or information disclosure are impossible because there is no generated prose.

`README.md` and `MODEL_CARD.md` have stronger opening marketing wording. This handbook follows the root contract's explicit caution and the saved failure evidence instead of repeating an absolute “cannot hallucinate” claim.

## Historical evidence and fit

The report dates its runs to October 8–9 on one RTX 3070 Ti. It scores human labels, not agreement with Jev.

| Cohort | Questions | Dex reported accuracy | Interpretation |
|---|---:|---:|---|
| A: ten use cases | 1,244 | 81.5% | Partly in-distribution; other rows of some datasets appeared in training. Routing uses proxy gold. |
| B: whole held-out tasks | 1,737 | 74.4% | 161 tasks reported never trained on. |
| C: eight held-out exam datasets | 2,346 | 63.8% | Knowledge and retrieval gaps remain. |
| Combined | 5,327 | 71.4% | This saved cohort is not a guarantee for a new workload. |

Source: `BENCHMARKS.md`, setup/results sections. Aggregates were reviewed; raw rows and individual saved answers were not re-scored here.

## Where to be cautious

- Reported MedMCQA accuracy is 30.7%, PubMedQA 55.0%. These are not suitable medical decision guarantees.
- Work-correctness judging is 52.5%. Do not use it as a code correctness test.
- Stock Laya beats Dex on saved jailbreak screening and moderation/spam results.
- English-only training claims, input training limit of 1,792 tokens and up to 30 choice options are stated limits, not an adapter byte-validation rule.
- Many questions/long inputs are slower than stock Laya in the saved run. Concurrent throughput, other languages and training-run variation are not measured.
- Probabilities are temperature-fitted. A saved calibration error of 0.058 does not establish calibration on new traffic.

## Decision Index is a separate method

The report's October 9 self-run records skill 12.99, raw 32.47 and 89.2% coverage over 140,620 requests. It is **not an official board score**. Private board tests cannot be self-run; unsupported answers count wrong there. No Index harness or full run receipt is shipped in this source tree.

The saved table report skips missing/error predictions in local scoring. Do not compare denominators without reading [evidence schemas and scoring](reference/evidence-schemas-and-scoring.md).

## Choose the next step

For an unfamiliar task, use the saved report only to select a hypothesis. Obtain approval for an appropriate labeled evaluation before deploying automation. Start learning the interface with the [offline tutorial](tutorials/read-a-decision-offline.md), not a blind live install. Check [status](status.md) for remaining uncertainty.
