---
title: "Review an existing-environment launch"
description: "Prepare the real launch command without treating documentation as runtime authorization."
kind: "how-to"
source_ref: ["server/dex_server.py#L33-L57", "server/dex_server.py#L104-L108", "README.md#L7-L31", "CONTEXT.md", "requirements.txt#L1-L6"]
---

# Review an existing-environment launch

**This page is a launch review, not permission to start a model.** The command below is unrun for this documentation. Use the [offline tutorial](../tutorials/read-a-decision-offline.md) if you only need to learn the interface.

## Prerequisites

Obtain separate runtime approval; read [requirements](../getting-started/requirements.md). Confirm an existing environment and selected artifact provenance privately. Decide loopback/auth/input privacy first. No install, model download or environment repair is implicit.

## Review the actual startup command

The source accepts `python server/dex_server.py [PORT]`; with the existing project interpreter the loopback/default-port form is:

```bash
.venv/bin/python server/dex_server.py 18766
```

It imports Torch/Laya, loads the selected model, converts encoder dtype, may use CUDA, performs a warm-up and then opens a listener until stopped. It is not a safe `--help` or syntax check.

Review current environment privately before an approved launch: `DEX_MODEL` defaults to repository `model`; `DEX_DEVICE` defaults to exact `cuda`, otherwise CPU is retained; `DEX_HOST` defaults loopback; token unset means no POST auth; extras unset means default answer filtering. See [configuration](../reference/configuration.md) for read timing and deployment overrides. Never put the token value in a command history, docs or receipt.

## Observable result and failure handling

A completed startup permits HTTP requests; source supplies no readiness banner. A known authorized health request reports `ok`, model label, device and fixed dtype string, not artifact history or quality. Do not probe a listener unless the runtime task explicitly allows it.

Invalid port parsing, missing/import-incompatible model/runtime, warm-up errors or bind failure can terminate with an uncaught exception. Preserve a minimal redacted error. Do not install dependencies, rename weights, change dtype or restart an owner-managed instance just to complete a docs example.

## Next action and cleanup boundary

Use [authorized server checks](check-an-authorized-server.md) only after the owner confirms the target. Stopping/restarting a process follows that runtime task's explicit ownership; this guide does not stop a shared service. For deployment templates, read [deployment review](review-deployment.md).
