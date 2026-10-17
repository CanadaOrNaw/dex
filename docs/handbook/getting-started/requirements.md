---
title: "Requirements and environment"
description: "Know which setup inputs exist, what is unverified and why installation is not the first safe check."
kind: "how-to"
source_ref: ["requirements.txt#L1-L6", "Dockerfile#L1-L10", "README.md#L7-L31", "deploy/dex.service#L1-L16", ".gitignore#L1-L4", "CONTEXT.md"]
---

# Requirements and environment

## Safe first result

A checkout with its **existing** `.venv/bin/python` can run the documentation-only [offline tutorial](../tutorials/read-a-decision-offline.md). It uses the standard library and reads only reviewed source functions. It does not need weights, PyTorch imports, a server or a GPU.

If the interpreter is absent or broken, stop and ask the maintainer. These pages do not authorize creating or repairing an environment.

## Runtime dependencies recorded in source

| Package | Constraint in `requirements.txt` |
|---|---|
| `laya` | `>=0.3.11` |
| `torch` | `>=2.4` |
| `transformers` | `>=5.0` |
| `safetensors` | Unpinned |
| `numpy` | Unpinned |

The comment reports testing with Laya 0.3.11/0.4.1, torch 2.14 and Transformers 5.17/5.19. This task did not verify those combinations or installed versions. There is no lockfile or host Python support matrix. The CPU Docker image selects Python 3.12, not a general support guarantee.

## What a separately approved setup needs

- An explicitly selected, provenance-reviewed local model directory. `model/` is ignored by Git. Metadata/weights/tokenizer files must be supplied separately; their presence is not checked by a docs build.
- A dependency environment compatible with the runtime's private attributes used by `load()`: `agent.model.encoder`, `agent.device` and `agent.dtype`.
- CPU or a CUDA setup approved for the target. The adapter falls back to CPU only when its exact CUDA preference cannot be used; it does not validate arbitrary accelerator names.
- A listener/authentication/privacy decision. Start with loopback; remote exposure needs more than a host flag.

`README.md`, install section, records cloning the code, creating a venv, installing requirements and downloading `CanadaOrNaw/dex-1b` with `huggingface-cli`. Those network/install actions were **not run** for this handbook. The requirements do not explicitly pin or prove that CLI command's availability. Do not substitute a remembered modern command without checking the approved environment.

## Deployment-specific prerequisites

Docker copies an already present `model/` into the image, binds all interfaces and defaults to CPU/offline mode. The user systemd template expects code, venv and model under `~/dex`; it is not a path-discovery mechanism or proof of an installed unit. See [deployment review](../how-to/review-deployment.md).

## Recovery and next step

Missing model, import failure or an unsupported runtime version is not repaired by refreshing a documentation hash. Preserve the error without tokens/private text and take it to the owning maintainer. Continue with [offline shape](../tutorials/read-a-decision-offline.md) for a safe result, or [authorized launch](../how-to/existing-environment-launch.md) only after separate runtime approval.
