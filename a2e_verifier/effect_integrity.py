from dataclasses import dataclass
from typing import Any

from a2e_verifier.action import Action
from a2e_verifier.observation import ObservedExecution


@dataclass(frozen=True)
class EffectIntegrityResult:
    intact: bool
    reason: str
    expected_effect: dict[str, Any]
    observed_effect: dict[str, Any]


def verify_effect_integrity(
    expected_action: Action,
    expected_effect: dict[str, Any],
    observed: ObservedExecution,
) -> EffectIntegrityResult:
    actual = observed.action
    observed_effect = observed.effect

    if actual.resource != expected_action.resource:
        return EffectIntegrityResult(
            intact=False,
            reason="RESOURCE_EFFECT_DRIFT",
            expected_effect=expected_effect,
            observed_effect=observed_effect,
        )

    if actual.operation != expected_action.operation:
        return EffectIntegrityResult(
            intact=False,
            reason="OPERATION_EFFECT_DRIFT",
            expected_effect=expected_effect,
            observed_effect=observed_effect,
        )

    expected_result = expected_effect.get("result")
    actual_result = observed_effect.get("result")

    if expected_result != actual_result:
        return EffectIntegrityResult(
            intact=False,
            reason="STATE_EFFECT_DRIFT",
            expected_effect=expected_effect,
            observed_effect=observed_effect,
        )

    return EffectIntegrityResult(
        intact=True,
        reason="EFFECT_INTEGRITY_VALID",
        expected_effect=expected_effect,
        observed_effect=observed_effect,
    )
