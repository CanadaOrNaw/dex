# dex: workspace contract

One job: maintain the typed-decision model release, HTTP adapter and reproducible
benchmark evidence. This contract does not certify a loaded model or running service.

## Entry routes

- [AGENTS.md](AGENTS.md): agent route; [README.md](README.md): existing use/API guide.
- [MODEL_CARD.md](MODEL_CARD.md), [DATA_CARD.md](DATA_CARD.md),
  [BENCHMARKS.md](BENCHMARKS.md), [RELEASE_NOTES.md](RELEASE_NOTES.md): release claims
  and their stated limits. Saved benchmark results are historical evidence.
- [server/CONTEXT.md](server/CONTEXT.md): HTTP code; [deploy/CONTEXT.md](deploy/CONTEXT.md):
  deployment definitions; [examples/CONTEXT.md](examples/CONTEXT.md): client examples.
- [benchmarks/CONTEXT.md](benchmarks/CONTEXT.md): saved evidence/report and rerun boundary;
  [tests/CONTEXT.md](tests/CONTEXT.md): running-server checks.

## Inputs

Working: the requested adapter, release or evidence change. Reference: the cards,
[server/dex_server.py](server/dex_server.py), [requirements.txt](requirements.txt),
[Dockerfile](Dockerfile) and selected files in [model/](model/). Model weights and
benchmark row payloads stay in place; do not copy them into a docs portal.

## Process

Read `MODEL_CARD.md` and the selected artifact config before repeating a capability
claim. The canonical source identity is the Ettin-1B encoder with the Laya runtime;
AGENTS routes to that card rather than maintaining an incompatible model lineage.
A saved config/card does not verify a loaded artifact, fresh benchmark or running
service. Do not change weights or behavior as a contract repair.

## Outputs

The server source, deployment definitions, examples, cards, and benchmark tables/charts
at the existing paths. `benchmarks/report.py` reads saved evidence; speed/order reruns
are separate GPU work. No service activation, model execution or rerun occurred here.

## Human check

Zack approves runtime/deployment, costly evaluation and publication changes. Distinguish
local checks, saved benchmark runs and real deployment proof; a typed output does not
prove correctness or that hallucinations/knowledge failures are impossible. Check
credentials privately if a runtime task needs them; never put their values in docs.
