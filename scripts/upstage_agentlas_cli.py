#!/usr/bin/env python3
"""Agentlas custom CLI provider wrapper for Upstage chat completions.

Agentlas sends the full LLM prompt on stdin when AGENTLAS_LLM_CLI_COMMAND is
configured. This wrapper returns a JSON object with a `text` field so
Agentlas' `json-wrapper` CLI normalizer can unwrap it.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request


UPSTAGE_URL = "https://api.upstage.ai/v1/chat/completions"


def main() -> int:
    api_key = os.environ.get("UPSTAGE_API_KEY")
    if not api_key:
        print("UPSTAGE_API_KEY is required", file=sys.stderr)
        return 2

    prompt = sys.stdin.read()
    if not prompt.strip():
        print("stdin prompt is empty", file=sys.stderr)
        return 2

    model = os.environ.get("UPSTAGE_MODEL") or os.environ.get("AGENTLAS_LLM_CLI_MODEL") or "solar-pro2"
    max_tokens = int(os.environ.get("UPSTAGE_MAX_TOKENS", "8000"))
    temperature = float(os.environ.get("UPSTAGE_TEMPERATURE", "0.25"))
    timeout = int(os.environ.get("UPSTAGE_TIMEOUT", "180"))
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    req = urllib.request.Request(
        UPSTAGE_URL,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        print(f"Upstage HTTP {exc.code}: {detail[:1200]}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 - CLI wrapper should surface concise failures.
        print(f"Upstage request failed: {exc}", file=sys.stderr)
        return 1

    text = ""
    try:
        text = data["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError):
        text = json.dumps(data, ensure_ascii=False)

    usage = data.get("usage") or {}
    print(json.dumps({"text": text, "usage": usage, "model": model}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
