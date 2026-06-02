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

> A reproducible benchmark for comparing how model runtimes design installable meta-agent operating systems.

## Research Question

Which model/runtime can produce an operational meta-agent OS instead of a role list or conceptual org chart?

This benchmark gives each runtime the same common prefix and 10 domain prompts. The output is scored on dynamic tool discovery, context engineering, workflow state machines, governance, tests, observability, and installable artifact quality.

## Main Result

The final run uses the real Agentlas meta-agent pipeline from the Agentlas app: compact meta-agent synthesis, Agentlas draft JSON, generated repo export, ZIP sandbox extraction, readiness checks, and reviewed score aggregation.

| Runtime | Model | Cases | LLM draft success | Failures | Reviewed avg | Interpretation |
|---------|-------|------:|------------------:|---------:|-------------:|----------------|
| Upstage custom CLI | `solar-pro2` | 10 | 10 | 0 | 90.0 | Fastest successful Agentlas provider in this run. |
| Gemini CLI | `gemini-3-flash-preview` | 10 | 10 | 0 | 90.0 | Same reviewed quality as Upstage, slower wall time. |
| Codex CLI | `gpt-5.5` | 10 | 7 | 3 | 63.0 | Strong when it completed; unstable under the 180s per-case contract. |
| Claude Code | `claude-sonnet-4-6` | 10 | 0 | 10 | 0.0 | Timed out in the Agentlas CLI provider path. |
| Antigravity CLI | `default` | 10 | 0 | 10 | 0.0 | Local headless CLI returned no stdout, so Agentlas could not consume it. |

The earlier direct Upstage API baseline is retained as historical context, but it is not the headline comparison because it did not exercise the Agentlas meta-agent repo-generation path.

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

Agentlas meta-agent runs are saved outside the public repo with this contract:

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

# Upstage via Agentlas custom CLI provider.
export UPSTAGE_API_KEY="..."
npx tsx <benchmark-repo>/scripts/agentlas_meta_benchmark.ts \
  --runtime upstage \
  --model solar-pro2 \
  --all \
  --out-dir <raw-run-dir> \
  --public-out-dir <benchmark-repo>/data/evaluations

# Produce the reviewed aggregate table from raw automated summaries.
cd <benchmark-repo>
python3 scripts/review_agentlas_meta_scores.py
```

The runner only reads the key from the environment. Do not place provider keys in this repository.

## Research Outputs

- [docs/methodology.md](docs/methodology.md): benchmark design, metadata, and scoring method.
- [docs/paper.md](docs/paper.md): paper-style report and interpretation.
- [docs/upstage-solar-pro2-baseline.md](docs/upstage-solar-pro2-baseline.md): first Upstage/Solar baseline report.
- [benchmark/prompts.json](benchmark/prompts.json): common prefix, 10 prompts, and red flags.
- [benchmark/rubric.json](benchmark/rubric.json): 100-point rubric.
- [data/evaluations/](data/evaluations/): public score tables and summaries.

## Repository Map

- [agent.md](agent.md): benchmark chair contract.
- [agents/](agents/): visible role hierarchy for running and reviewing the benchmark.
- [skills/](skills/): reusable benchmark skills.
- [scripts/agentlas_meta_benchmark.ts](scripts/agentlas_meta_benchmark.ts): Agentlas meta-agent runner.
- [scripts/upstage_agentlas_cli.py](scripts/upstage_agentlas_cli.py): Upstage custom CLI provider wrapper for Agentlas.
- [scripts/antigravity_agentlas_cli.py](scripts/antigravity_agentlas_cli.py): Antigravity wrapper used to record stdout-contract failures.
- [scripts/review_agentlas_meta_scores.py](scripts/review_agentlas_meta_scores.py): reviewed aggregate score builder.
- [scripts/run_benchmark.py](scripts/run_benchmark.py): public-safe API/CLI runner scaffold.
- [scripts/score_runs.py](scripts/score_runs.py): rubric-aligned evidence extractor and draft scorer.
- [CLAUDE.md](CLAUDE.md): Claude Code guide.
- [AGENTS.md](AGENTS.md): Codex operating rules.
- [memory.md](memory.md): public benchmark memory.
