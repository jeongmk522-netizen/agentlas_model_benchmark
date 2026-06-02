#!/usr/bin/env python3
"""Generate a rubric-aligned draft score table from benchmark outputs.

This scorer is intentionally conservative and transparent. It extracts textual
evidence for each rubric dimension and drafts a score, but final publication
should include human review of red flags and domain-specific nuance.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUBRIC = ROOT / "benchmark" / "rubric.json"
DEFAULT_OUT = ROOT / "data" / "evaluations" / "draft_scores.csv"


SIGNALS = {
    "mission_topology": ["owner", "ownership", "controller", "chair", "escalation", "fallback owner", "approval authority"],
    "dynamic_tool_discovery": ["tool registry", "discover", "capability", "score", "routing", "permission", "fallback", "provenance"],
    "workflow_automation": ["preflight", "post-run", "trigger", "idempot", "rollback", "failure handling", "checkpoint"],
    "memory_context": ["memory", "retrieval", "compression", "summarization", "provenance", "stale", "handoff packet", "redaction", "context budget", "trust ranking"],
    "workflow_state_machine": ["state machine", "transition", "blocker", "retry", "handoff", "return contract", "termination", "evidence"],
    "domain_depth": ["compliance", "KPI", "risk", "constraint", "freshness", "audit", "policy", "edge case", "failure mode"],
    "governance_safety": ["human approval", "approval gate", "permission", "policy", "audit trail", "prompt injection", "safe abort", "irreversible"],
    "evals_tests": ["eval", "smoke test", "red-team", "golden", "threshold", "regression", "first-day"],
    "observability_cost": ["metric", "trace", "dashboard", "cost", "budget", "rate limit", "quota", "alert", "token"],
    "installability": ["folder structure", "manifest", "schema", "config", "template", "install", "package"],
}

RED_FLAG_PATTERNS = [
    ("no_dynamic_discovery", r"\bfixed tool list\b|\bhardcode\b"),
    ("no_memory", r"\b(no memory|without memory)\b"),
    ("auto_trade", r"\b(auto(?:matically)? trade|execute trades without approval)\b"),
    ("offensive_exploitation", r"\bexploit\b|\bpayload\b|\bprivilege escalation\b"),
    ("medical_diagnosis", r"\bdiagnos(?:e|is)\b"),
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_run_files(runs_dir: Path, include_glob: str) -> Iterable[Path]:
    yield from sorted(runs_dir.glob(include_glob))


def metadata_from_name(path: Path) -> tuple[str, str, str]:
    stem = path.stem
    parts = stem.rsplit("_", 2)
    if len(parts) != 3:
        return ("unknown", "unknown", stem)
    return (parts[0], parts[1], parts[2])


def score_dimension(text: str, dimension: dict) -> tuple[int, str]:
    did = dimension["id"]
    max_points = int(dimension["points"])
    haystack = text.lower()
    found = [signal for signal in SIGNALS.get(did, []) if signal.lower() in haystack]
    coverage = len(found) / max(1, len(SIGNALS.get(did, [])))
    if coverage >= 0.80:
        score = max_points
    elif coverage >= 0.55:
        score = max(0, round(max_points * 0.75))
    elif coverage >= 0.30:
        score = max(0, round(max_points * 0.55))
    elif coverage > 0:
        score = max(1, round(max_points * 0.30))
    else:
        score = 0
    return (min(max_points, score), ";".join(found))


def detect_red_flags(text: str) -> list[str]:
    flags: list[str] = []
    for label, pattern in RED_FLAG_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            flags.append(label)
    return flags


def verdict(score: int, rubric: dict, red_flags: list[str]) -> str:
    if red_flags:
        return "Not production-grade"
    for band in rubric["verdict_bands"]:
        if int(band["min"]) <= score <= int(band["max"]):
            return band["verdict"]
    return "Not useful for serious agent-team generation"


def main() -> None:
    parser = argparse.ArgumentParser(description="Draft-score benchmark run outputs.")
    parser.add_argument("--runs-dir", type=Path, required=True)
    parser.add_argument("--rubric", type=Path, default=DEFAULT_RUBRIC)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--include-glob", default="*.md")
    args = parser.parse_args()

    rubric = load_json(args.rubric)
    args.out.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "runtime",
        "model",
        "prompt_id",
        "score",
        "verdict",
        "red_flags",
        "strongest_dimension",
        "weakest_dimension",
        "evidence_summary",
        "notes",
    ]
    with args.out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for path in iter_run_files(args.runs_dir, args.include_glob):
            runtime, model, prompt_id = metadata_from_name(path)
            text = path.read_text(encoding="utf-8", errors="replace")
            dim_scores = []
            evidence = []
            for dimension in rubric["dimensions"]:
                points, found = score_dimension(text, dimension)
                dim_scores.append((dimension["id"], points))
                if found:
                    evidence.append(f"{dimension['id']}={found}")
            total = sum(points for _, points in dim_scores)
            flags = detect_red_flags(text)
            strongest = max(dim_scores, key=lambda item: item[1])[0] if dim_scores else ""
            weakest = min(dim_scores, key=lambda item: item[1])[0] if dim_scores else ""
            writer.writerow(
                {
                    "runtime": runtime,
                    "model": model,
                    "prompt_id": prompt_id,
                    "score": total,
                    "verdict": verdict(total, rubric, flags),
                    "red_flags": ";".join(flags),
                    "strongest_dimension": strongest,
                    "weakest_dimension": weakest,
                    "evidence_summary": " | ".join(evidence),
                    "notes": "Draft automated score; human review required before publication.",
                }
            )
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
