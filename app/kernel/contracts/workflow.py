"""
Workflow contracts for the ADE-APEX platform.

Workflows coordinate multiple agents, plugins and services into
repeatable execution pipelines.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(slots=True)
class WorkflowContext:
    """
    Shared execution context for a workflow.
    """

    workflow_id: str
    variables: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class WorkflowContract(ABC):
    """
    Base contract implemented by all ADE-APEX workflows.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Workflow name."""

    @abstractmethod
    async def execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowStatus:
        """
        Execute the workflow.
        """

    @abstractmethod
    async def cancel(self) -> None:
        """
        Cancel workflow execution.
        """
