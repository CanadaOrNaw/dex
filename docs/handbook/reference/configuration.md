---
title: Configuration and dependencies
description: Environment defaults, read timing, server constants and dependency compatibility
  limits.
kind: reference
source_ref:
- server/dex_server.py#L29-L57
- server/dex_server.py#L69-L108
- requirements.txt#L1-L6
- Dockerfile#L1-L10
- deploy/dex.service#L1-L16
- model/rl_agent_config.json#L1-L33
- .gitignore#L1-L25
---

# Configuration and dependencies

## Environment and read timing

| Name | Default | Read when | Effect / important limit |
|---|---|---|---|
| `DEX_MODEL` | Repository `model` resolved from server file | Module import | Local directory passed to `Agent`; no adapter download step |
| `DEX_TOKEN` | Empty/unset | Module import | Exact optional POST bearer only; health unaffected |
| `DEX_EXTRAS` | Off; only exact string `1` enables | Module import | Raw runtime answer fields instead of whitelist |
| `DEX_DEVICE` | `cuda` | `load()` | Only exact `cuda` plus available CUDA moves model/sets device+dtype; any other value leaves CPU |
| `DEX_HOST` | `127.0.0.1` | Main listener construction | Bind address, no TLS added |
| `HF_HUB_OFFLINE` | Not set by adapter | External dependency behavior | Supplied container/unit set `1`; upstream offline behavior not independently verified |

There is no authored `.env` loader, config-file precedence stack or flag/environment merging for these values. The port is separate first positional argv, default 18766. Captured import-time settings do not refresh because the shell environment changes later.

## Source constants

| Constant | Value | Meaning |
|---|---|---|
| `NAME` | `dex-1b` | Response/health label, not weight attestation |
| `MAX_BODY` | 1,000,000 | Content-Length byte maximum; positive length required |
| `POST_PATHS` | Three aliases in [HTTP](http.md) | Exact literal path membership |
| `LOCK` | One global `threading.Lock` | Serialized runtime scoring |

## Runtime dependency boundary

Requirements are Laya >=0.3.11, Torch >=2.4, Transformers >=5.0, unpinned safetensors/numpy. No lockfile or verified installed support matrix exists. Comments report tested versions but are not a fresh environment receipt.

`load()` uses `agent.model.encoder.to(torch.bfloat16)` and may assign `agent.device`/`agent.dtype`. These private object relationships can change with dependency upgrades. Source converts the encoder only before optional GPU move; health's fixed dtype string is not an independent statement about every model tensor on CPU.

No detailed Laya validation/extras API is redefined here. Local `rl_agent_config.json` is loaded indirectly by Agent; its fields are observed metadata, not an adapter-supported CLI/config tuning interface. See [artifact/deployment metadata](model-and-deployment-metadata.md).


## Git tracking boundary for documentation

Root `.gitignore` keeps model/environment/bytecode state ignored. Its documentation rules recursively ignore `_generated`, `.generated`, build, node_modules and `.fixture` directories beneath `docs`. Within the handbook, `.env*`, `*.env`, `credentials*`, `*.log` and `*.db` forms are ignored at every depth; root `.docs-check` is also ignored. These controls affect ordinary Git discovery, not arbitrary file access. Handbook assets are currently ignored; no asset has been approved for this handbook.

Inside `docs/verification`, only `manifest.json`, `review.json` and the two exact named safe Python fixture files are allowed by these rules. Other private verification output, including author-checks.txt, remains ignored. Do not treat an untracked private file's presence on disk as a submission or released reader input.

These are source-control discovery rules, not a security barrier or documentation acceptance. The private verification JSON is review input, never public site content. Ignore rules do not remove already tracked files, cannot prevent explicit force-add, and do not replace source/review/site input validation. The parent-owned rule change performed no staging or untracking; acceptance still requires independent review of exact source, prose, navigation and examples.

## Deployment overrides and privacy

Container sets `/dex/model`, CPU, bind-all and offline1; user unit sets model under `%h/dex/model` and offline1, inherits source defaults otherwise. Neither supplies a token/TLS policy. Never print actual environment values or credential-bearing requests to establish a docs receipt.

See [requirements](../getting-started/requirements.md), [deployment review](../how-to/review-deployment.md) and [security](../concepts/security-and-compatibility.md).
