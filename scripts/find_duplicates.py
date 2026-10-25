#!/usr/bin/env python3
"""Find duplicate and near-duplicate questions in the Daham Danuma dataset.

Three layers, from cheap and certain to expensive and fuzzy:

1. exact     - question and correct answer identical after normalisation
               (NFC, zero-width joiners removed, punctuation/spaces removed).
   conflict  - question text identical but the correct answers differ. This
               is a question that depends on the previous one ("එය ...") or a
               contradiction; both need a human.
2. lexical   - TF-IDF over character n-grams, compared with cosine similarity.
               Character n-grams work for Sinhala without a tokenizer or
               stemmer, and catch reworded questions that share most words.
               The correct-answer text is compared too: two questions that
               look different but have the same correct answer are often the
               same question asked two ways.
3. semantic  - optional (--semantic). A multilingual sentence-embedding model
               that supports Sinhala (default: LaBSE) catches paraphrases that
               share meaning but few characters. Needs `sentence-transformers`.

Every flagged pair can be reviewed once and recorded in
data/review/duplicate-decisions.json so it is not reported again.

Usage:
    python scripts/find_duplicates.py                 # exact + lexical
    python scripts/find_duplicates.py --semantic      # + embeddings
    python scripts/find_duplicates.py --fail-on exact # CI: fail on new exact dupes
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import date

from common import REPORTS_DIR, REVIEW_DIR, correct_text, fold, load_questions, normalize, write_json

DECISIONS_PATH = REVIEW_DIR / "duplicate-decisions.json"

# Thresholds tuned on the first 472 questions.
QUESTION_SIM = 0.85        # questions alone look almost the same
COMBINED_Q_SIM = 0.60      # question fairly similar ...
COMBINED_A_SIM = 0.85      # ... and correct answer almost the same
SAME_ANSWER_Q_SIM = 0.25   # identical answer + loosely related question
SEMANTIC_SIM = 0.90        # embedding cosine similarity


@dataclass
class Pair:
    a: str
    b: str
    kind: str                       # exact | lexical | semantic
    question_sim: float = 0.0
    answer_sim: float = 0.0
    semantic_sim: float | None = None
    reasons: list[str] = field(default_factory=list)

    @property
    def key(self) -> tuple[str, str]:
        return tuple(sorted((self.a, self.b)))  # type: ignore[return-value]


def load_decisions() -> dict[tuple[str, str], dict]:
    if not DECISIONS_PATH.exists():
        return {}
    data = json.loads(DECISIONS_PATH.read_text(encoding="utf-8"))
    return {tuple(sorted(d["pair"])): d for d in data.get("decisions", [])}


def lexical_matrices(questions: list[dict]):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    q_texts = [fold(q["question"]) for q in questions]
    a_texts = [fold(correct_text(q)) for q in questions]
    vec = TfidfVectorizer(analyzer="char", ngram_range=(2, 4), sublinear_tf=True)
    vec.fit(q_texts + a_texts)
    q_sim = cosine_similarity(vec.transform(q_texts))
    a_sim = cosine_similarity(vec.transform(a_texts))
    return q_sim, a_sim


def semantic_matrix(questions: list[dict], model_name: str):
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        sys.exit(
            "--semantic needs sentence-transformers:\n"
            "    pip install -r requirements-ml.txt"
        )
    from sklearn.metrics.pairwise import cosine_similarity

    model = SentenceTransformer(model_name)
    texts = [f"{q['question']} {correct_text(q)}" for q in questions]
    emb = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return cosine_similarity(emb)


def find_pairs(questions: list[dict], semantic: bool, model_name: str) -> list[Pair]:
    pairs: dict[tuple[str, str], Pair] = {}
    ids = [q["id"] for q in questions]
    norm_q = [normalize(q["question"]) for q in questions]
    norm_a = [fold(correct_text(q)) for q in questions]

    q_sim, a_sim = lexical_matrices(questions)
    s_sim = semantic_matrix(questions, model_name) if semantic else None

    n = len(questions)
    for i in range(n):
        for j in range(i + 1, n):
            qs, as_ = float(q_sim[i, j]), float(a_sim[i, j])
            reasons = []
            kind = None
            if norm_q[i] == norm_q[j]:
                if norm_a[i] == norm_a[j]:
                    kind = "exact"
                    reasons.append("identical question and correct answer")
                else:
                    # Same wording, different answers: the question only makes
                    # sense next to the one before it ("එය ..."), or the two
                    # contradict each other. Either way it must be rewritten.
                    kind = "conflict"
                    reasons.append("identical question text but different correct answers")
            else:
                if qs >= QUESTION_SIM:
                    reasons.append(f"question similarity {qs:.2f}")
                if qs >= COMBINED_Q_SIM and as_ >= COMBINED_A_SIM:
                    reasons.append(f"similar question ({qs:.2f}) and answer ({as_:.2f})")
                if norm_a[i] == norm_a[j] and qs >= SAME_ANSWER_Q_SIM:
                    reasons.append(f"same correct answer, related question ({qs:.2f})")
                if reasons:
                    kind = "lexical"
            ss = float(s_sim[i, j]) if s_sim is not None else None
            if ss is not None and ss >= SEMANTIC_SIM and kind is None:
                kind = "semantic"
                reasons.append(f"embedding similarity {ss:.2f}")
            if kind:
                p = Pair(ids[i], ids[j], kind, qs, as_, ss, reasons)
                pairs[p.key] = p
    order = {"exact": 0, "conflict": 1, "lexical": 2, "semantic": 3}
    return sorted(pairs.values(), key=lambda p: (order[p.kind], -p.question_sim))


def write_report(pairs: list[Pair], questions: list[dict], decisions: dict) -> None:
    by_id = {q["id"]: q for q in questions}
    lines = [
        "# Duplicate question report",
        "",
        f"Generated {date.today().isoformat()} by `scripts/find_duplicates.py` "
        f"over {len(questions)} questions.",
        "",
        "| Status | Kind | Pair | Q sim | Answer sim | Why |",
        "|---|---|---|---|---|---|",
    ]
    for p in pairs:
        decision = decisions.get(p.key, {}).get("decision", "unreviewed")
        lines.append(
            f"| {decision} | {p.kind} | `{p.a}` / `{p.b}` | {p.question_sim:.2f} | "
            f"{p.answer_sim:.2f} | {'; '.join(p.reasons)} |"
        )
    lines += ["", "## Details", ""]
    for p in pairs:
        qa, qb = by_id[p.a], by_id[p.b]
        lines += [
            f"### `{p.a}` / `{p.b}` ({p.kind})",
            "",
            f"- **{p.a}** ({qa['category']}): {qa['question']}  ",
            f"  ✔ {correct_text(qa)}",
            f"- **{p.b}** ({qb['category']}): {qb['question']}  ",
            f"  ✔ {correct_text(qb)}",
            "",
        ]
    REPORTS_DIR.mkdir(exist_ok=True)
    (REPORTS_DIR / "duplicates.md").write_text("\n".join(lines), encoding="utf-8")
    write_json(
        REPORTS_DIR / "duplicates.json",
        [
            {
                "pair": [p.a, p.b],
                "kind": p.kind,
                "question_sim": round(p.question_sim, 3),
                "answer_sim": round(p.answer_sim, 3),
                "semantic_sim": None if p.semantic_sim is None else round(p.semantic_sim, 3),
                "reasons": p.reasons,
                "decision": decisions.get(p.key, {}).get("decision", "unreviewed"),
            }
            for p in pairs
        ],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--semantic", action="store_true", help="also use sentence embeddings")
    parser.add_argument("--model", default="sentence-transformers/LaBSE", help="embedding model for --semantic")
    parser.add_argument(
        "--fail-on",
        choices=["none", "exact", "any"],
        default="none",
        help="exit 1 if unreviewed pairs of this kind exist",
    )
    args = parser.parse_args()

    questions = load_questions()
    decisions = load_decisions()
    pairs = find_pairs(questions, args.semantic, args.model)
    write_report(pairs, questions, decisions)

    unreviewed = [p for p in pairs if p.key not in decisions]
    counts = {k: sum(p.kind == k for p in pairs) for k in ("exact", "conflict", "lexical", "semantic")}
    print(f"Flagged {len(pairs)} pair(s): {counts}; {len(unreviewed)} unreviewed.")
    for p in unreviewed:
        print(f"  [{p.kind}] {p.a} / {p.b}: {'; '.join(p.reasons)}")
    print("Report: reports/duplicates.md")

    if args.fail_on == "exact" and any(p.kind in ("exact", "conflict") for p in unreviewed):
        print("\nUnreviewed exact duplicates / conflicts found. Fix the question or record a"
              " decision in data/review/duplicate-decisions.json.")
        return 1
    if args.fail_on == "any" and unreviewed:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
