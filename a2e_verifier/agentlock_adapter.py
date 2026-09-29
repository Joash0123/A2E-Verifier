from dataclasses import dataclass
from typing import Any, Callable

from agentlock import AgentLockPermissions, AuthorizationGate, ExecutionToken


@dataclass(frozen=True)
class AgentLockAuthorization:
    allowed: bool
    token: ExecutionToken | None
    audit_id: str
    denial: dict[str, Any] | None


class AgentLockAdapter:
    """Thin adapter connecting AgentLock authorization to A2E."""

    def __init__(self) -> None:
        self.gate = AuthorizationGate()

    def register_tool(
        self,
        tool_name: str,
        permissions: AgentLockPermissions,
    ) -> None:
        self.gate.register_tool(tool_name, permissions)

    def authorize(
        self,
        tool_name: str,
        *,
        user_id: str,
        role: str,
        parameters: dict[str, Any] | None = None,
    ) -> AgentLockAuthorization:
        result = self.gate.authorize(
            tool_name,
            user_id=user_id,
            role=role,
            parameters=parameters,
        )

        return AgentLockAuthorization(
            allowed=result.allowed,
            token=result.token,
            audit_id=result.audit_id,
            denial=result.denial,
        )

    def execute(
        self,
        tool_name: str,
        func: Callable[..., Any],
        *,
        token: ExecutionToken,
        parameters: dict[str, Any] | None = None,
    ) -> Any:
        return self.gate.execute(
            tool_name,
            func,
            token=token,
            parameters=parameters,
        )
