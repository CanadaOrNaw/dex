---
title: Change the HTTP adapter
description: Find the owning layer and update every affected client, test and reader
  contract.
kind: developer
source_ref:
- server/dex_server.py#L32-L108
- examples/client.py#L5-L20
- examples/curl.sh#L3-L10
- tests/test_server.py#L8-L45
- CONTEXT.md#L24-L44
- .githooks/docs-pre-commit#L1-L4
---

# Change the HTTP adapter

This is a contribution guide, not authorization to change runtime behavior. First read the root/area contracts and obtain the task's source/runtime scope.

## Locate the behavior

| Change | Owning symbols | Must review with it |
|---|---|---|
| Route aliases | `POST_PATHS`, `Handler.do_POST` | client URLs, three-alias smoke loop, [HTTP reference](../reference/http.md) |
| Body/auth/error behavior | `MAX_BODY`, `_authorised`, `do_POST` | token limitations in clients/tests, privacy diagnostics, [configuration](../reference/configuration.md) |
| Default answer fields / extras | `EXTRAS`, `jev_shape`, response assembly | exact-field test, synthetic fixture, type reference and downstream report consumers |
| Loading/device/dtype | `MODEL_DIR`, `load`, startup warmup | requirements, deployment values, provenance and dated evaluation limits |
| Listener/port | main argument parse and server creation | fixed client/test defaults, container/unit, exposure policy |

Detailed input schema/scoring belongs to Laya, not a parallel local implementation. Do not add a second source of truth to silence a documentation mismatch.

## A bounded change workflow

1. Read all callers and tests for the selected symbol. Note current defaults, errors and security boundaries before editing.
2. Name affected pages/interfaces in `docs/verification/manifest.json`. A new meaningful source/interface must be classified, not omitted.
3. Add a narrowly scoped failing check in an approved source task. The current live suite has known gaps; docs-only examples cover pure shape/scoring only.
4. Make the smallest complete source change, then update clients, tests, reference, tutorial expected output and compatibility notes together.
5. Run authorized checks in the existing project environment. Do not start a model, endpoint or GPU benchmark as a side effect of docs validation.
6. Record claim-to-source observations and exact outcomes. Ask an independent reviewer to recheck affected source, prose and reader tasks. A new hash is not acceptance.

## Existing traps to preserve or address explicitly

Nonnumeric `Content-Length` parsing is outside the 422 exception block; nonobject JSON can raise AttributeError. Result filtering is also outside that block. These are static observations, not freshly reproduced endpoint failures. If changing them, do so as an approved adapter task with tests—not a silent docs fix.

`DEX_TOKEN` and `DEX_EXTRAS` are captured at import. Setting environment values after module import does not change those captured globals. Extras-on changes field shape; the provided integration script expects default shape and has no bearer support.

## Collaboration and maintenance

Preserve unrelated dirty work and real Git index state. Do not hand-edit old generated HTML/PDF or infer hook enforcement from `.githooks/docs-pre-commit` presence. Parent owns shared-site validation/release. [Status](../status.md) records current documentation limits; [collaboration](../collaboration.md) names source authority and approval boundaries.
