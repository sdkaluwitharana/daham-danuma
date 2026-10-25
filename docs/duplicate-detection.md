# Duplicate detection

A question bank that grows from many contributors collects repeats: the same question typed twice, the same fact asked with different wording, or two questions that only made sense one after the other. `scripts/find_duplicates.py` finds these in layers, from cheap and certain to expensive and fuzzy.

## Layer 1: normalised exact match

Text is compared after:

- Unicode NFC normalisation
- removing zero-width joiner / non-joiner (rakaransaya, yansaya and touching letters are typed with or without them)
- removing punctuation and whitespace
- folding common spelling variants: ඛ→ක, ඝ→ග, ඡ→ච, ඣ→ජ, ඨ→ට, ඪ→ඩ, ථ→ත, ධ→ද, ඵ→ප, භ→බ, ණ→න, ළ→ල, ශ/ෂ→ස (so කලේ = කළේ, විශාකා = විශාඛා)

This normalisation is for comparison only. Stored text is never changed.

Two outcomes:

- **exact**: same question, same correct answer → a true duplicate.
- **conflict**: same question, different correct answers → the question depends on the one before it (e.g. starts with "එය ...") or the two contradict each other. Either way, a human must rewrite it.

CI fails on unreviewed `exact` and `conflict` pairs.

## Layer 2: lexical similarity (TF-IDF over character n-grams)

Sinhala has no widely available tokenizer or stemmer, and case endings change words (සූත්‍රය / සූත්‍රයේ / සූත්‍ර). Character 2–4-grams sidestep that: two sentences that share most of their letter sequences score high even when endings differ.

Each pair gets two cosine scores: **question similarity** and **correct-answer similarity**. A pair is flagged when:

| Rule | Catches |
|---|---|
| question ≥ 0.85 | the same question, lightly edited |
| question ≥ 0.60 and answer ≥ 0.85 | rewording plus the same answer |
| same answer and question ≥ 0.25 | different wording of the same fact, e.g. *ත්‍රිවිධ ශික්ෂා නම් කරන්න* / *ත්‍රී ශික්‍ෂා මොනවාද?* |

Thresholds were tuned on the first 472 questions. Lexical pairs are reported for review but do not fail CI.

## Layer 3: semantic similarity (machine learning, optional)

Some duplicates share meaning but almost no letters:

> *විශාකා සිටු දුව පිදූ ආරාමය නම් කරන්න.*
> *විශාඛා මහ උපාසිකාව කරවූ විහාරය කුමක්ද?*

`--semantic` encodes each question together with its correct answer using a multilingual sentence-embedding model that supports Sinhala (default [`sentence-transformers/LaBSE`](https://huggingface.co/sentence-transformers/LaBSE)), and flags pairs with cosine similarity ≥ 0.90.

```bash
pip install -r requirements-ml.txt
python scripts/find_duplicates.py --semantic
python scripts/find_duplicates.py --semantic --model intfloat/multilingual-e5-base
```

The **Semantic duplicates** GitHub Action runs this on demand (Actions → Semantic duplicates → Run workflow), so nobody needs a GPU or a local model download.

## The human review loop

Every flagged pair is reviewed once and recorded in `data/review/duplicate-decisions.json`:

```json
{ "pair": ["daham_234", "daham_276"], "decision": "duplicate", "note": "...", "reviewed_on": "2026-10-25" }
```

| Decision | Meaning |
|---|---|
| `duplicate` | One copy will be removed |
| `not-duplicate` | Different questions; stop flagging this pair |
| `needs-rewrite` | Keep both, but rewrite so each stands alone |

Reviewed pairs are not reported again.

## Where machine learning goes next

The review file is more than a to-do list: every decision is a **labelled training example** (pair → duplicate / not duplicate) for Sinhala Buddhist text, which does not exist anywhere else today.

1. **Now:** zero-shot embeddings (LaBSE / multilingual-e5) and hand-tuned thresholds.
2. **After about 200 reviewed pairs:** learn the thresholds from the decisions (logistic regression over lexical + semantic scores) instead of guessing them.
3. **After about 1,000 pairs:** fine-tune a small cross-encoder on the decisions. It would also be publishable as a Sinhala paraphrase-detection model on Hugging Face.
4. **Related uses of the same embeddings:** suggest a category, tags and levels for new questions; find weak distractors (wrong options that are obviously wrong); cluster topics to show syllabus gaps.
5. **Phase 2 (apps):** anonymous answer statistics let difficulty be measured from real students using Item Response Theory, instead of being guessed.
