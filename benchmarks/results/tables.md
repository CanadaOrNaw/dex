## Accuracy against the human label

| test | questions | JEV | Dex | Stock Laya |
|---|---|---|---|---|
| A. Ten use cases | 1244 | 84.6% (83%-87%) | 81.5% (79%-84%) | 68.2% (66%-71%) |
| B. Tasks never trained on | 1737 | 84.5% (83%-86%) | 74.4% (72%-76%) | 63.0% (61%-65%) |
| C. Exam: 8 datasets never used | 2346 | 78.2% (76%-80%) | 63.8% (62%-66%) | 62.5% (61%-64%) |
| **All three** | 5327 | **81.8%** | **71.4%** | **64.0%** |

## A. Ten use cases

| use case | questions | JEV | Dex | Stock Laya |
|---|---|---|---|---|
| 1 routing (proxy gold) | 120 | 88.3% (81%-93%) | 100.0% (97%-100%) | 70.0% (61%-77%) |
| 2 command gating | 120 | 91.7% (85%-95%) | 93.3% (87%-97%) | 47.5% (39%-56%) |
| 3 injection screening | 120 | 86.7% (79%-92%) | 93.3% (87%-97%) | 87.5% (80%-92%) |
| 4 support triage | 100 | 100.0% (96%-100%) | 99.0% (95%-100%) | 99.0% (95%-100%) |
| 5 moderation and spam | 159 | 89.9% (84%-94%) | 83.0% (76%-88%) | 89.9% (84%-94%) |
| 6 bulk classification | 145 | 82.1% (75%-87%) | 83.4% (77%-89%) | 58.6% (50%-66%) |
| 7 verification | 160 | 96.9% (93%-99%) | 90.0% (84%-94%) | 82.5% (76%-88%) |
| 8 work correctness | 120 | 90.8% (84%-95%) | 52.5% (44%-61%) | 47.5% (39%-56%) |
| 9 intent and skill selection | 100 | 82.0% (73%-88%) | 82.0% (73%-88%) | 53.0% (43%-62%) |
| 10 security severity | 100 | 25.0% (18%-34%) | 29.0% (21%-39%) | 34.0% (25%-44%) |

## C. Exam datasets, one by one (accuracy against the human label)

| dataset | questions | JEV | Dex | Stock Laya |
|---|---|---|---|---|
| cve | 177 | 28.8% (23%-36%) | 34.5% (28%-42%) | 40.7% (34%-48%) |
| dbpedia | 300 | 98.0% (96%-99%) | 95.3% (92%-97%) | 85.7% (81%-89%) |
| hate | 234 | 89.3% (85%-93%) | 86.3% (81%-90%) | 83.3% (78%-88%) |
| jailbreak | 299 | 94.0% (91%-96%) | 89.3% (85%-92%) | 98.7% (97%-99%) |
| medmcqa | 300 | 78.7% (74%-83%) | 30.7% (26%-36%) | 32.7% (28%-38%) |
| msmarco | 137 | 49.6% (41%-58%) | 39.4% (32%-48%) | 24.1% (18%-32%) |
| pubmedqa | 600 | 78.3% (75%-81%) | 55.0% (51%-59%) | 52.8% (49%-57%) |
| yahoo | 299 | 75.3% (70%-80%) | 68.6% (63%-74%) | 66.6% (61%-72%) |

## When a model and JEV disagree, who is right?

| model | both right | JEV only | model only | both wrong | of the disagreements, the model is right |
|---|---|---|---|---|---|
| Dex | 3477 | 878 | 326 | 646 | 27% |
| Stock Laya | 3038 | 1317 | 371 | 601 | 22% |

## Is the confidence honest? (all three tests together)

| system | accuracy | calibration error (lower is better) | sure (90%+): share of questions | sure (90%+): accuracy there |
|---|---|---|---|---|
| JEV | 81.8% | 0.052 | 63% | 94.5% |
| Dex | 71.4% | 0.058 | 29% | 93.2% |
| Stock Laya | 64.0% | 0.092 | 33% | 88.7% |

## What helped (accuracy against the human label)

| model | A. Ten use cases | B. Tasks never trained on | C. Exam datasets |
|---|---|---|---|
| Stock Laya | 68.2% (66%-71%) | 63.0% (61%-65%) | 62.5% (61%-64%) |
| ModernBERT body, 285 task wordings | 81.4% (79%-83%) | 65.2% (63%-67%) | 60.8% (59%-63%) |
| ModernBERT body, 1,080 task wordings | 80.4% (78%-82%) | 69.2% (67%-71%) | 61.3% (59%-63%) |
| Dex | 81.5% (79%-84%) | 74.4% (72%-76%) | 63.8% (62%-66%) |

## Speed and memory (NVIDIA GeForce RTX 3070 Ti, median / 95th percentile in ms per call)

| call | Dex | Stock Laya | JEV API |
|---|---|---|---|
| short text, 1 question | 18 / 19 | 19 / 19 | 886 / 932 |
| short text, 3 questions | 24 / 24 | 20 / 20 | - |
| short text, 5 questions | 33 / 34 | 22 / 23 | 855 / 890 |
| short text, 10 questions | 62 / 63 | 35 / 37 | - |
| short text, 15 questions | 95 / 97 | 47 / 48 | 780 / 804 |
| long text, 1 question | 72 / 73 | 26 / 27 | - |
| long text, 3 questions | 188 / 190 | 61 / 63 | - |
| long text, 5 questions | 305 / 308 | 95 / 96 | - |
| long text, 10 questions | 590 / 593 | 179 / 181 | - |
| long text, 15 questions | 878 / 884 | 260 / 262 | - |

GPU memory after loading: Dex 2.41 GB, Stock Laya 1.69 GB. Weights on disk: Dex 2379 MB, Stock Laya 843 MB.

## Answer-order check (400 multiple-choice questions, asked twice: as written and with the options reversed)

| system | picks a different option when the order is reversed | accuracy as written | accuracy reversed |
|---|---|---|---|
| JEV | 3.0% | 89.0% | 87.5% |
| Dex | 7.0% | 81.2% | 81.5% |
| Stock Laya | 25.2% | 65.2% | 66.2% |
