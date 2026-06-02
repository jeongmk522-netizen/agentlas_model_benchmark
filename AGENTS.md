# Agentlas Model Benchmark Agent Instructions

This is an Agentlas public output repository for benchmarking model/runtime ability to design installable agent-team operating systems.

## Contract

- Keep this repo self-contained and public-safe.
- Do not add provider API keys, local machine paths, raw private transcripts, unpublished user data, or private logs.
- Keep API-key use environment-only. The benchmark runner reads `UPSTAGE_API_KEY` and must never print or persist it.
- Preserve the distinction between pure model/API behavior and runtime harness behavior.
- Keep `README.md`, `CLAUDE.md`, `AGENTS.md`, `memory.md`, and `agent.md` useful for someone discovering the repo on GitHub.
- Run `scripts/public_safety_check.sh` before publishing.

## Benchmark Rules

- Use the same `COMMON_PREFIX` for every prompt and runtime.
- Save raw run artifacts to `/tmp/test_agent/model_runs/` using the naming contract in `README.md`.
- Record runtime, model label, prompt id, start/end time, wall time, token usage if available, cost type, failure reason if failed, and runtime notes.
- Apply red-flag ceilings before assigning final verdicts.
- Do not compare a CLI harness against a direct API result without labeling the runtime difference.

## Agent Memory

Use `memory.md` for durable public memory about this benchmark. Do not store private coordination notes here.
