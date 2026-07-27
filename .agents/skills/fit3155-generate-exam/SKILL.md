---
name: fit3155-generate-exam
description: Generate the next FIT3155 sample exam PDF by following the observed exam structure, teaching material, labs, and original sample exam.
---

# Generate FIT3155 Sample Exam

Use this when asked to generate another FIT3155 sample exam under `fit3155/exams/`.

The exam rules and observed structure are imported from:

@fit3155/exams/README.md

## Goal

Create the next generated exam folder and paper, e.g. if `01/` exists, create:

- `fit3155/exams/02/GENERATED_EXAM_02.tex`
- `fit3155/exams/02/GENERATED_EXAM_02.pdf`

Do not overwrite an existing generated exam.

## Workflow

- Treat the imported README as the source of truth for structure, topic coverage, and style.
- Examinable scope is wk01-wk11 only. Week 12 (approximation algorithms) is NOT examinable, so never generate questions on it.
- Inspect existing generated exams so the new paper does not repeat questions.
- Read `ORIGINAL_SAMPLE_EXAM.pdf` with `pdftotext` to refresh the layout and wording style.
- Read the relevant `LEARNING_INTENTIONS.md`, `notesXX.pdf`, and `labXX.pdf` files before writing questions.
- Pick the next two-digit folder number by scanning existing numeric folders in `fit3155/exams/`.
- Write the `.tex` and compile the matching `.pdf` in that new folder.
- Do not include solutions unless explicitly requested.

## Build And Verify

- Compile from the new exam folder with:

```bash
rtk latexmk -pdf -interaction=nonstopmode GENERATED_EXAM_XX.tex
```

- Verify the generated PDF:
    - `rtk pdfinfo GENERATED_EXAM_XX.pdf` should show 22 pages.
    - `rtk pdftotext -layout GENERATED_EXAM_XX.pdf -` should show all questions and `End of Exam`.
    - Check the LaTeX log for warnings/errors.
- Clean intermediate files with:

```bash
rtk latexmk -c GENERATED_EXAM_XX.tex
```

- Final response should give clickable paths to the `.tex` and `.pdf`.
