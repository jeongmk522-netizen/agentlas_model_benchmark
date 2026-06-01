# Claude Guide: Agentlas Model Benchmark

This is a public Agentlas output repo for model/runtime benchmark research.

## Mission

Help run and publish a reproducible benchmark for meta-agent OS generation. The benchmark asks whether a runtime can design installable systems with dynamic tool discovery, memory policy, hook lifecycle, state machines, governance, evals, and operational controls.

## Rules

- Keep output public-safe.
- Do not include provider keys, local-only researcher notes, private paths, or raw private user data.
- Use environment variables for provider keys and never store them in files.
- Keep raw model outputs in `/tmp/test_agent/model_runs/` unless they have been reviewed for publication.
- Label runtime effects clearly: API, CLI, and agent harness results are not interchangeable.
- Run `scripts/public_safety_check.sh` before publishing.

## Preferred Workflow

1. Update `benchmark/prompts.json` and `benchmark/rubric.json` first.
2. Run one runtime at a time with `scripts/run_benchmark.py`.
3. Generate a draft score table with `scripts/score_runs.py`.
4. Review red flags and adjust final scores with evidence.
5. Update `docs/upstage-solar-pro2-baseline.md` or the relevant runtime report.
