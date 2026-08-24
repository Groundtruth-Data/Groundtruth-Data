# We tested a frontier model against 873 source-verified facts. Here's exactly where it lies.

## The setup

Hallucination rate isn't one number. It's not even close to one number. We wanted to know, concretely, when a frontier model can be trusted to answer from its own knowledge and when it can't — so we built 17 small, source-verified datasets across law, medicine, finance, science, math, code, history, and government records, and used them as an eval.

Every claim in every dataset traces to a primary source: SEC EDGAR, USPTO, openFDA, ClinicalTrials.gov, UK Companies House's authenticated API, Wikidata's structured statements, NIST CODATA, Harvard's Caselaw Access Project, real Python/Node execution on pinned interpreter versions. Nothing scraped from a blog, nothing pattern-matched from model memory and presented as ground truth. Where a fact couldn't be independently confirmed, the row is marked `unverifiable` — not guessed.

Every dataset was then adversarially audited: a separate pass whose only job was to try to prove each row wrong by re-deriving the fact from the live source again, independently, with fresh code. That audit found and fixed roughly 55 real errors across the catalog — including one case where an *earlier* correction turned out to be wrong itself, caught by a later audit re-checking a DOI.

## The test

For each of 873 fully-graded claims, we derived a fair, open, non-leading question — never "is it true that X," which only tests whether the model agrees with a leading statement — and asked it cold to Claude Sonnet 5: no tools, no web access, no retrieval, just the model's own training. A separate grading pass then compared the response against the verified ground truth.

Four outcomes:
- **Correct** — matches the verified answer
- **Hallucinated** — confidently wrong, stated as fact
- **Hedged correctly** — the model declined to guess rather than fabricate
- **Refused** — declined to answer at all

## The result

| Outcome | Count | Share |
|---|---|---|
| Correct | 619 | 70.9% |
| Hedged correctly | 163 | 18.7% |
| **Hallucinated** | **88** | **10.1%** |
| Refused | 3 | 0.3% |

One in ten answers, across a broad factual spread, was confidently wrong. Not "uncertain." Not "hedged." Stated as fact, and false.

## Where it actually breaks down

The 10.1% average hides the real story:

| Domain | Rows | Hallucination rate |
|---|---:|---:|
| Citation-graph verification (does paper A actually cite paper B, and say what?) | 43 | **32.6%** |
| Patent & IP claims | 40 | 20.0% |
| Clinical trial outcomes | 47 | 19.1% |
| Cross-source verification | 42 | 14.3% |
| English language / literary attribution | 35 | 14.3% |
| FDA drug/device safety | 28 | 14.3% |
| Code-reality (npm/PyPI/crates.io claims) | 42 | 11.9% |
| Scientific claims | 43 | 11.6% |
| Government contracts | 39 | 7.7% |
| SEC EDGAR financial filings | 41 | 7.3% |
| Mathematical claims | 43 | 7.0% |
| General fact-verification | 237 | 6.8% |
| Geographic facts | 30 | 6.7% |
| Legal citation / case law | 35 | 5.7% |
| Code execution semantics | 39 | 5.1% |
| UK Companies House records | 55 | 1.8% |
| Historical events/dates/figures | 34 | **0.0%** |

Citation graphs are the clear outlier — nearly a third of answers confidently wrong. This makes mechanical sense: a model has no way to actually check whether paper A cites paper B and what it says without tools. It falls back on plausible-sounding completion, and plausible-sounding is exactly what a citation hallucination looks like until someone checks.

History is the opposite extreme — zero hallucinations across 34 graded rows. Well-documented, heavily-repeated historical facts appear to be reliably internalized.

## The interesting middle: honest hedging

Two domains stand out for a different reason. UK Companies House records hedged correctly 94.5% of the time; government contracts hedged 79.5% of the time. In both cases the model mostly declined to guess a specific director's name, incorporation date, or contract award figure — rather than inventing one. That's the behavior you actually want: not omniscience, but calibrated uncertainty. A low hallucination number in these two domains isn't because the model knows UK corporate filings — it's because it correctly recognized it didn't, and said so.

## Why this matters beyond one benchmark run

This isn't a one-time stunt test. It's the same grading layer that ships inside every dataset in the catalog — every purchased row includes the exact question asked, the model's actual response, and the verdict, so the claim is auditable row by row rather than taken on faith. The numbers above will drift slightly as the catalog is audited and expanded further; they're a snapshot of a live, ongoing measurement, not a static marketing claim.

## Run it yourself

A 100-row free sample (10% of the full set) is published as [`groundtruth-hallucination-bench-sample`](https://huggingface.co/datasets/groundtruth-data/groundtruth-hallucination-bench-sample) on Hugging Face, along with a small runner script that works against Anthropic, OpenAI-compatible endpoints, or literally any model/CLI you can pipe a prompt into:

```bash
curl -O https://groundtruthdata.dev/eval-runner.mjs
ANTHROPIC_API_KEY=... node eval-runner.mjs groundtruth-sample.jsonl
```

Full methodology, per-row sourcing, and the complete 17-dataset / 918-case catalog: [groundtruthdata.dev](https://groundtruthdata.dev)

---

*Corrections welcome — if you find a row you believe is wrong, that's exactly the kind of scrutiny this was built to survive. Open an issue or reach out via the site.*
