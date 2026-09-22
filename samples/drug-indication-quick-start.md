# Browser-safe evaluation quick start

Use the public Groundtruth Data sample without downloading or running an executable:

**Dataset:** [Groundtruth Data Hallucination Benchmark Sample](https://huggingface.co/datasets/Groundtruth-Data/groundtruth-hallucination-bench-sample)

## Fastest test

1. Open the dataset in the Hugging Face viewer.
2. Give the model only the question or prompt field.
3. Keep the verified answer, source URL, and grade hidden until review.
4. Save the exact model response, model and version, test date, and retrieval setting.
5. Compare the response with the source-backed answer.
6. Mark disagreements for review. Do not automatically label every wording difference as a hallucination.

## What to record

- Case ID
- Exact prompt
- Exact model response
- Model and version
- Retrieval enabled or disabled
- Test date
- Reviewer decision
- Notes and source URL

## Important scope note

This 180-row public sample is a diagnostic preview. It is not untouched held-out validation data, and it is separate from Groundtruth Data's larger proof evaluations, remediation datasets, and held-out validation sets.

## Gmail compatibility

This page and the linked Hugging Face dataset are browser-safe links. There is no ZIP file or executable attachment.
