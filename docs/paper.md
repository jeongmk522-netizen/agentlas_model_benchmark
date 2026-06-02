# Agentlas Model Benchmark

Date: 2026-06-02

## Abstract

This report evaluates model runtimes on their ability to produce installable Agentlas agent-team packages for complex public workflows. The current public aggregate uses nine scored cases: investment research, AML/fraud investigation, disaster-response drones, film production, marketing, enterprise software delivery, hospital operations, supply-chain control, and SOC response.

The long-timeout result changes the interpretation of the benchmark. Earlier short-timeout runs made Claude and GPT appear weak, but the 900-second per-case run shows that the earlier result was a harness artifact. Claude Sonnet 4.6, GPT-5.5, and Gemini 3.1 Pro each average 96.0/100. Solar Pro 2 averages 95.9/100 while being much faster and cheaper by the proxy estimate.

## Research Question

Can a model runtime produce an operational Agentlas agent-team package for complex workflows, rather than a conceptual org chart or raw plan?

## Public Dataset

The published aggregate is based on:

- 9 public workflow cases.
- 6 runtime/model entries.
- 54 prompt-level rows before excluding failed/non-LLM cases from quality charts.
- 100-point reviewed rubric.
- 900,000 ms per-case timeout.

One non-public case is excluded from the scored public aggregate. The marketplace use-case pack includes a public-safe procurement workflow replacement for that slot.

## Method

Each runtime was evaluated against the same public prompt contract. The required output is an installable agent-team package with structured roles, tool and credential setup, memory/context handling, workflow handoffs, approval gates, tests, observability, and cost controls.

The benchmark is not a general chat benchmark. It measures operational package generation under the Agentlas export path.

Scoring dimensions:

| Dimension | Points |
|---|---:|
| Request fit and domain depth | 15 |
| Agentlas team structure | 15 |
| Dynamic tools and credential setup | 15 |
| Memory and context handling | 12 |
| Workflow hooks and handoffs | 12 |
| Runnable installability | 10 |
| Governance and safety | 10 |
| Observability and cost control | 11 |

Failed LLM runs remain 0. A runtime that fails the stdout/consumption contract is treated as a runtime failure, not as direct evidence about the underlying model.

## Results

| Runtime | Model | Cases | LLM success | Avg score | Avg wall time | Est. tokens | Est. suite cost* |
|---|---|---:|---:|---:|---:|---:|---:|
| Claude Code | `claude-sonnet-4-6` | 9 | 9 | 96.0 | 353.50s | 92,099 | $1.3289 |
| Codex CLI | `gpt-5.5` | 9 | 9 | 96.0 | 67.40s | 42,142 | $0.9718 |
| Gemini CLI | `gemini-3.1-pro-preview` | 9 | 9 | 96.0 | 41.41s | 26,753 | $0.2040 |
| Upstage CLI | `solar-pro2` | 9 | 9 | 95.9 | 9.79s | 25,212 | $0.0099 |
| Gemini CLI | `gemini-3-flash-preview` | 9 | 9 | 94.1 | 65.78s | 41,424 | $0.0950 |
| Antigravity CLI | `default` | 9 | 0 | 0.0 | 1.43s | 0 | n/a |

*Cost is a proxy estimate, not an invoice. The public table uses observed character-count usage divided by 4, then applies public API list prices.

## Figure Interpretation

### Quality vs Time

`assets/agentlas_meta_score_time_zoom.png`

Solar Pro 2 is the speed outlier. It remains within 0.1 points of the 96.0 quality leaders while averaging under 10 seconds per case.

### Quality vs Estimated Cost

`assets/agentlas_meta_score_cost_zoom.png`

The quality leaders do not have similar cost profiles. Claude and GPT-5.5 match the highest score, but cost much more under the proxy estimate. Gemini 3.1 Pro is a stronger cost/quality compromise. Solar Pro 2 dominates on estimated cost.

### Tokens, Cost, and Score

`assets/agentlas_meta_tokens_cost_score.png`

Token footprint separates the top-quality models. Gemini 3.1 Pro reaches 96.0 with a much smaller estimated token footprint than Claude and GPT-5.5. Solar Pro 2 has the lowest estimated token footprint among successful high-quality runs.

## Findings

1. **Timeout correction**: The previous weak Claude/GPT conclusion is not supported by the long-timeout run.
2. **Quality cluster**: Claude Sonnet 4.6, GPT-5.5, and Gemini 3.1 Pro tie at 96.0; Solar Pro 2 is effectively tied at 95.9.
3. **Efficiency split**: Solar Pro 2 is the clear speed/cost outlier. Gemini 3.1 Pro is the strongest balance among the 96.0 models.
4. **Flash tradeoff**: Gemini 3 Flash completed all public cases, but its average score is lower at 94.1.
5. **Runtime-contract failure**: Antigravity did not return consumable output in this setup. It is excluded from quality interpretation.

## Limitations

- Single-machine, single-date benchmark.
- CLI authentication state, rate limits, and runtime versions can affect results.
- Token and cost data are proxy estimates, not exact invoices.
- The benchmark measures Agentlas package-generation performance, not general reasoning or chat quality.
- One non-public case is excluded from the public aggregate.

## Artifacts

- Reviewed summary: `data/evaluations/agentlas_meta_long_timeout_summary.csv`
- Prompt-level scores: `data/evaluations/agentlas_meta_long_timeout_scores.csv`
- Token/cost table: `data/evaluations/agentlas_meta_token_cost_score.csv`
- Figures: `assets/agentlas_meta_score_time_zoom.png`, `assets/agentlas_meta_score_cost_zoom.png`, `assets/agentlas_meta_tokens_cost_score.png`
- Methodology: `docs/methodology.md`
- Marketplace public workflows: `docs/marketplace-use-cases.md`
