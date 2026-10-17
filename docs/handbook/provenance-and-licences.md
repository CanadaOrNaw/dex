---
title: Provenance and licences
description: Keep model identity, training claims, dataset permissions and dated release
  evidence separate.
kind: reference
source_ref:
- AGENTS.md#L5-L6
- CONTEXT.md#L26-L44
- MODEL_CARD.md#L1-L71
- DATA_CARD.md#L3-L30
- NOTICE#L1-L39
- LICENSE
- CITATION.cff#L1-L17
- RELEASE_NOTES.md#L1-L9
- model/rl_agent_config.json#L1-L33
- model/SHA256SUMS#L1-L1
---

# Provenance and licences

## Unresolved identity wording

Short `AGENTS.md` says fine-tuned Laya-1B. README/card and local runtime metadata describe an Ettin-1B encoder using Laya's head/scoring runtime; the card declares `base_model: jhu-clsp/ettin-encoder-1b`. Root `CONTEXT.md` explicitly preserves this conflict pending artifact verification.

Small local config fields are consistent with the latter narrative, but weight bytes were not read/hashed and the saved checksum was not compared. ModernBERT architecture naming in encoder config is not sufficient to settle provenance. Do not rename weights, change behavior or silently normalize source identity prose during docs work.

## Training claims and absent reproduction pieces

The card/metadata describe a head trained from scratch with CE+KL proper scoring, 3epochs, bf16, batch64, encoder/head learning rates,30%choice-order shuffle, frozen embeddings/lowest7of28layers and about1,080instructions. Those are release metadata/narrative claims, not a reproduced trainer.

Training data is explicitly not released. There is no authored trainer, complete A/B/C/Jev response collector, Index harness or release publisher in this tree. Benchmarks/Index statements remain tied to their dates/methods. See [evidence reference](reference/evidence-schemas-and-scoring.md).

## Code, weights and dependencies

`LICENSE`, `NOTICE`, card and release notes declare Apache2.0 for Dex code/weights; Laya runtime Apache2.0 (Convai Innovations); Ettin encoder MIT (Johns Hopkins University CLSP). NOTICE retains the MIT text and upstream attribution. Dex states no affiliation with TypeSafe AI or Convai Innovations.

This is an explanation of recorded licensing, not independent legal clearance or proof every local artifact has matching provenance. Preserve notices when redistributing under an approved release task. `CITATION.cff` records software version1.0.0/date2026-10-09 and asks citation of Dex/Ettin/Laya.

## Benchmark data is not uniformly relicensed

| Dataset named in data card | Recorded licence |
|---|---|
| CIRCL/vulnerability-scores | CC-BY4.0 |
| Yahoo answers topics | Unknown |
| DBpedia14 | CC-BY-SA3.0 |
| Jailbreak classification | Apache2.0 |
| MS MARCO | None listed |
| MedMCQA | Apache2.0 |
| PubMedQA | MIT |
| Measuring hate speech | CC-BY4.0 |

Super-NaturalInstructions and PromptSource/P3 credits are recorded, while underlying datasets retain their own licences. Benchmark A partly shares datasets with training (different rows); B/C are reported held out. Public text may contain personal data. Keep raw rows in their owner location, not copied into the unified reader site.

## Release status and next decision

`RELEASE_NOTES.md` records Dex1.0.0 on October9, not a new publication approval. Resolve artifact identity through the model/release owner before asserting a new provenance or model version. [Status](status.md) preserves unknown checks; [collaboration](collaboration.md) describes contribution boundaries.
