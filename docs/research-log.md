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

## 2026-06-02: Agentlas Meta-Agent Sweep

Claim type: observed

### Claim

The final comparison must use the Agentlas meta-agent repo-generation path, not direct model answers.

### Evidence

The runner calls the Agentlas answer-aware team draft path with an empty question set, then exports the generated draft repo and scores the extracted artifacts. Upstage `solar-pro2` and Gemini CLI `gemini-3-flash-preview` completed all 10 prompts with reviewed averages of 90/100. Codex CLI `gpt-5.5` completed 7 of 10 and averaged 63/100 after failed cases were kept at 0. Claude Code timed out across the full sweep. Antigravity returned no stdout and could not be consumed by Agentlas.

### Interpretation

Upstage and Gemini were tied on reviewed quality, but Upstage was much faster in this run. Codex quality was competitive when it completed, but reliability was lower. Claude and Antigravity failed operationally under the Agentlas CLI-provider contract.

### Scorer Review

The raw scorer over-triggered several phrase-style red flags. The reviewed aggregate corrects only those false positives when score evidence already shows the required workflow/gate/domain signals. Deterministic fallback cases remain failures.
