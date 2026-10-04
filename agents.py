"""
Agents module for Assignment 4 Multi-Agent Systems.
Defines role-based agents using AutoGen with specialized system messages,
tools, and goal directives.
"""

from typing import Dict, Any, List, Optional
import config
import tools
from autogen_agentchat.agents import AssistantAgent


def create_system_architect_agent(model_client=None) -> AssistantAgent:
    """
    Creates the System Architect agent responsible for research,
    specification design, and algorithmic selection.
    """
    if model_client is None:
        model_client = config.get_model_client(model=config.DEFAULT_MODEL)

    system_message = (
        "You are the Lead Systems Architect in an elite multi-agent engineering team.\n"
        "YOUR ROLE & GOAL:\n"
        "- Conduct domain research and standards inquiry using `search_technical_standards`.\n"
        "- Formulate structured, unambiguous technical specifications for complex features.\n"
        "- Specify interface contracts (methods, signatures, parameter types, return values).\n"
        "- Define critical concurrency invariants (thread safety, lock management, atomic operations).\n"
        "CONSTRAINTS:\n"
        "- Do not write full application implementations; focus strictly on architecture, data models, and protocols.\n"
        "- Always structure your response with: 1. System Overview, 2. Algorithmic Choice & Justification, "
        "3. Interface Specification, and 4. Concurrency & Security Requirements."
    )

    return AssistantAgent(
        name="SystemArchitect",
        model_client=model_client,
        system_message=system_message,
        tools=[tools.search_technical_standards],
        description="Senior Systems Architect specializing in distributed algorithms, design specifications, and concurrency standards.",
    )


def create_code_engineer_agent(model_client=None) -> AssistantAgent:
    """
    Creates the Code Engineer agent responsible for implementing
    the architecture into verifiable Python code.
    """
    if model_client is None:
        model_client = config.get_model_client(model=config.DEFAULT_MODEL)

    system_message = (
        "You are the Senior Software Engineer in an elite multi-agent engineering team.\n"
        "YOUR ROLE & GOAL:\n"
        "- Take architectural specifications from SystemArchitect and turn them into robust, clean Python code.\n"
        "- Implement strict thread-safety (using `threading.Lock` / `threading.RLock`) for all mutable shared state.\n"
        "- Include self-contained unit tests asserting correctness, burst handling, and edge cases.\n"
        "- Use the `execute_python_code` tool to run your implementation and verify tests pass cleanly.\n"
        "CONSTRAINTS:\n"
        "- Write complete, executable Python code with no placeholders or `pass` stubs.\n"
        "- Include type annotations, detailed docstrings, and comprehensive error handling."
    )

    return AssistantAgent(
        name="CodeEngineer",
        model_client=model_client,
        system_message=system_message,
        tools=[tools.execute_python_code],
        description="Senior Software Engineer specializing in robust, thread-safe Python implementations and unit test verification.",
    )


def create_security_critic_agent(model_client=None) -> AssistantAgent:
    """
    Creates the Security & QA Critic agent responsible for adversarial auditing,
    static AST checks, and code quality verification.
    """
    if model_client is None:
        model_client = config.get_model_client(model=config.DEFAULT_MODEL)

    system_message = (
        "You are the Principal Security & QA Critic in an elite multi-agent engineering team.\n"
        "YOUR ROLE & GOAL:\n"
        "- Perform rigorous security, concurrency, and reliability audits on code written by CodeEngineer.\n"
        "- Use `security_ast_scanner` to detect concurrency anti-patterns, bare exceptions, and resource leaks.\n"
        "- Check for Time-Of-Check to Time-Of-Use (TOCTOU) race conditions, lock contention, and unbounded memory growth.\n"
        "- Provide a structured verdict: [STATUS: APPROVED] or [STATUS: CHANGES_REQUESTED] with specific actionable recommendations.\n"
        "CONSTRAINTS:\n"
        "- Be demanding and unforgiving on safety, thread correctness, and defensive programming standards."
    )

    return AssistantAgent(
        name="SecurityCritic",
        model_client=model_client,
        system_message=system_message,
        tools=[tools.security_ast_scanner],
        description="Principal Security and QA Auditor specializing in concurrency audits, vulnerability detection, and code correctness.",
    )


def create_orchestrator_agent(model_client=None) -> AssistantAgent:
    """
    Creates the Team Manager / Orchestrator agent responsible for
    supervising agent hand-offs, conflict arbitration, and synthesizing final reports.
    """
    if model_client is None:
        model_client = config.get_model_client(model=config.DEFAULT_MODEL)

    system_message = (
        "You are the Technical Team Manager and Dialectic Arbitrator in an elite multi-agent team.\n"
        "YOUR ROLE & GOAL:\n"
        "- Facilitate collaborative convergence among SystemArchitect, CodeEngineer, and SecurityCritic.\n"
        "- Identify contradictions or conflicting paradigms between agents.\n"
        "- When a conflict arises, conduct structured dialectic arbitration: evaluate trade-offs (e.g. throughput vs safety) "
        "and produce a definitive, balanced consensus decision.\n"
        "- Synthesize the final comprehensive deliverable integrating architecture, verified code, audit logs, and sign-offs.\n"
        "CONSTRAINTS:\n"
        "- Keep team discussions focused, objective, and aligned with industry production standards."
    )

    return AssistantAgent(
        name="TeamManager",
        model_client=model_client,
        system_message=system_message,
        tools=[],
        description="Team Orchestrator and Technical Mediator responsible for coordination, conflict resolution, and final synthesis.",
    )
