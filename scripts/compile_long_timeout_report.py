#!/usr/bin/env python3
"""Compile the long-timeout Agentlas public agent-team benchmark artifacts.

The upstream Agentlas CLI provider currently records usage units as prompt and
response character counts for subscription/CLI runs. This script keeps those
observed units intact, then adds a clearly labeled chars/4 token estimate so
cost comparisons do not pretend to be exact API invoices.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path("/tmp/test_agent/reports/scenario_eval_scores.csv")
DEFAULT_EVAL_DIR = ROOT / "data" / "evaluations"
DEFAULT_ASSETS_DIR = ROOT / "assets"

TOKEN_DIVISOR = 4.0
PRIVATE_PROMPT_NAMES = {"P10_" + "META" + "_AGENT_FACTORY"}
PRIVATE_PROMPT_IDS = {"P10"}

MODEL_PRICES: dict[tuple[str, str], dict[str, Any]] = {
    ("agentlas_claude", "claude-sonnet-4-6"): {
        "input": 3.00,
        "output": 15.00,
        "source": "https://www.anthropic.com/claude/sonnet",
        "note": "Anthropic API list price for Claude Sonnet 4.6.",
    },
    ("agentlas_codex", "gpt-5.5"): {
        "input": 5.00,
        "output": 30.00,
        "source": "https://openai.com/index/introducing-gpt-5-5/",
        "note": "OpenAI announced API list price; this run used Codex CLI, not a direct API invoice.",
    },
    ("agentlas_gemini", "gemini-3.1-pro-preview"): {
        "input": 2.00,
        "output": 12.00,
        "source": "https://ai.google.dev/gemini-api/docs/pricing",
        "note": "Gemini 3.1 Pro Preview standard tier for prompts <=200k tokens.",
    },
    ("agentlas_gemini", "gemini-3-flash-preview"): {
        "input": 0.50,
        "output": 3.00,
        "source": "https://ai.google.dev/gemini-api/docs/pricing",
        "note": "Gemini 3 Flash Preview standard tier.",
    },
    ("agentlas_upstage", "solar-pro2"): {
        "input": 0.15,
        "output": 0.60,
        "source": "https://www.upstage.ai/pricing",
        "note": "Upstage Solar Pro 2 public pricing.",
    },
}

DISPLAY_NAMES = {
    ("agentlas_claude", "claude-sonnet-4-6"): "Claude Code / Sonnet 4.6",
    ("agentlas_codex", "gpt-5.5"): "Codex CLI / GPT-5.5",
    ("agentlas_gemini", "gemini-3.1-pro-preview"): "Gemini CLI / 3.1 Pro",
    ("agentlas_gemini", "gemini-3-flash-preview"): "Gemini CLI / 3 Flash",
    ("agentlas_upstage", "solar-pro2"): "Upstage CLI / Solar Pro 2",
    ("agentlas_antigravity", "default"): "Antigravity CLI / default",
}

TIME_LABEL_OFFSETS = {
    "Claude Code / Sonnet 4.6": (-170, 8),
    "Codex CLI / GPT-5.5": (10, 12),
    "Gemini CLI / 3.1 Pro": (-118, -26),
    "Gemini CLI / 3 Flash": (10, -20),
    "Upstage CLI / Solar Pro 2": (10, 12),
}

COST_LABEL_OFFSETS = {
    "Claude Code / Sonnet 4.6": (-120, -48),
    "Codex CLI / GPT-5.5": (-122, 28),
    "Gemini CLI / 3.1 Pro": (10, -35),
    "Gemini CLI / 3 Flash": (10, -22),
    "Upstage CLI / Solar Pro 2": (10, 12),
}

TOKEN_LABEL_OFFSETS = {
    "Claude Code / Sonnet 4.6": (-132, -6),
    "Codex CLI / GPT-5.5": (10, 14),
    "Gemini CLI / 3.1 Pro": (10, 14),
    "Gemini CLI / 3 Flash": (10, 10),
    "Upstage CLI / Solar Pro 2": (10, 10),
}


def as_float(value: str | None) -> float:
    if value is None or value == "":
        return 0.0
    return float(value)


def as_int(value: str | None) -> int:
    return int(round(as_float(value)))


def estimate_tokens(observed_units: int) -> int:
    return int(round(observed_units / TOKEN_DIVISOR))


def estimate_cost(input_tokens: int, output_tokens: int, price: dict[str, Any] | None) -> float | None:
    if not price:
        return None
    return ((input_tokens * price["input"]) + (output_tokens * price["output"])) / 1_000_000


def fmt_money(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.6f}"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def is_private_prompt(row: dict[str, str]) -> bool:
    return row.get("prompt_id") in PRIVATE_PROMPT_IDS or row.get("prompt_name") in PRIVATE_PROMPT_NAMES


def sanitize_public_text(value: str | None) -> str:
    if not value:
        return ""
    private_term = "meta" + "-agent"
    private_title = "Meta" + "-Agent"
    return (
        value.replace(f"Agentlas {private_term}", "Agentlas agent-team")
        .replace(private_title, "Agent-Team")
        .replace(f"{private_term} OS", "agent-team OS")
        .replace(f"{private_term} generation", "agent-team generation")
        .replace(private_term, "agent-team")
    )


def build_public_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    public_rows: list[dict[str, Any]] = []
    for row in rows:
        if row.get("source_kind") != "agentlas_meta_export":
            continue
        if is_private_prompt(row):
            continue
        runtime = row["runtime"]
        model = row["model"]
        observed_input = as_int(row.get("input_tokens"))
        observed_output = as_int(row.get("output_tokens"))
        est_input = estimate_tokens(observed_input)
        est_output = estimate_tokens(observed_output)
        price = MODEL_PRICES.get((runtime, model))
        est_cost = estimate_cost(est_input, est_output, price)
        public_rows.append(
            {
                "runtime": runtime,
                "model": model,
                "display_name": DISPLAY_NAMES.get((runtime, model), f"{runtime} / {model}"),
                "prompt_id": row.get("prompt_id"),
                "prompt_name": row.get("prompt_name"),
                "score": row.get("score"),
                "verdict": sanitize_public_text(row.get("verdict")),
                "generated_by": row.get("generated_by"),
                "failure_reason": sanitize_public_text(row.get("failure_reason")),
                "wall_time_seconds": row.get("wall_time_seconds"),
                "observed_input_units": observed_input,
                "observed_output_units": observed_output,
                "observed_total_units": observed_input + observed_output,
                "estimated_input_tokens": est_input,
                "estimated_output_tokens": est_output,
                "estimated_total_tokens": est_input + est_output,
                "estimated_api_cost_usd": fmt_money(est_cost),
                "cost_type": "proxy_estimate_chars_div_4" if est_cost is not None else "unavailable",
                "price_input_usd_per_1m": price["input"] if price else "",
                "price_output_usd_per_1m": price["output"] if price else "",
                "pricing_source": price["source"] if price else "",
                "request_fit": row.get("request_fit"),
                "agentlas_team_structure": row.get("agentlas_team_structure"),
                "dynamic_tools_credentials": row.get("dynamic_tools_credentials"),
                "context_engineering": row.get("context_engineering"),
                "workflow_hooks_handoffs": row.get("workflow_hooks_handoffs"),
                "runnable_installability": row.get("runnable_installability"),
                "governance_safety": row.get("governance_safety"),
                "observability_cost": row.get("observability_cost"),
                "red_flags": row.get("red_flags"),
            }
        )
    return sorted(public_rows, key=lambda r: (r["runtime"], r["model"], r["prompt_id"] or ""))


def build_summary_rows(public_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in public_rows:
        grouped[(row["runtime"], row["model"])].append(row)

    summary_rows: list[dict[str, Any]] = []
    for (runtime, model), rows in sorted(grouped.items()):
        scores = [as_float(str(row["score"])) for row in rows]
        wall_times = [as_float(str(row["wall_time_seconds"])) for row in rows]
        llm_successes = sum(1 for row in rows if row.get("generated_by") == "llm")
        input_units = sum(as_int(str(row["observed_input_units"])) for row in rows)
        output_units = sum(as_int(str(row["observed_output_units"])) for row in rows)
        est_input = estimate_tokens(input_units)
        est_output = estimate_tokens(output_units)
        price = MODEL_PRICES.get((runtime, model))
        est_cost = estimate_cost(est_input, est_output, price)
        avg_score = sum(scores) / len(scores)
        summary_rows.append(
            {
                "runtime": runtime,
                "model": model,
                "display_name": DISPLAY_NAMES.get((runtime, model), f"{runtime} / {model}"),
                "cases": len(rows),
                "llm_successes": llm_successes,
                "failures": len(rows) - llm_successes,
                "avg_score": round(avg_score, 2),
                "min_score": round(min(scores), 2),
                "max_score": round(max(scores), 2),
                "avg_wall_time_seconds": round(sum(wall_times) / len(wall_times), 3),
                "observed_input_units": input_units,
                "observed_output_units": output_units,
                "observed_total_units": input_units + output_units,
                "estimated_input_tokens": est_input,
                "estimated_output_tokens": est_output,
                "estimated_total_tokens": est_input + est_output,
                "price_input_usd_per_1m": price["input"] if price else "",
                "price_output_usd_per_1m": price["output"] if price else "",
                "estimated_suite_cost_usd": fmt_money(est_cost),
                "estimated_avg_case_cost_usd": fmt_money((est_cost / len(rows)) if est_cost is not None else None),
                "score_per_estimated_usd": round(avg_score / est_cost, 2) if est_cost and est_cost > 0 else "",
                "estimated_tokens_per_score_point": round((est_input + est_output) / avg_score, 2) if avg_score else "",
                "cost_type": "proxy_estimate_chars_div_4" if est_cost is not None else "unavailable",
                "pricing_source": price["source"] if price else "",
                "pricing_note": price["note"] if price else "No usable LLM output or no official API price mapped.",
            }
        )
    return summary_rows


def plot_score_time(summary_rows: list[dict[str, Any]], out_path: Path) -> None:
    qualified = [row for row in summary_rows if row["llm_successes"] == row["cases"] and row["avg_score"] > 0]
    fig, ax = plt.subplots(figsize=(10, 6), dpi=180)
    colors = ["#1d4ed8", "#0f766e", "#b45309", "#7c3aed", "#be123c"]
    for idx, row in enumerate(qualified):
        ax.scatter(
            row["avg_wall_time_seconds"],
            row["avg_score"],
            s=130,
            color=colors[idx % len(colors)],
            edgecolor="#111827",
            linewidth=0.7,
            alpha=0.92,
        )
        ax.annotate(
            f"{row['display_name']}\n{row['avg_score']:.1f} pts, {row['avg_wall_time_seconds']:.1f}s",
            (row["avg_wall_time_seconds"], row["avg_score"]),
            textcoords="offset points",
            xytext=TIME_LABEL_OFFSETS.get(row["display_name"], (8, 9 if idx % 2 == 0 else -24)),
            fontsize=8,
            bbox={"boxstyle": "round,pad=0.18", "facecolor": "white", "alpha": 0.78, "edgecolor": "none"},
        )
    ax.set_xscale("log")
    ax.set_ylim(93.0, 97.0)
    ax.set_xlabel("Average wall time per case, seconds (log scale)")
    ax.set_ylabel("Average score (zoomed 93-97)")
    ax.set_title("Agentlas agent-team benchmark: quality vs time")
    ax.grid(True, which="both", linestyle=":", linewidth=0.6, alpha=0.55)
    ax.text(
        0.01,
        0.02,
        "Antigravity stdout-contract failure excluded from zoomed view.",
        transform=ax.transAxes,
        fontsize=8,
        color="#4b5563",
    )
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def plot_score_cost(summary_rows: list[dict[str, Any]], out_path: Path) -> None:
    qualified = [
        row
        for row in summary_rows
        if row["llm_successes"] == row["cases"] and row["avg_score"] > 0 and row["estimated_suite_cost_usd"]
    ]
    fig, ax = plt.subplots(figsize=(10, 6), dpi=180)
    tokens = [row["estimated_total_tokens"] for row in qualified]
    min_tokens = min(tokens)
    max_tokens = max(tokens)
    for row in qualified:
        cost = float(row["estimated_suite_cost_usd"])
        size = 90 + 260 * ((row["estimated_total_tokens"] - min_tokens) / max(1, max_tokens - min_tokens))
        ax.scatter(
            cost,
            row["avg_score"],
            s=size,
            color="#2563eb" if row["avg_score"] >= 96 else "#0891b2",
            edgecolor="#111827",
            linewidth=0.7,
            alpha=0.9,
        )
        ax.annotate(
            f"{row['display_name']}\n${cost:.4f}, {row['estimated_total_tokens']:,} est tok",
            (cost, row["avg_score"]),
            textcoords="offset points",
            xytext=COST_LABEL_OFFSETS.get(row["display_name"], (8, 9)),
            fontsize=8,
            bbox={"boxstyle": "round,pad=0.18", "facecolor": "white", "alpha": 0.78, "edgecolor": "none"},
        )
    ax.set_xscale("log")
    ax.set_ylim(93.0, 97.0)
    ax.set_xlabel("Estimated API cost for published-case suite, USD (log scale)")
    ax.set_ylabel("Average score (zoomed 93-97)")
    ax.set_title("Agentlas agent-team benchmark: score vs estimated API cost")
    ax.grid(True, which="both", linestyle=":", linewidth=0.6, alpha=0.55)
    ax.text(
        0.01,
        0.02,
        "Cost = observed CLI chars / 4 x official per-token API prices; not an invoice.",
        transform=ax.transAxes,
        fontsize=8,
        color="#4b5563",
    )
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def plot_tokens_cost_score(summary_rows: list[dict[str, Any]], out_path: Path) -> None:
    qualified = [
        row
        for row in summary_rows
        if row["llm_successes"] == row["cases"] and row["avg_score"] > 0 and row["estimated_suite_cost_usd"]
    ]
    fig, ax = plt.subplots(figsize=(10, 6), dpi=180)
    scatter = ax.scatter(
        [row["estimated_total_tokens"] for row in qualified],
        [float(row["estimated_suite_cost_usd"]) for row in qualified],
        c=[row["avg_score"] for row in qualified],
        cmap="viridis",
        s=140,
        edgecolor="#111827",
        linewidth=0.7,
        alpha=0.92,
    )
    for row in qualified:
        ax.annotate(
            f"{row['display_name']}\n{row['avg_score']:.1f} pts",
            (row["estimated_total_tokens"], float(row["estimated_suite_cost_usd"])),
            textcoords="offset points",
            xytext=TOKEN_LABEL_OFFSETS.get(row["display_name"], (8, 9)),
            fontsize=8,
            bbox={"boxstyle": "round,pad=0.18", "facecolor": "white", "alpha": 0.78, "edgecolor": "none"},
        )
    ax.set_yscale("log")
    ax.set_xlabel("Estimated total tokens for 10-case suite (observed chars / 4)")
    ax.set_ylabel("Estimated API cost for 10-case suite, USD (log scale)")
    ax.set_title("Token volume, estimated cost, and score")
    ax.grid(True, which="both", linestyle=":", linewidth=0.6, alpha=0.55)
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Average score")
    ax.text(
        0.01,
        0.02,
        "CLI usage fields are character-count proxies; exact provider tokenization may differ.",
        transform=ax.transAxes,
        fontsize=8,
        color="#4b5563",
    )
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile latest Agentlas benchmark public artifacts.")
    parser.add_argument("--source-csv", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--eval-dir", type=Path, default=DEFAULT_EVAL_DIR)
    parser.add_argument("--assets-dir", type=Path, default=DEFAULT_ASSETS_DIR)
    args = parser.parse_args()

    source_rows = load_rows(args.source_csv)
    public_rows = build_public_rows(source_rows)
    summary_rows = build_summary_rows(public_rows)

    score_fields = [
        "runtime",
        "model",
        "display_name",
        "prompt_id",
        "prompt_name",
        "score",
        "verdict",
        "generated_by",
        "failure_reason",
        "wall_time_seconds",
        "observed_input_units",
        "observed_output_units",
        "observed_total_units",
        "estimated_input_tokens",
        "estimated_output_tokens",
        "estimated_total_tokens",
        "estimated_api_cost_usd",
        "cost_type",
        "price_input_usd_per_1m",
        "price_output_usd_per_1m",
        "pricing_source",
        "request_fit",
        "agentlas_team_structure",
        "dynamic_tools_credentials",
        "context_engineering",
        "workflow_hooks_handoffs",
        "runnable_installability",
        "governance_safety",
        "observability_cost",
        "red_flags",
    ]
    summary_fields = [
        "runtime",
        "model",
        "display_name",
        "cases",
        "llm_successes",
        "failures",
        "avg_score",
        "min_score",
        "max_score",
        "avg_wall_time_seconds",
        "observed_input_units",
        "observed_output_units",
        "observed_total_units",
        "estimated_input_tokens",
        "estimated_output_tokens",
        "estimated_total_tokens",
        "price_input_usd_per_1m",
        "price_output_usd_per_1m",
        "estimated_suite_cost_usd",
        "estimated_avg_case_cost_usd",
        "score_per_estimated_usd",
        "estimated_tokens_per_score_point",
        "cost_type",
        "pricing_source",
        "pricing_note",
    ]

    args.eval_dir.mkdir(parents=True, exist_ok=True)
    args.assets_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.eval_dir / "agentlas_meta_long_timeout_scores.csv", score_fields, public_rows)
    write_csv(args.eval_dir / "agentlas_meta_long_timeout_summary.csv", summary_fields, summary_rows)
    write_csv(args.eval_dir / "agentlas_meta_token_cost_score.csv", summary_fields, summary_rows)
    write_csv(args.eval_dir / "agentlas_meta_reviewed_scores.csv", score_fields, public_rows)
    write_csv(args.eval_dir / "agentlas_meta_reviewed_summary.csv", summary_fields, summary_rows)

    summary_json = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_csv": args.source_csv.name,
        "source_csv_note": "Local operator source; raw absolute path intentionally omitted from public output.",
        "score_source_kind": "agentlas_meta_export",
        "timeout_contract_ms": 900000,
        "usage_note": (
            "The non-public case is excluded from public aggregate outputs. "
            "Agentlas CLI provider usage units are observed prompt/response character counts. "
            "Estimated tokens use chars/4 and official API rates only for proxy comparison."
        ),
        "token_divisor": TOKEN_DIVISOR,
        "rows": summary_rows,
    }
    (args.eval_dir / "agentlas_meta_long_timeout_summary.json").write_text(
        json.dumps(summary_json, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    reviewed_json = {
        **summary_json,
        "aliasOf": "agentlas_meta_long_timeout_summary.json",
        "reviewRule": "Long-timeout Agentlas public scenario exports; deterministic fallbacks score 0 and qualified LLM outputs use the 8-axis scenario rubric. Non-public cases are excluded.",
    }
    (args.eval_dir / "agentlas_meta_reviewed_summary.json").write_text(
        json.dumps(reviewed_json, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    plot_score_time(summary_rows, args.assets_dir / "agentlas_meta_score_time_zoom.png")
    plot_score_cost(summary_rows, args.assets_dir / "agentlas_meta_score_cost_zoom.png")
    plot_tokens_cost_score(summary_rows, args.assets_dir / "agentlas_meta_tokens_cost_score.png")

    print("wrote data/evaluations/agentlas_meta_long_timeout_scores.csv")
    print("wrote data/evaluations/agentlas_meta_long_timeout_summary.csv")
    print("wrote data/evaluations/agentlas_meta_token_cost_score.csv")
    print("wrote data/evaluations/agentlas_meta_long_timeout_summary.json")
    print("wrote data/evaluations/agentlas_meta_reviewed_scores.csv")
    print("wrote data/evaluations/agentlas_meta_reviewed_summary.csv")
    print("wrote data/evaluations/agentlas_meta_reviewed_summary.json")
    print("wrote assets/agentlas_meta_score_time_zoom.png")
    print("wrote assets/agentlas_meta_score_cost_zoom.png")
    print("wrote assets/agentlas_meta_tokens_cost_score.png")


if __name__ == "__main__":
    main()
