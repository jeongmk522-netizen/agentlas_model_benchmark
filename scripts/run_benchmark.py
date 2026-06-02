#!/usr/bin/env python3
"""Run benchmark prompts against API or CLI runtimes.

The Upstage adapter reads UPSTAGE_API_KEY from the environment and never writes
it to logs. Raw outputs are written outside the repo by default.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shlex
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROMPTS = ROOT / "benchmark" / "prompts.json"
DEFAULT_OUTPUT_DIR = Path("/tmp/test_agent/model_runs")
UPSTAGE_URL = "https://api.upstage.ai/v1/chat/completions"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def safe_slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", value).strip("_")


def load_prompts(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def selected_prompts(catalog: dict[str, Any], prompt_id: str | None, run_all: bool) -> list[dict[str, Any]]:
    prompts = catalog["prompts"]
    if run_all:
        return prompts
    if not prompt_id:
        raise SystemExit("Choose --all or --prompt-id")
    matches = [p for p in prompts if p["id"] == prompt_id or p["short_id"] == prompt_id]
    if not matches:
        known = ", ".join(p["short_id"] for p in prompts)
        raise SystemExit(f"Unknown prompt id {prompt_id!r}. Known short ids: {known}")
    return matches


def build_prompt(catalog: dict[str, Any], prompt: dict[str, Any]) -> str:
    return catalog["common_prefix"].strip() + "\n\n" + prompt["text"].strip()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def upstage_chat(model: str, prompt: str, temperature: float, max_tokens: int, timeout: int) -> dict[str, Any]:
    api_key = os.environ.get("UPSTAGE_API_KEY")
    if not api_key:
        raise RuntimeError("UPSTAGE_API_KEY is required for runtime=upstage_api")

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
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"Upstage HTTP {exc.code}: {detail[:1200]}") from exc


def cli_run(command_template: str, prompt: str, timeout: int, execution_dir: Path) -> dict[str, Any]:
    if "{prompt}" not in command_template:
        raise RuntimeError("CLI command template must contain {prompt}")
    command = [part if part != "{prompt}" else prompt for part in shlex.split(command_template)]
    execution_dir.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(command, cwd=execution_dir, capture_output=True, text=True, timeout=timeout, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"CLI exited {completed.returncode}: {completed.stderr[:1200]}")
    return {
        "choices": [{"message": {"content": completed.stdout}}],
        "usage": None,
        "runtime_notes": {"stderr": completed.stderr[:2000]},
    }


def runtime_command(runtime: str, model: str, prompt: str, execution_dir: Path) -> tuple[list[str], str | None]:
    """Return argv and stdin for known CLI runtimes."""
    execution_dir.mkdir(parents=True, exist_ok=True)
    if runtime == "claude_code":
        return (
            [
                "claude",
                "-p",
                "--model",
                model,
                "--tools",
                "",
                "--permission-mode",
                "dontAsk",
                "--no-session-persistence",
                "--output-format",
                "text",
            ],
            prompt,
        )
    if runtime == "codex_cli":
        return (
            [
                "codex",
                "exec",
                "--sandbox",
                "read-only",
                "--skip-git-repo-check",
                "--ephemeral",
                "--color",
                "never",
                "--config",
                'model_reasoning_effort="low"',
                "--model",
                model,
                "-",
            ],
            prompt,
        )
    if runtime == "gemini_cli":
        return (
            [
                "gemini",
                "--model",
                model,
                "--prompt",
                prompt,
                "--skip-trust",
                "--approval-mode",
                "plan",
                "--output-format",
                "text",
            ],
            None,
        )
    if runtime == "antigravity_cli":
        return (
            [
                "/Applications/Antigravity IDE.app/Contents/Resources/app/bin/antigravity-ide",
                "chat",
                "-m",
                "ask",
                "--new-window",
                prompt,
            ],
            None,
        )
    raise RuntimeError(f"Unsupported runtime: {runtime}")


def known_cli_run(runtime: str, model: str, prompt: str, timeout: int, execution_dir: Path) -> dict[str, Any]:
    command, stdin = runtime_command(runtime, model, prompt, execution_dir)
    completed = subprocess.run(
        command,
        cwd=execution_dir,
        input=stdin,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"{runtime} exited {completed.returncode}: {completed.stderr[:1600] or completed.stdout[:1600]}")
    content = completed.stdout.strip()
    if not content:
        raise RuntimeError(f"{runtime} returned no stdout; stderr={completed.stderr[:1600]}")
    return {
        "choices": [{"message": {"content": content}}],
        "usage": None,
        "runtime_notes": {
            "stderr": completed.stderr[:2000],
            "execution_dir": str(execution_dir),
        },
    }


def response_text(response: dict[str, Any]) -> str:
    try:
        return response["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError):
        return json.dumps(response, indent=2, ensure_ascii=False)


def run_one(args: argparse.Namespace, catalog: dict[str, Any], prompt: dict[str, Any]) -> None:
    runtime = safe_slug(args.runtime)
    model = safe_slug(args.model)
    prompt_id = prompt["short_id"]
    stem = f"{runtime}_{model}_{prompt_id}"
    md_path = args.output_dir / f"{stem}.md"
    log_path = args.output_dir / f"{stem}.log"
    usage_path = args.output_dir / f"{stem}.usage.json"
    error_path = args.output_dir / f"{stem}.error.txt"
    full_prompt = build_prompt(catalog, prompt)

    start = utc_now()
    t0 = time.perf_counter()
    metadata: dict[str, Any] = {
        "runtime": args.runtime,
        "model": args.model,
        "prompt_id": prompt["short_id"],
        "prompt_name": prompt["id"],
        "start_time": start,
        "cost_usd": None,
        "cost_type": "unavailable",
        "notes": args.notes or "",
    }

    try:
        if args.dry_run:
            response = {"choices": [{"message": {"content": "# Dry Run\n\nNo model call was made."}}], "usage": None}
        elif args.runtime == "upstage_api":
            response = upstage_chat(args.model, full_prompt, args.temperature, args.max_tokens, args.timeout)
        elif args.runtime == "cli":
            response = cli_run(args.command_template, full_prompt, args.timeout, args.execution_dir)
        elif args.runtime in {"claude_code", "codex_cli", "gemini_cli", "antigravity_cli"}:
            response = known_cli_run(args.runtime, args.model, full_prompt, args.timeout, args.execution_dir)
        else:
            raise RuntimeError(f"Unsupported runtime: {args.runtime}")

        wall = time.perf_counter() - t0
        end = utc_now()
        content = response_text(response)
        usage = response.get("usage") or {}

        metadata.update(
            {
                "end_time": end,
                "wall_time_seconds": round(wall, 3),
                "input_tokens": usage.get("prompt_tokens"),
                "output_tokens": usage.get("completion_tokens"),
                "total_tokens": usage.get("total_tokens"),
                "failure_reason": None,
                "output_path": str(md_path),
            }
        )
        header = (
            f"---\nruntime: {args.runtime}\nmodel: {args.model}\nprompt_id: {prompt['short_id']}\n"
            f"prompt_name: {prompt['id']}\nstart_time: {start}\nend_time: {end}\n"
            f"wall_time_seconds: {metadata['wall_time_seconds']}\n---\n\n"
        )
        write_text(md_path, header + content.strip() + "\n")
        write_json(usage_path, {"usage": usage, "metadata": metadata})
        write_text(log_path, json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")
        if error_path.exists():
            error_path.unlink()
        print(f"ok {stem} {metadata['wall_time_seconds']}s")
    except Exception as exc:
        wall = time.perf_counter() - t0
        end = utc_now()
        metadata.update(
            {
                "end_time": end,
                "wall_time_seconds": round(wall, 3),
                "input_tokens": None,
                "output_tokens": None,
                "total_tokens": None,
                "failure_reason": str(exc),
            }
        )
        write_text(error_path, str(exc) + "\n")
        write_text(log_path, json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")
        print(f"failed {stem}: {exc}", file=sys.stderr)
        if not args.continue_on_error:
            raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run meta-agent OS benchmark prompts.")
    parser.add_argument("--runtime", required=True, choices=["upstage_api", "cli", "claude_code", "codex_cli", "gemini_cli", "antigravity_cli"])
    parser.add_argument("--model", required=True)
    parser.add_argument("--prompt-id")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--prompts", type=Path, default=DEFAULT_PROMPTS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--command-template", default="")
    parser.add_argument("--execution-dir", type=Path, default=Path("/tmp/test_agent/isolated/default"))
    parser.add_argument("--notes", default="")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    catalog = load_prompts(args.prompts)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for prompt in selected_prompts(catalog, args.prompt_id, args.all):
        run_one(args, catalog, prompt)


if __name__ == "__main__":
    main()
