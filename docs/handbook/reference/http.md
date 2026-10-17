---
title: HTTP interface
description: Exact paths, envelope, validation order, statuses and unhandled input
  boundaries.
kind: reference
source_ref:
- server/dex_server.py#L32-L45
- server/dex_server.py#L60-L108
- tests/test_server.py#L24-L45
---

# HTTP interface

## Routes

| Method | Exact path(s) | Behavior |
|---|---|---|
| POST | `/v1/systemone`, `/api/v1/decide`, `/v1/decide` | Optional bearer, byte gate, JSON/runtime call and typed answer response |
| GET | `/health` | Unauthenticated model-loaded/device report |
| GET/POST | Other literal path | 404 JSON `{error: "not found"}` |

The adapter compares literal `self.path`; trailing slash/query strings are not normalized. No authored PUT/DELETE/OPTIONS or CORS behavior exists. Standard-library responses for other methods are not a promised JSON interface.

## Request and validation order

```json
{"state": "A synthetic message", "questions": {"urgent": {"type": "noul", "instructions": "Does it sound urgent?"}}}
```

1. Reject an unsupported path before auth.
2. If `DEX_TOKEN` was set at import, require exact `Authorization: Bearer ` plus that private value.
3. Parse `Content-Length` as integer, default 0; require 1–1,000,000 bytes.
4. `json.loads` exactly the read bytes.
5. Under a global lock call `AGENT.system_one(body.get("state"), body["questions"])`.

No local Content-Type check, standalone JSON Schema, question-count limit or detailed input-type validator exists. State/examples are text, but missing state is passed as None; questions lookup is locally required. Laya owns detailed validation/token/scoring behavior.

## Responses

POST success is HTTP 200 JSON with `model: "dex-1b"`, `answers` and `usage`. Usage is a copied runtime mapping with `cost_usd` overwritten to zero. Other usage fields, including token counts, are runtime-provided; no independent output-token insertion occurs here. Default answers are filtered to the [per-type whitelist](question-answer-shapes.md), unless extras-on returns raw runtime answers.

Health is HTTP 200 `{ok, model, device, dtype}`: ok tests agent non-None, model is the fixed name, device string comes from agent, dtype is the fixed string `bfloat16`. Main loads/warms before binding, so a source definition alone does not prove a health response exists. Health is not token protected and does not attest identity, quality or calibration.

`_send` JSON-encodes payloads and sets JSON Content-Type/Content-Length. Access logging is suppressed by the adapter.

## Error table

| Status | Condition in source | Payload |
|---|---|---|
| 401 | Accepted POST, configured bearer absent/wrong | `missing or wrong bearer token` error |
| 404 | GET/POST path not recognized | `not found` error |
| 413 | Numeric length <=0 or >1,000,000 | `bad size` error |
| 422 | ValueError, KeyError or TypeError during JSON decode or runtime call | `str(exc)[:200]` error |

The maximum is **bytes**, not the runtime's token budget. Missing questions is a tested 422 case. The source does not guarantee every malformed request becomes 422:

- Nonnumeric Content-Length conversion is outside the try block.
- A valid nonobject JSON body can cause uncaught AttributeError at `.get`.
- Other runtime exceptions and usage/answer-shaping failures are not caught by that block.
- No generic exception-to-JSON barrier, body-read timeout or rate-control policy is supplied locally.

These are static source observations, not fresh endpoint reproductions. Exception diagnostics may include private values from a dependency; redact before sharing.

## Compatibility boundary

README claims Jev-shaped compatibility based on prior checks; this audit did not query Jev. Default field keys and aliases are local facts. No `credits_remaining_usd`; extras-on is a different field boundary. One lock serializes inference. See [security and compatibility](../concepts/security-and-compatibility.md), [configuration](configuration.md) and [calls](../how-to/call-and-handle-errors.md).
