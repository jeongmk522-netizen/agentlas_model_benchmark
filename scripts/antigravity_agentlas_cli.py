#!/usr/bin/env python3
"""Experimental Agentlas custom CLI provider wrapper for Antigravity IDE chat.

The local Antigravity CLI currently behaves like an IDE handoff surface on this
machine, so this wrapper is intentionally strict: it only succeeds when the CLI
returns stdout. Silent IDE handoff runs are recorded as benchmark failures.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys


DEFAULT_BIN = "/Applications/Antigravity IDE.app/Contents/Resources/app/bin/antigravity-ide"


def main() -> int:
    prompt = sys.stdin.read()
    if not prompt.strip():
        print("stdin prompt is empty", file=sys.stderr)
        return 2

    binary = os.environ.get("ANTIGRAVITY_CLI") or DEFAULT_BIN
    model = os.environ.get("AGENTLAS_LLM_CLI_MODEL") or os.environ.get("ANTIGRAVITY_MODEL") or "default"
    timeout = int(os.environ.get("ANTIGRAVITY_TIMEOUT", "180"))
    command = [
        binary,
        "chat",
        "-m",
        "ask",
        "--new-window",
        prompt,
    ]
    if model != "default":
        command[2:2] = ["--model", model]

    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        print(f"Antigravity CLI timed out after {timeout}s", file=sys.stderr)
        return 1

    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "no output").strip()
        print(f"Antigravity CLI exited {completed.returncode}: {detail[:1200]}", file=sys.stderr)
        return 1

    text = completed.stdout.strip()
    if not text:
        detail = completed.stderr.strip() or "no stdout"
        print(f"Antigravity CLI returned no stdout: {detail[:1200]}", file=sys.stderr)
        return 1

    print(json.dumps({"text": text, "model": model}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
