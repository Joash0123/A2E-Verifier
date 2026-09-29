from dataclasses import dataclass
from datetime import datetime

from a2e_verifier.freshness import (
    AuthorizationWindow,
    FreshnessResult,
    verify_freshness,
)


@dataclass(frozen=True)
class FreshnessAwareResult:
    freshness: FreshnessResult
    allowed: bool
    reason: str


def verify_authorization_freshness(
    window: AuthorizationWindow,
    action_id: str,
    now: datetime,
) -> FreshnessAwareResult:
    freshness = verify_freshness(
        window,
        action_id,
        now,
    )

    if not freshness.valid:
        return FreshnessAwareResult(
            freshness=freshness,
            allowed=False,
            reason=f"FRESHNESS_FAILED:{freshness.reason}",
        )

    return FreshnessAwareResult(
        freshness=freshness,
        allowed=True,
        reason="AUTHORIZATION_FRESH",
    )
