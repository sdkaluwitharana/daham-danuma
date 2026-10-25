# Field reference

Each file in `data/questions/` is a JSON array of question objects. The file name must match the question's `category`. The authoritative definition is [`schema/question.schema.json`](../schema/question.schema.json).

| Field | Type | Rules |
|---|---|---|
| `id` | string | `daham_` + number (`daham_473`). Unique, permanent: never reuse or renumber an id, because apps and bug reports refer to it. New questions take the next free number. |
| `category` | string | One of the categories below. |
| `levels` | string[] | One or more levels the question suits. |
| `level_confidence` | `high` \| `medium` \| `low` | How sure we are about `levels`. |
| `level_reason` | string | Short English note explaining the level choice. |
| `difficulty` | `easy` \| `medium` \| `hard` | Difficulty *within* its levels. |
| `tags` | string[] | Lower-case kebab-case topic tags in romanised Pali/Sinhala, e.g. `ratana-sutta`, `ata-maha-kusal`. |
| `question` | string | Sinhala Unicode. Must make sense on its own (see CONTRIBUTING). |
| `options` | object[4] | Exactly four, ids `a`, `b`, `c`, `d` in order, all different. |
| `answer` | `a`–`d` | Id of the correct option. |
| `explanation` | string | Sinhala explanation shown after answering. |
| `source_suggestion` | string | Reference such as `SN 56.11`, `Snp 2.1`, `DN 13`, or a textbook reference. `UNKNOWN` until a source is added. |

## Categories

| Value | Sinhala | Scope |
|---|---|---|
| `buddha-charitaya` | බුද්ධ චරිතය | Life of the Buddha, from Sumedha to the Parinibbana |
| `dharmaya` | ධර්මය | Teachings: suttas, Abhidhamma, lists, meditation |
| `bauddha-ithihasaya` | බෞද්ධ ඉතිහාසය | Buddhist history of India and Sri Lanka, councils, sacred places |
| `sravaka-charitha` | ශ්‍රාවක චරිත | Lives of disciples, monks, nuns and lay followers |
| `sila` | සීලය | Precepts and conduct |
| `pinkam` | පින්කම් | Meritorious deeds, festivals and observances |
| `jataka` | ජාතක කතා | Jataka stories |
| `pali` | පාලි | Pali language and gathas |

## Levels

| Value | Meaning |
|---|---|
| `grade-1` … `grade-11` | Dhamma school / school grade |
| `ol` | G.C.E. Ordinary Level Buddhism |
| `al` | G.C.E. Advanced Level Buddhism / Buddhist Civilisation |
| `daham-awasana` | Dhamma school final examination (දහම් පාසල් අවසාන විභාගය) |
| `dharmacharya` | Dharmacharya examination |
