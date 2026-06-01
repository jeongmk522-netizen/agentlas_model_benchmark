# Research Log

Use this file for public-safe dated notes.

## 2026-06-01: Benchmark Seed

Claim type: observed

### Claim

The benchmark should compare model/runtime ability to produce an installable meta-agent OS, not just a conceptual role list.

### Evidence

The seed prompt requires dynamic tool discovery, tool scoring, permission gates, hook lifecycle, context engineering, workflow state machines, smoke tests, red-team tests, observability, cost controls, and human approval gates. It also defines 10 domain prompts and a 100-point rubric.

### Interpretation

The benchmark is useful only if it preserves the same prompt contract across runtimes and separates direct API output from CLI or agent-harness behavior.

### Next Experiment

Run `Upstage API + solar-pro2` across P01-P10, collect usage metadata, and produce the first score table.
