# Agentlas Model Benchmark Memory

This file is public memory for the benchmark agent. Keep it safe to publish.

## Stable Context

- Repo: `agentlas_model_benchmark`
- Agent name: Agentlas Model Benchmark
- Benchmark target: compare model/runtime ability to drive the Agentlas agent-team pipeline into installable agent-team operating-system repos.
- Headline result: with the long-timeout contract, Claude Code `claude-sonnet-4-6`, Codex CLI `gpt-5.5`, and Gemini CLI `gemini-3.1-pro-preview` tied at a reviewed average of 96.0/100 across the 9 published public prompts.
- Cost/speed result: Upstage `solar-pro2` through the custom Agentlas CLI wrapper averaged 95.9/100, was the fastest completed runtime at about 9.3 seconds per case, and had the lowest proxy API cost estimate.
- Gemini Flash result: Gemini CLI `gemini-3-flash-preview` completed the 9 published public prompts at 94.1/100; it is usable but no longer tied for the top result after long-timeout reruns.
- Failure label: Antigravity CLI default scored 0 because the stdout contract failed, not because the underlying model was judged directly.
- Historical baseline: direct Upstage API with `solar-pro2` exists, but it is not the headline result because it did not exercise Agentlas repo generation.

## Decisions

- Raw run artifacts stay outside the public repo so the repo does not accumulate unreviewed model outputs by default.
- Provider API keys are environment-only and must never be committed.
- Scores use a 100-point rubric, production-grade red-flag ceilings, and a reviewed aggregate for narrow phrase-match false positives.
- Failed LLM runs stay 0 even if Agentlas deterministic fallback creates a draft.
- API, CLI, custom CLI, and agent harness results must be labeled separately.
- Token and cost comparisons are proxy estimates only: observed CLI character-count usage divided by 4, then multiplied by public API list prices.
- The 10 benchmark prompts are now also packaged as public marketplace-grade agent-team use cases.

## Open Questions

- Should raw model outputs be published after review, or should the public repo keep only score tables and analysis?
- Should `solar-pro3` be added as a separate modern Upstage comparison after the `solar-pro2` baseline?
- Should exact provider-native token accounting be collected in a future run instead of the chars/4 proxy?
