from datetime import datetime, timedelta, timezone

from a2e_verifier.freshness import AuthorizationWindow
from a2e_verifier.freshness_verifier import (
    verify_authorization_freshness,
)


def test_freshness_aware_verification_allows_valid_action():
    issued = datetime(2026, 1, 1, tzinfo=timezone.utc)
    window = AuthorizationWindow(
        issued_at=issued,
        expires_at=issued + timedelta(minutes=10),
        action_id="action-1",
    )

    result = verify_authorization_freshness(
        window,
        "action-1",
        issued + timedelta(minutes=5),
    )

    assert result.allowed is True
    assert result.reason == "AUTHORIZATION_FRESH"


def test_freshness_aware_verification_blocks_expired_action():
    issued = datetime(2026, 1, 1, tzinfo=timezone.utc)
    window = AuthorizationWindow(
        issued_at=issued,
        expires_at=issued + timedelta(minutes=10),
        action_id="action-1",
    )

    result = verify_authorization_freshness(
        window,
        "action-1",
        issued + timedelta(minutes=11),
    )

    assert result.allowed is False
    assert result.reason == "FRESHNESS_FAILED:AUTHORIZATION_EXPIRED"
