from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class AuthorizationWindow:
    issued_at: datetime
    expires_at: datetime
    action_id: str


@dataclass(frozen=True)
class FreshnessResult:
    valid: bool
    reason: str


def verify_freshness(
    window: AuthorizationWindow,
    action_id: str,
    now: datetime | None = None,
) -> FreshnessResult:
    current = now or datetime.now(timezone.utc)

    if action_id != window.action_id:
        return FreshnessResult(
            valid=False,
            reason="ACTION_ID_MISMATCH",
        )

    if current < window.issued_at:
        return FreshnessResult(
            valid=False,
            reason="AUTHORIZATION_NOT_YET_VALID",
        )

    if current > window.expires_at:
        return FreshnessResult(
            valid=False,
            reason="AUTHORIZATION_EXPIRED",
        )

    return FreshnessResult(
        valid=True,
        reason="AUTHORIZATION_FRESH",
    )
