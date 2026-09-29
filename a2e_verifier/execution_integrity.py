from dataclasses import dataclass
from typing import Any

from a2e_verifier.action import Action
from a2e_verifier.observation import ObservedExecution


@dataclass(frozen=True)
class ExecutionIntegrityResult:
    intact: bool
    reason: str
    expected_action: Action
    observed_action: Action
    observed_effect: dict[str, Any]


def verify_execution_integrity(
    expected_action: Action,
    observed: ObservedExecution,
) -> ExecutionIntegrityResult:
    actual = observed.action

    if expected_action.tool != actual.tool:
        return ExecutionIntegrityResult(
            intact=False,
            reason="TOOL_EXECUTION_DRIFT",
            expected_action=expected_action,
            observed_action=actual,
            observed_effect=observed.effect,
        )

    if expected_action.operation != actual.operation:
        return ExecutionIntegrityResult(
            intact=False,
            reason="OPERATION_EXECUTION_DRIFT",
            expected_action=expected_action,
            observed_action=actual,
            observed_effect=observed.effect,
        )

    if expected_action.resource != actual.resource:
        return ExecutionIntegrityResult(
            intact=False,
            reason="RESOURCE_EXECUTION_DRIFT",
            expected_action=expected_action,
            observed_action=actual,
            observed_effect=observed.effect,
        )

    if expected_action.parameters != actual.parameters:
        return ExecutionIntegrityResult(
            intact=False,
            reason="PARAMETER_EXECUTION_DRIFT",
            expected_action=expected_action,
            observed_action=actual,
            observed_effect=observed.effect,
        )

    if expected_action.actor != actual.actor:
        return ExecutionIntegrityResult(
            intact=False,
            reason="ACTOR_EXECUTION_DRIFT",
            expected_action=expected_action,
            observed_action=actual,
            observed_effect=observed.effect,
        )

    return ExecutionIntegrityResult(
        intact=True,
        reason="EXECUTION_INTEGRITY_VALID",
        expected_action=expected_action,
        observed_action=actual,
        observed_effect=observed.effect,
    )
