# Agentlas Model Benchmark Memory

This file is public memory for the benchmark agent. Keep it safe to publish.

## Stable Context

- Repo: `agent_agentlas_model_benchmark`
- Agent name: Agentlas Model Benchmark
- Benchmark target: compare model/runtime ability to design installable meta-agent operating systems.
- Primary baseline: Upstage API with `solar-pro2`, because the initial benchmark seed requested Upstage/Solar.

## Decisions

- Raw run artifacts use `/tmp/test_agent/model_runs/` so the public repo does not accumulate unreviewed model outputs by default.
- Provider API keys are environment-only and must never be committed.
- Scores use a 100-point rubric plus production-grade red-flag ceilings.
- API, CLI, and agent harness results must be labeled separately.

## Open Questions

- Which CLI runtimes are available and authenticated on the operator machine?
- Should raw model outputs be published after review, or should the public repo keep only score tables and analysis?
- Should `solar-pro3` be added as a separate modern Upstage comparison after the `solar-pro2` baseline?
