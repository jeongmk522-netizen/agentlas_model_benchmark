# Methodology

Date: 2026-06-02
Claim type: observed benchmark execution

## Goal

This benchmark evaluates whether a model/runtime can drive the Agentlas meta-agent pipeline to produce an installable meta-agent operating system. The target output is not an org chart or raw Markdown answer. A strong run must generate an Agentlas draft, export a repo, pass readiness checks, and include dynamic tool discovery, context engineering, permissioned routing, state machines, tests, red-team probes, observability, and cost controls.

## Runtime Separation

The final comparison treats each runtime as part of the Agentlas provider path:

| Runtime type | Example | Interpretation rule |
|--------------|---------|---------------------|
| Native CLI preset | Codex CLI, Gemini CLI, Claude Code | Measures whether the runtime can satisfy Agentlas' stdin/stdout JSON contract. |
| Custom CLI provider | Upstage `solar-pro2` wrapper | Measures a non-native provider through `AGENTLAS_LLM_CLI_COMMAND`. |
| Headless agent shell | Antigravity CLI wrapper | Measures whether an IDE-like agent shell can return stdout for Agentlas consumption. |

The earlier direct Upstage API run is historical baseline only. It should not be merged with the final Agentlas meta-agent results.

## Prompt Contract

Every prompt is built as:

```text
COMMON_PREFIX

<domain prompt>
```

The common prefix forbids local file inspection, asks the model to make assumptions without follow-up questions, and requires a self-contained package spec. The Agentlas runner respects this by calling the answer-aware team draft path with an empty question set.

## Output Contract

Raw Agentlas meta-agent runs are written outside the repo by default:

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

The rubric totals 100 points:

| Dimension | Points |
|-----------|--------|
| Mission topology and ownership | 10 |
| Dynamic tool discovery and routing | 12 |
| Hook lifecycle and automation architecture | 8 |
| Context engineering and memory | 14 |
| Workflow state machine and handoffs | 12 |
| Domain-specific depth | 10 |
| Governance, safety, and human approval | 12 |
| Evaluation, smoke tests, and red-team tests | 10 |
| Observability, cost, and operational controls | 8 |
| Installability and artifact quality | 4 |

Final raw verdicts are capped at `Not production-grade` if any required red flag appears, even when the numeric score is high. The reviewed aggregate may correct narrow phrase-based false positives when score evidence already proves the required workflow/gate/domain signal exists. Failed LLM runs stay 0 even if Agentlas deterministic fallback creates a draft.

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
