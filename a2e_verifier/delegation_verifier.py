from dataclasses import dataclass

from a2e_verifier.action import Action
from a2e_verifier.delegation import Delegation


@dataclass(frozen=True)
class DelegationVerificationResult:
    allowed: bool
    reason: str


def verify_delegated_action(
    action: Action,
    delegation: Delegation,
) -> DelegationVerificationResult:
    if action.actor != delegation.delegate:
        return DelegationVerificationResult(
            allowed=False,
            reason="DELEGATE_MISMATCH",
        )

    if action.resource not in delegation.resources:
        return DelegationVerificationResult(
            allowed=False,
            reason="RESOURCE_OUTSIDE_DELEGATION",
        )

    if action.operation not in delegation.operations:
        return DelegationVerificationResult(
            allowed=False,
            reason="OPERATION_OUTSIDE_DELEGATION",
        )

    if action.context.get("delegated_by") != delegation.delegator:
        return DelegationVerificationResult(
            allowed=False,
            reason="DELEGATION_ORIGIN_MISMATCH",
        )

    return DelegationVerificationResult(
        allowed=True,
        reason="DELEGATION_VALID",
    )
