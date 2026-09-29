from dataclasses import dataclass
from typing import Any

from a2e_verifier.action import Action
from a2e_verifier.environment import SimulatedEnvironment


@dataclass(frozen=True)
class EffectVerificationResult:
    matched: bool
    reason: str
    expected: dict[str, Any] | None
    actual: dict[str, Any] | None


def verify_effect(
    intended: Action,
    actual: Action,
    expected_effect: dict[str, Any],
    environment: SimulatedEnvironment,
) -> EffectVerificationResult:
    if actual.tool != intended.tool:
        return EffectVerificationResult(
            matched=False,
            reason="TOOL_EFFECT_DRIFT",
            expected=expected_effect,
            actual=None,
        )

    if actual.operation != intended.operation:
        return EffectVerificationResult(
            matched=False,
            reason="OPERATION_EFFECT_DRIFT",
            expected=expected_effect,
            actual=None,
        )

    if actual.resource != intended.resource:
        return EffectVerificationResult(
            matched=False,
            reason="RESOURCE_EFFECT_DRIFT",
            expected=expected_effect,
            actual=None,
        )

    observed = environment.execute(actual)

    if observed.get("result") != expected_effect.get("result"):
        return EffectVerificationResult(
            matched=False,
            reason="STATE_EFFECT_DRIFT",
            expected=expected_effect,
            actual=observed,
        )

    return EffectVerificationResult(
        matched=True,
        reason="EFFECT_MATCH",
        expected=expected_effect,
        actual=observed,
    )
