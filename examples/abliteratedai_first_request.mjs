#!/usr/bin/env node

/** A bounded, non-streaming AbliteratedAI request. Dry-run unless --send is supplied. */
import { randomUUID } from 'node:crypto';

const ENDPOINT = 'https://api.abliteratedai.dev/v1/chat/completions';
const MODEL = 'abliterated-235b-a22b-fp8';
const WARMING_CODES = new Set(['provider_warming', 'session_starting']);

function argument(name, fallback) {
  const index = process.argv.indexOf(name);
  return index === -1 ? fallback : process.argv[index + 1];
}

const send = process.argv.includes('--send');
const prompt = argument('--prompt', 'Write one original opening sentence for a quiet science-fiction story.');
const waitBudgetSeconds = Number(argument('--wait-budget', '600'));

if (!Number.isInteger(waitBudgetSeconds) || waitBudgetSeconds < 0 || waitBudgetSeconds > 1800) {
  throw new Error('--wait-budget must be a whole number from 0 to 1800.');
}

const payload = {
  model: MODEL,
  messages: [{ role: 'user', content: prompt }],
  max_tokens: 128,
  stream: false,
};

if (!send) {
  console.log(`Dry run: no network request, no charge. Endpoint: ${ENDPOINT}`);
  console.log(JSON.stringify(payload, null, 2));
  console.log('After checking account rates and access, set ABLITERATED_API_KEY and add --send.');
  process.exit(0);
}

const key = process.env.ABLITERATED_API_KEY?.trim();
if (!key) throw new Error('Set ABLITERATED_API_KEY; never put the key in source control.');

const deadline = Date.now() + waitBudgetSeconds * 1000;
const idempotencyKey = randomUUID();

for (;;) {
  let response;
  try {
    response = await fetch(ENDPOINT, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${key}`,
        'Content-Type': 'application/json',
        'Idempotency-Key': idempotencyKey,
      },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(180_000),
    });
  } catch {
    throw new Error('Network failure. Admission is unknown; inspect usage before retrying.');
  }

  const result = await response.json().catch(() => null);
  if (response.ok) {
    const content = result?.choices?.[0]?.message?.content;
    if (typeof content !== 'string') throw new Error('Expected a text response.');
    console.log(content);
    console.log(JSON.stringify({
      request_id: response.headers.get('x-request-id') ?? idempotencyKey,
      usage: result.usage ?? null,
    }));
    break;
  }

  const code = result?.error?.code;
  if (response.status === 503 && WARMING_CODES.has(code)) {
    const delaySeconds = Number(response.headers.get('retry-after'));
    if (!Number.isInteger(delaySeconds) || delaySeconds < 1 || Date.now() + delaySeconds * 1000 > deadline) {
      throw new Error('Warming wait budget reached; check the session page.');
    }
    console.error(`Session is warming; retrying after ${delaySeconds} seconds.`);
    await new Promise((resolve) => setTimeout(resolve, delaySeconds * 1000));
    continue;
  }

  const hint = new Map([
    [401, 'Check your API key.'],
    [402, 'Check credits and session access.'],
    [409, 'The request was already admitted; inspect usage before trying again.'],
    [429, 'Rate limited; check limits before trying again.'],
  ]).get(response.status) ?? 'Inspect request history before trying again.';
  throw new Error(`HTTP ${response.status}. ${hint} No automatic retry.`);
}
