# Benchmark Harness Skill

## Use When

You need to run the shared prompt catalog against an API or CLI runtime.

## Steps

1. Confirm the runtime and model label.
2. Load `benchmark/prompts.json`.
3. Build each prompt as `COMMON_PREFIX + domain prompt`.
4. Save artifacts under `/tmp/test_agent/model_runs/`.
5. Record usage metadata when available.
6. Do not store API keys in files or logs.

## Done

Every selected prompt has markdown output, log metadata, usage JSON or unavailable marker, and error details if failed.
