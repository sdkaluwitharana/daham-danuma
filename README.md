# දහම් දැනුම · Daham Danuma

**An open Sinhala Buddhist multiple-choice question bank.**
**සිංහල බෞද්ධ ධර්ම දැනුම සඳහා විවෘත බහුවරණ ප්‍රශ්න සංචිතයක්.**

[![Validate dataset](https://github.com/sdkaluwitharana/daham-danuma/actions/workflows/validate.yml/badge.svg)](https://github.com/sdkaluwitharana/daham-danuma/actions/workflows/validate.yml)
[![Data: CC BY-SA 4.0](https://img.shields.io/badge/data-CC%20BY--SA%204.0-lightgrey.svg)](LICENSE)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE-CODE)
![Questions](https://img.shields.io/badge/questions-472-orange.svg)
![Language](https://img.shields.io/badge/language-සිංහල-yellow.svg)

---

## සිංහලෙන්

දහම් දැනුම යනු දහම් පාසල් සිසුන්, ගුරුවරුන්, දෙමාපියන් සහ බුදු දහම ඉගෙන ගන්නා සැමට නොමිලේ භාවිත කළ හැකි, විවෘත සිංහල බෞද්ධ ප්‍රශ්න සංචිතයකි.

- **ප්‍රශ්න 472ක්**, එක් එක් ප්‍රශ්නයට පිළිතුරු හතරක්, නිවැරදි පිළිතුර සහ සිංහල පැහැදිලි කිරීමක් සමඟ
- බුද්ධ චරිතය, ධර්මය, බෞද්ධ ඉතිහාසය, ශ්‍රාවක චරිත, සීලය, පින්කම්, ජාතක කතා සහ පාලි යන මාතෘකා
- 1 ශ්‍රේණියේ සිට සාමාන්‍ය පෙළ, දහම් පාසල් අවසාන විභාගය සහ ධර්මාචාර්ය දක්වා මට්ටම් අනුව වර්ග කර ඇත
- ඕනෑම කෙනෙකුට ඇප්, වෙබ් අඩවි, ප්‍රශ්න පත්‍ර හෝ පර්යේෂණ සඳහා නොමිලේ භාවිත කළ හැකිය ([CC BY-SA 4.0](LICENSE))

**වැරැද්දක් දුටුවොත්?** [මෙතැනින් වාර්තා කරන්න](https://github.com/sdkaluwitharana/daham-danuma/issues/new?template=report-mistake.yml). ප්‍රශ්නයේ අංකය (උදා: `daham_042`) සහ නිවැරදි කළ යුතු දේ සඳහන් කරන්න. ධර්මාචාර්යවරුන්ගේ, දහම් පාසල් ගුරුවරුන්ගේ සහ ස්වාමීන් වහන්සේලාගේ සහාය ඉතා අගය කරමු.

**අලුත් ප්‍රශ්න එකතු කිරීමට?** [CONTRIBUTING.md](CONTRIBUTING.md) බලන්න.

---

## In English

Daham Danuma is a free, openly licensed bank of Sinhala-language multiple-choice questions on Buddhism, shaped around the Sri Lankan Dhamma school (දහම් පාසල) syllabus. It is built to be reused: in quiz apps, websites, printed papers, and Sinhala NLP research.

### What's inside

| Category | Sinhala | Questions |
|---|---|---:|
| `dharmaya` | ධර්මය | 122 |
| `bauddha-ithihasaya` | බෞද්ධ ඉතිහාසය | 122 |
| `buddha-charitaya` | බුද්ධ චරිතය | 116 |
| `sravaka-charitha` | ශ්‍රාවක චරිත | 66 |
| `sila` | සීලය | 20 |
| `pinkam` | පින්කම් | 17 |
| `jataka` | ජාතක කතා | 7 |
| `pali` | පාලි | 2 |
| **Total** | | **472** |

**Difficulty:** 350 easy · 105 medium · 17 hard
**Levels:** `grade-1` … `grade-11`, `ol` (G.C.E. O/L), `al` (G.C.E. A/L), `daham-awasana` (Dhamma school final exam), `dharmacharya`. A question can belong to several levels.

### Repository layout

```
data/
  questions/<category>.json   ← the dataset, one file per category (edit these)
  review/duplicate-decisions.json
schema/question.schema.json    ← JSON Schema every question must pass
scripts/
  validate.py                  ← schema + Sinhala text checks
  find_duplicates.py           ← duplicate / near-duplicate detection
  build.py                     ← builds dist/ (JSON, JSONL, CSV, stats)
docs/                          ← field reference, duplicate detection design
huggingface/README.md          ← dataset card for the Hugging Face mirror
```

### Question format

```json
{
  "id": "daham_001",
  "category": "buddha-charitaya",
  "levels": ["grade-4", "grade-5"],
  "level_confidence": "high",
  "level_reason": "Foundational event of the Bodhisattva receiving the first definite prediction (niyata vivarana).",
  "difficulty": "easy",
  "tags": ["bodhisattva", "niyata-vivarana"],
  "question": "බෝසතුන් නියත විවරණ ලැබුවේ කුමන බුදුරජාණන් වහන්සේගෙන්ද?",
  "options": [
    { "id": "a", "text": "කාශ්‍යප බුදුරජාණන් වහන්සේගෙන්" },
    { "id": "b", "text": "දීපංකර බුදුරජාණන් වහන්සේගෙන්" },
    { "id": "c", "text": "කෝණාගමන බුදුරජාණන් වහන්සේගෙන්" },
    { "id": "d", "text": "කකුසඳ බුදුරජාණන් වහන්සේගෙන්" }
  ],
  "answer": "b",
  "explanation": "අප මහා බෝසතාණන් වහන්සේ සුමේධ තාපස අවධියේදී ප්‍රථම වරට නියත විවරණ ලබා ගත්තේ දීපංකර බුදුරජාණන් වහන්සේගෙනි.",
  "source_suggestion": "UNKNOWN"
}
```

Every field is described in [docs/fields.md](docs/fields.md).

### Using the data

Ready-made files (`daham_danuma.json`, `.jsonl`, `.csv`) are attached to every [GitHub release](https://github.com/sdkaluwitharana/daham-danuma/releases), or build them yourself:

```bash
pip install -r requirements.txt
python scripts/build.py        # writes dist/
```

Python:

```python
import json
questions = [json.loads(line) for line in open("dist/daham_danuma.jsonl", encoding="utf-8")]
grade6 = [q for q in questions if "grade-6" in q["levels"]]
```

JavaScript:

```js
const questions = await fetch("daham_danuma.json").then(r => r.json());
const quiz = questions.filter(q => q.category === "jataka");
```

> **Tip for app builders:** shuffle the option order on every attempt. It keeps the quiz fresh and stops students guessing from position or length.

### Quality checks

Every pull request runs automatically:

1. **`validate.py`**: JSON Schema, unique ids, answer key matches an option, no duplicate options, Unicode NFC, and no stray Latin / Malayalam / Tamil / Thai characters mixed into Sinhala words (a common input-method glitch).
2. **`find_duplicates.py`**: finds repeated questions in layers: exact matches, conflicting copies (same question, different answer), and near-duplicates using character n-gram similarity with Sinhala spelling-variant folding (ක/ඛ, න/ණ, ල/ළ, ස/ශ/ෂ …). An optional semantic layer uses multilingual sentence embeddings to catch paraphrases. See [docs/duplicate-detection.md](docs/duplicate-detection.md).

```bash
python scripts/validate.py
python scripts/find_duplicates.py              # writes reports/duplicates.md
python scripts/find_duplicates.py --semantic   # needs requirements-ml.txt
```

### Roadmap

- **Phase 1 – Dataset (now):** collect, clean, fact-check and de-duplicate questions; publish on GitHub and Hugging Face.
- **Phase 2 – Apps:** offline quiz apps for Android, iOS and Windows built on this dataset, with quiz by category or grade, flashcards, timed exams, and a "report a mistake" button that feeds back into this repository.

### Contributing

Corrections and new questions are very welcome, especially from Dhamma school teachers, Dharmacharyas and members of the Maha Sangha. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

### License

- **Questions and explanations** (`data/`): [Creative Commons Attribution-ShareAlike 4.0](LICENSE). You may use, share and adapt them, including commercially, as long as you credit *Daham Danuma* and share adaptations under the same license.
- **Scripts and tooling**: [MIT](LICENSE-CODE).

### Citation

If you use this dataset in research, please cite it (see [CITATION.cff](CITATION.cff)):

```
Kaluwitharana, S. D. (2026). Daham Danuma: An open Sinhala Buddhist multiple-choice question bank (Version 0.1.0) [Data set]. https://github.com/sdkaluwitharana/daham-danuma
```

---

**Maintainer:** [Sachith Dilshan Kaluwitharana](https://sdkaluwitharana.lk) · *සබ්බදානං ධම්මදානං ජිනාති*: the gift of Dhamma excels all gifts.
