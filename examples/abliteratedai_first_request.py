#!/usr/bin/env python3
"""A bounded, non-streaming first request. Dry-run unless --send is supplied."""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
import uuid

ENDPOINT = 'https://api.abliteratedai.dev/v1/chat/completions'
MODEL = 'abliterated-235b-a22b-fp8'
WARMING = {'provider_warming', 'session_starting'}


def request_payload(prompt):
    return {
        'model': MODEL,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 128,
        'stream': False,
    }


def first_request(key, prompt, wait_budget=600, *, opener=urllib.request.urlopen,
                  sleep=time.sleep, clock=time.monotonic):
    """Retry only explicit, pre-admission warming responses; never unknown failures."""
    deadline = clock() + wait_budget
    request_id = str(uuid.uuid4())
    body = json.dumps(request_payload(prompt)).encode()
    while True:
        request = urllib.request.Request(ENDPOINT, data=body, method='POST', headers={
            'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json',
            'Idempotency-Key': request_id})
        try:
            with opener(request, timeout=180) as response:
                result = json.load(response)
                content = result['choices'][0]['message']['content']
                if not isinstance(content, str):
                    raise ValueError('Expected a text response.')
                return {'content': content, 'usage': result.get('usage'),
                        'request_id': response.headers.get('X-Request-ID', request_id)}
        except urllib.error.HTTPError as error:
            try:
                code = json.load(error).get('error', {}).get('code')
            except (ValueError, AttributeError, TypeError):
                code = None
            if error.code == 503 and code in WARMING:
                try:
                    delay = int(error.headers.get('Retry-After', ''))
                except (TypeError, ValueError):
                    raise RuntimeError('Warming without a usable Retry-After; check the session page.') from None
                if delay < 1 or clock() + delay > deadline:
                    raise RuntimeError('Warming wait budget reached; check the session page.') from None
                print('Session is warming; retrying after %s seconds.' % delay, file=sys.stderr)
                sleep(delay)
                continue
            hint = {401: 'Check your API key.', 402: 'Check credits and session access.',
                    409: 'The request was already admitted; inspect usage before trying again.',
                    429: 'Rate limited; check limits before trying again.'}.get(error.code,
                          'Inspect request history before trying again.')
            raise RuntimeError('HTTP %s. %s No automatic retry.' % (error.code, hint)) from None
        except (urllib.error.URLError, TimeoutError):
            raise RuntimeError('Network failure. Admission is unknown; inspect usage before retrying.') from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--send', action='store_true', help='Make a real request; usage may be charged.')
    parser.add_argument('--prompt', default='Write one original opening sentence for a quiet science-fiction story.')
    parser.add_argument('--wait-budget', type=int, default=600, help='Maximum warming wait in seconds (0–1800).')
    args = parser.parse_args()
    if not 0 <= args.wait_budget <= 1800:
        parser.error('--wait-budget must be between 0 and 1800')
    if not args.send:
        print('Dry run: no network request, no charge. Endpoint: ' + ENDPOINT)
        print(json.dumps(request_payload(args.prompt), indent=2, ensure_ascii=False))
        print('After checking account rates and access, set ABLITERATED_API_KEY and add --send.')
        return 0
    key = os.environ.get('ABLITERATED_API_KEY', '').strip()
    if not key:
        parser.error('Set ABLITERATED_API_KEY in your environment; never put the key in source control.')
    try:
        result = first_request(key, args.prompt, args.wait_budget)
        print(result['content'])
        print(json.dumps({'request_id': result['request_id'], 'usage': result['usage']}))
        return 0
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 1
    except (ValueError, KeyError, IndexError, TypeError):
        # Avoid printing upstream bodies, credentials or user content in failure logs.
        print('Request did not complete. Check session status, credits and request history before retrying.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
