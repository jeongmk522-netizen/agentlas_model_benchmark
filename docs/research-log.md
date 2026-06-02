# Research Log

Use this file for public-safe dated notes.

## 2026-06-01: Benchmark Seed

Claim type: observed

### Claim

The benchmark should compare model/runtime ability to produce an installable agent-team OS, not just a conceptual role list.

### Evidence

The seed prompt requires dynamic tool discovery, tool scoring, permission gates, workflow automation, memory/context handling, workflow state machines, smoke tests, red-team tests, observability, cost controls, and human approval gates. The public prompt catalog excludes non-public cases.

### Interpretation

The benchmark is useful only if it preserves the same prompt contract across runtimes and separates direct API output from CLI or agent-harness behavior.

### Next Experiment

Run `Upstage API + solar-pro2` across the public prompt set, collect usage metadata, and produce the first score table.

## 2026-06-02: Agentlas Agent-Team Sweep

Claim type: observed

### Claim

The final comparison must use the Agentlas agent-team repo-generation path, not direct model answers.

### Evidence

The runner calls the Agentlas answer-aware team draft path with an empty question set, then exports the generated draft repo and scores the extracted artifacts. The initial short-timeout sweep was later superseded by a 900s per-case run; the short run incorrectly classified slower providers as quality failures.

### Interpretation

Under the long-timeout public aggregate, Claude, Codex, and Gemini 3.1 tied at 96.0, while Solar Pro 2 reached 95.9 with the best speed/cost proxy. Antigravity remained a stdout-contract failure.

### Scorer Review

The raw scorer over-triggered several phrase-style red flags. The reviewed aggregate corrects only those false positives when score evidence already shows the required workflow/gate/domain signals. Deterministic fallback cases remain failures.
