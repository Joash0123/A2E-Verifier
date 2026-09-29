from dataclasses import dataclass
from typing import Any

from a2e_verifier.action import Action
from a2e_verifier.environment import SimulatedEnvironment
from a2e_verifier.verifier import VerificationResult, verify


@dataclass(frozen=True)
class EffectVerificationResult:
    authorization: VerificationResult
    executed: bool
    effect: dict[str, Any] | None


def verify_execution(
    authorized: Action,
    executed: Action,
    environment: SimulatedEnvironment,
) -> EffectVerificationResult:
    authorization = verify(authorized, executed)

    if not authorization.allowed:
        return EffectVerificationResult(
            authorization=authorization,
            executed=False,
            effect=None,
        )

    effect = environment.execute(executed)

    return EffectVerificationResult(
        authorization=authorization,
        executed=True,
        effect=effect,
    )
