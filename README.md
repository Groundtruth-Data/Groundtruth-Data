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

**[Try the free 25-case starter (ZIP)](https://groundtruthdata.dev/samples/drug-indication-starter.zip)**

Use Node.js 22 or newer. Give your model only the questions in `prompts.jsonl`, then copy its responses into `outputs.jsonl` using the supplied template. Run `node run.mjs grade outputs.jsonl report.json` to compare responses with the historical references. A mismatch calls for review. The ZIP includes source dates and the grading instructions. [Read the walkthrough](https://groundtruthdata.dev/docs).

**[Buy the 500-case Proof Evaluation — $999](https://groundtruthdata.dev/checkout?product=drug-indication-proof-500&src=github)**

The 500 unique proof cases are packaged with JSONL, provenance, historical grades, a hash manifest, and an internal-use license. Automatic delivery was verified with completed test payments. Live checkout is now enabled; payment is followed by a private download and delivery email. This is a historical source-grounding evaluation, not a clinical recommendation or independently blinded holdout.

The 10,000 remediation rows and separate 1,000-row held-out validation set remain locally validated and pending commercial publication. These assets are distinct from the smaller public diagnostic sample.

#### Preview a request with AbliteratedAI

To try one historical evaluation prompt with an OpenAI-compatible client, download and extract the starter ZIP above. From the extracted folder, run this Python 3 snippet. It prints a request locally so you can inspect exactly what the model would see. It needs no API key, network request or credits.

```sh
python3 - <<'PY'
import json
from pathlib import Path

with Path("prompts.jsonl").open(encoding="utf-8") as prompts:
    case = json.loads(next(prompts))

request = {
    "model": "abliterated-235b-a22b-fp8",
    "messages": [{"role": "user", "content": case["question"]}],
    "stream": False,
    "max_tokens": 128,
}
print(json.dumps(request, indent=2))
PY
```

For a runnable Python client, [download the first-request example](https://raw.githubusercontent.com/Groundtruth-Data/Groundtruth-Data/main/examples/abliteratedai_first_request.py). Run `python3 abliteratedai_first_request.py` for the free offline check. The example sends a request only when you supply `--send` and an API key.

To run it on a funded account, follow the [AbliteratedAI quickstart](https://abliteratedai.dev/docs/quickstart?utm_source=github&utm_medium=referral&utm_campaign=nov15_sprint&utm_content=groundtruth_example) for access and authentication. A live generation can incur usage charges. Pair the text from `choices[0].message.content` with the original case ID in the starter's `outputs-template.jsonl`. Keep the reference answers out of the request.

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
