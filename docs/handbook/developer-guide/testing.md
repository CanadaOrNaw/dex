---
title: Testing and documentation evidence
description: Separate safe offline fixture checks from live integration, GPU measurements
  and acceptance.
kind: developer
source_ref:
- tests/test_server.py#L1-L45
- tests/CONTEXT.md#L12-L26
- benchmarks/report.py#L209-L216
- benchmarks/speed.py#L57-L79
- benchmarks/order.py#L34-L84
- docs/verification/examples/offline_examples.py
- docs/verification/examples/test_offline_examples.py
---

# Testing and documentation evidence

## Safe documentation checks

From the project root, use the existing environment:

```bash
.venv/bin/python -B -m unittest discover -s docs/verification/examples -p test_offline_examples.py -v
```

Expected: two passing tests and `OK`. These docs-only tests call AST-selected pure `jev_shape` and `pred` with synthetic data. They do not import the server/report modules, load weights, contact an endpoint, read retained rows or write outputs. Their scope is intentionally small; they are not a replacement product suite.

The [shape](../tutorials/read-a-decision-offline.md) and [scoring](../tutorials/trace-saved-evidence.md) commands expose exact observable examples. A changed function contract should fail a test and trigger prose review, not automatic expected-output refresh.

## Existing live integration suite

`tests/test_server.py [BASE_URL]` is a standalone script that immediately sends requests. It checks:

- All three POST aliases answer choice/score/noul questions.
- The chosen option is offered; choice and score probability sums are within 0.01 of one; noul is in [0,1].
- Exact default field sets, local cost zero and an obvious banana choice.
- Missing questions produces 422; health reports ok.

There are twelve named checks. Completed checks exit 0 if all pass, 1 if any check fails. Connection/HTTP/JSON errors may terminate sooner. The script has no token parameter and assumes `DEX_EXTRAS` is off. It does not test authentication, 404/413, malformed length/nonobject JSON, runtime exception shaping, provenance, concurrency or calibration.

**Do not run it in a docs-only task.** Follow [authorized server checks](../how-to/check-an-authorized-server.md) only with an already approved endpoint.

## Other commands are not tests

- `benchmarks/report.py` is offline inference-wise but reads retained payloads and overwrites tables/charts.
- Speed/order scripts perform real model loads and GPU measurements. They are not smoke checks.
- `server/dex_server.py --help` is not help: the script tries to parse the argument as an integer port.
- No authored CI workflow, standalone product fixture suite or dependency lock was found in the reviewed source inventory. The existing docs hook wrapper does not prove hook activation or server protection.

## Evidence and handoff

Record the exact command, environment, effects, exit and output. Keep a failed run separate from an unrun check. Source hashes prove byte identity, not correctness or product acceptance. New docs remain changes-required until an independent reviewer verifies claims and performs the documented first-use and developer tasks without author assistance.
