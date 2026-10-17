# Dex benchmark evidence: folder contract

Saved prompts/results plus report generation, separate from GPU remeasurement.

## Entry routes

- [workspace contract](../CONTEXT.md).
- [method and limits](../BENCHMARKS.md).
- [data provenance](../DATA_CARD.md).
- [report builder](report.py).
- [saved results](results/).
- [saved prompts](data/).
- [speed rerun](speed.py).
- [order rerun](order.py).

## Inputs

The selected saved prompts, labels and result/summary files. Respect dataset provenance and do not copy raw rows into a general docs portal.

## Process

Follow BENCHMARKS for methods. report.py rebuilds tables/charts from saved evidence; speed.py and order.py are separate model/GPU runs. Do not conflate a regenerated table with new measurements.

## Outputs

Tables/charts and result files at their existing paths; report claims retain the measurement date and coverage limits.

## Human check

Zack approves costly reruns. Keep unsupported inputs, self-run vs official-board status and knowledge/correctness limitations visible; no benchmark was rerun for this contract.
