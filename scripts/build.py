#!/usr/bin/env python3
"""Build distributable files from data/questions/*.json into dist/.

Outputs:
    dist/daham_danuma.json    one JSON array (apps)
    dist/daham_danuma.jsonl   one question per line (Hugging Face, ML tools)
    dist/daham_danuma.csv     flat table (Kaggle, spreadsheets)
    dist/stats.json           counts by category, level and difficulty
"""

from __future__ import annotations

import csv
import json
from collections import Counter

from common import DIST_DIR, correct_text, load_questions, strip_private, write_json

GRADE_ORDER = [f"grade-{i}" for i in range(1, 12)] + ["ol", "al", "daham-awasana", "dharmacharya"]


def build_stats(questions: list[dict]) -> dict:
    levels = Counter(level for q in questions for level in q["levels"])
    return {
        "total": len(questions),
        "by_category": dict(Counter(q["category"] for q in questions).most_common()),
        "by_difficulty": {k: sum(q["difficulty"] == k for q in questions) for k in ("easy", "medium", "hard")},
        "by_level": {k: levels[k] for k in GRADE_ORDER if levels[k]},
        "with_source": sum(q["source_suggestion"] != "UNKNOWN" for q in questions),
        "answer_distribution": dict(sorted(Counter(q["answer"] for q in questions).items())),
    }


def main() -> None:
    questions = [strip_private(q) for q in load_questions()]
    DIST_DIR.mkdir(exist_ok=True)

    write_json(DIST_DIR / "daham_danuma.json", questions)

    with (DIST_DIR / "daham_danuma.jsonl").open("w", encoding="utf-8") as fh:
        for q in questions:
            fh.write(json.dumps(q, ensure_ascii=False) + "\n")

    fields = [
        "id", "category", "levels", "difficulty", "tags", "question",
        "option_a", "option_b", "option_c", "option_d", "answer", "answer_text",
        "explanation", "source_suggestion", "level_confidence", "level_reason",
    ]
    # utf-8-sig so Excel opens Sinhala correctly
    with (DIST_DIR / "daham_danuma.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for q in questions:
            opts = {o["id"]: o["text"] for o in q["options"]}
            writer.writerow({
                "id": q["id"],
                "category": q["category"],
                "levels": "|".join(q["levels"]),
                "difficulty": q["difficulty"],
                "tags": "|".join(q["tags"]),
                "question": q["question"],
                "option_a": opts["a"],
                "option_b": opts["b"],
                "option_c": opts["c"],
                "option_d": opts["d"],
                "answer": q["answer"],
                "answer_text": correct_text(q),
                "explanation": q["explanation"],
                "source_suggestion": q["source_suggestion"],
                "level_confidence": q["level_confidence"],
                "level_reason": q["level_reason"],
            })

    stats = build_stats(questions)
    write_json(DIST_DIR / "stats.json", stats)
    print(f"Built {stats['total']} questions into {DIST_DIR.relative_to(DIST_DIR.parent)}/")


if __name__ == "__main__":
    main()
