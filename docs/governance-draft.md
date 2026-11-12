# Governing a patient-facing AI helper: a trauma-informed reproductive health prototype

First draft, for revision. Bracketed items are open.

## 1. What I built and why

I built a prototype web app that helps people get ready for reproductive health appointments. It has two parts. The first is a short library of plain-language pages, written at about a third-grade reading level, on two topics so far: pain options for IUD insertion and cervical cancer screening. Every claim points to a source. The second is a helper, powered by Claude, that talks with the person, asks what they are thinking about, and drafts a plan to bring to the visit. The plan lists what they want the provider to know, what they want to ask, and how they would like the visit to go.

The design is trauma-informed. That means the person has control, can skip anything, is told what to expect, and is never asked to explain their history or their reasons. People who have had bad experiences with health care may avoid care that would help them, so a tool that gets this wrong could do real harm. I chose these topics because the options are often not explained and the stronger choices, like sedation or self-collected HPV tests, are harder to get. [Add why this matters to you / to the course.]

## 2. How I would assess the risks

I am using the NIST AI Risk Management Framework as the outline (govern, map, measure, manage) and the WHO guidance on ethics and governance of AI for health as a check on principles. [Verify both and quote the specific functions and principles I use.]

**Map: what could go wrong**

| Risk | Example in this app | Safeguard now | Gap |
|---|---|---|---|
| Made-up medical facts | Helper invents a pain option or a number | Given only the library text; every plan fact must cite a library card; the page checks the citation exists | The page checks that the card exists, not that the card supports the sentence. That needs a person or a second check. |
| Bad or outdated sources | Older guides say self-collection is not FDA-approved, a 2026 guideline says it is | Source table shows date and type; app follows the newest source and says older guides may disagree | Library still relies on some weak sources (blog, student review, one Australian clinic sheet for sedation rules) |
| Drifting into medical advice | Person asks for a dose or for a diagnosis | Rules in the prompt; page removes dose-like numbers; fixed text for urgent symptoms | Prompt rules can fail. Needs testing at scale. |
| Re-traumatizing the user | Helper asks why someone wants sedation | Rules forbid asking about the past or reasons; short replies; skip option | Needs rater review of real outputs |
| Missing a crisis | Person mentions self-harm or heavy bleeding | Fixed text, model skipped, hotline numbers on every screen | Pattern matching misses unusual wording |
| Privacy | Someone types sensitive details | Page stores nothing; the model call uses the viewer's own Claude account | The model provider still processes the text. Terms and retention need checking. [Verify] |
| Access and equity | Plain language helps, but English only, needs a Claude account, and may not work for people with low vision | Plain-language design, readable sizes | No translation, no testing with real readers, access limited to Claude users |
| Over-trust | Person treats the plan as medical advice | Clear labels; "ask your provider" on every card | Labels are easy to ignore |

**Measure.** I wrote 24 test scenarios in 10 categories (see `eval/scenarios.json`) and a scoring rubric (see `eval/rubric.md`). They cover ordinary use, dose requests, diagnosis requests, urgent symptoms, self-harm, disclosure, questions the library does not cover, conflicting sources, pressure to break the rules, and a person who wants to skip questions. **Results (three runs of the same 24 scenarios; one run each).** I ran the scenarios through the live helper after each of two rounds of changes. The page's own checks gave these counts for the 21 scenarios that reach the model (3 more use fixed text).

| Check | Run 1 (first build) | Run 2 (after changing the prompt and plan) | Run 3 (final) |
|---|---|---|---|
| Routing (urgent, self-harm, support note) | 24/24 | 24/24 | 24/24 |
| Medicine amount in a reply or plan | 0 | 0 | 0 |
| Chat replies of 3 sentences or fewer | 10/21 | 21/21 | 21/21 |
| Plan reading grade 4 or lower | 19/21 | 21/21 | 8/8 (11 plans too short to score) |
| Items the helper filed as the person's own that she never said | 8+ runs | none seen; 1 borderline | none seen |
| Plan size (median items) | 6 | 10 | 2 to 3 |

What the testing found: the first build passed its own code checks but the real helper wrote long replies, put invented wishes in the person's voice, and padded plans. Moving "what you said" to quote-checked text and making every other item an opt-in suggestion fixed the invented wishes. The second run showed the plans were padded and off topic, so I capped suggestions, removed repeats, and stopped the plan when a person describes a symptom. Each fix came from a failed test, which is the point of the Measure step.

Limits. One run per scenario, so I cannot say how much the results vary. The judgment items (faithful to the source card, trauma-informed tone, staying in scope) were read by an AI from the same model family as the helper, not by an independent person, and no clinician has reviewed anything. Known gaps in run 3: the laughing-gas reply says it "helped some people in studies" when the library says one study found less pain and another found no change; the at-home test reply (C1) no longer mentions the age 30 to 65 limit; and a plan can drop a useful comfort request (like a stop signal) when the person did not ask for it. [Add: second human rater on 6 to 8 runs, and the result.]

**Manage.** What would need to happen before real patients used this: clinician review of every library page; replacing weak sources with ACOG, CDC and other primary guidance; testing readability and trust with real readers, including survivors of sexual violence, with their input in design; a privacy review; and a decision about who is responsible when the helper is wrong.

## 3. Regulation and law [needs research]

I have not yet researched these and will not state conclusions until I do:

- Whether the FDA would treat this as a medical device or as software that falls outside device rules, and how its guidance on clinical decision support and on general wellness software applies. The key facts are that the app does not diagnose, treat, or recommend a specific therapy for an individual, and it gives information and drafts questions.
- Whether HIPAA applies. A tool offered directly to the public, and not by a health plan or provider, may not be a covered entity. State health privacy laws may apply anyway. [Check Texas and Washington.]
- State rules on AI in health care, including any disclosure rules for AI used with patients. [Check Texas.]
- The rules of the model provider for health-related uses.

## 4. Source quality: one worked example

For cervical screening, I found three US sources that disagree on one point. The CDC treatment guidelines page says self-collected HPV tests are not FDA-cleared. The USPSTF December 2024 draft says the FDA approves self-collection only in clinical settings. The January 2026 federal guideline update from HRSA says self-collection should be offered for ages 30 to 65 and notes FDA approval of clinic kits in May 2024 and an at-home kit in May 2025. The USPSTF final statement from 2018 predates all of this and calls self-collection a research question. A reader or an AI that picked one source at random would get a different answer. The app follows the newest source, says that older guides may disagree, and shows the sources in a table. This is a real governance problem for any health AI that learns from documents: the documents age at different speeds. [Add: what a maintenance process would look like.]

## 5. Limits of this prototype

- No clinician has reviewed the content.
- Some sources are weak, especially for sedation and anesthesia for IUDs.
- Reading level is estimated with a simple formula and has not been tested with readers.
- The helper has not yet been tested on the full scenario set.
- Two topics only. A trauma-informed birth plan is next.

## 6. Where this could go

[Optional, short. A tool like this could fit with a telehealth or benefits company that wants members to show up to care prepared. That would raise new questions: who owns the content, who is liable, and what data the company would hold.]

## Sources used so far

See the sources table in the app and in `content/iud.json` and `content/cervical.json`.
