"""
Baseline module for Assignment 4 Multi-Agent Systems.
Implements the Single-Agent Baseline to provide an empirical, reproducible
benchmark against the Collaborative Multi-Agent Team.
"""

import asyncio
from typing import Dict, Any
import config
from autogen_agentchat.agents import AssistantAgent


def create_monolithic_single_agent(model_client=None) -> AssistantAgent:
    """
    Creates a single general-purpose agent expected to solve research,
    architecture, coding, security auditing, and documentation in a single step.
    """
    if model_client is None:
        model_client = config.get_model_client(model=config.DEFAULT_MODEL)

    system_message = (
        "You are an AI software assistant. Given a task, do your best to research, "
        "design, code, audit security, and document everything in a single response."
    )

    return AssistantAgent(
        name="SingleAgentBaseline",
        model_client=model_client,
        system_message=system_message,
        tools=[],  # Baseline lacks dedicated multi-agent tool specialization
        description="Monolithic single-agent baseline without role division or collaborative peer review.",
    )


async def run_single_agent_baseline(task_prompt: str) -> Dict[str, Any]:
    """
    Executes the single-agent baseline on the exact same complex task.
    """
    agent = create_monolithic_single_agent()
    prompt = (
        f"Objective: {task_prompt}\n\n"
        "Please provide the complete end-to-end solution including:\n"
        "1. Architectural design\n"
        "2. Complete Python implementation\n"
        "3. Security and concurrency audit\n"
        "4. Unit tests and verification notes."
    )

    res = await agent.run(task=prompt)
    output = res.messages[-1].content

    return {
        "agent_name": "SingleAgentBaseline",
        "task_prompt": task_prompt,
        "output": output,
    }
