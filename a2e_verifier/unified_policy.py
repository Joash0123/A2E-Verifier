from dataclasses import dataclass
from datetime import datetime
from typing import Any

from a2e_verifier.action import Action
from a2e_verifier.effect_integrity import (
    EffectIntegrityResult,
    verify_effect_integrity,
)
from a2e_verifier.execution_integrity import (
    ExecutionIntegrityResult,
    verify_execution_integrity,
)
from a2e_verifier.freshness import AuthorizationWindow
from a2e_verifier.freshness_verifier import (
    FreshnessAwareResult,
    verify_authorization_freshness,
)
from a2e_verifier.observation import ObservedExecution
from a2e_verifier.parameter_policy import (
    ParameterConstraint,
    ParameterPolicyResult,
    verify_parameters,
)


@dataclass(frozen=True)
class UnifiedPolicyResult:
    allowed: bool
    reason: str
    parameters: ParameterPolicyResult


def verify_unified_policy(
    authorized: Action,
    authorization_window: AuthorizationWindow,
    action_id: str,
    observed: ObservedExecution,
    expected_effect: dict[str, Any],
    parameter_constraints: list[ParameterConstraint],
    now: datetime,
) -> UnifiedPolicyResult:
    freshness = verify_authorization_freshness(
        authorization_window,
        action_id,
        now,
    )

    parameters = verify_parameters(
        observed.action,
        parameter_constraints,
    )

    execution = verify_execution_integrity(
        authorized,
        observed,
    )

    effect = verify_effect_integrity(
        authorized,
        expected_effect,
        observed,
    )

    if not freshness.allowed:
        return UnifiedPolicyResult(
            allowed=False,
            reason=freshness.reason,
            parameters=parameters,
        )

    if not parameters.allowed:
        return UnifiedPolicyResult(
            allowed=False,
            reason=parameters.reason,
            parameters=parameters,
        )

    if not execution.intact:
        return UnifiedPolicyResult(
            allowed=False,
            reason=execution.reason,
            parameters=parameters,
        )

    if not effect.intact:
        return UnifiedPolicyResult(
            allowed=False,
            reason=effect.reason,
            parameters=parameters,
        )

    return UnifiedPolicyResult(
        allowed=True,
        reason="UNIFIED_POLICY_VALID",
        parameters=parameters,
    )
