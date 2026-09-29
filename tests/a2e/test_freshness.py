from datetime import datetime, timedelta, timezone

from a2e_verifier.freshness import (
    AuthorizationWindow,
    verify_freshness,
)


def test_fresh_authorization_is_valid():
    issued = datetime(2026, 1, 1, tzinfo=timezone.utc)
    expires = issued + timedelta(minutes=10)

    window = AuthorizationWindow(
        issued_at=issued,
        expires_at=expires,
        action_id="action-1",
    )

    result = verify_freshness(
        window,
        "action-1",
        issued + timedelta(minutes=5),
    )

    assert result.valid is True
    assert result.reason == "AUTHORIZATION_FRESH"


def test_expired_authorization_is_rejected():
    issued = datetime(2026, 1, 1, tzinfo=timezone.utc)
    expires = issued + timedelta(minutes=10)

    window = AuthorizationWindow(
        issued_at=issued,
        expires_at=expires,
        action_id="action-1",
    )

    result = verify_freshness(
        window,
        "action-1",
        issued + timedelta(minutes=11),
    )

    assert result.valid is False
    assert result.reason == "AUTHORIZATION_EXPIRED"


def test_replay_with_different_action_id_is_rejected():
    issued = datetime(2026, 1, 1, tzinfo=timezone.utc)
    expires = issued + timedelta(minutes=10)

    window = AuthorizationWindow(
        issued_at=issued,
        expires_at=expires,
        action_id="action-1",
    )

    result = verify_freshness(
        window,
        "action-2",
        issued + timedelta(minutes=5),
    )

    assert result.valid is False
    assert result.reason == "ACTION_ID_MISMATCH"
