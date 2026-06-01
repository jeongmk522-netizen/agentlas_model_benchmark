# Methodology

Date: 2026-06-01
Claim type: observed benchmark design

## Goal

This benchmark evaluates whether a model/runtime can design an installable meta-agent operating system. The target output is not an org chart. A strong answer must include dynamic tool discovery, context engineering, permissioned routing, hook lifecycle, state machines, tests, red-team probes, observability, and cost controls.

## Runtime Separation

The benchmark treats each runtime as part of the result:

| Runtime type | Example | Interpretation rule |
|--------------|---------|---------------------|
| Direct API | Upstage API + `solar-pro2` | Measures model response with minimal harness effects. |
| CLI runtime | Claude Code, Codex CLI, Gemini CLI | Measures model plus CLI system behavior. |
| Agent harness | Antigravity CLI or other agent shell | Measures model plus workflow scaffolding. |

Do not merge these categories without labeling the difference.

## Prompt Contract

Every prompt is built as:

```text
COMMON_PREFIX

<domain prompt>
```

The common prefix forbids local file inspection, asks the model to make assumptions without follow-up questions, and requires a self-contained Markdown package spec.

## Output Contract

Raw runs are written outside the repo by default:

```text
/tmp/test_agent/model_runs/<runtime>_<model>_<prompt_id>.md
/tmp/test_agent/model_runs/<runtime>_<model>_<prompt_id>.log
/tmp/test_agent/model_runs/<runtime>_<model>_<prompt_id>.usage.json
/tmp/test_agent/model_runs/<runtime>_<model>_<prompt_id>.error.txt
```

The public repo stores only reviewed score tables and reports unless raw outputs are intentionally curated.

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

Final verdicts are capped at `Not production-grade` if any required red flag appears, even when the numeric score is high.

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

## Public Safety

Provider keys must be supplied through environment variables. The safety check blocks common secrets, private local paths, and Upstage token patterns.
