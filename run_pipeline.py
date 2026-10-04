"""
End-to-End Pipeline Execution Script for Assignment 4 Multi-Agent Systems.
Executes the collaborative team of 4 role-based agents with Human-in-the-Loop checkpoint,
captures the full interaction trace, and saves the verified logs.
"""

import asyncio
import json
from pathlib import Path
from coordination import MultiAgentOrchestrator
import config

COMPLEX_TASK_PROMPT = (
    "Design, implement, and audit an enterprise-grade Distributed Rate Limiting & Circuit Breaker Engine in Python. "
    "Functional Requirements:\n"
    "1. Multi-tier Token Bucket algorithm supporting configurable burst capacity and continuous refill rate.\n"
    "2. Integrated Circuit Breaker pattern with states CLOSED, OPEN, and HALF-OPEN, with failure threshold and cooldown reset.\n"
    "3. High-concurrency thread safety preventing race conditions (TOCTOU) and thread starvation.\n"
    "4. Self-contained unit tests asserting burst behavior, rate-limiting rejection, circuit breaker state transitions, and concurrency under multi-threaded stress."
)


async def main():
    print("=" * 80)
    print("ASSIGNMENT 04: COLLABORATIVE MULTI-AGENT TEAM (MIT ADT UNIVERSITY)")
    print("Task: Enterprise-grade Distributed Rate Limiter & Circuit Breaker Engine")
    print("=" * 80)

    orchestrator = MultiAgentOrchestrator()

    def progress_logger(stage: str, msg: str):
        print(f"\n>>> [{stage}] {msg}")

    print("\n[+] Starting End-to-End Multi-Agent Pipeline Execution...")
    result = await orchestrator.run_end_to_end(
        task_prompt=COMPLEX_TASK_PROMPT,
        human_decision="APPROVE",
        human_feedback="Architecture approved. Ensure rigorous multi-threaded stress tests and clear state-transition logging.",
        progress_callback=progress_logger,
    )

    # Save logs
    json_path = config.LOGS_DIR / "task_run_log.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    md_path = config.LOGS_DIR / "task_run_log.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Full Multi-Agent End-to-End Communication & Execution Log\n\n")
        f.write(f"**Task Objective**:\n{COMPLEX_TASK_PROMPT}\n\n")
        f.write(f"**Human Checkpoint Decision**: `{result['human_decision']}`\n")
        f.write(f"**Human Supervisor Directive**: `{result['human_feedback']}`\n\n")
        f.write("## Shared Task Board Final State\n\n")
        f.write("| Task ID | Title | Assigned Agent | Status |\n")
        f.write("|---------|-------|----------------|--------|\n")
        for tid, card in result["task_board"].items():
            f.write(f"| {tid} | {card['title']} | {card['assigned_to']} | {card['status']} |\n")
        f.write("\n---\n\n## Inter-Agent Message Log\n\n")
        f.write(orchestrator.bus.export_markdown_log())

    print("\n" + "=" * 80)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"[+] Total Messages Recorded: {result['messages_count']}")
    print(f"[+] JSON Trace Log saved to: {json_path}")
    print(f"[+] Markdown Trace Log saved to: {md_path}")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
