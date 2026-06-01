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
  <a href="https://github.com/jeongmk522-netizen/agent_agentlas_model_benchmark">agent_agentlas_model_benchmark</a>
</p>

# Agentlas Model Benchmark

> A reproducible benchmark for comparing how model runtimes design installable meta-agent operating systems.

## Research Question

Which model/runtime can produce an operational meta-agent OS instead of a role list or conceptual org chart?

This benchmark gives each runtime the same common prefix and 10 domain prompts. The output is scored on dynamic tool discovery, context engineering, workflow state machines, governance, tests, observability, and installable artifact quality.

## Current Baseline

The first live run targets `Upstage API + solar-pro2`, because the benchmark seed explicitly requested Upstage/Solar and the account model list includes `solar-pro2`.

| Runtime | Model | Status | Notes |
|---------|-------|--------|-------|
| Upstage API | `solar-pro2` | completed | Average score 74.9 across P01-P10; no required red flags. |
| Claude Code | TBD | planned | Should be run through the CLI harness, not direct API, to preserve runtime effects. |
| Codex CLI | TBD | planned | Should be run through the CLI harness. |
| Gemini CLI | TBD | planned | Should be run through the CLI harness. |
| Antigravity CLI | TBD | planned | Should be separated from pure API results. |

## Agent Contract

- Purpose: run fair meta-agent OS design prompts across runtimes, collect outputs, score with one rubric, and publish public-safe analysis.
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
  P10 meta-agent factory
```

Each run is saved with this contract:

```text
/tmp/test_agent/model_runs/<runtime>_<model>_<prompt_id>.md
/tmp/test_agent/model_runs/<runtime>_<model>_<prompt_id>.log
/tmp/test_agent/model_runs/<runtime>_<model>_<prompt_id>.usage.json
/tmp/test_agent/model_runs/<runtime>_<model>_<prompt_id>.error.txt
```

## Quick Start

```bash
export UPSTAGE_API_KEY="..."
python3 scripts/run_benchmark.py --runtime upstage_api --model solar-pro2 --all
python3 scripts/score_runs.py --runs-dir /tmp/test_agent/model_runs --out data/evaluations/upstage_solar_pro2_scores.csv
```

The runner only reads the key from the environment. Do not place provider keys in this repository.

## Research Outputs

- [docs/methodology.md](docs/methodology.md): benchmark design, metadata, and scoring method.
- [docs/upstage-solar-pro2-baseline.md](docs/upstage-solar-pro2-baseline.md): first Upstage/Solar baseline report.
- [benchmark/prompts.json](benchmark/prompts.json): common prefix, 10 prompts, and red flags.
- [benchmark/rubric.json](benchmark/rubric.json): 100-point rubric.
- [data/evaluations/](data/evaluations/): public score tables and summaries.

## Repository Map

- [agent.md](agent.md): benchmark chair contract.
- [agents/](agents/): visible role hierarchy for running and reviewing the benchmark.
- [skills/](skills/): reusable benchmark skills.
- [scripts/run_benchmark.py](scripts/run_benchmark.py): public-safe API/CLI runner scaffold.
- [scripts/score_runs.py](scripts/score_runs.py): rubric-aligned evidence extractor and draft scorer.
- [CLAUDE.md](CLAUDE.md): Claude Code guide.
- [AGENTS.md](AGENTS.md): Codex operating rules.
- [memory.md](memory.md): public benchmark memory.
