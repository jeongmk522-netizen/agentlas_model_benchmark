# Agentlas Model Benchmark Memory

This file is public memory for the benchmark agent. Keep it safe to publish.

## Stable Context

- Repo: `agentlas_model_benchmark`
- Agent name: Agentlas Model Benchmark
- Benchmark target: compare model/runtime ability to drive the Agentlas meta-agent pipeline into installable meta-agent operating-system repos.
- Headline result: Upstage `solar-pro2` through the custom Agentlas CLI wrapper and Gemini CLI `gemini-3-flash-preview` both completed all 10 prompts with reviewed averages of 90/100.
- Historical baseline: direct Upstage API with `solar-pro2` exists, but it is not the headline result because it did not exercise Agentlas repo generation.

## Decisions

- Raw run artifacts stay outside the public repo so the repo does not accumulate unreviewed model outputs by default.
- Provider API keys are environment-only and must never be committed.
- Scores use a 100-point rubric, production-grade red-flag ceilings, and a reviewed aggregate for narrow phrase-match false positives.
- Failed LLM runs stay 0 even if Agentlas deterministic fallback creates a draft.
- API, CLI, custom CLI, and agent harness results must be labeled separately.

## Open Questions

- Should raw model outputs be published after review, or should the public repo keep only score tables and analysis?
- Should `solar-pro3` be added as a separate modern Upstage comparison after the `solar-pro2` baseline?
- Should future runs raise or standardize per-provider timeout budgets, especially for Claude and Codex?
