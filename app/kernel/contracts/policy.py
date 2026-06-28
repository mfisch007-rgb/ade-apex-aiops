"""
Policy contracts for the ADE-APEX platform.

Policies define platform governance, authorization,
validation, and execution rules.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PolicyContext:
    """
    Context supplied during policy evaluation.
    """

    subject: str
    action: str
    resource: str
    tenant_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class PolicyDecision:
    """
    Result of evaluating a policy.
    """

    allowed: bool
    reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class PolicyContract(ABC):
    """
    Base contract implemented by every policy.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Policy name."""

    @abstractmethod
    async def evaluate(
        self,
        context: PolicyContext,
    ) -> PolicyDecision:
        """
        Evaluate a policy decision.
        """
