---
title: "Workflow guide"
description: "Choose an existing workflow and keep offline reading separate from live runtime work."
kind: "overview"
source_ref: ["README.md#L7-L31", "README.md#L84-L87", "CONTEXT.md", "examples/client.py#L5-L20", "tests/test_server.py#L1-L45"]
---

# Workflow guide

This previous handbook entry now routes to complete task pages. It does not combine install, API reference, architecture and runtime acceptance into one generic page.

## Learn safely

Start with [requirements](getting-started/requirements.md), then run [offline answer filtering](tutorials/read-a-decision-offline.md) and [synthetic scoring](tutorials/trace-saved-evidence.md). Neither needs a server, weights, private text or GPU.

## Use an authorized endpoint

Review [launch prerequisites](how-to/existing-environment-launch.md) only after runtime approval. For an already approved target, use [calls/error handling](how-to/call-and-handle-errors.md), [live smoke scope](how-to/check-an-authorized-server.md) and exact [HTTP/types reference](reference/http.md).

## Maintain code and evidence

Read [architecture](architecture.md), [repository map](developer-guide/repository.md), [adapter change impact](developer-guide/change-the-adapter.md) and [evaluation maintenance](developer-guide/maintain-evaluation.md). Report regeneration writes files; speed/order reruns load models. Neither belongs to an ordinary docs link check.

## Judge claims and status

Use [capabilities/limits](capabilities-and-limits.md), [provenance/licences](provenance-and-licences.md), [collaboration](collaboration.md) and [status](status.md). Historical benchmark percentages and source fingerprints are not current uptime, identity or product acceptance.
