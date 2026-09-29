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


@dataclass(frozen=True)
class UnifiedVerificationResult:
    allowed: bool
    reason: str
    freshness: FreshnessAwareResult
    execution: ExecutionIntegrityResult
    effect: EffectIntegrityResult


def verify_unified(
    authorized: Action,
    authorization_window: AuthorizationWindow,
    action_id: str,
    observed: ObservedExecution,
    expected_effect: dict[str, Any],
    now: datetime,
) -> UnifiedVerificationResult:
    freshness = verify_authorization_freshness(
        authorization_window,
        action_id,
        now,
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
        return UnifiedVerificationResult(
            allowed=False,
            reason=freshness.reason,
            freshness=freshness,
            execution=execution,
            effect=effect,
        )

    if not execution.intact:
        return UnifiedVerificationResult(
            allowed=False,
            reason=execution.reason,
            freshness=freshness,
            execution=execution,
            effect=effect,
        )

    if not effect.intact:
        return UnifiedVerificationResult(
            allowed=False,
            reason=effect.reason,
            freshness=freshness,
            execution=execution,
            effect=effect,
        )

    return UnifiedVerificationResult(
        allowed=True,
        reason="AUTHORIZATION_TO_EXECUTION_INTEGRITY_VALID",
        freshness=freshness,
        execution=execution,
        effect=effect,
    )
