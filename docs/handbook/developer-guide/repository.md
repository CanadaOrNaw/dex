---
title: Repository and module map
description: Locate every first-party executable module, its dependencies, owner and
  real extension points.
kind: developer
source_ref:
- server/dex_server.py#L22-L108
- examples/client.py#L1-L20
- examples/curl.sh#L1-L10
- tests/test_server.py#L1-L45
- benchmarks/report.py#L1-L216
- benchmarks/speed.py#L1-L79
- benchmarks/order.py#L1-L84
- requirements.txt#L1-L6
- CONTEXT.md#L6-L44
---

# Repository and module map

## Executable modules

| File / entry | Responsibility | Dependencies and limits |
|---|---|---|
| `server/dex_server.py` | `load`, `jev_shape`, `Handler`, startup/listener | stdlib HTTP/threading/JSON + Torch + `laya.agent.Agent`; no authored inference engine |
| `examples/client.py` | `decide(state, questions, url=URL, token=None)` and synthetic main | stdlib urllib/JSON; returns answers only, timeout 60s |
| `examples/curl.sh` | One synthetic request with all three types | curl + `python3 -m json.tool`; fixed loopback, no bearer/HTTP-fail flag |
| `tests/test_server.py` | Live endpoint checks, `post`, `check` | stdlib urllib; no fixtures or model mock; executes requests at module top level |
| `benchmarks/report.py` | Read saved evidence, `pred`, `conf`, Wilson/ECE, join/score, table/SVG generation | stdlib only; writes outputs and reads retained payloads |
| `benchmarks/speed.py` | `questions`, `timed`, `local`, argparse `main` | Torch CUDA, Laya and adapter loader; current main measures local models, not HTTP |
| `benchmarks/order.py` | `load_server`, `reverse`, argparse `main` and inner `run` | Torch CUDA/Laya, A/B datasets; adapter picked via first `*_server.py` glob |

All six Python modules and the shell example were reviewed. No package dispatcher, plugin registry, training module or offline product fixture suite exists here. Never import `tests/test_server.py` merely to inspect symbols: it performs network calls at import.

## Supporting inputs and outputs

- `requirements.txt` records minimum runtime dependencies, not a locked environment.
- `Dockerfile` and `deploy/dex.service` are deployment inputs, not installed-state evidence.
- `model/` is ignored local artifact state. Small config/manifest files describe intended metadata; weights and tokenizer vocabulary were not read or verified.
- `benchmarks/data/` and per-item `benchmarks/results/` are retained bulk evidence. Source consumer contracts and aggregate summaries are documented; raw rows are not exported into this handbook.
- Cards, README, NOTICE, citation and release notes own the release narrative/licences. `CONTEXT.md` preserves explicit identity/runtime approval boundaries.
- `docs/handbook` owns reader pages. `docs/verification` is private review/fixture data, not site content. Old generated handbook products are excluded from admission and were not edited or rebuilt by this Dex authoring task; the parent separately disclosed legacy regeneration.

## Real extension points, not a plugin API

- A route alias is a concrete `POST_PATHS` edit; a response-field change is a `jev_shape` edit. Update clients, tests and [HTTP/types reference](../reference/http.md) together.
- A report system/suite requires changes to `SYS`, `NAME`, `load_results`, `collect` and table/chart code plus compatible retained evidence. Adding one string is not a full new evaluator.
- `DEX_MODEL` and speed's `--dex` select an existing artifact. They do not prove arbitrary weights are compatible or authorize publication.
- No trainer/collector/publisher should be documented as working without new owned source and approval.

Continue with [testing](testing.md), [adapter changes](change-the-adapter.md), [evaluation maintenance](maintain-evaluation.md) or [architecture](../architecture.md).
