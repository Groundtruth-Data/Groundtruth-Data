# Groundtruth Data

**Verified data for finding and fixing AI model failures.**

Groundtruth Data builds source-backed AI evaluation datasets from authoritative sources, measures real model failure, builds targeted remediation data when a weakness is demonstrated, and preserves untouched held-out data for validation.

## What we sell

Groundtruth Data is organized around three product types:

1. **Proof evaluations** — fresh, source-backed datasets used to measure whether a model has a repeatable weakness.
2. **Remediation datasets** — larger training-oriented datasets targeted only at demonstrated failure modes.
3. **Held-out validation sets** — untouched records isolated from remediation/training so post-training performance can be measured honestly.

We also build **custom model failure studies** for teams that need a new capability evaluated against authoritative truth.

## Current flagship systems

### Drug Indication Grounding

Authoritative source family: NLM / RxNav / MED-RT.

Locally validated assets include a 500-case proof evaluation, 10,000 remediation rows, and a separate 1,000-row held-out validation set. Commercial delivery is pending publication and checkout acceptance; these are not automatically downloadable purchases today. These assets are not the same as the smaller public diagnostic sample.

### FDA Label Grounding

Authoritative source family: openFDA.

A completed 1,000-row proof evaluation identified a repeatable label-grounding error pattern. The 10k remediation and 1k held-out assets are validated locally and pending publication.

### Citation / OpenAlex Metadata Grounding

Authoritative source: OpenAlex.

A completed 1,000-row source-aware proof evaluation produced 869/1,000 correct (86.9%) and 131/1,000 incorrect (13.1%). The strongest demonstrated weakness was **OpenAlex open-access metadata grounding**; this should not be interpreted as a blanket citation-graph failure.

Locally validated assets, pending commercial publication, include:

- 1,000-row proof evaluation
- 10,000-row remediation dataset
- 1,000-row untouched held-out validation set
- 115 DPO rows based on real observed incorrect responses

No model-improvement claim is made from the existence of remediation data alone.

## Public benchmark sample

A 180-row public sample is available on Hugging Face:

**[Groundtruth Data Hallucination Benchmark Sample](https://huggingface.co/datasets/Groundtruth-Data/groundtruth-hallucination-bench-sample)**

The sample spans research citations, clinical trials, FDA safety data, code execution and package behavior, Companies House records, SEC filings, legal facts, math, science, history, geography, government data, and cross-source verification.

### Try the public sample in three steps

1. Give the model only the value in the `question` field. Keep `verified_answer`, `verification_summary`, source URLs, and prior model responses out of the model context.
2. Save the exact response with the model name, model version, run date, and whether retrieval was enabled.
3. Review the response against the acceptable reference and provenance. Treat a non-match as review-required until synonyms, scope, and source timing have been checked.

The public sample is for inspecting the schema and running a quick diagnostic. It is not an untouched held-out set and should not be used to claim post-training improvement.

## Verification methodology

Groundtruth Data does not treat another language model's answer as factual ground truth.

Depending on the dataset, truth comes from sources such as:

- authoritative APIs and government databases
- official filings and registries
- primary-source documents
- structured publication metadata
- package source archives
- direct Python / Node execution
- deterministic computation

The workflow is:

```text
authoritative source
       ↓
verified source record
       ↓
answer-free proof question
       ↓
model response
       ↓
deterministic/source-aware grading
       ↓
observed failure taxonomy
       ↓
targeted remediation (only if justified)
       ↓
untouched held-out validation
```

Proof, remediation, and held-out sets are kept separate to prevent leakage.

## Public sample schema

Rows in the public sample include:

- `id`
- `dataset`
- `domain`
- `question`
- `verified_answer`
- `verification_summary`
- `source_urls`
- `reference_model`
- `model_response`
- `verdict`
- `grading_mode`
- `difficulty`
- `tags`

The sample is intentionally small and does not contain the full commercial proof, remediation, or held-out datasets. The `samples/` directory contains a quick-start guide linking to Hugging Face; it does not contain a second copy of the 180-row data.

## Commercial datasets

See the catalog and methodology at **https://groundtruthdata.dev**.

Product families include (commercial scope and delivery must be confirmed):

- verified evaluation datasets
- proof evaluations
- targeted remediation datasets
- untouched held-out validation sets
- observed-failure training examples
- custom model failure studies

## Important interpretation note

Benchmark results are specific to the exact dataset, source truth, model/interface, date, and grading method used. A measured error rate on one proof set should not be generalized into a universal claim about a model or an entire capability.

## Historical benchmark article

This repository also contains an earlier benchmark write-up:

[`article-how-often-do-models-hallucinate.md`](./article-how-often-do-models-hallucinate.md)

That article is a historical snapshot of an earlier multi-domain run. Newer, larger proof evaluations should take precedence where available.

---

**Groundtruth Data**  
https://groundtruthdata.dev

## Questions and commercial inquiries

[Discuss a dataset or pilot](https://groundtruthdata.dev/custom). No model-improvement or live Runtime service is promised.
