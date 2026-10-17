---
title: Dex typed decisions
description: Choose a safe first result, client workflow, or maintainer task for Dex.
kind: overview
source_ref:
- CONTEXT.md#L3-L44
- README.md#L5-L31
- BENCHMARKS.md#L106-L154
- RELEASE_NOTES.md#L1-L9
---

# Dex

Dex is a local typed-decision model release with a small HTTP adapter. A caller sends text and named questions. The runtime returns choices, ordered scores or yes/no probabilities rather than generated prose.

**Start with an offline example.** It demonstrates real answer filtering without loading weights, using a GPU or contacting a server. Output shape is not evidence that a decision is correct.

## Choose your task

| You want to… | Start here |
|---|---|
| Understand purpose, decisions and contribution boundaries | [Project and collaboration overview](collaboration.md) |
| Get a first safe observable result | [Offline decision tutorial](tutorials/read-a-decision-offline.md) |
| Know what must exist before a launch | [Requirements and environment](getting-started/requirements.md) |
| Call an already authorized endpoint | [Calls and error handling](how-to/call-and-handle-errors.md) |
| Change the adapter or evaluation tools | [Repository map](developer-guide/repository.md) and [change the adapter](developer-guide/change-the-adapter.md) |
| Look up an exact route, environment variable or script argument | [HTTP reference](reference/http.md), [commands](reference/commands.md), [configuration](reference/configuration.md) |
| Judge a use case against measured limits | [Capabilities and limits](capabilities-and-limits.md) and [evidence method](reference/evidence-schemas-and-scoring.md) |
| Find current assessment and missing checks | [Status](status.md) |

## What is supported by this source snapshot

The adapter implements three POST route aliases, optional bearer protection on POST, a health GET, one model call at a time and default Jev answer-field filtering. Synthetic Python/curl clients and a live-only smoke script exist. Saved-evidence reporting and two GPU measurement scripts are separate tools.

The October 8–9 benchmark report is historical evidence, not a fresh installation or uptime check. The model-identity wording in short instructions conflicts with the cards; [provenance](provenance-and-licences.md) preserves that uncertainty. No running model, deployment or official Jev compatibility was verified for this documentation.

## Before any runtime action

Loading weights, starting a listener, sending inference requests, installing dependencies and running GPU measurements need a separate authorized task. Source defaults to loopback with no token; the container instead binds all interfaces. Do not expose the service by changing a host value alone. See [security](concepts/security-and-compatibility.md).
