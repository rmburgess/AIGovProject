# Project state (as of November 12, 2026)

## Decisions made

- Concept: a patient education app with an AI helper that drafts a plan for reproductive health visits. Trauma-informed. The proposal does not name the app or lock to one topic.
- Two modules first: IUD pain options and cervical cancer screening. A trauma-informed birth plan is next if time allows.
- Stay tied to Claude for the live helper. The public site (Vercel) is a click-through demo with pre-written replies, labeled as such.
- IUD pain options include nitrous oxide, conscious sedation, and general anesthesia, with a plain explanation of why those are harder to get.
- Patient text at about a 3rd-grade reading level, with simple pictures.

## Done

- Library for both modules, with sources and a source-quality table.
- Claude-powered helper (runs inside Claude), with page-side checks.
- Click-through demo mode for the public site.
- 24 test scenarios and a scoring rubric (not yet run).
- First draft of the governance writeup.

## To do, in rough order

1. Fill the bracketed parts of `docs/governance-draft.md` that are personal.
2. Run the 24 scenarios on the live helper, score them with the rubric, and record results.
3. Research the regulation and law section: FDA, HIPAA, state rules (Texas), and the model provider's rules.
4. Replace weak sources: ACOG and CDC directly for IUD pain; US guidance for sedation and anesthesia rules.
5. Ask a clinician to review the library.
6. Optional: trauma-informed birth plan module.
7. Optional: test reading level with real readers; replace the formula estimate.

## Known weak spots

- The sedation and anesthesia claims rest on one state bulletin and one Australian clinic sheet.
- The CDC page and a 2024 draft conflict with the January 2026 federal update on self-collected HPV tests.
- The live helper has not been run on the scenarios yet.
