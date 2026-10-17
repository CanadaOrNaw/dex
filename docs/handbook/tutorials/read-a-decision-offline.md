---
title: Read a typed decision offline
description: Run the real answer filter on synthetic answers without loading a model
  or making an HTTP request.
kind: tutorial
source_ref:
- server/dex_server.py#L42-L45
- examples/curl.sh#L3-L10
- tests/test_server.py#L9-L35
- docs/verification/examples/offline_examples.py
- docs/verification/examples/test_offline_examples.py
---

# Read a typed decision offline

This is a **documentation example**, not a live prediction. You will observe the adapter's real answer-key filter on invented answer values. The fixture selects `jev_shape` from source with Python AST; it does not import the server module, PyTorch or Laya.

## Prerequisites and safety

- Work from the Dex repository root with its existing `.venv/bin/python`.
- Review `docs/verification/examples/offline_examples.py` first. It reads only the named source functions and uses synthetic data.
- Do not start a server, download a model, read benchmark rows or supply real customer text.

## 1. Identify the question types

`examples/curl.sh` contains a synthetic billing request with `intent` (`choice` with named criteria), `urgency` (`score` with ordered labels) and `refund` (`noul`). Those question IDs belong to the caller. Read them as source; **do not run the curl script** for this tutorial.

The server's `jev_shape` permits these answer fields:

| Type | Kept fields |
|---|---|
| `choice` | `type`, `choice`, `confidence`, `probabilities` |
| `score` | `type`, `score`, `confidence`, `legend`, `probabilities` |
| `noul` | `type`, `noul` |

Only fields present in an answer are retained. The filter does not fill or validate missing fields.

## 2. Run the safe example

```bash
.venv/bin/python -B docs/verification/examples/offline_examples.py shape
```

Expected exact output:

```json
{"input_unchanged": true, "runtime_only_removed": true, "types": ["choice", "noul", "score"]}
```

This confirms that the synthetic answers still cover all three types, runtime-only fields were removed and the input dictionary was not mutated. It does **not** confirm a model label, probability, semantic truth or remote Jev behavior.

## 3. Inspect the source boundary

The fixture deliberately adds `action` and a yes/no `confidence` field to its synthetic input. `jev_shape` removes them in the default response. The live handler bypasses this filter when `DEX_EXTRAS=1`; see [question and answer shapes](../reference/question-answer-shapes.md).

## 4. Recheck the fixture

```bash
.venv/bin/python -B -m unittest discover -s docs/verification/examples -p test_offline_examples.py -v
```

Expected: two tests run, exit 0 and `OK`. These tests cover the shape and [scoring example](trace-saved-evidence.md), not the live `tests/test_server.py` suite.

## Failure, recovery and cleanup

If a function moved or was renamed, the fixture fails its source-selection assertion. If its contract changed, an assertion or expected output changes. Stop and review the source/doc impact; do not weaken the fixture merely to get green. Missing interpreter means the environment needs a separate owner task, not an automatic install.

The example writes no files, opens no endpoint and imports no model runtime. `-B` suppresses bytecode output. There is nothing to clean up. Next, follow [scoring](trace-saved-evidence.md) or [HTTP reference](../reference/http.md).
