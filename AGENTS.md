# Instructions for coding agents

This is a class project for AI in Public Health Governance (due December 3, 2026). It is a trauma-informed patient education prototype with an AI helper. The owner is an epidemiologist, not a full-time developer. Explain changes in plain language.

## Layout

- `content/*.json`: the library (cards, sources). `content/demo.json`: pre-written demo conversations.
- `app/template.html`: the page. `app/index.html` is generated.
- `tools/build.py`: builds `app/index.html` and checks citations.
- `tests/e2e.py`: browser test. `eval/`: test scenarios and rubric. `docs/`: writeup and project state.

## Rules

1. Never edit `app/index.html` by hand. Edit `content/` or `app/template.html`, run `python3 tools/build.py`, and commit the built file.
2. Patient-facing text stays at about a 3rd-grade reading level: short sentences, common words, medical words explained.
3. Every factual claim in a library card needs a source id from that module's `sources`. Do not add a medical claim without a source. If sources disagree, follow the newest one and say older guides may disagree.
4. No medicine doses, amounts, or how-to steps anywhere. No diagnosis. Do not tell the reader which option to pick.
5. Trauma-informed: give choices, allow skipping, never ask about the person's past or why they want something.
6. Keep these safeguards working: grounding in the library, the code that checks that cited card ids exist, the dose filter, the fixed text for urgent symptoms and self-harm, hotline numbers on the helper screen, and the reading-level estimate. If you change the helper's prompt or these checks, tell the owner so the scenarios in `eval/` can be re-run.
7. Never commit API keys or secrets. Do not store or log anything users type.
8. The live helper uses Claude's `sample` feature, which only exists when the page is opened as a Claude artifact. Anywhere else the page runs in demo mode. Moving the live helper to a public site needs a server function and an API key; ask the owner first.
9. Before finishing: run `python3 tools/build.py`, check the script parses, and run `python3 tests/e2e.py` if Playwright is available.
