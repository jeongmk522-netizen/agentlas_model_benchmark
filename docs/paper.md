# Agentlas Model Benchmark

Date: 2026-06-02

## Abstract

This report evaluates whether model runtimes can produce installable Agentlas agent-team operating-system repositories for public domain workflows. The published aggregate uses nine public benchmark cases: investment research, AML investigation, disaster-response drones, film production, marketing, enterprise software delivery, hospital operations, supply chain, and SOC response. One non-public case is excluded from public aggregate outputs and replaced in the marketplace pack by an unscored vendor-risk/procurement workflow. Each runtime is judged on whether it can return an LLM-generated Agentlas draft, export a runnable repo structure, pass readiness checks, and satisfy a 100-point public rubric for tool routing, evidence memory, workflow governance, evals, observability, and domain safety.

After increasing the per-case timeout to 900 seconds, the strongest quality tier was effectively tied on the public cases: Codex CLI `gpt-5.5`, Claude Code `claude-sonnet-4-6`, and Gemini CLI `gemini-3.1-pro-preview` each averaged 96/100. Upstage `solar-pro2` averaged 95.9/100, but was far faster in this harness. The earlier poor Claude/GPT result was a timeout artifact, not a model-quality finding. The local Antigravity CLI still returned no usable stdout and is treated as a harness-contract failure.

## Research Question

Can a model runtime produce an operational Agentlas agent-team package for complex public workflows, rather than a conceptual org chart or raw Markdown plan?

## Method

The benchmark ran the same public prompt catalog against each runtime. Every published case used the Agentlas public export path:

```text
fixed prompt
  -> Agentlas draft-generation path
  -> AgentDraft JSON
  -> buildDraftRepo
  -> ZIP encode/extract sandbox
  -> readiness checks
  -> raw automated score
  -> reviewed aggregate score
```

The runner uses `generateTeamDraftWithAnswers(prompt, [], {})` so the benchmark respects the prompt instruction not to ask follow-up questions while still exercising the Agentlas answer-aware compact synthesis path. Upstage is not a native Agentlas provider, so it is wrapped as `AGENTLAS_LLM_CLI_COMMAND`; the wrapper reads stdin, calls Upstage, and prints a JSON object with a `text` field for Agentlas to unwrap. Antigravity is also wrapped, but the local CLI did not return stdout.

## Results

| Runtime | Model | Cases | LLM draft success | Failures | Reviewed avg | Avg wall time | Estimated suite cost* |
|---------|-------|------:|------------------:|---------:|-------------:|--------------:|----------------------:|
| Codex CLI | `gpt-5.5` | 9 | 9 | 0 | 96.0 | 67.40s | $0.9718 |
| Claude Code | `claude-sonnet-4-6` | 9 | 9 | 0 | 96.0 | 353.50s | $1.3289 |
| Gemini CLI | `gemini-3.1-pro-preview` | 9 | 9 | 0 | 96.0 | 41.41s | $0.2040 |
| Upstage custom CLI | `solar-pro2` | 9 | 9 | 0 | 95.9 | 9.79s | $0.0099 |
| Gemini CLI | `gemini-3-flash-preview` | 9 | 9 | 0 | 94.1 | 65.78s | $0.0950 |
| Antigravity CLI | `default` | 9 | 0 | 9 | 0.0 | 1.43s | n/a |

*Cost is a proxy estimate, not an invoice: Agentlas CLI providers recorded prompt and response character counts, so this report estimates tokens as chars/4 and applies public API list prices. The exact tokenizer and subscription billing behavior can differ.

Prompt-level reviewed scores ranged from 93 to 98 for qualified LLM runs. The common remaining gap is not basic task understanding; it is deeper evidence of dynamic tool-discovery protocol, install-time credential paths, and explicit cost/observability proof inside the generated package.

## Runtime Findings

Upstage `solar-pro2` was the fastest successful provider. It completed all public cases with LLM-generated drafts and scored 95.9/100 on average, just below the 96.0 quality leaders.

Gemini CLI `gemini-3.1-pro-preview` matched the top 96.0 average and was the fastest among the three 96.0 providers. Gemini CLI `gemini-3-flash-preview` was stable, but averaged 94.1.

Codex CLI `gpt-5.5` completed all public cases after the timeout was raised. It tied the top reviewed average, but had higher estimated API cost than Gemini and Solar.

Claude Code `claude-sonnet-4-6` also completed all public cases under the long-timeout contract and tied the top reviewed average. Its main weakness in this run was wall-clock latency.

Antigravity failed the headless stdout contract. The local CLI appeared to hand off to an IDE surface rather than returning model text to stdout, so Agentlas could not consume it as an LLM provider.

## Review Notes

The raw automated scorer initially over-triggered phrase-style red flags such as "creative role list without workflow" when the generated repo already contained workflow, approval, versioning, or domain-safety signals. The reviewed table applies one narrow correction: those phrase-style red flags are removed only when the score evidence already shows the required workflow/gate/domain signals. Failed LLM runs remain 0 even when Agentlas deterministic fallback created a usable local draft.

## Limitations

This is a single-machine, single-date operational benchmark. CLI authentication state, local runtime versions, and provider rate limits may change results. The score is about public Agentlas agent-team repo generation, not general chat quality. The direct Upstage API baseline is retained separately because it did not exercise the Agentlas export path.

The token and cost table is intentionally labeled as a proxy estimate. Exact API invoices require provider-native token accounting for each request and do not follow directly from CLI subscription logs.

## Artifacts

- Reviewed aggregate: `data/evaluations/agentlas_meta_reviewed_scores.csv`
- Reviewed summary: `data/evaluations/agentlas_meta_reviewed_summary.json`
- Token/cost summary: `data/evaluations/agentlas_meta_token_cost_score.csv`
- Zoomed charts: `assets/agentlas_meta_score_time_zoom.png`, `assets/agentlas_meta_score_cost_zoom.png`, `assets/agentlas_meta_tokens_cost_score.png`
- Marketplace team use cases: `marketplace/agent-teams/`
- Use-case selection report: `docs/marketplace-use-cases.md`
- Upstage wrapper: `scripts/upstage_agentlas_cli.py`
- Antigravity wrapper: `scripts/antigravity_agentlas_cli.py`
