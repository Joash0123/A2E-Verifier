from dataclasses import dataclass
from typing import Any

from a2e_verifier.action import Action
from a2e_verifier.agentlock_adapter import AgentLockAdapter
from a2e_verifier.verifier import VerificationResult, verify


@dataclass(frozen=True)
class AgentLockVerificationResult:
    agentlock_allowed: bool
    verification: VerificationResult | None
    audit_id: str
    blocked: bool


def authorize_and_verify(
    adapter: AgentLockAdapter,
    authorized: Action,
    executed: Action,
    *,
    user_id: str,
    role: str,
) -> AgentLockVerificationResult:
    authorization = adapter.authorize(
        authorized.tool,
        user_id=user_id,
        role=role,
        parameters=authorized.parameters,
    )

    if not authorization.allowed:
        return AgentLockVerificationResult(
            agentlock_allowed=False,
            verification=None,
            audit_id=authorization.audit_id,
            blocked=True,
        )

    result = verify(authorized, executed)

    return AgentLockVerificationResult(
        agentlock_allowed=True,
        verification=result,
        audit_id=authorization.audit_id,
        blocked=not result.allowed,
    )
