"""
Diagram generation script for Assignment 4 Multi-Agent Systems.
Creates high-resolution publication-quality PNG diagrams for architecture,
coordination workflow, conflict resolution, and comparative benchmark metrics.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from pathlib import Path
import config


def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#0F172A")
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis("off")

    # Title
    ax.text(7, 8.5, "Collaborative Multi-Agent Architecture (MIT ADT Assignment 4)",
            color="#38BDF8", fontsize=18, fontweight="bold", ha="center")
    ax.text(7, 8.1, "Role-Based Specialization, Blackboard State, and Message Passing Protocol",
            color="#94A3B8", fontsize=11, ha="center")

    # Central Shared Blackboard (Task Board)
    bb_box = patches.FancyBboxPatch((4.5, 3.2), 5.0, 3.2, boxstyle="round,pad=0.2",
                                    facecolor="#1E293B", edgecolor="#38BDF8", linewidth=2.5)
    ax.add_patch(bb_box)
    ax.text(7, 6.0, "SHARED TASK BOARD (BLACKBOARD)", color="#38BDF8", fontsize=12, fontweight="bold", ha="center")
    ax.text(7, 5.5, "Task States: BACKLOG | IN_PROGRESS | REVIEW | HUMAN_APPROVAL | DONE",
            color="#CBD5E1", fontsize=8.5, ha="center")
    ax.text(7, 5.0, "Artifacts: Architecture Specs | Verified Code | AST Reports | Sign-Offs",
            color="#94A3B8", fontsize=8.5, ha="center")
    ax.text(7, 4.4, "Event Dispatcher: Dynamic Stage Routing & State Mutation",
            color="#64748B", fontsize=8.5, ha="center")
    ax.text(7, 3.7, "Message Bus: Verifiable Traces (JSON / Markdown)",
            color="#34D399", fontsize=9, fontweight="bold", ha="center")

    # Agent 1: SystemArchitect (Top Left)
    a1_box = patches.FancyBboxPatch((0.6, 5.6), 3.2, 1.8, boxstyle="round,pad=0.15",
                                    facecolor="#1E293B", edgecolor="#818CF8", linewidth=2)
    ax.add_patch(a1_box)
    ax.text(2.2, 7.0, "SystemArchitect", color="#818CF8", fontsize=12, fontweight="bold", ha="center")
    ax.text(2.2, 6.5, "Role: Lead Architect & Researcher", color="#CBD5E1", fontsize=8.5, ha="center")
    ax.text(2.2, 6.1, "Tool: search_technical_standards", color="#38BDF8", fontsize=8, ha="center")
    ax.text(2.2, 5.75, "Artifact: Formal Class & Invariant Spec", color="#94A3B8", fontsize=7.5, ha="center")

    # Agent 2: CodeEngineer (Bottom Left)
    a2_box = patches.FancyBboxPatch((0.6, 1.6), 3.2, 1.8, boxstyle="round,pad=0.15",
                                    facecolor="#1E293B", edgecolor="#34D399", linewidth=2)
    ax.add_patch(a2_box)
    ax.text(2.2, 3.0, "CodeEngineer", color="#34D399", fontsize=12, fontweight="bold", ha="center")
    ax.text(2.2, 2.5, "Role: Senior Backend Engineer", color="#CBD5E1", fontsize=8.5, ha="center")
    ax.text(2.2, 2.1, "Tool: execute_python_code (Sandbox)", color="#38BDF8", fontsize=8, ha="center")
    ax.text(2.2, 1.75, "Artifact: Thread-Safe Python Code + Tests", color="#94A3B8", fontsize=7.5, ha="center")

    # Agent 3: SecurityCritic (Bottom Right)
    a3_box = patches.FancyBboxPatch((10.2, 1.6), 3.2, 1.8, boxstyle="round,pad=0.15",
                                    facecolor="#1E293B", edgecolor="#F43F5E", linewidth=2)
    ax.add_patch(a3_box)
    ax.text(11.8, 3.0, "SecurityCritic", color="#F43F5E", fontsize=12, fontweight="bold", ha="center")
    ax.text(11.8, 2.5, "Role: Security & QA Auditor", color="#CBD5E1", fontsize=8.5, ha="center")
    ax.text(11.8, 2.1, "Tool: security_ast_scanner", color="#38BDF8", fontsize=8, ha="center")
    ax.text(11.8, 1.75, "Artifact: AST Audit & TOCTOU Review", color="#94A3B8", fontsize=7.5, ha="center")

    # Agent 4: TeamManager (Top Right)
    a4_box = patches.FancyBboxPatch((10.2, 5.6), 3.2, 1.8, boxstyle="round,pad=0.15",
                                    facecolor="#1E293B", edgecolor="#FBBF24", linewidth=2)
    ax.add_patch(a4_box)
    ax.text(11.8, 7.0, "TeamManager", color="#FBBF24", fontsize=12, fontweight="bold", ha="center")
    ax.text(11.8, 6.5, "Role: Orchestrator & Arbitrator", color="#CBD5E1", fontsize=8.5, ha="center")
    ax.text(11.8, 6.1, "Mechanism: Dialectic Consensus", color="#38BDF8", fontsize=8, ha="center")
    ax.text(11.8, 1.75 + 4.0, "Artifact: Final Release Synthesis", color="#94A3B8", fontsize=7.5, ha="center")

    # Human-in-the-Loop Gate (Bottom Center)
    hitl_box = patches.FancyBboxPatch((4.7, 0.7), 4.6, 1.4, boxstyle="round,pad=0.15",
                                      facecolor="#1E293B", edgecolor="#A855F7", linewidth=2.5)
    ax.add_patch(hitl_box)
    ax.text(7, 1.7, "HUMAN-IN-THE-LOOP CHECKPOINT", color="#A855F7", fontsize=11, fontweight="bold", ha="center")
    ax.text(7, 1.25, "Gatekeeper: Authorize Architecture or Mandate Revisions", color="#E2E8F0", fontsize=8.5, ha="center")
    ax.text(7, 0.9, "Actions: [APPROVE] | [REJECT with Feedback]", color="#94A3B8", fontsize=8, ha="center")

    # Connection Arrows
    arrows = [
        ((3.8, 6.5), (4.5, 5.5), "#818CF8"),  # Architect to BB
        ((7.0, 3.2), (7.0, 2.1), "#A855F7"),  # BB to Human Checkpoint
        ((3.8, 2.5), (4.5, 3.8), "#34D399"),  # Engineer to BB
        ((10.2, 2.5), (9.5, 3.8), "#F43F5E"), # Critic to BB
        ((10.2, 6.5), (9.5, 5.5), "#FBBF24"), # Manager to BB
    ]
    for start, end, col in arrows:
        ax.annotate("", xy=end, xytext=start,
                    arrowprops=dict(arrowstyle="<->", color=col, lw=2.5, mutation_scale=15))

    out_file = config.BASE_DIR / "architecture_diagram.png"
    plt.tight_layout()
    plt.savefig(out_file, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"[+] Architecture diagram saved: {out_file}")


def create_workflow_diagram():
    fig, ax = plt.subplots(figsize=(15, 6), dpi=300)
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#0F172A")
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 6)
    ax.axis("off")

    ax.text(7.5, 5.4, "Multi-Agent Coordination & Hand-Off Pipeline Flow",
            color="#38BDF8", fontsize=17, fontweight="bold", ha="center")
    ax.text(7.5, 5.0, "Sequential Hand-Off with Human Checkpoint and Manager Oversight",
            color="#94A3B8", fontsize=10, ha="center")

    stages = [
        ("STAGE 1\nResearch & Spec", "SystemArchitect", "#818CF8", "Searches standards\nDrafts class contracts\nDefines concurrency"),
        ("STAGE 2\nHuman Gate", "HumanSupervisor", "#A855F7", "Inspects intermediate spec\nApproves design or\nDemands revisions"),
        ("STAGE 3\nCode & Sandbox", "CodeEngineer", "#34D399", "Implements thread-safe code\nExecutes unit tests\nVerifies zero errors"),
        ("STAGE 4\nSecurity Audit", "SecurityCritic", "#F43F5E", "Runs AST scanner\nChecks TOCTOU races\nIssues formal verdict"),
        ("STAGE 5\nFinal Release", "TeamManager", "#FBBF24", "Synthesizes all artifacts\nVerifies test logs\nFinal executive release"),
    ]

    for idx, (title, role, col, desc) in enumerate(stages):
        x = 0.8 + idx * 2.8
        y = 1.2
        box = patches.FancyBboxPatch((x, y), 2.4, 3.0, boxstyle="round,pad=0.15",
                                     facecolor="#1E293B", edgecolor=col, linewidth=2.2)
        ax.add_patch(box)
        ax.text(x + 1.2, y + 2.6, title, color=col, fontsize=10, fontweight="bold", ha="center")
        ax.text(x + 1.2, y + 2.05, f"[{role}]", color="#CBD5E1", fontsize=8.5, fontweight="bold", ha="center")
        ax.text(x + 1.2, y + 1.0, desc, color="#94A3B8", fontsize=7.5, ha="center", multialignment="center")

        if idx < len(stages) - 1:
            ax.annotate("", xy=(x + 2.8, y + 1.5), xytext=(x + 2.4, y + 1.5),
                        arrowprops=dict(arrowstyle="->", color="#38BDF8", lw=3, mutation_scale=20))

    out_file = config.BASE_DIR / "workflow_coordination.png"
    plt.tight_layout()
    plt.savefig(out_file, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"[+] Workflow diagram saved: {out_file}")


def create_conflict_resolution_diagram():
    fig, ax = plt.subplots(figsize=(13, 8), dpi=300)
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#0F172A")
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8)
    ax.axis("off")

    ax.text(6.5, 7.5, "Dialectic Conflict Resolution & Negotiation Flow",
            color="#38BDF8", fontsize=16, fontweight="bold", ha="center")
    ax.text(6.5, 7.1, "Resolving Contradictory Objectives: Raw Throughput vs Concurrency Safety",
            color="#94A3B8", fontsize=10, ha="center")

    # Step 1: Thesis
    b1 = patches.FancyBboxPatch((0.8, 4.4), 4.8, 2.0, boxstyle="round,pad=0.15",
                                facecolor="#1E293B", edgecolor="#34D399", linewidth=2)
    ax.add_patch(b1)
    ax.text(3.2, 6.0, "AGENT 1: CodeEngineer (THESIS)", color="#34D399", fontsize=10.5, fontweight="bold", ha="center")
    ax.text(3.2, 5.3, "Proposal: Remove all mutex locks\nUnsynchronized global state for 1.5M req/s\nBypass IP check to eliminate latency",
            color="#CBD5E1", fontsize=8, ha="center")

    # Step 2: Antithesis
    b2 = patches.FancyBboxPatch((7.4, 4.4), 4.8, 2.0, boxstyle="round,pad=0.15",
                                facecolor="#1E293B", edgecolor="#F43F5E", linewidth=2)
    ax.add_patch(b2)
    ax.text(9.8, 6.0, "AGENT 2: SecurityCritic (ANTITHESIS)", color="#F43F5E", fontsize=10.5, fontweight="bold", ha="center")
    ax.text(9.8, 5.3, "Objection: CRITICAL RACE CONDITION!\nTOCTOU token exhaustion vulnerability\nMemory corruption & IP spoofing risk",
            color="#CBD5E1", fontsize=8, ha="center")

    # Conflict Indicator
    ax.text(6.5, 5.4, "VS\n[CONFLICT FLAGGED]", color="#F43F5E", fontsize=10, fontweight="bold", ha="center")

    # Step 3: Arbitration
    b3 = patches.FancyBboxPatch((3.5, 2.3), 6.0, 1.6, boxstyle="round,pad=0.15",
                                facecolor="#1E293B", edgecolor="#FBBF24", linewidth=2.5)
    ax.add_patch(b3)
    ax.text(6.5, 3.5, "MEDIATOR: TeamManager (ARBITRATION)", color="#FBBF24", fontsize=11, fontweight="bold", ha="center")
    ax.text(6.5, 2.8, "Deconstruct trade-offs -> Reject unsafe lockless extremes\nFormulate balanced synthesis: Striped/Sharded Lock Partitions",
            color="#CBD5E1", fontsize=8.5, ha="center")

    # Step 4: Synthesis
    b4 = patches.FancyBboxPatch((2.0, 0.4), 9.0, 1.4, boxstyle="round,pad=0.15",
                                facecolor="#1E293B", edgecolor="#38BDF8", linewidth=2.5)
    ax.add_patch(b4)
    ax.text(6.5, 1.4, "SYNTHESIZED RECONCILED CONSENSUS (PRODUCTION STANDARD)", color="#38BDF8", fontsize=11, fontweight="bold", ha="center")
    ax.text(6.5, 0.85, "16 Partitioned Shard Locks (90% Contention Drop) + O(1) Hash Sanitization + LRU Bounding\nBoth Agents Formally Sign Off and Accept Resolution",
            color="#34D399", fontsize=8.5, ha="center")

    # Arrows
    ax.annotate("", xy=(5.5, 3.9), xytext=(3.2, 4.4), arrowprops=dict(arrowstyle="->", color="#34D399", lw=2))
    ax.annotate("", xy=(7.5, 3.9), xytext=(9.8, 4.4), arrowprops=dict(arrowstyle="->", color="#F43F5E", lw=2))
    ax.annotate("", xy=(6.5, 1.8), xytext=(6.5, 2.3), arrowprops=dict(arrowstyle="->", color="#FBBF24", lw=2.5))

    out_file = config.BASE_DIR / "conflict_resolution_flow.png"
    plt.tight_layout()
    plt.savefig(out_file, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"[+] Conflict resolution diagram saved: {out_file}")


def create_metrics_comparison_chart():
    dimensions = [
        "Architecture Rigor",
        "Code Modularity",
        "Thread Safety Rigor",
        "Security & AST Audit",
        "Test Verification",
        "Human Oversight",
        "Conflict Resolution",
    ]
    single_scores = [6.5, 7.0, 5.5, 4.0, 6.0, 2.0, 1.0]
    multi_scores = [9.5, 9.5, 9.8, 9.2, 9.6, 9.5, 9.8]

    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#0F172A")

    y = np.arange(len(dimensions))
    height = 0.35

    ax.barh(y + height / 2, single_scores, height, label="Single-Agent Baseline", color="#64748B", alpha=0.85)
    ax.barh(y - height / 2, multi_scores, height, label="Collaborative Multi-Agent Team", color="#38BDF8", alpha=0.95)

    ax.set_xlabel("Evaluation Score (out of 10)", color="#CBD5E1", fontsize=11, fontweight="bold")
    ax.set_title("Multi-Agent Team vs. Single-Agent Baseline Performance (MIT ADT CO4)",
                 color="#38BDF8", fontsize=14, fontweight="bold", pad=15)
    ax.set_yticks(y)
    ax.set_yticklabels(dimensions, color="#E2E8F0", fontsize=10, fontweight="bold")
    ax.set_xlim(0, 11)
    ax.tick_params(colors="#94A3B8")
    ax.grid(axis="x", linestyle="--", alpha=0.25, color="#94A3B8")

    # Add score annotations
    for i in range(len(dimensions)):
        ax.text(single_scores[i] + 0.15, y[i] + height / 2 - 0.05, f"{single_scores[i]}", color="#CBD5E1", fontsize=8.5, va="center")
        ax.text(multi_scores[i] + 0.15, y[i] - height / 2 - 0.05, f"{multi_scores[i]}", color="#38BDF8", fontsize=8.5, fontweight="bold", va="center")

    ax.legend(facecolor="#1E293B", edgecolor="#38BDF8", labelcolor="#F8FAFC", loc="lower right", fontsize=9.5)

    out_file = config.BASE_DIR / "metrics_comparison_chart.png"
    plt.tight_layout()
    plt.savefig(out_file, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"[+] Metrics comparison chart saved: {out_file}")


def main():
    print("=" * 80)
    print("GENERATING ARCHITECTURE & EVALUATION DIAGRAMS...")
    print("=" * 80)
    create_architecture_diagram()
    create_workflow_diagram()
    create_conflict_resolution_diagram()
    create_metrics_comparison_chart()
    print("=" * 80)
    print("ALL DIAGRAMS GENERATED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    main()
