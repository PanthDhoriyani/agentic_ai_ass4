"""
Conflict Resolution Execution Script for Assignment 4 Multi-Agent Systems.
Demonstrates:
- Agent-to-agent contradiction injection (Throughput vs. Security/Concurrency).
- Structured dialectic arbitration by the TeamManager / Orchestrator.
- Consensus synthesis and formal agreement sign-offs.
"""

import asyncio
import json
from coordination import ConflictResolutionEngine
import config


async def main():
    print("=" * 80)
    print("ASSIGNMENT 04: CONFLICT SCENARIO & DIALECTIC ARBITRATION")
    print("Domain: Concurrency Locking vs Ultra-Low Latency Performance")
    print("=" * 80)

    engine = ConflictResolutionEngine()

    print("\n[+] Injecting Contradictory Agent Outputs & Initiating Negotiation Protocol...")
    result = await engine.run_conflict_simulation()

    # Save conflict resolution logs
    json_path = config.LOGS_DIR / "conflict_resolution_log.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    md_path = config.LOGS_DIR / "conflict_resolution_log.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Conflict Resolution & Dialectic Arbitration Documentation\n\n")
        f.write(f"**Scenario Description**: {result['conflict_description']}\n")
        f.write(f"**Final Status**: `{result['status']}`\n\n")
        f.write("## 1. Contradictory Agent Positions\n\n")
        f.write("### Agent 1: CodeEngineer (Thesis: Throughput & Speed)\n")
        f.write(f"```text\n{result['engineer_proposal']}\n```\n\n")
        f.write("### Agent 2: SecurityCritic (Antithesis: Race Condition & Security)\n")
        f.write(f"```text\n{result['critic_objection']}\n```\n\n")
        f.write("## 2. TeamManager Dialectic Arbitration Ruling (Synthesis)\n\n")
        f.write(f"{result['arbitration_verdict']}\n\n")
        f.write("## 3. Communication Protocol Messages\n\n")
        f.write(engine.bus.export_markdown_log())

    print("\n" + "=" * 80)
    print("CONFLICT RESOLUTION SIMULATION COMPLETED!")
    print(f"[+] Status: {result['status']}")
    print(f"[+] Conflict JSON Log saved to: {json_path}")
    print(f"[+] Conflict Markdown Log saved to: {md_path}")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
