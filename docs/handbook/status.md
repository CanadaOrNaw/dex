---
title: Status and verification limits
description: Source-reviewed behavior, historical evidence, documentation checks and
  outstanding owner decisions.
kind: status
source_ref:
- CONTEXT.md#L24-L44
- BENCHMARKS.md#L3-L11
- BENCHMARKS.md#L120-L154
- RELEASE_NOTES.md#L1-L9
- server/dex_server.py#L32-L108
- docs/verification/examples/offline_examples.py
- docs/verification/examples/test_offline_examples.py
---

# Status and verification limits

## Works and evidence

- Source review covers all authored executable modules, client/deployment/dependency definitions, cards, contracts, small local model metadata and saved aggregates. The original whole-tree audit classified retained bulk/generated/runtime exclusions explicitly.
- Server source implements three POST aliases, optional POST bearer, health, serialized scoring and default answer filtering. No server/model was launched or queried for these docs.
- The October8–9 report records human-label results and a separate October9 self-run Index. Saved aggregates/code were reviewed; raw prompts/per-item answers were not re-scored.
- Documentation-only native offline shape/scoring examples and two fixture tests ran successfully with the existing project interpreter. They use real AST-selected pure functions and synthetic values, not inference. See [first-use tutorial](tutorials/read-a-decision-offline.md).

## Failed, limited and unknown

Saved evaluation reports weak knowledge/code-correctness performance and tasks where stock Laya wins. Typed output is not proof of correctness/calibration. Short model identity wording conflicts with cards/root contract; actual weight provenance/checksum match is unverified.

There was no fresh failed server run: missing live checks are unknown, not failures. Supported dependency/host/device versions and exact upstream Laya validation/extras semantics were not checked. Static error/auth/exposure gaps are described in [security](concepts/security-and-compatibility.md), not silently fixed.

The first docs-fixture test attempt exposed incomplete stub output; assertions were then made to fail normally on missing behavior, followed by implementation and two passing tests. These are author test-development observations, not independent acceptance.

## In progress and authority

This handbook does not assert active training, restart, deployment or public release. Root `CONTEXT.md` and `RELEASE_NOTES.md` remain the owner boundary/history. No new task queue or roadmap is created here.

The current documentation authorship snapshot is **changes-required pending independent source review and reader/developer trials**. Author checks, source hashes and a recent date do not self-accept prose or product behavior. Parent owns shared-site integration/release and its current delivery status.

## Outstanding owner decisions

- Resolve artifact identity with provenance without changing weights by assumption.
- Revalidate environment/device/API only in a separately approved runtime task.
- Locate or create properly owned evidence collectors if full training/Jev/Index reproducibility is required.
- Approve labeled evaluation and exposure/privacy controls before automation/deployment.
- Have a fresh reviewer inspect claims/interfaces/navigation/examples and perform the first-use and maintainer tasks without author memory.

## Verification boundaries

No install/download, model import/weight read, endpoint request, GPU/service query, report regeneration, container build, live integration suite, publication or actual Git staging/commit ran in this authoring task. Old generated handbook HTML/PDF/receipt were not edited or rebuilt by this Dex authoring task and remain excluded from admission. The parent separately disclosed legacy-renderer regeneration; no byte-preservation or product proof is inferred from those outputs. Private `docs/verification` records exact authored inputs/checks; those records are not public website content.
