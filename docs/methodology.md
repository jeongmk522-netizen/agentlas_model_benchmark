# Methodology

Date: 2026-06-02
Claim type: observed benchmark execution

## Goal

This benchmark evaluates whether a model/runtime can produce an installable Agentlas agent-team operating system for complex public workflows. The target output is not an org chart or raw Markdown answer. A strong run must generate an Agentlas draft, export a repo, pass readiness checks, and include tool discovery, evidence memory, permissioned routing, state machines, tests, adversarial probes, observability, and cost controls.

## Runtime Separation

The final comparison treats each runtime as part of the Agentlas provider path:

| Runtime type | Example | Interpretation rule |
|--------------|---------|---------------------|
| Native CLI preset | Codex CLI, Gemini CLI, Claude Code | Measures whether the runtime can satisfy Agentlas' stdin/stdout JSON contract. |
| Custom CLI provider | Upstage `solar-pro2` wrapper | Measures a non-native provider through `AGENTLAS_LLM_CLI_COMMAND`. |
| Headless agent shell | Antigravity CLI wrapper | Measures whether an IDE-like agent shell can return stdout for Agentlas consumption. |

The earlier direct Upstage API run is historical baseline only. It should not be merged with the final Agentlas export-path results.

## Timeout Contract

The current headline result uses a 900,000ms per-case timeout for public Agentlas exports. Shorter 60-180s runs are preserved only as historical harness diagnostics because they incorrectly classified slower providers as model-quality failures. In the current interpretation, deterministic fallbacks score 0, but a provider is not judged on quality until it has enough time to return an LLM-generated draft.

## Prompt Contract

Every prompt is built as:

```text
COMMON_PREFIX

<domain prompt>
```

The common prefix forbids local file inspection, asks the model to make assumptions without follow-up questions, and requires a self-contained package spec. The Agentlas runner respects this by calling the answer-aware team draft path with an empty question set.

## Output Contract

Raw Agentlas runs are written outside the repo by default:

```text
<raw-run-dir>/<runtime>_<model>_direct-draft/Pxx/
  prompt.md
  draft.json
  export_paths.json
  readiness.json
  result.json
  repo/
```

The public repo stores score tables and reports. Raw generated repos stay outside the repo unless deliberately curated.

## Scoring

The current long-timeout aggregate uses an 8-axis, 100-point scenario rubric:

| Dimension | Points |
|-----------|--------|
| Request fit and domain depth | 15 |
| Agentlas team structure | 15 |
| Dynamic tools and credential setup | 15 |
| Memory and context handling | 12 |
| Workflow handoffs | 12 |
| Runnable installability | 10 |
| Governance and safety | 10 |
| Observability and cost control | 11 |

Final raw verdicts are capped at `Not production-grade` if any required red flag appears, even when the numeric score is high. Failed LLM runs stay 0 even if Agentlas deterministic fallback creates a draft.

Older raw Agentlas summary files used a 10-item readiness scorer. The current published aggregate is `data/evaluations/agentlas_meta_long_timeout_summary.*` and the `agentlas_meta_reviewed_*` alias files. Non-public cases are excluded from these public aggregate files.

## Token and Cost Method

The CLI provider path does not expose exact billable provider tokens for every runtime. Agentlas currently records observed prompt/response character counts for these runs. Public cost tables therefore use:

```text
estimated_tokens = observed_character_units / 4
estimated_cost = estimated_input_tokens * input_price + estimated_output_tokens * output_price
```

Prices are public API list prices as of 2026-06-02. These estimates are useful for relative comparison, not billing reconciliation.

## Metadata

Each run should record:

- runtime
- model label
- prompt id
- start time
- end time
- wall time seconds
- input tokens if available
- output tokens if available
- total tokens if available
- cost USD if available
- cost type: exact, range estimate, proxy estimate, or unavailable
- failure reason if failed
- notes on runtime differences
- whether the draft was `generatedBy=llm` or deterministic fallback

## Public Safety

Provider keys must be supplied through environment variables. The safety check blocks common secrets, private local paths, and Upstage token patterns.
