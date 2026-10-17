---
title: Review deployment definitions
description: Compare container and user-unit defaults without installing, activating
  or exposing a service.
kind: how-to
source_ref:
- Dockerfile#L1-L10
- deploy/dex.service#L1-L16
- deploy/CONTEXT.md#L14-L26
- server/dex_server.py#L69-L108
- CONTEXT.md#L39-L44
---

# Review deployment definitions

A Dockerfile or unit file is an **installation input**, not evidence that anything is installed or running. This guide does not build images, copy units, reload systemd, activate/restart services or expose a port.

## Compare defaults

| Decision | Direct server | CPU container | User systemd template |
|---|---|---|---|
| Code/environment | Selected existing environment | Python 3.12-slim + unpinned requirement resolution at build | `%h/dex/.venv/bin/python` |
| Model | Repository model unless DEX_MODEL | Copied `/dex/model` | `%h/dex/model` |
| Device | CUDA preferred, fallback CPU | CPU | Direct-source default unless privately overridden |
| Bind | `127.0.0.1` | `0.0.0.0` | Direct-source default |
| Port | First argument, default 18766 | 18766 CMD/EXPOSE | 18766 ExecStart |
| Offline setting | Not set by adapter | `HF_HUB_OFFLINE=1` | `HF_HUB_OFFLINE=1` |
| Token/TLS | Optional POST bearer, no TLS | No supplied token/TLS | No supplied token/TLS |

The user template assumes `~/dex` for code, venv and model, not arbitrary checkout discovery. Its comment describes daemon-reload/enable-now; those are activation instructions, not docs verification commands. It restarts on failure after five seconds.

## Before an approved deployment

- Resolve target paths and model identity explicitly; do not move/rename artifacts to fit a template.
- Confirm dependency/runtime/device support on the target, not from saved benchmark hardware.
- Decide private-input policy and authentication/TLS/network controls. Container bind-all is not safe remote policy.
- Account for image copying of model bytes and no automated download. `EXPOSE` is metadata, not a privacy control.
- Define separate acceptance and rollback under the runtime task. This handbook supplies neither installed-state nor rollback success proof.

See [configuration](../reference/configuration.md), [security](../concepts/security-and-compatibility.md) and [authorized launch](existing-environment-launch.md). No current service/GPU query is needed to read these definitions.
