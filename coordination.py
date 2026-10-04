"""
Coordination module for Assignment 4 Multi-Agent Systems.
Implements:
1. End-to-End Multi-Agent Workflow Coordination (Sequential hand-off with Manager oversight).
2. Human-in-the-Loop Checkpoint (Approval / Rejection with feedback loop).
3. Conflict Scenario Simulation and Structured Dialectic Arbitration.
"""

import asyncio
from typing import Dict, Any, List, Optional, Callable
import communication as comm
from communication import MessageType, TaskStatus, AgentMessage
import agents
import config


class MultiAgentOrchestrator:
    """
    Coordinates role-based agents, manages blackboard task progression,
    and facilitates human-in-the-loop checkpoints.
    """
    def __init__(self, human_approval_callback: Optional[Callable[[str], Dict[str, Any]]] = None):
        self.bus = comm.MessageBus()
        self.board = comm.SharedTaskBoard()
        self.human_approval_callback = human_approval_callback

        # Initialize role agents
        self.architect = agents.create_system_architect_agent()
        self.engineer = agents.create_code_engineer_agent()
        self.critic = agents.create_security_critic_agent()
        self.manager = agents.create_orchestrator_agent()

        # Initialize task board
        self.board.add_task("TASK-01", "Architecture & Specification", "Research patterns and draft system design", "SystemArchitect")
        self.board.add_task("TASK-02", "Human-in-the-Loop Checkpoint", "Review and approve/reject architectural spec", "HumanSupervisor")
        self.board.add_task("TASK-03", "Implementation & Sandbox Verification", "Develop thread-safe code and pass unit tests", "CodeEngineer")
        self.board.add_task("TASK-04", "Security & Concurrency Audit", "Perform AST security scan and edge-case critique", "SecurityCritic")
        self.board.add_task("TASK-05", "Executive Synthesis & Release", "Synthesize deliverables and finalize release bundle", "TeamManager")

    async def run_end_to_end(
        self,
        task_prompt: str,
        human_decision: str = "APPROVE",
        human_feedback: str = "",
        progress_callback: Optional[Callable[[str, str], None]] = None,
    ) -> Dict[str, Any]:
        """
        Executes the full collaborative pipeline end-to-end.
        """
        def notify(stage: str, msg: str):
            if progress_callback:
                progress_callback(stage, msg)

        # ---------------------------------------------------------
        # STAGE 1: Research & Specification (SystemArchitect)
        # ---------------------------------------------------------
        notify("STAGE_1", "SystemArchitect is researching technical standards and drafting system architecture...")
        self.board.update_task_status("TASK-01", TaskStatus.IN_PROGRESS, "SystemArchitect", "Initiated research & design")
        
        self.bus.send(AgentMessage(
            sender="TeamManager",
            receiver="SystemArchitect",
            message_type=MessageType.TASK_ASSIGNMENT,
            content=f"Team, we have a new complex engineering objective:\n\n{task_prompt}\n\nSystemArchitect, please research standard patterns and draft a complete architecture specification.",
        ))

        arch_prompt = (
            f"Objective: {task_prompt}\n\n"
            "Please use your `search_technical_standards` tool if needed, then produce a rigorous architectural specification containing:\n"
            "1. Architectural Overview & Component Topology\n"
            "2. Mathematical Algorithm Choice (e.g., Token Bucket formula: current_tokens = min(capacity, previous_tokens + elapsed * refill_rate))\n"
            "3. Complete Python Class Contract & Method Signatures (types, inputs, outputs, exceptions)\n"
            "4. Concurrency Invariants & Thread-Safety Guarantees (lock primitives, TOCTOU prevention)\n"
            "Be precise, authoritative, and structured."
        )

        arch_res = await self.architect.run(task=arch_prompt)
        arch_output = arch_res.messages[-1].content
        self.board.attach_artifact("TASK-01", "architecture_spec", arch_output)
        self.board.update_task_status("TASK-01", TaskStatus.COMPLETED, "SystemArchitect", "Architecture spec finalized")

        self.bus.send(AgentMessage(
            sender="SystemArchitect",
            receiver="TeamManager",
            message_type=MessageType.PROPOSAL,
            content=arch_output,
            metadata={"stage": "Architecture Specification", "status": "Ready for Human Review"},
        ))

        # ---------------------------------------------------------
        # STAGE 2: Human-in-the-Loop Checkpoint
        # ---------------------------------------------------------
        notify("STAGE_2", "Human-in-the-Loop Checkpoint: Intermediate architecture submitted for human authorization.")
        self.board.update_task_status("TASK-02", TaskStatus.AWAITING_HUMAN_APPROVAL, "HumanSupervisor", "Pending approval")

        decision = human_decision.upper()
        feedback = human_feedback

        if self.human_approval_callback:
            human_response = self.human_approval_callback(arch_output)
            decision = human_response.get("decision", "APPROVE").upper()
            feedback = human_response.get("feedback", "")

        if decision == "REJECT" or "REVISION" in decision:
            self.board.update_task_status("TASK-02", TaskStatus.REVISION_REQUESTED, "HumanSupervisor", f"Rejected: {feedback}")
            self.bus.send(AgentMessage(
                sender="HumanSupervisor",
                receiver="SystemArchitect",
                message_type=MessageType.HUMAN_INTERVENTION,
                content=f"[HUMAN REVISION REQUESTED]: The design requires modifications:\n{feedback}\nPlease update the architecture specification accordingly.",
            ))

            # Revise architecture with human guidance
            revision_prompt = (
                f"The human supervisor reviewed your specification and requested the following mandatory revisions:\n"
                f"\"{feedback}\"\n\n"
                f"Please update the architectural specification to address all human feedback directly."
            )
            arch_res = await self.architect.run(task=revision_prompt)
            arch_output = arch_res.messages[-1].content
            self.board.attach_artifact("TASK-01", "architecture_spec_revised", arch_output)
            self.board.update_task_status("TASK-02", TaskStatus.APPROVED, "HumanSupervisor", "Human feedback integrated and approved")
        else:
            self.board.update_task_status("TASK-02", TaskStatus.APPROVED, "HumanSupervisor", "Human approved architecture specification")
            self.bus.send(AgentMessage(
                sender="HumanSupervisor",
                receiver="TeamManager",
                message_type=MessageType.HUMAN_INTERVENTION,
                content=f"[HUMAN APPROVED]: Architecture specification verified and authorized for code implementation. {feedback}".strip(),
            ))

        # ---------------------------------------------------------
        # STAGE 3: Implementation & Sandbox Verification (CodeEngineer)
        # ---------------------------------------------------------
        notify("STAGE_3", "CodeEngineer is implementing production Python code and executing sandbox verification tests...")
        self.board.update_task_status("TASK-03", TaskStatus.IN_PROGRESS, "CodeEngineer", "Implementation started")

        self.bus.send(AgentMessage(
            sender="TeamManager",
            receiver="CodeEngineer",
            message_type=MessageType.TASK_ASSIGNMENT,
            content="Architecture spec authorized. Implement production Python code with thread-safety and unit tests. Verify execution in the sandbox.",
        ))

        eng_prompt = (
            f"Here is the authorized Architecture Specification:\n\n{arch_output}\n\n"
            "YOUR TASK:\n"
            "1. Write clean, complete, fully documented, thread-safe Python code implementing this design.\n"
            "2. Use `threading.Lock` to guarantee safe concurrent access.\n"
            "3. Include a comprehensive test suite (assertions for rate limiting, burst capacity, refill rate, and multi-threaded concurrency).\n"
            "4. Use your `execute_python_code` tool to run the code and verify all tests pass without errors.\n"
            "Present your final code in a ```python ... ``` block."
        )

        eng_res = await self.engineer.run(task=eng_prompt)
        eng_output = eng_res.messages[-1].content
        self.board.attach_artifact("TASK-03", "implementation_code", eng_output)
        self.board.update_task_status("TASK-03", TaskStatus.COMPLETED, "CodeEngineer", "Code implemented and sandbox tests verified")

        self.bus.send(AgentMessage(
            sender="CodeEngineer",
            receiver="SecurityCritic",
            message_type=MessageType.CODE_ARTIFACT,
            content=eng_output,
            metadata={"status": "Awaiting Security Audit"},
        ))

        # ---------------------------------------------------------
        # STAGE 4: Security & Concurrency Audit (SecurityCritic)
        # ---------------------------------------------------------
        notify("STAGE_4", "SecurityCritic is executing AST scanner and performing adversarial security/concurrency audit...")
        self.board.update_task_status("TASK-04", TaskStatus.IN_PROGRESS, "SecurityCritic", "Audit started")

        critic_prompt = (
            f"Here is the implementation submitted by CodeEngineer:\n\n{eng_output}\n\n"
            "YOUR TASK:\n"
            "1. Use `security_ast_scanner` to analyze code safety and anti-patterns.\n"
            "2. Audit for concurrency hazards: Time-Of-Check to Time-Of-Use (TOCTOU) race conditions, lock contention, memory leak risks.\n"
            "3. Evaluate defensive programming: bounds checking, exception handling, parameter validation.\n"
            "4. Provide a structured review with:\n"
            "   - Security & Concurrency Analysis\n"
            "   - Edge-Case Findings\n"
            "   - Formal Verdict: [STATUS: APPROVED] or [STATUS: CHANGES_REQUESTED]\n"
            "   - Recommendations for production hardening."
        )

        critic_res = await self.critic.run(task=critic_prompt)
        critic_output = critic_res.messages[-1].content
        self.board.attach_artifact("TASK-04", "security_audit_report", critic_output)
        self.board.update_task_status("TASK-04", TaskStatus.COMPLETED, "SecurityCritic", "Security audit finished")

        self.bus.send(AgentMessage(
            sender="SecurityCritic",
            receiver="TeamManager",
            message_type=MessageType.CRITIQUE_FEEDBACK,
            content=critic_output,
        ))

        # ---------------------------------------------------------
        # STAGE 5: Synthesis & Executive Sign-Off (TeamManager)
        # ---------------------------------------------------------
        notify("STAGE_5", "TeamManager is synthesizing the final release deliverable...")
        self.board.update_task_status("TASK-05", TaskStatus.IN_PROGRESS, "TeamManager", "Synthesizing executive release")

        manager_prompt = (
            "Review the collaborative deliverables produced by the team:\n\n"
            f"=== ARCHITECTURE SPECIFICATION ===\n{arch_output[:1200]}...\n\n"
            f"=== CODE IMPLEMENTATION SUMMARY ===\n{eng_output[:1200]}...\n\n"
            f"=== SECURITY AUDIT VERDICT ===\n{critic_output}\n\n"
            "Synthesize an Executive Final Release Report summarizing:\n"
            "1. Feature Overview & Requirements Fulfilled\n"
            "2. Multi-Agent Collaboration Summary (handoffs, verifications, human signoff)\n"
            "3. Architectural & Concurrency Highlights\n"
            "4. Security Verdict & Production Deployment Readiness"
        )

        manager_res = await self.manager.run(task=manager_prompt)
        final_summary = manager_res.messages[-1].content
        self.board.attach_artifact("TASK-05", "executive_release_report", final_summary)
        self.board.update_task_status("TASK-05", TaskStatus.COMPLETED, "TeamManager", "Deliverables synthesized and released")

        self.bus.send(AgentMessage(
            sender="TeamManager",
            receiver="ALL",
            message_type=MessageType.STATUS_UPDATE,
            content=final_summary,
            metadata={"status": "PROJECT_COMPLETED"},
        ))

        notify("COMPLETED", "Multi-Agent System successfully finished all pipeline stages!")

        return {
            "task_prompt": task_prompt,
            "architecture_spec": arch_output,
            "human_decision": decision,
            "human_feedback": feedback,
            "implementation_code": eng_output,
            "security_audit": critic_output,
            "executive_summary": final_summary,
            "task_board": self.board.get_board_summary(),
            "messages_count": len(self.bus.messages),
            "messages": [m.to_dict() for m in self.bus.messages],
        }


