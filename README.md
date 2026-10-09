# Dex

**Dex**: an open-source, Jev-compatible, non-autoregressive System 1 decision model. Typed choice, score and yes/no decisions over any text in a single forward pass. It never generates text, so there is nothing to parse and nothing to hallucinate. Ettin-1B bidirectional encoder (1.1B parameters, 784M fine-tuned) with a decision head trained from scratch, trained against strictly proper scoring rules. Same `POST /v1/systemone` request and response shape as TypeSafe Jev. Apache 2.0.

Dex answers the same typed questions the Jev API answers, locally and for free: you send a `state` and a set of `questions` (choice, score, yes/no) and get typed answers with probabilities, in one forward pass. Point an existing Jev client at `http://127.0.0.1:18766/v1/systemone` and drop the key.

## Install and run

```bash
git clone https://github.com/CanadaOrNaw/dex && cd dex
python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
huggingface-cli download CanadaOrNaw/dex-1b --local-dir model          # 2.4 GB of weights
python server/dex_server.py 18766                                  # serves the Jev API shape on 127.0.0.1:18766
```
```bash
sh examples/curl.sh            # one call with a choice, a score and a yes/no question
python tests/test_server.py    # 12 checks against the running server
```
From Python without the server:
```python
import torch
from laya.agent import Agent
agent = Agent("model", device="cpu")            # load on the CPU, keep the encoder in bfloat16, then move: a full-precision copy never touches an 8 GB card
agent.model.encoder.to(torch.bfloat16)
agent.model.to("cuda"); agent.device = torch.device("cuda"); agent.dtype = torch.bfloat16
print(agent.system_one("Hi, I was charged twice. Please refund the duplicate.",
      {"refund": {"type": "noul", "instructions": "Is the customer asking for money back?"}})["answers"])
```

Drop-in for Jev clients: the request body is `{"state": ..., "questions": {...}}`, the response is `{"model": "dex-1b", "answers": {...}, "usage": {"input_tokens": n, "cost_usd": 0}}`. The answer fields are exactly Jev's for each question type (`choice`: type, choice, confidence, probabilities; `score`: type, score, confidence, legend, probabilities; `noul`: type, noul), checked against real Jev responses. `/api/v1/decide` and `/v1/decide` are accepted too. Differences: no `credits_remaining_usd`, no key (set `DEX_TOKEN` to require a bearer token), one request is run at a time.
Run it as a service with `deploy/dex.service` (systemd) or the `Dockerfile` (CPU image).

## How well does it work?

Everything below is scored against the original human labels, not against JEV (agreeing with JEV is not the same as being right). Same prompts to every system, on one RTX 3070 Ti (8 GB).

| accuracy against the human label | questions | JEV | **Dex** | Stock Laya |
|---|---|---|---|---|
| A. Ten most-cited JEV use cases | 1,244 | 84.6% | **81.5%** | 68.2% |
| B. Tasks never trained on | 1,737 | 84.5% | **74.4%** | 63.0% |
| C. Exam: 8 datasets never used | 2,346 | 78.2% | **63.8%** | 62.5% |
| **All three** | 5,327 | **81.8%** | **71.4%** | **64.0%** |

Dex closes about 40% of the gap between stock Laya and JEV overall, and 81% of it on the ten everyday use cases (sorting, screening, triage, routing, intent and skill selection). On tasks it was never trained on it is 11 points ahead of stock Laya and 10 behind JEV. Full report, per-dataset tables, charts, calibration, speed and answer-order results: [BENCHMARKS.md](BENCHMARKS.md).

![ten use cases](benchmarks/charts/usecases.svg)

| | Dex | Stock Laya | JEV API |
|---|---|---|---|
| 1 question, short text | 18 ms | 19 ms | 886 ms |
| 15 questions, short text | 95 ms | 47 ms | 780 ms |
| 15 questions, ~900-token text | 878 ms | 260 ms | - |
| GPU memory (bfloat16 / fp32) | 2.4 GB | 1.7 GB | - |
| picks a different option when the answer order is reversed | 7.0% | 25.2% | 3.0% |

## What Dex is, and how it was made

