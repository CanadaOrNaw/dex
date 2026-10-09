# Dex 1.0.0 (2026-10-09)

First release.

- Model `dex-1b`: Ettin-1B encoder (784M of 1.1B parameters fine-tuned) with a typed decision head, trained against strictly proper scoring rules. Apache 2.0.
- Jev-compatible HTTP server (`server/dex_server.py`): `POST /v1/systemone`, `/api/v1/decide`, `/v1/decide`, `GET /health`; answer fields identical to Jev's; optional bearer token; systemd unit and Dockerfile in `deploy/` and the repo root.
- Benchmark report with data, answers and scripts (`BENCHMARKS.md`, `benchmarks/`) and data card (`DATA_CARD.md`).
- Headline: 71.4% against the human label across 5,327 questions (JEV 81.8%, stock Laya 64.0%); 81.5% on the ten everyday use cases (JEV 84.6%, stock Laya 68.2%).
- Known limits: knowledge-heavy tasks, jailbreak screening and moderation/spam (stock Laya is better), code correctness, many questions on long texts (slower than Laya), English only. See the limits section of the README.
