# AI Governance Project: trauma-informed reproductive health helper

A class prototype for AI in Public Health Governance. It has a plain-language, source-cited library and a Claude-powered helper that drafts a visit plan. See `docs/governance-draft.md` for the writeup.

## What is here

| Path | What it is |
|---|---|
| `content/iud.json`, `content/cervical.json` | The library: cards, sources, and the "why this is harder" notes. Edit these to change the content. |
| `app/template.html` | The page: Learn tab, Visit helper, and "How it is checked". |
| `app/index.html` | The built page (library inlined). Generated. |
| `tools/build.py` | Builds `app/index.html` and checks that every citation points to a real source. |
| `eval/scenarios.json`, `eval/rubric.md` | 24 test scenarios and the scoring rubric. |
| `content/demo.json` | Pre-written example conversations used by the click-through demo mode. |
| `docs/governance-draft.md` | First draft of the written analysis. |

## Build

```
python3 tools/build.py
```

## How the helper works

The page uses the artifact `sample` capability to call Claude on the viewer's own account. Each call sends the rules plus the library text for the chosen topic. The plan comes back as JSON with a card id on every fact. The page then checks that ids exist, removes dose-like numbers, flags facts without a source, and estimates reading level. Urgent-symptom and self-harm messages skip the model and show fixed text.

## Status

First draft. Not reviewed by a clinician. Not for use with real patients.

## Demo mode

When the page is opened outside Claude (for example on Vercel), the live helper is off and the page switches to a click-through demo. The chat replies are pre-written (`content/demo.json`) and labeled as such. The plan checks (source check, dose filter, reading level) run for real on the pre-written plans. A "Show what the checks catch" button runs the same checks on a made-up bad plan.

## Deploying

`vercel.json` serves the `app` folder with no build step. Run `python3 tools/build.py` and commit `app/index.html` before pushing.
