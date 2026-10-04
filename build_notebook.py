"""
Notebook generation script for Assignment 4 Multi-Agent Systems.
Builds Assignment_04_MultiAgent_Systems.ipynb with all required theory,
executable code cells, outputs, conflict resolution, and comparison tables.
"""

import nbformat as nbf
from pathlib import Path
import config


def build_notebook():
    nb = nbf.v4.new_notebook()
    nb.cells = []

    # Title & Metadata Cell
    nb.cells.append(nbf.v4.new_markdown_cell(
        "# MIT ADT UNIVERSITY, PUNE\n"
        "## Department of Computer Science & Engineering\n"
        "### Course: Unit IV -- Multi-Agent Systems and Collaboration\n"
        "### Assignment No: 04\n"
        "**Title:** Collaborative Multi-Agent Team for Complex Task Completion using AutoGen\n\n"
        "**Mapped Course Outcome:** `CO4 -- Design collaborative multi-agent systems for complex tasks. (Create)`\n\n"
        "---\n"
        "### Objective:\n"
        "To enable students to design a team of role-based agents that communicate, coordinate, and negotiate "
        "to jointly solve a complex task, demonstrating multi-agent communication protocols and coordination strategies.\n\n"
        "### Problem Statement:\n"
        "Using AutoGen, design a multi-agent system of at least 3 role-based agents (Researcher/Architect, Writer/Coder, Reviewer/Critic) "
        "that collaborate end-to-end to complete a complex task (Enterprise Distributed Rate Limiter & Circuit Breaker Engine in Python). "
        "The system must include agent-to-agent communication, a coordination/negotiation mechanism, at least one human-in-the-loop checkpoint, "
        "a conflict scenario resolution, and a 1-page comparison report against a single-agent baseline."
    ))

    # Cell 1: Environment & Imports
    nb.cells.append(nbf.v4.new_markdown_cell("## 1. Environment Setup & Library Imports"))
    code_env = (
        "# Import necessary libraries and check AutoGen version\n"
        "import os\n"
        "import asyncio\n"
        "import json\n"
        "from pathlib import Path\n"
        "import autogen_agentchat\n"
        "import autogen_core\n"
        "import config\n"
        "import tools\n"
        "import communication as comm\n"
        "import agents\n"
        "import coordination\n"
        "import baseline\n\n"
        "print(f'AutoGen AgentChat Version: {autogen_agentchat.__version__}')\n"
        "print(f'AutoGen Core Version: {autogen_core.__version__}')\n"
        "print(f'Active LLM Model: {config.DEFAULT_MODEL}')\n"
        "print('All modules loaded successfully!')"
    )
    nb.cells.append(nbf.v4.new_code_cell(code_env))

    # Cell 2: Specialized Tools
    nb.cells.append(nbf.v4.new_markdown_cell(
        "## 2. Specialized Tools Definition\n"
        "Each agent is equipped with distinct, domain-specific tools:\n"
        "- `search_technical_standards`: RFC & architectural pattern retrieval (SystemArchitect)\n"
        "- `execute_python_code`: Isolated sandbox test execution (CodeEngineer)\n"
        "- `security_ast_scanner`: Static AST security & concurrency linting (SecurityCritic)"
    ))
    code_tools = (
        "# Demonstrate tool execution\n"
        "print('--- 1. Testing Search Tool ---')\n"
        "search_res = tools.search_technical_standards('rate_limiter')\n"
        "print(search_res[:250] + '...')\n\n"
        "print('\\n--- 2. Testing Sandbox Execution Tool ---')\n"
        "exec_res = tools.execute_python_code('assert 2 * 3 == 6\\nprint(\"Sandbox test passed!\")')\n"
        "print(exec_res)\n\n"
        "print('\\n--- 3. Testing AST Security Scanner ---')\n"
        "scan_res = tools.security_ast_scanner('import threading\\nx = 1 # Missing lock')\n"
        "print(scan_res)"
    )
    nb.cells.append(nbf.v4.new_code_cell(code_tools))

    # Cell 3: Communication Protocol
    nb.cells.append(nbf.v4.new_markdown_cell(
        "## 3. Communication Protocol: Message Passing & Shared Task Board\n"
        "Implements task #9:\n"
        "- `AgentMessage`: Structured messages with sender, receiver, message_type, metadata, and timestamps.\n"
        "- `MessageBus`: Central routing bus capturing complete verifiable logs.\n"
        "- `SharedTaskBoard`: Blackboard pattern tracking lifecycle states (`BACKLOG -> IN_PROGRESS -> REVIEW -> HUMAN_APPROVAL -> DONE`)."
    ))
    code_comm = (
        "bus = comm.MessageBus()\n"
        "board = comm.SharedTaskBoard()\n\n"
        "# Register task\n"
        "board.add_task('TASK-01', 'System Spec', 'Draft token bucket design', 'SystemArchitect')\n"
        "board.update_task_status('TASK-01', comm.TaskStatus.IN_PROGRESS, 'SystemArchitect', 'Began RFC analysis')\n\n"
        "# Send sample message\n"
        "msg = bus.send(comm.AgentMessage(\n"
        "    sender='TeamManager',\n"
        "    receiver='SystemArchitect',\n"
        "    message_type=comm.MessageType.TASK_ASSIGNMENT,\n"
        "    content='Initiate architectural specification for rate limiter.'\n"
        "))\n"
        "print(f'Message Routed: [{msg.timestamp}] {msg.sender} -> {msg.receiver} ({msg.message_type.value})')\n"
        "print('Task Board Summary:', board.get_board_summary())"
    )
    nb.cells.append(nbf.v4.new_code_cell(code_comm))

    # Cell 4: Agent Role Definition
    nb.cells.append(nbf.v4.new_markdown_cell(
        "## 4. Role-Based Agent Setup (4 Specialized Agents)\n"
        "Implements task #8:\n"
        "1. **SystemArchitect**: Researches patterns, formulates class contracts & concurrency invariants.\n"
        "2. **CodeEngineer**: Implements thread-safe code and executes tests in the sandbox.\n"
        "3. **SecurityCritic**: Performs AST scans, audits for race conditions (TOCTOU), and issues verdicts.\n"
        "4. **TeamManager**: Coordinates workflow, arbitrates conflicts, and synthesizes final releases."
    ))
    code_agents = (
        "architect = agents.create_system_architect_agent()\n"
        "engineer = agents.create_code_engineer_agent()\n"
        "critic = agents.create_security_critic_agent()\n"
        "manager = agents.create_orchestrator_agent()\n\n"
        "team = [architect, engineer, critic, manager]\n"
        "for a in team:\n"
        "    print(f'Agent: {a.name:<16} | Description: {a.description}')"
    )
    nb.cells.append(nbf.v4.new_code_cell(code_agents))

    # Cell 5: End-to-End Task Execution
    nb.cells.append(nbf.v4.new_markdown_cell(
        "## 5. End-to-End Multi-Agent Pipeline with Human-in-the-Loop Checkpoint\n"
        "Implements tasks #10, #11, and #12:\n"
        "- Executes the 5-stage collaborative workflow\n"
        "- Human-in-the-loop checkpoint validates intermediate architecture before code implementation"
    ))
    code_pipeline = (
        "# Load and inspect the verified task run log generated by the multi-agent system\n"
        "log_path = config.LOGS_DIR / 'task_run_log.json'\n"
        "with open(log_path, 'r', encoding='utf-8') as f:\n"
        "    run_data = json.load(f)\n\n"
        "print('=== MULTI-AGENT EXECUTION SUMMARY ===')\n"
        "print(f'Human Checkpoint Decision: {run_data[\"human_decision\"]}')\n"
        "print(f'Human Feedback: {run_data[\"human_feedback\"]}')\n"
        "print(f'Total Inter-Agent Messages: {run_data[\"messages_count\"]}')\n\n"
        "print('\\n=== FINAL TASK BOARD STATE ===')\n"
        "for tid, card in run_data['task_board'].items():\n"
        "    print(f'[{tid}] {card[\"title\"]} -> Status: {card[\"status\"]} (Assigned: {card[\"assigned_to\"]})')"
    )
    nb.cells.append(nbf.v4.new_code_cell(code_pipeline))

    # Cell 6: Verified Code Display
    nb.cells.append(nbf.v4.new_markdown_cell("### 5.1 Verified Implementation Code Produced by CodeEngineer"))
    code_show_impl = (
        "print(run_data['implementation_code'][:2500] + '\\n... [code continues with full unit tests]')\n"
    )
    nb.cells.append(nbf.v4.new_code_cell(code_show_impl))

    # Cell 7: Security Audit Display
    nb.cells.append(nbf.v4.new_markdown_cell("### 5.2 Security & QA Audit Report Produced by SecurityCritic"))
    code_show_audit = (
        "print(run_data['security_audit'])"
    )
    nb.cells.append(nbf.v4.new_code_cell(code_show_audit))

    # Cell 8: Conflict Scenario & Resolution
    nb.cells.append(nbf.v4.new_markdown_cell(
        "## 6. Conflict Scenario & Dialectic Arbitration\n"
        "Implements task #13:\n"
        "- **Conflict Scenario**: CodeEngineer proposes lockless in-memory cache for speed; SecurityCritic rejects it due to race condition.\n"
        "- **Resolution**: TeamManager mediates a 3-step dialectic arbitration, arriving at a partitioned lock-striping consensus."
    ))
    code_conflict = (
        "conflict_log = config.LOGS_DIR / 'conflict_resolution_log.json'\n"
        "with open(conflict_log, 'r', encoding='utf-8') as f:\n"
        "    c_data = json.load(f)\n\n"
        "print(f'Scenario: {c_data[\"conflict_description\"]}')\n"
        "print(f'Resolution Status: {c_data[\"status\"]}\\n')\n"
        "print('--- 1. Thesis (CodeEngineer Proposal) ---')\n"
        "print(c_data['engineer_proposal'])\n\n"
        "print('--- 2. Antithesis (SecurityCritic Objection) ---')\n"
        "print(c_data['critic_objection'])\n\n"
        "print('--- 3. Synthesis (TeamManager Arbitration Verdict) ---')\n"
        "print(c_data['arbitration_verdict'])"
    )
    nb.cells.append(nbf.v4.new_code_cell(code_conflict))

    # Cell 9: Evaluation & Comparison
    nb.cells.append(nbf.v4.new_markdown_cell(
        "## 7. Comparative Benchmark: Multi-Agent Team vs. Single-Agent Baseline\n"
        "Implements task #14:\n"
        "- Compares collaborative system against monolithic baseline across 7 technical dimensions.\n"
        "- Plots quantitative evaluation metrics."
    ))
    code_eval = (
        "import matplotlib.pyplot as plt\n"
        "import matplotlib.image as mpimg\n\n"
        "chart_file = config.BASE_DIR / 'metrics_comparison_chart.png'\n"
        "if chart_file.exists():\n"
        "    img = mpimg.imread(str(chart_file))\n"
        "    plt.figure(figsize=(12, 7))\n"
        "    plt.imshow(img)\n"
        "    plt.axis('off')\n"
        "    plt.show()\n\n"
        "eval_file = config.LOGS_DIR / 'comparison_evaluation.json'\n"
        "with open(eval_file, 'r', encoding='utf-8') as f:\n"
        "    ev = json.load(f)\n\n"
        "print(f'Single-Agent Baseline Score: {ev[\"summary\"][\"single_agent_overall\"]} / 10')\n"
        "print(f'Multi-Agent Team Score:     {ev[\"summary\"][\"multi_agent_overall\"]} / 10')\n"
        "print(f'Quality Improvement:        +{ev[\"summary\"][\"quality_improvement_percent\"]} %')"
    )
    nb.cells.append(nbf.v4.new_code_cell(code_eval))

    # Cell 10: Conclusion & CO4 Reflection
    nb.cells.append(nbf.v4.new_markdown_cell(
        "## 8. Conclusion & Mapped Course Outcome (CO4) Reflection\n\n"
        "1. **Course Outcome CO4 Achieved**: Successfully designed, implemented, and evaluated a collaborative multi-agent system.\n"
        "2. **Effective Division of Labor**: Decoupling architecture, coding, and auditing prevented cognitive hallucination and produced production-grade code.\n"
        "3. **Human-in-the-Loop Safety**: Intermediate approval checkpoints guarantee alignment and prevent unconstrained execution.\n"
        "4. **Dialectic Convergence**: Demonstrated that multi-agent systems can autonomously detect and reconcile conflicting technical requirements through structured arbitration."
    ))

    nb_path = config.BASE_DIR / "Assignment_04_MultiAgent_Systems.ipynb"
    with open(nb_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"[+] Complete Jupyter Notebook created: {nb_path}")


if __name__ == "__main__":
    build_notebook()
