---
title: Check an authorized server
description: Run the existing live smoke script only against a separately approved
  endpoint.
kind: how-to
source_ref:
- tests/test_server.py#L1-L45
- tests/CONTEXT.md#L12-L26
- server/dex_server.py#L69-L98
---

# Check an authorized server

The existing script is **live integration**, not an offline unit test. It sends inference requests. No endpoint was started or queried for this documentation.

## Preconditions

1. The owner explicitly approves this exact running endpoint and synthetic input.
2. Model/environment provenance is known to that runtime task.
3. `DEX_TOKEN` is unset and `DEX_EXTRAS` is off for the unchanged script. It sends no Authorization header and requires exact default answer fields. Do not disable real security to fit a test; an authenticated deployment needs a separately reviewed test change.
4. Work from the project root in its existing environment.

## Command

For the approved default loopback endpoint:

```bash
.venv/bin/python tests/test_server.py
```

An optional first argument supplies a full base URL, default `http://127.0.0.1:18766`. Inspect any alternate target before use; arbitrary URL substitution can send text elsewhere.

## Expected result and limits

A completed success prints twelve named `PASS` checks and exits 0. A completed logical failure prints `FAIL` and exits 1; transport/HTTP/JSON failures may abort sooner. Record full redacted output and exit, not just the final line.

It checks three aliases, all three types, offered option, probability sums/range, default field sets, cost zero, banana case, missing questions 422 and health. It does not establish calibration, general quality, auth, model identity, real dtype, security, concurrency or deployment safety. The presence of a test file is not passing evidence.

## Recovery and cleanup

For 401, stop: this script lacks auth support. For field mismatch, check extras mode before claiming model failure. For connection errors, ask the owner to inspect the approved runtime; do not start/restart/install anything as an automatic fix. Do not stop a shared service at the end. Continue with [testing scope](../developer-guide/testing.md) or [HTTP errors](../reference/http.md).
