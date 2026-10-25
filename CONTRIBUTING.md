# Contributing · දායක වීම

Thank you for helping improve Daham Danuma. Accuracy matters more than size here: students learn from these questions, so one correct question is worth more than ten doubtful ones.

## Report a mistake (no coding needed)

Open a [**Report a mistake**](https://github.com/sdkaluwitharana/daham-danuma/issues/new?template=report-mistake.yml) issue with the question id (e.g. `daham_042`), what is wrong, the correct version, and a source if you have one.

වැරැද්දක් දුටුවොත් ප්‍රශ්න අංකය, වැරැද්ද සහ නිවැරදි පිළිතුර සඳහන් කර issue එකක් විවෘත කරන්න. මූලාශ්‍රයක් (සූත්‍රය, පොත, පිටුව) ඇත්නම් එයද සඳහන් කරන්න.

## Suggest new questions (no coding needed)

Open a [**New question**](https://github.com/sdkaluwitharana/daham-danuma/issues/new?template=new-question.yml) issue and a maintainer will add it.

## Add or edit questions directly (pull request)

1. Fork the repository and edit the right file in `data/questions/<category>.json`.
2. New questions take the next free id (check the highest existing `daham_###`). Never renumber or reuse ids.
3. Run the checks:

   ```bash
   pip install -r requirements.txt
   python scripts/validate.py
   python scripts/find_duplicates.py
   ```

4. Open a pull request. CI runs the same checks.

## Writing good questions

**The question must stand on its own.** Apps shuffle questions, so never start with "එය", "එම", "උන්වහන්සේ" referring to a previous question. Name the person, sutta or event.

> ✗ එය පැවැත්වූයේ බුද්ධ පරිනිර්වාණයෙන් කොපමණ කලකට පසුවද?
> ✓ ප්‍රථම ධර්ම සංගායනාව පැවැත්වූයේ බුද්ධ පරිනිර්වාණයෙන් කොපමණ කලකට පසුවද?

**Make the wrong options believable.** They should come from the same family as the answer (other Buddhas, other suttas, other lists of the same length). An option no student would pick is wasted.

**Don't let the correct answer stand out.** The correct option should not regularly be the longest or the most detailed one. Write the distractors to a similar length and style. The validator warns when the whole dataset leans this way.

**One clearly correct answer.** If two options could be argued as correct, rewrite.

**Explain, don't repeat.** The `explanation` should teach something: the context, the full list, or why the others are wrong.

**Cite a source when you can.** Use `source_suggestion` for a sutta id (`MN 63`, `SN 56.11`, `Snp 2.1`, `Dhp 183`), a Mahavamsa chapter, or a textbook (`Grade 6 Dhamma school textbook, lesson 4`).

**Use clean Sinhala Unicode.** No legacy (FM-font) text, and no Latin or other-script letters inside Sinhala words. The validator catches these.

**Use your own words.** Facts cannot be copyrighted, but someone else's wording can. Don't copy questions word for word from books, past papers or other apps.

## Reviewing duplicates

`find_duplicates.py` writes `reports/duplicates.md`. For each flagged pair, add a decision to `data/review/duplicate-decisions.json` (`duplicate`, `not-duplicate` or `needs-rewrite`), with a short note. See [docs/duplicate-detection.md](docs/duplicate-detection.md).

## License of contributions

By contributing you agree that your questions and explanations are published under [CC BY-SA 4.0](LICENSE) and your code under [MIT](LICENSE-CODE).
