"""
Communication module for Assignment 4 Multi-Agent Systems.
Implements:
1. Agent Communication Protocol: Structured Message Passing with message types, metadata, and routing.
2. Shared Task Board (Blackboard Pattern): Centralized collaborative task state management.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
import json
import uuid


class MessageType(str, Enum):
    TASK_ASSIGNMENT = "TASK_ASSIGNMENT"
    PROPOSAL = "PROPOSAL"
    CODE_ARTIFACT = "CODE_ARTIFACT"
    CRITIQUE_FEEDBACK = "CRITIQUE_FEEDBACK"
    HUMAN_INTERVENTION = "HUMAN_INTERVENTION"
    CONFLICT_NOTIFICATION = "CONFLICT_NOTIFICATION"
    ARBITRATION_RULING = "ARBITRATION_RULING"
    STATUS_UPDATE = "STATUS_UPDATE"
    SYSTEM_NOTIFICATION = "SYSTEM_NOTIFICATION"


class TaskStatus(str, Enum):
    BACKLOG = "BACKLOG"
    IN_PROGRESS = "IN_PROGRESS"
    REVIEW_PENDING = "REVIEW_PENDING"
    AWAITING_HUMAN_APPROVAL = "AWAITING_HUMAN_APPROVAL"
    APPROVED = "APPROVED"
    REVISION_REQUESTED = "REVISION_REQUESTED"
    COMPLETED = "COMPLETED"
    CONFLICT_FLAGGED = "CONFLICT_FLAGGED"


@dataclass
class AgentMessage:
    sender: str
    receiver: str
    message_type: MessageType
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    message_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["message_type"] = self.message_type.value
        return data


@dataclass
class TaskCard:
    task_id: str
    title: str
    description: str
    assigned_to: str
    status: TaskStatus = TaskStatus.BACKLOG
    artifacts: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, str]] = field(default_factory=list)

    def transition(self, new_status: TaskStatus, actor: str, note: str = ""):
        old_status = self.status
        self.status = new_status
        self.history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "actor": actor,
            "transition": f"{old_status.value} -> {new_status.value}",
            "note": note,
        })


class MessageBus:
    """
    Message Passing Bus for multi-agent coordination.
    Stores complete verifiable conversation traces and dispatches messages to subscribers.
    """
    def __init__(self):
        self.messages: List[AgentMessage] = []
        self._subscribers: Dict[str, List[Callable[[AgentMessage], None]]] = {}

    def subscribe(self, agent_name: str, callback: Callable[[AgentMessage], None]):
        if agent_name not in self._subscribers:
            self._subscribers[agent_name] = []
        self._subscribers[agent_name].append(callback)

    def send(self, message: AgentMessage) -> AgentMessage:
        self.messages.append(message)
        # Notify direct receiver and broadcast subscribers
        targets = [message.receiver]
        if message.receiver == "ALL":
            targets = list(self._subscribers.keys())

        for target in targets:
            if target in self._subscribers:
                for cb in self._subscribers[target]:
                    cb(message)
        return message

    def get_conversation_history(self, filter_sender: Optional[str] = None, filter_receiver: Optional[str] = None) -> List[AgentMessage]:
        res = self.messages
        if filter_sender:
            res = [m for m in res if m.sender == filter_sender]
        if filter_receiver:
            res = [m for m in res if m.receiver in (filter_receiver, "ALL")]
        return res

    def export_json(self) -> str:
        return json.dumps([m.to_dict() for m in self.messages], indent=2)

    def export_markdown_log(self) -> str:
        lines = ["# Multi-Agent Communication Trace Log\n"]
        for idx, m in enumerate(self.messages, 1):
            lines.append(f"### Message #{idx} [{m.timestamp}]")
            lines.append(f"- **Sender**: `{m.sender}`")
            lines.append(f"- **Receiver**: `{m.receiver}`")
            lines.append(f"- **Type**: `{m.message_type.value}`")
            if m.metadata:
                lines.append(f"- **Metadata**: `{m.metadata}`")
            lines.append(f"\n```markdown\n{m.content}\n```\n")
            lines.append("---\n")
        return "\n".join(lines)


class SharedTaskBoard:
    """
    Blackboard Architecture: Shared Task Board accessed and mutated by collaborating agents.
    """
    def __init__(self):
        self.tasks: Dict[str, TaskCard] = {}

    def add_task(self, task_id: str, title: str, description: str, assigned_to: str) -> TaskCard:
        card = TaskCard(task_id=task_id, title=title, description=description, assigned_to=assigned_to)
        self.tasks[task_id] = card
        return card

    def update_task_status(self, task_id: str, new_status: TaskStatus, actor: str, note: str = ""):
        if task_id in self.tasks:
            self.tasks[task_id].transition(new_status, actor=actor, note=note)

    def attach_artifact(self, task_id: str, artifact_name: str, artifact_data: Any):
        if task_id in self.tasks:
            self.tasks[task_id].artifacts[artifact_name] = artifact_data

    def get_board_summary(self) -> Dict[str, Any]:
        return {
            task_id: {
                "title": card.title,
                "assigned_to": card.assigned_to,
                "status": card.status.value,
                "artifacts_count": len(card.artifacts),
                "history_length": len(card.history),
            }
            for task_id, card in self.tasks.items()
        }
