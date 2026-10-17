---
title: Model and deployment metadata
description: Observed local model fields and deployment definitions without weight
  or live-state attestation.
kind: reference
source_ref:
- model/rl_agent_config.json#L1-L33
- model/encoder/config.json#L1-L85
- model/tokenizer/tokenizer_config.json#L1-L15
- model/SHA256SUMS#L1-L1
- Dockerfile#L1-L10
- deploy/dex.service#L1-L16
- .gitignore#L1-L4
---

# Model and deployment metadata

These values were read from small local metadata files. `model/` is ignored by Git; weight bytes and tokenizer vocabulary were not read, hashed or executed. Metadata and a checksum file do **not** prove the current artifact matches release claims.

## Local typed-runtime config

| Field | Observed value |
|---|---|
| `encoder`, `base_encoder` | `jhu-clsp/ettin-encoder-1b` |
| `model_name` | `dex-1b` |
| `description` | Ettin-1B typed decision model description |
| `head_layers` | 2 |
| `max_len`, `head_max_len`, `max_prefixes` | 1792, 1024, 6 |
| `act_costs.escalate`, `cost_wrong_act` | 0.5, 3.0 |
| `amp_dtype` | `bf16` |
| `temperature` | `[1.15, 1.2514300346374512, 1.983399510383606]` |
| `temperature_by_options` | Empty object |

Training metadata records CE+KL method/head from scratch; epochs3, batch64, encoder_lr0.00004, head_lr0.0002, option shuffle0.3, seed8, frozen embeddings/lowest7of28layers, selected_epoch3 and temperature fit on validation choice split. This is metadata, not an executable trainer or reproduced run. The adapter does not directly validate/expose these fields as public tuning options.

## Encoder and tokenizer fields

The encoder config describes `ModernBertForMaskedLM`, `model_type=modernbert`, hidden1792/intermediate3840, 28heads/28layers, 28 full/sliding layer entries, global attention every3layers, local attention128, max positions7999, vocab50368, Transformers5.17.0 and dtype float32. Token IDs are BOS/CLS50281, EOS/SEP50282, PAD50283.

Other encoder fields are attention bias false/dropout0; causal flags false; classifier gelu/biasfalse/dropout0/poolingmean; decoder biastrue; deterministic flash attentionfalse; embedding/MLP dropout0, MLP biasfalse; gradient checkpointingfalse; hidden activationgelu; initializer cutoff2/range0.02; layer/norm epsilon0.00001, norm biasfalse; position type sans_pos; full/sliding rope default theta160000; sparse ignore -100/predictionfalse; tied word embeddingstrue.

Tokenizer config records clean-up true, `[CLS]`, `[SEP]`, `[PAD]`, `[MASK]`, `[UNK]`, input names input_ids/attention_mask, `model_max_length=8192`, `PreTrainedTokenizerFast` and `local_files_only=false`. These are not supported Dex input-length promises; runtime max_len1792 is a distinct boundary. Model-name vocabulary does not resolve weight provenance.

`model/SHA256SUMS` records a checksum for model.safetensors. No comparison was performed. Do not turn the recorded checksum into a verified claim by copying it into status.

## Container definition

`Dockerfile` starts Python3.12-slim, works in `/dex`, installs `requirements.txt`, copies server and model, sets DEX_MODEL `/dex/model`, host0.0.0.0, devicecpu and offline1, exposes18766 and runs Python server with18766. CPU compatibility is the definition's intent, not a fresh run. No GPU image recipe or build/run wrapper is authored.

## User-unit definition

Unit description names loopback18766, After=network.target; Type=simple; offline1 and model `%h/dex/model`; ExecStart uses `%h/dex/.venv/bin/python` and `%h/dex/server/dex_server.py 18766`; Restart=on-failure; RestartSec=5; WantedBy=default.target. No WorkingDirectory, token/TLS or hardening settings are supplied. The comment's copy/reload/enable-now instructions are activation, not verification.

See [provenance](../provenance-and-licences.md), [configuration](configuration.md) and [deployment review](../how-to/review-deployment.md).
