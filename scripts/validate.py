#!/usr/bin/env python3
"""Validate the Daham Danuma question bank.

Errors make the script exit with status 1 (used by CI to block a pull request).
Warnings are printed but do not fail the run.

Usage:
    python scripts/validate.py            # errors + warnings
    python scripts/validate.py --strict   # warnings also fail
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter

from jsonschema import Draft202012Validator

from common import SCHEMA_PATH, correct_text, load_questions

# Sinhala block is U+0D80–U+0DFF. Any letter from these scripts inside Sinhala
# text is almost always an input-method or copy-paste glitch
# (e.g. Malayalam "ാ" instead of Sinhala "ා", or Latin "ame" inside a word).
FOREIGN_SCRIPTS = {
    "Latin": r"[A-Za-z]",
    "Malayalam": r"[ഀ-ൿ]",
    "Tamil": r"[஀-௿]",
    "Devanagari": r"[ऀ-ॿ]",
    "Thai": r"[฀-๿]",
    "Telugu/Kannada": r"[ఀ-೿]",
}

# Questions starting like this usually depend on the previous question
# ("එය" = "it", "උන්වහන්සේ" = "he (venerable)") and break in shuffle mode.
CONTEXT_STARTERS = ("එය ", "එම ", "එයින් ", "උන්වහන්සේ", "එතුමා", "ඒ ")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, qid: str, msg: str) -> None:
        self.errors.append(f"{qid}: {msg}")

    def warn(self, qid: str, msg: str) -> None:
        self.warnings.append(f"{qid}: {msg}")


def check_text(report: Report, qid: str, field: str, text: str) -> None:
    for script, pattern in FOREIGN_SCRIPTS.items():
        found = re.findall(pattern, text)
        if found:
            report.error(qid, f"{field} contains {script} characters {''.join(found)!r}")
    if unicodedata.normalize("NFC", text) != text:
        report.error(qid, f"{field} is not Unicode NFC normalised")
    if text != text.strip():
        report.error(qid, f"{field} has leading/trailing whitespace")
    if "  " in text:
        report.warn(qid, f"{field} has double spaces")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--quiet", action="store_true", help="only print the summary")
    args = parser.parse_args()

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    questions = load_questions()
    report = Report()

    ids = Counter(q.get("id") for q in questions)
    for qid, count in ids.items():
        if count > 1:
            report.error(qid, f"id used {count} times")

    longest_is_answer = 0
    for q in questions:
        qid = q.get("id", "<no id>")
        data = {k: v for k, v in q.items() if not k.startswith("_")}

        for err in validator.iter_errors(data):
            path = "/".join(str(p) for p in err.absolute_path) or "(root)"
            report.error(qid, f"schema: {path}: {err.message}")

        if q.get("category") and q["_file"] != f"{q['category']}.json":
            report.error(qid, f"category '{q['category']}' but stored in {q['_file']}")

        options = q.get("options", [])
        option_ids = [o.get("id") for o in options]
        if option_ids != ["a", "b", "c", "d"]:
            report.error(qid, f"option ids must be a,b,c,d in order (got {option_ids})")
        if q.get("answer") not in option_ids:
            report.error(qid, "answer does not match any option id")

        texts = [o.get("text", "") for o in options]
        if len({t.strip() for t in texts}) != len(texts):
            report.error(qid, "two options have the same text")

        check_text(report, qid, "question", q.get("question", ""))
        check_text(report, qid, "explanation", q.get("explanation", ""))
        for o in options:
            check_text(report, qid, f"option {o.get('id')}", o.get("text", ""))

        if q.get("question", "").startswith(CONTEXT_STARTERS):
            report.warn(qid, "question may depend on a previous question (starts with a pronoun)")

        if texts and correct_text(q) and max(texts, key=len) == correct_text(q):
            longest_is_answer += 1

    total = len(questions)
    if total:
        ratio = longest_is_answer / total
        msg = (
            f"correct option is the longest one in {longest_is_answer}/{total} "
            f"questions ({ratio:.0%}); aim for close to 25%"
        )
        if ratio > 0.30:
            report.warn("dataset", msg)

    if not args.quiet:
        for line in report.errors:
            print(f"ERROR   {line}")
        for line in report.warnings:
            print(f"WARNING {line}")

    print(
        f"\nChecked {total} questions: "
        f"{len(report.errors)} error(s), {len(report.warnings)} warning(s)."
    )
    failed = report.errors or (args.strict and report.warnings)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
