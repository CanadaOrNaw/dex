# dex

Workspace contract and model-identity caveat: [CONTEXT.md](CONTEXT.md).

Dex-1B: typed-decision release with an Ettin-1B encoder and the Laya runtime, as specified in `MODEL_CARD.md` and `model/encoder/config.json`; served by the HTTP adapter. This source identity does not certify a loaded service or model capability.
Public model repo (GitHub + HuggingFace `CanadaOrNaw/dex-1b`).

- Model + cards: `model/`, `MODEL_CARD.md`, `DATA_CARD.md`, `BENCHMARKS.md`
- Server: `server/`, `deploy/`, `Dockerfile`
- Benchmarks + evals: `benchmarks/`, `tests/`, `examples/`
- Results: `README.md`, `RELEASE_NOTES.md`

Read [handbook](docs/handbook/index.md) and its status before work. Before handoff, follow the [living-docs contract](file:///home/zack/Projects/fleet-index/_system/documentation/POLICY.md): review evidence, refresh canonical pages/status, rebuild views and pass working/staged checks.
