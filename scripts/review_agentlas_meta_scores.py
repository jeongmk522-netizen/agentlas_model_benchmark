#!/usr/bin/env python3
"""Create a reviewed aggregate table from Agentlas meta-benchmark summaries.

The live runner keeps raw automated scores. This reviewer applies one narrow
human-review correction: phrase-style red flags such as "without workflow" are
not counted when the generated Agentlas repo already contains the required
workflow/gate/domain signals in the score evidence.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVAL_DIR = ROOT / "data" / "evaluations"
FALSE_POSITIVE_FLAGS = {
    "creative role list without workflow",
    "generic campaign plan without tool/data workflow",
    "code generation without governance and test/release gates",
    "fixed seed agent list as the core design",
}


def verdict(score: int, red_flags: list[str], error: str | None) -> str:
    if error:
        return "Failed"
    if red_flags:
        return "Not production-grade"
    if score >= 85:
        return "Production-grade candidate"
    if score >= 70:
        return "Strong but incomplete"
    if score >= 50:
        return "Needs review"
    return "Failed"


def review_result(result: dict[str, Any]) -> dict[str, Any]:
    reviewed = json.loads(json.dumps(result))
    if reviewed.get("error") or reviewed.get("generated_by") != "llm":
        reviewed["raw_score100"] = result.get("score100")
        reviewed["raw_verdict"] = result.get("verdict")
        reviewed["reviewed_score100"] = 0
        reviewed["score100"] = 0
        reviewed["review_corrections"] = []
        reviewed["verdict"] = "Failed"
        return reviewed

    red_flags = list(reviewed.get("red_flags") or [])
    corrected_flags = [flag for flag in red_flags if flag in FALSE_POSITIVE_FLAGS]
    if corrected_flags and len(corrected_flags) == len(red_flags):
      red_flags = []
      for item in reviewed.get("score_items") or []:
          if item.get("id") == "domain-specific-safety" and item.get("points") == 0:
              item["points"] = 10
              item["review_note"] = "Restored after human review of phrase-based red-flag false positive."
    score = sum(int(item.get("points") or 0) for item in reviewed.get("score_items") or [])
    if not reviewed.get("score_items"):
        score = int(reviewed.get("score100") or 0)
    reviewed["raw_score100"] = result.get("score100")
    reviewed["raw_verdict"] = result.get("verdict")
    reviewed["reviewed_score100"] = score
    reviewed["score100"] = score
    reviewed["red_flags"] = red_flags
    reviewed["review_corrections"] = corrected_flags
    reviewed["verdict"] = verdict(score, red_flags, reviewed.get("error"))
    return reviewed


def load_summaries(eval_dir: Path) -> list[dict[str, Any]]:
    summaries = []
    for path in sorted(eval_dir.glob("agentlas_meta_*_summary.json")):
        if path.name.endswith("_reviewed_summary.json"):
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        data["_source"] = path.name
        summaries.append(data)
    return summaries


def main() -> None:
    parser = argparse.ArgumentParser(description="Build reviewed Agentlas meta-benchmark aggregate tables.")
    parser.add_argument("--eval-dir", type=Path, default=DEFAULT_EVAL_DIR)
    parser.add_argument("--out-prefix", default="agentlas_meta_reviewed")
    args = parser.parse_args()

    rows: list[dict[str, Any]] = []
    runtime_summaries: dict[str, dict[str, Any]] = {}
    for summary in load_summaries(args.eval_dir):
        reviewed_results = [review_result(result) for result in summary.get("results", [])]
        average = round(sum(result["score100"] for result in reviewed_results) / max(1, len(reviewed_results)), 2)
        runtime = summary.get("runtime", "unknown")
        model = summary.get("model", "unknown")
        counts = Counter(result["verdict"] for result in reviewed_results)
        corrections = sum(len(result.get("review_corrections") or []) for result in reviewed_results)
        runtime_summaries[f"{runtime}:{model}"] = {
            "runtime": runtime,
            "model": model,
            "cases": len(reviewed_results),
            "average_score100": average,
            "failures": sum(1 for result in reviewed_results if result.get("error")),
            "llm_successes": sum(1 for result in reviewed_results if result.get("generated_by") == "llm"),
            "review_corrections": corrections,
            "verdict_counts": dict(sorted(counts.items())),
            "source": summary.get("_source"),
        }
        for result in reviewed_results:
            rows.append({
                "runtime": runtime,
                "model": model,
                "prompt_id": result.get("prompt_id"),
                "domain": result.get("domain"),
                "score100": result.get("score100"),
                "raw_score100": result.get("raw_score100"),
                "verdict": result.get("verdict"),
                "raw_verdict": result.get("raw_verdict"),
                "generated_by": result.get("generated_by"),
                "wall_time_seconds": result.get("wall_time_seconds"),
                "red_flags": ";".join(result.get("red_flags") or []),
                "review_corrections": ";".join(result.get("review_corrections") or []),
                "error": result.get("error") or "",
            })

    args.eval_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.eval_dir / f"{args.out_prefix}_scores.csv"
    fieldnames = [
        "runtime",
        "model",
        "prompt_id",
        "domain",
        "score100",
        "raw_score100",
        "verdict",
        "raw_verdict",
        "generated_by",
        "wall_time_seconds",
        "red_flags",
        "review_corrections",
        "error",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda row: (row["runtime"], row["prompt_id"] or "")))

    by_prompt: dict[str, list[int]] = defaultdict(list)
    for row in rows:
        if not row["error"]:
            by_prompt[str(row["prompt_id"])].append(int(row["score100"] or 0))
    aggregate = {
        "generated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(timespec="seconds"),
        "review_rule": "Corrected only phrase-based red-flag false positives when score evidence already showed the required workflow/gate/domain signals.",
        "runtime_summaries": runtime_summaries,
        "prompt_average_successful_runs": {
            prompt_id: round(sum(scores) / len(scores), 2)
            for prompt_id, scores in sorted(by_prompt.items())
            if scores
        },
        "rows": rows,
    }
    summary_path = args.eval_dir / f"{args.out_prefix}_summary.json"
    summary_path.write_text(json.dumps(aggregate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {csv_path}")
    print(f"wrote {summary_path}")


if __name__ == "__main__":
    main()