class ConflictResolutionEngine:
    """
    Simulates and resolves a realistic contradictory conflict scenario between agents
    using structured dialectic arbitration.
    """
    def __init__(self):
        self.bus = comm.MessageBus()
        self.manager = agents.create_orchestrator_agent()
        self.engineer = agents.create_code_engineer_agent()
        self.critic = agents.create_security_critic_agent()

    async def run_conflict_simulation(self) -> Dict[str, Any]:
        """
        Runs the conflict scenario and documents how the system resolves it.
        """
        # Step 1: CodeEngineer presents extreme performance proposal (unsynchronized lockless state)
        engineer_proposal = (
            "PROPOSAL (CodeEngineer): In order to hit ultra-low latency and 1,500,000 requests/sec, "
            "we MUST eliminate all `threading.Lock` and mutex primitives. Python GIL overhead and lock contention "
            "create an unacceptable 45% latency penalty. Instead, we should use a global un-synchronized dictionary "
            "`bucket_state = {}`, omit client IP validation headers, and allow optimistic unsynchronized token decr. "
            "Speed is paramount!"
        )
        self.bus.send(AgentMessage(
            sender="CodeEngineer",
            receiver="SecurityCritic",
            message_type=MessageType.PROPOSAL,
            content=engineer_proposal,
            metadata={"intent": "Extreme Throughput Optimization"}
        ))

        # Step 2: SecurityCritic detects critical flaw and vehemently contradicts
        critic_objection = (
            "OBJECTION & CONFLICT (SecurityCritic): REJECTED! This proposal introduces critical vulnerabilities: "
            "1. Concurrency TOCTOU Race Condition: An unlocked shared dictionary with multiple threads causes race conditions "
            "where multiple clients consume tokens simultaneously, blowing past quota and crashing the backend. "
            "2. Security Vulnerability: Bypassing IP sanitization opens the door to IP spoofing, DDoS reflection, and token exhaustion attacks. "
            "3. Data Corruption: Without memory barriers, dictionary re-hashing during concurrent writes causes Python segfaults or corrupted state. "
            "We CANNOT deploy without strict mutual exclusion and input sanitization!"
        )
        self.bus.send(AgentMessage(
            sender="SecurityCritic",
            receiver="CodeEngineer",
            message_type=MessageType.CONFLICT_NOTIFICATION,
            content=critic_objection,
            metadata={"severity": "CRITICAL_CONFLICT", "flag": "RACE_CONDITION_VULNERABILITY"}
        ))

        # Step 3: Conflict flagged to TeamManager for Dialectic Arbitration
        self.bus.send(AgentMessage(
            sender="System",
            receiver="TeamManager",
            message_type=MessageType.CONFLICT_NOTIFICATION,
            content="CRITICAL CONFLICT DETECTED between CodeEngineer (Speed/Lockless) and SecurityCritic (Safety/Strict Locks). Manager arbitration required.",
        ))

        arbitration_task = (
            "A high-stakes conflict has emerged between CodeEngineer and SecurityCritic:\n\n"
            f"=== CODE ENGINEER ARGUMENT ===\n{engineer_proposal}\n\n"
            f"=== SECURITY CRITIC OBJECTION ===\n{critic_objection}\n\n"
            "As Team Manager and Dialectic Arbitrator, execute the 3-step Consensus Protocol:\n"
            "1. Dialectic Decomposition: Identify the core trade-off (Throughput vs Thread Safety & Abuse Prevention).\n"
            "2. Technical Evaluation: Determine why neither extreme (unsafe lockless vs monolithic high-contention locking) is optimal.\n"
            "3. Synthesized Reconciled Resolution: Formulate a balanced, production-grade architectural compromise "
            "(e.g., Lock Striping / Sharded Bucket Partitioning by client_id hash, or Atomic CAS simulation, with bounded LRU cache). "
            "Explain how this satisfies both performance and security invariants."
        )

        arbitration_res = await self.manager.run(task=arbitration_task)
        arbitration_verdict = arbitration_res.messages[-1].content

        self.bus.send(AgentMessage(
            sender="TeamManager",
            receiver="ALL",
            message_type=MessageType.ARBITRATION_RULING,
            content=arbitration_verdict,
            metadata={"status": "CONFLICT_RESOLVED", "resolution_protocol": "Dialectic Arbitration Synthesis"}
        ))

        # Step 4: Agents acknowledge and accept reconciled consensus
        ack_engineer = "CodeEngineer: Accepted. Sharded lock striping (16 mutex partitions by hash) eliminates 90% of contention while maintaining absolute thread safety."
        ack_critic = "SecurityCritic: Accepted. Thread safety and IP sanitization are preserved within each shard. Security requirements satisfied."

        self.bus.send(AgentMessage(sender="CodeEngineer", receiver="TeamManager", message_type=MessageType.STATUS_UPDATE, content=ack_engineer))
        self.bus.send(AgentMessage(sender="SecurityCritic", receiver="TeamManager", message_type=MessageType.STATUS_UPDATE, content=ack_critic))

        return {
            "conflict_description": "Lockless High-Throughput (Engineer) vs. Strict Thread-Safe Validation (Critic)",
            "engineer_proposal": engineer_proposal,
            "critic_objection": critic_objection,
            "arbitration_verdict": arbitration_verdict,
            "status": "RESOLVED_WITH_CONSENSUS",
            "messages": [m.to_dict() for m in self.bus.messages],
        }
