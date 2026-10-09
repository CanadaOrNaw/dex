# Data card

## Training data

Dex was trained on typed decisions (a state, a question of type choice, score or yes/no, and a target answer with probabilities) over public text and public instruction-task collections, including [Super-NaturalInstructions](https://github.com/allenai/natural-instructions) (Wang et al., 2022, Apache-2.0) and the [PromptSource](https://huggingface.co/datasets/bigscience/P3) templates (Apache-2.0). The task instructions are varied on purpose: research on instruction tuning finds that generalisation to unseen tasks follows the number of distinct instructions, not the number of rows (see the ablation in [BENCHMARKS.md](BENCHMARKS.md)). 161 Super-NaturalInstructions tasks were held out whole and never trained on; they are benchmark B.

The training data is not part of this release. The datasets underneath the collections above keep their own licences.

## Benchmark data in this repository

`benchmarks/data` holds the benchmark prompts and human labels, `benchmarks/results` Dex's and stock Laya's answers, so the tables regenerate without any model or credit. JEV appears only as summary numbers. The rows come from public datasets, each under its own licence, credited here.

Exam datasets (benchmark C, used only to evaluate, never trained on):

| dataset | licence |
|---|---|
| [CIRCL/vulnerability-scores](https://huggingface.co/datasets/CIRCL/vulnerability-scores) | cc-by-4.0 |
| [community-datasets/yahoo_answers_topics](https://huggingface.co/datasets/community-datasets/yahoo_answers_topics) | unknown |
| [fancyzhx/dbpedia_14](https://huggingface.co/datasets/fancyzhx/dbpedia_14) | cc-by-sa-3.0 |
| [jackhhao/jailbreak-classification](https://huggingface.co/datasets/jackhhao/jailbreak-classification) | apache-2.0 |
| [microsoft/ms_marco](https://huggingface.co/datasets/microsoft/ms_marco) | none listed |
| [openlifescienceai/medmcqa](https://huggingface.co/datasets/openlifescienceai/medmcqa) | apache-2.0 |
| [qiaojin/PubMedQA](https://huggingface.co/datasets/qiaojin/PubMedQA) | mit |
| [ucberkeley-dlab/measuring-hate-speech](https://huggingface.co/datasets/ucberkeley-dlab/measuring-hate-speech) | cc-by-4.0 |

Benchmark A (ten use cases) uses held-out test or validation rows of public datasets that also appear in the training data (different rows), so it is partly in-distribution for Dex; benchmark B (tasks never trained on) and C are not.

## Personal data

Public-text datasets can contain personal information that was already public. A model that only chooses between listed options does not generate text, so it cannot recite its training data.
