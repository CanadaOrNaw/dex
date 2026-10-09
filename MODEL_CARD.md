---
license: apache-2.0
base_model: jhu-clsp/ettin-encoder-1b
library_name: laya
pipeline_tag: text-classification
language: en
tags:
  - system-1
  - decision-model
  - typed-decisions
  - non-autoregressive
  - jev-compatible
  - classification
---

# Dex

**Dex**: an open-source, Jev-compatible, non-autoregressive System 1 decision model. Typed choice, score and yes/no decisions over any text in a single forward pass. It never generates text, so there is nothing to parse and nothing to hallucinate. Ettin-1B bidirectional encoder (1.1B parameters, 784M fine-tuned) with a decision head trained from scratch, trained against strictly proper scoring rules. Same `POST /v1/systemone` request and response shape as TypeSafe Jev. Apache 2.0.

## Use

```bash
pip install laya torch transformers
huggingface-cli download CanadaOrNaw/dex-1b --local-dir dex-1b
```
```python
import torch
from laya.agent import Agent
agent = Agent("dex-1b", device="cpu")
agent.model.encoder.to(torch.bfloat16)
agent.model.to("cuda"); agent.device = torch.device("cuda"); agent.dtype = torch.bfloat16
agent.system_one("Hi, I was charged twice. Please refund the duplicate.",
    {"refund": {"type": "noul", "instructions": "Is the customer asking for money back?"}})["answers"]
```
A ready HTTP server with the Jev request/response shape (`POST /v1/systemone`), a systemd unit, a Dockerfile and tests are in the GitHub repository: https://github.com/CanadaOrNaw/dex

## Training

Trained against strictly proper scoring rules (cross-entropy on the chosen option plus KL divergence to the target probabilities). Ettin-1B encoder, 784M of 1.1B parameters fine-tuned (embeddings and the lowest 7 of 28 layers frozen), decision head trained from scratch; 3 epochs, bfloat16, batch 64, encoder learning rate 4e-5, head 2e-4, 30% option-order shuffling. Public text and instruction-task collections with about 1,080 distinct task instructions; see [DATA_CARD.md](DATA_CARD.md).

## Results (accuracy against the human label)

| accuracy against the human label | questions | JEV | **Dex** | Stock Laya |
|---|---|---|---|---|
| A. Ten most-cited JEV use cases | 1,244 | 84.6% | **81.5%** | 68.2% |
| B. Tasks never trained on | 1,737 | 84.5% | **74.4%** | 63.0% |
| C. Exam: 8 datasets never used | 2,346 | 78.2% | **63.8%** | 62.5% |
| **All three** | 5,327 | **81.8%** | **71.4%** | **64.0%** |

Speed on an RTX 3070 Ti: 18 ms for one question on a short text, 95 ms for fifteen; 2.4 GB GPU memory in bfloat16. Picks a different option when the answer order is reversed 7.0% of the time (stock Laya 25.2%, JEV 3.0%). Per-dataset tables, calibration, ablations and failure analysis: [BENCHMARKS.md](https://github.com/CanadaOrNaw/dex/blob/main/BENCHMARKS.md) in the GitHub repository.

## Jev Decision Index (self-run)

Self-run through the edition-0.3 harness on 2026-10-09 (140,620 requests, RTX 3070 Ti): skill **12.99**, raw 32.47 — about 3x stock Laya's 4.43 on the official board, mid-pack of the sub-2B class. Not an official board score (the board mixes in private tests only the maintainer can run); Dex is not on the board until it is evaluated there. Full per-area breakdown: [BENCHMARKS.md](https://github.com/CanadaOrNaw/dex/blob/main/BENCHMARKS.md).

## Limits

- **No knowledge it was never given.** On medical multiple choice (MedMCQA) Dex scores 30.7% against JEV's 78.7%; on reading an abstract (PubMedQA) 55.0% against 78.3%. More training did not change this: the gap is knowledge, not format.
- **Stock Laya is better at some screening tasks.** Jailbreak screening: stock Laya 98.7%, Dex 89.3%. Moderation and spam: stock Laya 89.9%, Dex 83.0%.
- **It cannot judge whether code is correct** (52.5%, a coin flip; JEV 90.8%), and it is behind on answer verification (90.0% against JEV's 96.9%).
- **Not a drop-in replacement for JEV in every workflow.** In our own multi-step automation checks it was well behind JEV; use it where the benchmark above shows it is close.
- **Slower than Laya for many questions or long texts**, still far faster than the Jev API: 15 questions on a short text take 95 ms (Laya 47 ms); on a ~900-token text 878 ms (Laya 260 ms); the Jev API takes 780 to 890 ms whatever the size. It needs 2.4 GB of GPU memory in bfloat16.
- **English only**, trained with inputs up to 1,792 tokens and up to 30 options per choice question.
- **Single training run.** We did not measure run-to-run variation.
- **Our benchmarks.** We built them, scored every system on the same prompts, and report intervals, but benchmark A shares datasets with the training data (different rows) and its routing suite uses a proxy answer key. B and C do not.
- **Probabilities are temperature-fitted, not guaranteed calibrated.** Calibration error 0.058 across our tests (JEV 0.052, stock Laya 0.092); when Dex is 90%+ sure it is right 93.2% of the time, but it is that sure on only 29% of questions (JEV 63%).
- **Decision Index coverage gaps.** About 11% of index requests come back unsupported (long texts past 1,792 tokens; API-Bank entirely unanswered), and the index counts unanswered as wrong. That coverage gap, not accuracy, is the biggest drag on the index score above.

## Licence

Apache 2.0. Built on the Laya runtime (Apache-2.0) and the Ettin-1B encoder (MIT). Data and benchmark credits are in the data card. Not affiliated with TypeSafe AI or Convai Innovations.
