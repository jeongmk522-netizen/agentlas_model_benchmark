# Agent Hierarchy

The benchmark uses a visible role hierarchy so public readers can inspect how runs, scoring, and publication are governed.

```text
00-benchmark-chair
  10-runtime-runner
  20-rubric-evaluator
  30-safety-auditor
  40-report-curator
```

No role both generates raw outputs and certifies final publication quality.
