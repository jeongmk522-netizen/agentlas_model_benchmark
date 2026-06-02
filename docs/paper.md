# Agentlas Model Benchmark

Date: 2026-06-02

## Abstract

This report evaluates whether model runtimes can drive the Agentlas meta-agent pipeline to produce installable meta-agent operating-system repositories. The benchmark uses 10 fixed domain prompts, including investment research, AML investigation, disaster-response drones, film production, marketing, enterprise software delivery, hospital operations, supply chain, SOC response, and a universal meta-agent factory. Each runtime is judged on whether it can return an LLM-generated Agentlas draft, export a runnable repo structure, pass readiness checks, and satisfy a 100-point rubric for dynamic tool discovery, context engineering, workflow governance, evals, observability, and domain safety.

The strongest observed providers were Upstage `solar-pro2` through a custom Agentlas CLI wrapper and Gemini CLI `gemini-3-flash-preview`. Both completed all 10 prompts with a reviewed average of 90/100. Codex CLI `gpt-5.5` produced strong drafts when it completed, but timed out or fell back on 3 of 10 cases. Claude Code `claude-sonnet-4-6` timed out on every case under the benchmark contract. The local Antigravity CLI returned no stdout and therefore could not be consumed by Agentlas.

## Research Question

Can a model runtime produce an operational meta-agent OS through the Agentlas meta-agent pipeline, rather than a conceptual org chart or raw Markdown plan?

## Method

The benchmark ran the same prompt catalog against each runtime. Every case used the Agentlas meta-agent path:

```text
fixed prompt
  -> Agentlas compact meta-agent synthesis
  -> AgentDraft JSON
  -> buildDraftRepo
  -> ZIP encode/extract sandbox
  -> readiness checks
  -> raw automated score
  -> reviewed aggregate score
```

The runner uses `generateTeamDraftWithAnswers(prompt, [], {})` so the benchmark respects the prompt instruction not to ask follow-up questions while still exercising the Agentlas answer-aware compact synthesis path. Upstage is not a native Agentlas provider, so it is wrapped as `AGENTLAS_LLM_CLI_COMMAND`; the wrapper reads stdin, calls Upstage, and prints a JSON object with a `text` field for Agentlas to unwrap. Antigravity is also wrapped, but the local CLI did not return stdout.

## Results

| Runtime | Model | Cases | LLM draft success | Failures | Reviewed avg | Avg wall time |
|---------|-------|------:|------------------:|---------:|-------------:|--------------:|
| Upstage custom CLI | `solar-pro2` | 10 | 10 | 0 | 90.0 | 9.29s |
| Gemini CLI | `gemini-3-flash-preview` | 10 | 10 | 0 | 90.0 | 63.96s |
| Codex CLI | `gpt-5.5` | 10 | 7 | 3 | 63.0 | 85.93s |
| Claude Code | `claude-sonnet-4-6` | 10 | 0 | 10 | 0.0 | 60.61s |
| Antigravity CLI | `default` | 10 | 0 | 10 | 0.0 | 1.49s |

Prompt-level reviewed scores for successful LLM-generated runs averaged 90/100 across P01-P10. The common remaining 10-point gap was explicit dynamic tool-discovery protocol detail: the Agentlas renderer emitted portable adapters and capability routing, but the generated public repo did not always spell out unknown-tool discovery and scoring as a first-class protocol.

## Runtime Findings

Upstage `solar-pro2` was the fastest successful provider. It completed all 10 cases with LLM-generated drafts and no deterministic fallback.

Gemini CLI matched Upstage on reviewed score and completion rate. It was slower but stable across all domains.

Codex CLI produced high-quality drafts on 7 cases, but failed on P05, P06, and P08 by returning deterministic fallback after the Agentlas LLM call failed or timed out. Its quality ceiling looked competitive, but its completion reliability was weaker in this run.

Claude Code failed operationally under this Agentlas CLI-provider contract. A P01 probe timed out at both 300s and 180s, and the full sweep used a 60s per-case failure contract to record all 10 cases as deterministic fallback failures.

Antigravity failed the headless stdout contract. The local CLI appeared to hand off to an IDE surface rather than returning model text to stdout, so Agentlas could not consume it as an LLM provider.

## Review Notes

The raw automated scorer initially over-triggered phrase-style red flags such as "creative role list without workflow" when the generated repo already contained workflow, approval, versioning, or domain-safety signals. The reviewed table applies one narrow correction: those phrase-style red flags are removed only when the score evidence already shows the required workflow/gate/domain signals. Failed LLM runs remain 0 even when Agentlas deterministic fallback created a usable local draft.

## Limitations

This is a single-machine, single-date operational benchmark. CLI authentication state, local runtime versions, and provider rate limits may change results. The score is about Agentlas meta-agent repo generation, not general chat quality. The direct Upstage API baseline is retained separately because it did not exercise the Agentlas meta-agent pipeline.

## Artifacts

- Reviewed aggregate: `data/evaluations/agentlas_meta_reviewed_scores.csv`
- Reviewed summary: `data/evaluations/agentlas_meta_reviewed_summary.json`
- Raw automated summaries: `data/evaluations/agentlas_meta_*_summary.json`
- Runner: `scripts/agentlas_meta_benchmark.ts`
- Upstage wrapper: `scripts/upstage_agentlas_cli.py`
- Antigravity wrapper: `scripts/antigravity_agentlas_cli.py`
