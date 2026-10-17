---
title: Question and answer shapes
description: Observed typed-question inputs, default retained answers and delegated
  scoring semantics.
kind: reference
source_ref:
- examples/curl.sh#L3-L10
- examples/client.py#L8-L20
- server/dex_server.py#L42-L45
- server/dex_server.py#L90-L98
- tests/test_server.py#L9-L35
- benchmarks/report.py#L31-L47
---

# Question and answer shapes

The request is `{state, questions}`. Questions is an object keyed by caller-chosen qid. Examples use text state/instructions and three types. These are observed source/example contracts, not a complete upstream schema specification. The adapter delegates detailed validation to Laya.

## Choice

```json
{"type": "choice", "instructions": "What is requested?", "criteria": {"refund": "money returned", "information": "general information"}}
```

Default retained answer keys: `type`, `choice`, `confidence`, `probabilities`. Choice is a stable offered key in the smoke case; probabilities is keyed by choices. The smoke checks sum within 0.01 of one and choice membership. More general constraints are not locally validated.

## Score

```json
{"type": "score", "instructions": "How urgent?", "criteria": ["low", "medium", "high"]}
```

Default retained keys: `type`, `score`, `confidence`, `legend`, `probabilities`. The runtime owns numeric score and legend meaning. The report evaluates **argmax probability key converted to int**, not the returned score. Avoid inventing a continuous-score formula or calibration guarantee.

## Noul (yes/no)

```json
{"type": "noul", "instructions": "Is money requested back?"}
```

Default retained keys: `type`, `noul`. The smoke checks noul lies between 0 and 1. Report prediction uses probability >=0.5; report confidence is max(p,1-p). No criteria are used in the supplied example.

## What filtering does and does not do

`jev_shape(answers)` builds each qid's mapping from fields present in the runtime answer's type-specific whitelist. Missing fields are not filled; unknown type lookup can fail. `DEX_EXTRAS=1` returns runtime answers instead and may include fields intentionally removed by the default shape. Exact extras inventory is not guaranteed here because external runtime code/version was not audited.

Run [the synthetic filter tutorial](../tutorials/read-a-decision-offline.md) to observe this boundary safely. The response envelope, errors and token/body distinction are in [HTTP](http.md); model/training limits are in [capabilities](../capabilities-and-limits.md).
