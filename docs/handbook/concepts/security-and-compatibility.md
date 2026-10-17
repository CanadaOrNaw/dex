---
title: "Security, privacy and compatibility"
description: "Understand exposure, data handling, errors and dependency assumptions before using Dex."
kind: "concept"
source_ref: ["server/dex_server.py#L29-L108", "Dockerfile#L1-L10", "deploy/dex.service#L1-L16", "requirements.txt#L1-L6", "DATA_CARD.md#L7-L30", "CONTEXT.md", "README.md#L30-L30"]
---

# Security, privacy and compatibility

## Network exposure

Source uses the standard-library HTTP server, not TLS. Loopback is default, with no key. Optional token applies only to accepted POST routes; health is unauthenticated. The container overrides bind to all interfaces but supplies no token/TLS. A host change or container port mapping is not a security policy.

No authored CORS, rate limiter, bounded queue, request timeout or remote authentication layer is supplied. ThreadingHTTPServer can accept handlers while one lock serializes scoring; this is not concurrent throughput proof or denial-of-service protection. Remote exposure needs a separately approved design.

## Private text and diagnostics

The adapter sends state/questions to a selected local runtime and has no authored request database. Access logging is suppressed. That does not prove upstream dependencies, process memory or exception messages cannot retain/disclose input.

422 returns the first200characters of selected exception text. Dependency errors may contain input. Use synthetic minimized reproducers and redact private text/tokens before reporting. Never place actual environment/credentials/customer payloads in docs, verification receipts or a portal.

Training data is not released; public benchmark text can contain personal information. Dataset licences vary, including unknown Yahoo and no listed MS MARCO licence in the data card. Raw benchmark rows/model artifacts stay outside reader content. Typed output does not prove that an adversarial query cannot reveal information via labels/probabilities.

## Failure handling is incomplete by design of this snapshot

The handler does not locally validate complete request/response schemas. Nonnumeric Content-Length and some body/result exceptions escape the 422 block. Default shape filters present fields but does not enforce completeness. Treat an HTTP error/disconnect separately from an incorrect decision. See [HTTP reference](../reference/http.md).

## Jev compatibility is scoped

Three route aliases and default field lists are source-backed. README reports previous Jev response checks, not an independently revalidated external API spec. No credits_remaining_usd field; local cost_usd forced0; extras-on changes fields. Client helper returns only answers. Live smoke script lacks token handling and expects extras-off.

## Runtime/platform compatibility is unverified

Dependency minima are broad; no lock or current support matrix. Adapter accesses model encoder/device/dtype internals. CPU path converts encoder to bf16 while health always says bfloat16; actual loaded artifact/dtype was not queried. Only exact cuda preference selects CUDA; other accelerator strings leave CPU. Saved RTX3070Ti timings do not prove performance on another platform or current dependencies.

Do not resolve these unknowns by installing/upgrading/repairing hardware in a documentation task. Follow [requirements](../getting-started/requirements.md), [deployment review](../how-to/review-deployment.md) and owner [status](../status.md).
