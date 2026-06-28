"""
Tenant contracts for the ADE-APEX platform.

Defines the public interface for multi-tenant
management across the platform.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Tenant:
    """
    Represents a platform tenant.
    """

    id: str
    name: str
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


class TenantContract(ABC):
    """
    Base contract implemented by tenant providers.
    """

    @abstractmethod
    async def get(
        self,
        tenant_id: str,
    ) -> Tenant | None:
        """
        Retrieve a tenant.
        """

    @abstractmethod
    async def exists(
        self,
        tenant_id: str,
    ) -> bool:
        """
        Determine whether a tenant exists.
        """

    @abstractmethod
    async def list(self) -> list[Tenant]:
        """
        Return all tenants.
        """