- **Architecture.** The [Laya](https://github.com/NandhaKishorM/laya) design: a bidirectional encoder reads the state and the questions together and a small typed head scores every option, so all questions are answered in one pass and the output can only be a valid option, level or probability. Laya's body is ModernBERT-large (395M). Dex swaps it for the 1.1B [Ettin](https://huggingface.co/jhu-clsp/ettin-encoder-1b) encoder; the decision head is trained from scratch. 784M of the 1.1B parameters are fine-tuned (embeddings and the lowest 7 of 28 layers are frozen).
- **Training.** Trained against strictly proper scoring rules (cross-entropy on the chosen option plus KL divergence to the target probabilities), 3 epochs in bfloat16, with the option order shuffled on 30% of choice questions.
- **Data.** Public text and instruction-task collections, with a wide variety of task wording (about 1,080 distinct instructions; see [DATA_CARD.md](DATA_CARD.md)).
- **What helped.** Research on instruction tuning says generalisation to unseen tasks follows the number of distinct instructions, not rows. Our first model saw 285 distinct wordings; widening to about 1,080 gave +4 points on never-trained tasks (65.2% to 69.2%), and swapping the 0.4B body for the 1.1B Ettin gave another +5 (69.2% to 74.4%). Both are in the ablation table in [BENCHMARKS.md](BENCHMARKS.md).

## Honest limits

- **No knowledge it was never given.** On medical multiple choice (MedMCQA) Dex scores 30.7% against JEV's 78.7%; on reading an abstract (PubMedQA) 55.0% against 78.3%. More training did not change this: the gap is knowledge, not format.
- **Stock Laya is better at some screening tasks.** Jailbreak screening: stock Laya 98.7%, Dex 89.3%. Moderation and spam: stock Laya 89.9%, Dex 83.0%.
- **It cannot judge whether code is correct** (52.5%, a coin flip; JEV 90.8%), and it is behind on answer verification (90.0% against JEV's 96.9%).
- **Not a drop-in replacement for JEV in every workflow.** In our own multi-step automation checks it was well behind JEV; use it where the benchmark above shows it is close.
- **Slower than Laya for many questions or long texts**, still far faster than the Jev API: 15 questions on a short text take 95 ms (Laya 47 ms); on a ~900-token text 878 ms (Laya 260 ms); the Jev API takes 780 to 890 ms whatever the size. It needs 2.4 GB of GPU memory in bfloat16.
- **English only**, trained with inputs up to 1,792 tokens and up to 30 options per choice question.
- **Single training run.** We did not measure run-to-run variation.
- **Our benchmarks.** We built them, scored every system on the same prompts, and report intervals, but benchmark A shares datasets with the training data (different rows) and its routing suite uses a proxy answer key. B and C do not.
- **Probabilities are temperature-fitted, not guaranteed calibrated.** Calibration error 0.058 across our tests (JEV 0.052, stock Laya 0.092); when Dex is 90%+ sure it is right 93.2% of the time, but it is that sure on only 29% of questions (JEV 63%).

## Where JEV leads, and where stock Laya wins

JEV leads everywhere except CVE severity (a task where JEV is worst of the three): by 3 points on everyday use cases, 10 on new tasks, 14 on the exam datasets, and by a wide margin on knowledge tasks. Stock Laya beats Dex on jailbreak screening (98.7% vs 89.3%) and on moderation and spam (89.9% vs 83.0%), and it is faster and smaller. Dex wins on command gating (93.3% vs 47.5%), bulk classification (83.4% vs 58.6%), intent and skill selection (82.0% vs 53.0%), routing, and tasks it hasn't seen.

## Reproduce

- `python benchmarks/report.py` rebuilds every table and chart from the saved prompts, human labels, Dex's and stock Laya's answers, and JEV's results as summary numbers (`benchmarks/results/jev_summary.json`). No model is run.
- `python benchmarks/speed.py --stock <stock-laya-dir>` and `python benchmarks/order.py --stock <stock-laya-dir>` re-measure speed and answer-order on your own GPU and write `*-rerun.json` next to the published results.

## Licence and credits

Apache 2.0 for the code and the weights (see [LICENSE](LICENSE) and [NOTICE](NOTICE)). Built on the [Laya](https://github.com/NandhaKishorM/laya) runtime (Apache-2.0, Convai Innovations) and the [Ettin](https://huggingface.co/jhu-clsp/ettin-encoder-1b) encoder (MIT, Johns Hopkins University CLSP; Weller et al., 2025). Data and benchmark credits: [DATA_CARD.md](DATA_CARD.md). Not affiliated with TypeSafe AI or Convai Innovations.
