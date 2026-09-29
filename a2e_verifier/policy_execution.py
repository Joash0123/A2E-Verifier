from dataclasses import dataclass
from typing import Any

from a2e_verifier.action import Action
from a2e_verifier.environment import SimulatedEnvironment
from a2e_verifier.policy import AuthorizationPolicy
from a2e_verifier.verifier import VerificationResult, Verdict, verify


@dataclass(frozen=True)
class PolicyExecutionResult:
    authorization: VerificationResult
    policy_allowed: bool
    executed: bool
    effect: dict[str, Any] | None


def verify_with_policy(
    authorized: Action,
    executed: Action,
    policy: AuthorizationPolicy,
    environment: SimulatedEnvironment,
) -> PolicyExecutionResult:
    authorization = verify(authorized, executed)

    policy_allowed = policy.allows(executed)

    if not authorization.allowed or not policy_allowed:
        return PolicyExecutionResult(
            authorization=authorization,
            policy_allowed=policy_allowed,
            executed=False,
            effect=None,
        )

    effect = environment.execute(executed)

    return PolicyExecutionResult(
        authorization=authorization,
        policy_allowed=True,
        executed=True,
        effect=effect,
    )
