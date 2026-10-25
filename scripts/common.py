"""Shared helpers for the Daham Danuma dataset scripts."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_DIR = ROOT / "data" / "questions"
REVIEW_DIR = ROOT / "data" / "review"
SCHEMA_PATH = ROOT / "schema" / "question.schema.json"
DIST_DIR = ROOT / "dist"
REPORTS_DIR = ROOT / "reports"

ZERO_WIDTH = {"‌", "‍", "﻿", "​"}


def load_questions() -> list[dict]:
    """Load every question from data/questions/*.json, sorted by id."""
    questions: list[dict] = []
    for path in sorted(QUESTIONS_DIR.glob("*.json")):
        with path.open(encoding="utf-8") as fh:
            items = json.load(fh)
        for item in items:
            item["_file"] = path.name
        questions.extend(items)
    questions.sort(key=lambda q: id_number(q["id"]))
    return questions


def id_number(qid: str) -> int:
    match = re.search(r"(\d+)$", qid)
    return int(match.group(1)) if match else 0


def correct_text(question: dict) -> str:
    for option in question["options"]:
        if option["id"] == question["answer"]:
            return option["text"]
    return ""


def strip_private(question: dict) -> dict:
    """Drop helper keys (those starting with '_') before exporting."""
    return {k: v for k, v in question.items() if not k.startswith("_")}


def normalize(text: str) -> str:
    """Normalise Sinhala text for comparison only (never for storage).

    - Unicode NFC
    - remove zero-width joiners / non-joiners (rakaransaya, yansaya and
      touching letters are written with or without them inconsistently)
    - drop punctuation and all whitespace
    """
    text = unicodedata.normalize("NFC", text)
    text = "".join(ch for ch in text if ch not in ZERO_WIDTH)
    text = re.sub(r"[\s\.,;:!?\"'“”‘’()\[\]{}\-–—_/\\|]+", "", text)
    return text


# Sinhala letters that are often written interchangeably in everyday spelling
# (aspirated vs unaspirated, retroflex vs dental, ශ/ෂ/ස). Folding them makes
# "විශාකා" match "විශාඛා" and "කලේ" match "කළේ". Comparison only.
SPELLING_FOLD = str.maketrans({
    "ඛ": "ක", "ඝ": "ග", "ඡ": "ච", "ඣ": "ජ", "ඨ": "ට", "ඪ": "ඩ",
    "ථ": "ත", "ධ": "ද", "ඵ": "ප", "භ": "බ", "ණ": "න", "ළ": "ල",
    "ශ": "ස", "ෂ": "ස", "ඈ": "ඇ", "ෑ": "ැ",
})


def fold(text: str) -> str:
    """normalize() plus Sinhala spelling-variant folding."""
    return normalize(text).translate(SPELLING_FOLD)


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
