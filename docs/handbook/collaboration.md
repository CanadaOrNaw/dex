---
title: Project and collaboration overview
description: Purpose, working evidence, decisions, contribution routes and honest
  demonstrations.
kind: overview
source_ref:
- CONTEXT.md#L3-L44
- AGENTS.md#L5-L13
- README.md#L33-L91
- RELEASE_NOTES.md#L1-L9
- DATA_CARD.md#L3-L30
---

# Project and collaboration overview

## Intended outcome and audiences

Dex aims to answer typed decision questions locally: route a request to an offered option, score against an ordered scale or assign a yes/no probability. Application developers need predictable envelopes and clear failure handling. Adapter maintainers need the boundary between HTTP and the external Laya runtime. Evaluators need dated, scoped evidence rather than claims inferred from structured output.

The root `CONTEXT.md` owns the workspace boundary: model release, HTTP adapter and reproducible benchmark evidence. `RELEASE_NOTES.md` owns release history. `MODEL_CARD.md`, `DATA_CARD.md` and `BENCHMARKS.md` own their provenance and measured claims. This handbook explains those sources; it is not a second training plan or task queue.

## What works and what that means

Source implements typed POST aliases, optional POST bearer, serialized model calls and field filtering. There are callable clients, a live-only integration script, saved-report generation and GPU speed/order tools. See [architecture](architecture.md) for ownership and [status](status.md) for checks actually performed.

The saved report records 71.4% overall accuracy across its 5,327 labeled questions and substantial weaknesses on knowledge and code-correctness tasks. These are dated report claims; retained raw answers were not recomputed by this documentation task. A generated table, a health response and a model label are three different kinds of evidence.

## Important decisions in the existing implementation

- **Separate adapter from scoring.** `server/dex_server.py` handles HTTP and delegates `system_one` to Laya. Detailed question validation and scoring are not implemented locally.
- **Constrain the default response.** `jev_shape` keeps a per-type field list. `DEX_EXTRAS=1` changes that boundary and is not the default Jev-shaped contract.
- **Serialize inference.** A global lock surrounds the shared runtime call; threaded HTTP handling is not parallel model throughput.
- **Keep measurements separate.** Report regeneration uses saved evidence. Speed/order scripts perform new GPU work and write separate rerun files.
- **Retain provenance uncertainty.** Short agent instructions say Laya-1B; cards and local metadata describe an Ettin encoder with Laya runtime. Resolving that needs artifact provenance, not prose normalization.

These decisions are visible in `server/dex_server.py`, `benchmarks/report.py` and the root contract. They are not a newly invented architecture roadmap.

## Limits and blockers

Model identity, the installed runtime/device support matrix and exact upstream schema guarantees remain unverified. There is no released training dataset, trainer, complete A/B/C/Jev result collector or Decision Index harness in this tree. The container is not secure remote-exposure policy. See [capabilities](capabilities-and-limits.md), [provenance](provenance-and-licences.md) and [security](concepts/security-and-compatibility.md).

## Human and agent contribution path

1. Read `AGENTS.md`, `CONTEXT.md` and the affected area's `CONTEXT.md`.
2. Locate owning source, tests and historical evidence with the [repository map](developer-guide/repository.md).
3. Identify impacted interfaces and reader pages using the [change guide](developer-guide/change-the-adapter.md) or [evaluation maintenance guide](developer-guide/maintain-evaluation.md).
4. Make only the authorized change. Preserve unrelated dirty work, retained rows and model artifacts. Never hand-edit generated products.
5. Use reviewed offline checks first. Runtime/deployment, costly evaluation and publication require Zack's approval under the root contract.
6. Update reader pages and the private verification map. Ask an independent reviewer to compare claims to source and complete the reader/developer tasks. Author checks are not self-acceptance.

## Progress and demonstrations

`RELEASE_NOTES.md` records release 1.0.0 on October 9. It is not proof of current uptime or new active training. [Status](status.md) distinguishes source review, historical results and outstanding runtime checks without duplicating a live queue.

The [answer-shape tutorial](tutorials/read-a-decision-offline.md) and [scoring tutorial](tutorials/trace-saved-evidence.md) demonstrate real pure functions on synthetic answers. They are safe documentation examples, not model-quality demonstrations. No live product demonstration or human acceptance trial was performed for these pages. Independent documentation review and integrated website delivery belong to the shared-site owner.
