---
license: cc-by-sa-4.0
language:
  - si
pretty_name: Daham Danuma (දහම් දැනුම)
size_categories:
  - n<1K
task_categories:
  - question-answering
  - multiple-choice
task_ids:
  - multiple-choice-qa
tags:
  - sinhala
  - buddhism
  - education
  - low-resource
  - sri-lanka
configs:
  - config_name: default
    data_files:
      - split: train
        path: data/train.jsonl
---

# දහම් දැනුම · Daham Danuma

An open Sinhala Buddhist multiple-choice question bank, shaped around the Sri Lankan Dhamma school (දහම් පාසල) syllabus.

**Source of truth, issues and contributions:** [github.com/sdkaluwitharana/daham-danuma](https://github.com/sdkaluwitharana/daham-danuma). This Hugging Face dataset is a mirror, updated on every release.

## Dataset summary

- 472 questions in Sinhala, each with four options, the correct answer and a Sinhala explanation
- 8 categories: Life of the Buddha, Dhamma, Buddhist history, lives of disciples, precepts, meritorious deeds, Jataka stories, Pali
- Graded from grade 1 to G.C.E. O/L, the Dhamma school final exam and Dharmacharya level
- Difficulty: 350 easy, 105 medium, 17 hard

## Usage

```python
from datasets import load_dataset

ds = load_dataset("sdkaluwitharana/daham-danuma", split="train")
print(ds[0]["question"])
```

## Fields

| Field | Description |
|---|---|
| `id` | Permanent id, e.g. `daham_001` |
| `category` | `buddha-charitaya`, `dharmaya`, `bauddha-ithihasaya`, `sravaka-charitha`, `sila`, `pinkam`, `jataka`, `pali` |
| `levels` | List of levels: `grade-1` … `grade-11`, `ol`, `al`, `daham-awasana`, `dharmacharya` |
| `level_confidence`, `level_reason` | How sure the level assignment is, and why |
| `difficulty` | `easy`, `medium`, `hard` |
| `tags` | Romanised topic tags |
| `question` | Question in Sinhala |
| `options` | Four objects `{id, text}` with ids `a`–`d` |
| `answer` | Id of the correct option |
| `explanation` | Sinhala explanation |
| `source_suggestion` | Canonical reference (e.g. `SN 56.11`), or `UNKNOWN` |

## Intended uses

- Quiz and revision apps for Dhamma school students
- Evaluating how well language models understand Sinhala and Buddhist knowledge (a low-resource benchmark)
- Sinhala NLP research: question answering, distractor generation, paraphrase detection

## Limitations

- Content reflects the Theravada tradition as taught in Sri Lankan Dhamma schools.
- Small (472 questions) and skewed toward easy, grade 4–8 questions.
- About 56% of questions do not have a recorded source yet.
- Questions are fact-checked by the maintainer, but errors may remain. Please report them on GitHub.

## License and citation

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

```bibtex
@dataset{kaluwitharana_daham_danuma_2026,
  author  = {Kaluwitharana, Sachith Dilshan},
  title   = {Daham Danuma: An open Sinhala Buddhist multiple-choice question bank},
  year    = {2026},
  version = {0.1.0},
  url     = {https://github.com/sdkaluwitharana/daham-danuma}
}
```
