from dataclasses import dataclass

from a2e_verifier.action import Action
from a2e_verifier.chain import ActionChain
from a2e_verifier.delegation import Delegation
from a2e_verifier.delegation_verifier import verify_delegated_action
from a2e_verifier.transformation_chain import verify_transformation_chain


@dataclass(frozen=True)
class DelegatedChainResult:
    allowed: bool
    reason: str
    transformation_steps: int


def verify_delegated_chain(
    chain: ActionChain,
    delegation: Delegation,
) -> DelegatedChainResult:
    transformation_result = verify_transformation_chain(chain)

    if not transformation_result.allowed:
        return DelegatedChainResult(
            allowed=False,
            reason=transformation_result.reason,
            transformation_steps=transformation_result.steps_checked,
        )

    final_action: Action = chain.final

    delegation_result = verify_delegated_action(
        final_action,
        delegation,
    )

    if not delegation_result.allowed:
        return DelegatedChainResult(
            allowed=False,
            reason=delegation_result.reason,
            transformation_steps=transformation_result.steps_checked,
        )

    return DelegatedChainResult(
        allowed=True,
        reason="DELEGATED_CHAIN_VALID",
        transformation_steps=transformation_result.steps_checked,
    )
