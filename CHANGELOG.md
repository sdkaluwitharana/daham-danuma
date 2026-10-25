# Changelog

All notable changes to the dataset are recorded here. Question ids are permanent, so changes are listed by id.

## [0.1.0] - 2026-10-25

First public release, published on a Poya day.

### Added
- 472 Sinhala multiple-choice questions across 8 categories, split into one file per category.
- JSON Schema (`schema/question.schema.json`).
- `scripts/validate.py`: schema, answer-key, option, Unicode and stray-script checks.
- `scripts/find_duplicates.py`: exact, conflict, lexical (character n-gram + Sinhala spelling folding) and optional semantic duplicate detection.
- `scripts/build.py`: JSON, JSONL, CSV and stats exports.
- GitHub Actions for validation, semantic duplicate checks and releases.

### Fixed
- `daham_013`: option d, Malayalam characters in "මාලයක්".
- `daham_026`: option d, Latin characters in "මහමේඝ".
- `daham_237`: question, "සතර බ්‍රහ්ම විවරණ" → "සතර බ්‍රහ්ම විහරණ".
- `daham_349`: question text did not match the options; now asks which sutta was preached to dispel the three fears (තුන් බිය) of Vesali.
- `daham_369`: question asked for eight sacred places but the answer covered only one; now asks for the correct description of Vesali, with city names removed from the options so the answer isn't given away.
- `daham_382`: option d, Thai characters in "පුක්කුසාති".

### Known issues
- `daham_198`/`daham_215` and `daham_202`/`daham_205` share identical wording for different Councils and need rewriting so each stands alone.
- 14 questions start with a pronoun referring to a previous question (see `validate.py` warnings).
- 264 questions have no recorded source yet (`source_suggestion: "UNKNOWN"`).
