<p align="center">
  <img src="assets/agentlas-agent-lab-banner.svg" alt="Agentlas Agent Lab banner">
</p>

<h1 align="center">Agentlas Agent Lab</h1>

<p align="center">
  <a href="https://agentlas.cloud">agentlas.cloud</a>
</p>

<p align="center">
  <a href="https://github.com/jeongmk522-netizen/Agentlas_public_repo">Lab Hub</a>
  ·
  <a href="https://github.com/jeongmk522-netizen/agentlas_model_benchmark">agentlas_model_benchmark</a>
</p>

# Agentlas Model Benchmark

> A reproducible benchmark for comparing how model runtimes design installable agent-team operating systems.

## Research Question

Which model/runtime can produce an operational agent-team OS instead of a role list or conceptual org chart?

This benchmark gives each runtime the same public prompt contract and domain prompts. The public aggregate excludes one non-public case; the marketplace pack replaces it with a public-safe procurement workflow. Outputs are scored on tool routing, evidence memory, workflow states, governance, tests, observability, and installable artifact quality.

## Main Result

The current headline run uses the Agentlas public agent-team export path: draft JSON, generated repo export, ZIP sandbox extraction, readiness checks, and reviewed score aggregation. After increasing the per-case timeout to 900s, Claude, Codex, Gemini 3.1, and Solar2 completed every public case. The earlier “Claude/GPT failed” result was a harness-timeout artifact.

| Runtime | Model | Cases | LLM draft success | Reviewed avg | Avg time | Estimated public-suite API cost* | Interpretation |
|---------|-------|------:|------------------:|-------------:|---------:|----------------------------:|----------------|
| Codex CLI | `gpt-5.5` | 9 | 9 | 96.0 | 67.40s | $0.9718 | Top quality, slower and more expensive than Gemini/Solar. |
| Claude Code | `claude-sonnet-4-6` | 9 | 9 | 96.0 | 353.50s | $1.3289 | Top quality, slowest in this harness. |
| Gemini CLI | `gemini-3.1-pro-preview` | 9 | 9 | 96.0 | 41.41s | $0.2040 | Top quality with much better speed/cost. |
| Upstage custom CLI | `solar-pro2` | 9 | 9 | 95.9 | 9.79s | $0.0099 | Essentially tied on quality; fastest and cheapest by the proxy estimate. |
| Gemini CLI | `gemini-3-flash-preview` | 9 | 9 | 94.1 | 65.78s | $0.0950 | Slightly lower quality in this rubric, still stable. |
| Antigravity CLI | `default` | 9 | 0 | 0.0 | 1.43s | n/a | Headless stdout contract failed; not model-quality evidence. |

*CLI runs did not produce exact billable API tokens. Cost is a proxy: observed CLI character-count usage divided by 4, multiplied by public API list prices.

![Quality vs time, zoomed y-axis](assets/agentlas_meta_score_time_zoom.png)

![Score vs estimated API cost, zoomed y-axis](assets/agentlas_meta_score_cost_zoom.png)

![Estimated tokens, cost, and score](assets/agentlas_meta_tokens_cost_score.png)

## Agent Contract

- Purpose: run fair agent-team OS design prompts across runtimes, collect outputs, score with one rubric, and publish public-safe analysis.
- Inputs: prompt catalog, runtime adapter, model label, rubric, raw run artifacts, usage metadata.
- Outputs: model run files, usage JSON, error logs, rubric scores, comparative research report.
- Tools: dynamic runtime adapters for API and CLI runners, scoring scripts, public safety checks.
- Memory: public benchmark decisions live in `memory.md`; raw keys, local paths, and private logs stay out of the repo.
- Permissions: never store provider API keys in files; high-cost or destructive runtime runs require operator approval.
- Evaluation: 100-point rubric with production-grade red flags and per-domain checks.
- Known failure modes: fixed tool lists, missing memory architecture, no human approval gates, org-chart-only output, scorer bias, runtime-specific hidden scaffolding.

## Benchmark Shape

```text
COMMON_PREFIX
  P01 investment fund agent
  P02 AML and fraud investigation agent
  P03 disaster drone swarm agent
  P04 film studio agent
  P05 marketing agency agent
  P06 enterprise software HQ agent
  P07 hospital operations agent
  P08 supply-chain control tower agent
  P09 SOC threat response agent
  S10 vendor risk and procurement desk (public marketplace replacement; not part of scored aggregate)
```

Raw Agentlas runs are saved outside the public repo with this contract:

```text
<raw-run-dir>/<runtime>_<model>_direct-draft/Pxx/
  prompt.md
  draft.json
  export_paths.json
  readiness.json
  result.json
  repo/
```

## Quick Start

```bash
cd <agentlas-app>/app

# Produce the reviewed public aggregate table, token/cost table, and charts
# from the reviewed operator source CSV.
cd <benchmark-repo>
python3 scripts/compile_long_timeout_report.py

# Export public-safe Agentlas team marketplace specs.
python3 scripts/export_team_use_cases.py
```

Provider keys and private execution runners stay outside this repository. Do not place provider keys or proprietary generation scripts in public outputs.

## Research Outputs

- [docs/methodology.md](docs/methodology.md): benchmark design, metadata, and scoring method.
- [docs/paper.md](docs/paper.md): paper-style report and interpretation.
- [docs/marketplace-use-cases.md](docs/marketplace-use-cases.md): public-safe team marketplace use cases; one non-public case is replaced by an unscored procurement workflow.
- [docs/upstage-solar-pro2-baseline.md](docs/upstage-solar-pro2-baseline.md): first Upstage/Solar baseline report.
- [benchmark/prompts.json](benchmark/prompts.json): common prefix, 10 prompts, and red flags.
- [benchmark/rubric.json](benchmark/rubric.json): 100-point rubric.
- [data/evaluations/](data/evaluations/): public score tables and summaries.
- [marketplace/agent-teams/](marketplace/agent-teams/): public-safe JSON team specs for the Agentlas web marketplace.

## Repository Map

- [agent.md](agent.md): benchmark chair contract.
- [agents/](agents/): visible role hierarchy for running and reviewing the benchmark.
- [skills/](skills/): reusable benchmark skills.
- [scripts/upstage_agentlas_cli.py](scripts/upstage_agentlas_cli.py): Upstage custom CLI provider wrapper for Agentlas.
- [scripts/antigravity_agentlas_cli.py](scripts/antigravity_agentlas_cli.py): Antigravity wrapper used to record stdout-contract failures.
- [scripts/compile_long_timeout_report.py](scripts/compile_long_timeout_report.py): current aggregate, token/cost CSVs, and charts.
- [scripts/export_team_use_cases.py](scripts/export_team_use_cases.py): exports public-safe Agentlas team marketplace specs.
- [scripts/run_benchmark.py](scripts/run_benchmark.py): public-safe API/CLI runner scaffold.
- [scripts/score_runs.py](scripts/score_runs.py): rubric-aligned evidence extractor and draft scorer.
- [CLAUDE.md](CLAUDE.md): Claude Code guide.
- [AGENTS.md](AGENTS.md): Codex operating rules.
- [memory.md](memory.md): public benchmark memory.
