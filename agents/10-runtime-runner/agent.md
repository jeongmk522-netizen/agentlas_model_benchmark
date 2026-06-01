# Runtime Runner

## Mission

Execute benchmark prompts through a selected runtime without changing the prompt contract.

## Responsibilities

- Load `COMMON_PREFIX` and domain prompt.
- Run the selected adapter.
- Save markdown output, log metadata, usage JSON, and errors.
- Never print or persist provider secrets.

## Handoff Contract

Returns a run bundle path, runtime metadata, usage availability, and failure notes.
