---
title: Commands and Python entry points
description: All implemented script arguments, defaults, effects, output paths and
  exit behavior.
kind: reference
source_ref:
- server/dex_server.py#L29-L108
- tests/test_server.py#L1-L45
- examples/client.py#L5-L20
- examples/curl.sh#L1-L10
- benchmarks/report.py#L1-L216
- benchmarks/speed.py#L57-L79
- benchmarks/order.py#L34-L84
---

# Commands and Python entry points

Commands are shown in their source form. Use the existing `.venv/bin/python` instead of generic `python` for authorized local execution. Only the documentation fixtures linked below were run for these pages. No installer, runtime, report, live test or GPU command is silently executed by documentation validation.

## Server

`python server/dex_server.py [PORT]`

- First positional integer, default 18766; extra argv unused. No argparse or `--help`.
- Imports Torch/Laya, loads/warmups model, may use GPU, binds configured host and serves forever.
- No explicit exit mapping; port/load/warmup/bind exceptions propagate nonzero. There is no normal “test passed” exit while serving.

## Live smoke checks

`python tests/test_server.py [BASE_URL]`

- Default base `http://127.0.0.1:18766`; first argument used literally. No auth parameter/parser.
- Three inference POSTs, one invalid POST and health GET; timeouts 60s POST/10s health.
- Completed checks exit 0 on all-pass, 1 on logical failure. Uncaught network/HTTP/JSON failures can abort earlier.

## Client examples

`python examples/client.py`: no parsed arguments; fixed loopback URL and synthetic backup text, prints answers. Normal completion 0; urllib/JSON exceptions propagate.

`sh examples/curl.sh`: no arguments; fixed loopback billing POST, JSON formatter pipeline. No bearer or curl HTTP-fail flag. Pipeline success may only mean an error JSON formatted successfully.

Reusable helper: `examples.client.decide(state, questions, url=URL, token=None)` adds Content-Type, optional bearer, urllib timeout60 and returns only `answers`. It is not a packaged/stable SDK or an automatic retry policy.

## Saved report

`python benchmarks/report.py`: no parsed flags or alternate root/out path. Reads retained data/results plus Jev/speed/order aggregates; writes two tables and two charts, prints table Markdown. Does not run inference or rewrite benchmark/card prose. Normal completion 0; file/JSON/schema/math errors propagate. See [report how-to](../how-to/rebuild-saved-report.md).

## GPU speed arguments

`python benchmarks/speed.py --stock PATH [--dex PATH] [--out PATH]`

| Argument | Type / default | Effect |
|---|---|---|
| `--stock` | Required path string | Stock Laya model directory |
| `--dex` | Repository `model` | Dex directory passed to adapter loader |
| `--out` | `benchmarks/results/speed-rerun.json` | JSON output; parent directory not created |

Argparse provides `-h/--help`; parser usage errors exit 2. Note Torch is imported before argument parsing; help is not a dependency-free check. Normal completion 0; CUDA/load/write errors uncaught. Current main queries CUDA and runs local models only, no HTTP/Jev loop. See [GPU planning](../how-to/plan-gpu-reruns.md).

## GPU answer-order arguments

`python benchmarks/order.py --stock PATH [--n N] [--out PATH]`

| Argument | Type / default | Effect |
|---|---|---|
| `--stock` | Required path string | Stock Laya model directory |
| `--n` | int / 400 | First N after seeded pool shuffle; no positivity guard |
| `--out` | `benchmarks/results/order-rerun.json` | Summary JSON output; parent directory not created |

No `--dex` or Jev target parameter. Argparse help/usage as above; Torch import precedes parse. Normal completion 0; file/model/CUDA/write or zero-denominator errors uncaught.

## Python internals and absent surfaces

`server.dex_server.jev_shape(answers)` is a pure whitelist helper; `load()` loads an agent using global MODEL_DIR and device environment. External `laya.agent.Agent(...).system_one(state, questions)` is called, not defined in this repository. Private model attribute access is a compatibility risk, not a new public API guarantee.

No authored package entry point, trainer, release publisher, complete A/B/C/Jev collector or Index runner exists here. [Offline documentation fixtures](../tutorials/read-a-decision-offline.md) have their own explicitly bounded commands and do not add product CLI features.
