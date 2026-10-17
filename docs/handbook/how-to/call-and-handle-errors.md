---
title: "Call Dex and handle errors"
description: "Use real client interfaces, keep tokens private and distinguish HTTP shape from decision quality."
kind: "how-to"
source_ref: ["examples/client.py#L5-L20", "examples/curl.sh#L3-L10", "server/dex_server.py#L69-L98", "CONTEXT.md"]
---

# Call Dex and handle errors

Use this only with an authorized endpoint and nonprivate input. The [offline shape example](../tutorials/read-a-decision-offline.md) is the safe no-server alternative. No HTTP calls were run for this handbook.

## Choose an existing client

`examples.client.decide(state, questions, url=URL, token=None)` constructs JSON and optional bearer, posts with a 60-second urllib timeout and returns `response["answers"]` only. Default URL is loopback `/v1/systemone`. It does not return model/usage or implement retries/error translation.

The synthetic main is invoked by:

```bash
.venv/bin/python examples/client.py
```

It sends a backup-problem example with noul/score questions and prints answer JSON. Inspect target/text first. `sh examples/curl.sh` sends a synthetic billing message with all three types to a fixed loopback URL; it has no bearer support and pipes to JSON formatting. Neither command should be run merely to check page links.

For an application integration, pass your approved URL and token privately to `decide`; do not paste token values into examples or logs. The request/answer fields are described in [type reference](../reference/question-answer-shapes.md). API routes/envelope/statuses are in [HTTP reference](../reference/http.md).

## Handle errors at the caller

| Symptom | Source-defined meaning | Action |
|---|---|---|
| 401 JSON error | Configured POST bearer absent/wrong | Check privately; never include token in issue/report |
| 404 JSON error | Literal path not accepted | Check aliases, trailing slash/query string |
| 413 `bad size` | Numeric Content-Length absent/zero/negative or above byte maximum | Fix transport/body length; do not confuse it with model token coverage |
| 422 truncated exception text | JSON/runtime ValueError/KeyError/TypeError in protected block | Retain minimal synthetic reproducer; redact private text |
| Connection/HTTP/JSON exception in Python client | urllib or JSON failure propagates | Record target authorization and failure; no silent model/environment repair |
| Other server exception/disconnect | Not every failure is translated | Consult static caveats in HTTP reference; do not assume 422 |

The curl pipeline lacks `--fail`/pipefail behavior: JSON error bodies can format successfully. Its exit status alone is not HTTP or inference success.

## Interpret a successful response

A 200 response reports `model: dex-1b`, shaped/runtime answers and runtime usage with `cost_usd=0` forced locally. It is not a provenance attestation, factual correctness guarantee or free-hardware claim. Check your labeled workload before automation; see [capabilities and limits](../capabilities-and-limits.md).
