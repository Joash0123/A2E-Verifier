from datetime import datetime, timedelta, timezone

from a2e_verifier.action import Action
from a2e_verifier.environment import SimulatedEnvironment
from a2e_verifier.freshness import AuthorizationWindow
from a2e_verifier.observation import observe_execution
from a2e_verifier.unified_verifier import verify_unified


def test_unified_verification_accepts_valid_execution():
    issued = datetime(2026, 1, 1, tzinfo=timezone.utc)

    window = AuthorizationWindow(
        issued_at=issued,
        expires_at=issued + timedelta(minutes=10),
        action_id="action-1",
    )

    environment = SimulatedEnvironment()

    environment.add_resource(
        "ticket:1001",
        {"status": "open"},
    )

    action = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"status": "closed"},
        actor="agent-1",
    )

    observed = observe_execution(
        action,
        environment,
    )

    result = verify_unified(
        authorized=action,
        authorization_window=window,
        action_id="action-1",
        observed=observed,
        expected_effect={
            "result": {
                "status": "closed",
            }
        },
        now=issued + timedelta(minutes=5),
    )

    assert result.allowed is True
    assert result.reason == "AUTHORIZATION_TO_EXECUTION_INTEGRITY_VALID"


def test_unified_verification_blocks_expired_authorization():
    issued = datetime(2026, 1, 1, tzinfo=timezone.utc)

    window = AuthorizationWindow(
        issued_at=issued,
        expires_at=issued + timedelta(minutes=10),
        action_id="action-1",
    )

    environment = SimulatedEnvironment()

    environment.add_resource(
        "ticket:1001",
        {"status": "open"},
    )

    action = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"status": "closed"},
        actor="agent-1",
    )

    observed = observe_execution(
        action,
        environment,
    )

    result = verify_unified(
        authorized=action,
        authorization_window=window,
        action_id="action-1",
        observed=observed,
        expected_effect={
            "result": {
                "status": "closed",
            }
        },
        now=issued + timedelta(minutes=11),
    )

    assert result.allowed is False
    assert result.reason == "FRESHNESS_FAILED:AUTHORIZATION_EXPIRED"
