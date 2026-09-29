from datetime import datetime, timedelta, timezone

from a2e_verifier.action import Action
from a2e_verifier.environment import SimulatedEnvironment
from a2e_verifier.freshness import AuthorizationWindow
from a2e_verifier.observation import observe_execution
from a2e_verifier.parameter_policy import ParameterConstraint
from a2e_verifier.unified_policy import verify_unified_policy


def test_unified_policy_allows_valid_parameters():
    issued = datetime(2026, 1, 1, tzinfo=timezone.utc)

    window = AuthorizationWindow(
        issued_at=issued,
        expires_at=issued + timedelta(minutes=10),
        action_id="action-1",
    )

    environment = SimulatedEnvironment()

    environment.add_resource(
        "ticket:1001",
        {"priority": "normal"},
    )

    action = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"priority": "normal"},
        actor="agent-1",
    )

    observed = observe_execution(
        action,
        environment,
    )

    result = verify_unified_policy(
        authorized=action,
        authorization_window=window,
        action_id="action-1",
        observed=observed,
        expected_effect={
            "result": {
                "priority": "normal",
            }
        },
        parameter_constraints=[
            ParameterConstraint(
                key="priority",
                allowed_values=frozenset({"normal", "low"}),
            )
        ],
        now=issued + timedelta(minutes=5),
    )

    assert result.allowed is True
    assert result.reason == "UNIFIED_POLICY_VALID"


def test_unified_policy_blocks_parameter_escalation():
    issued = datetime(2026, 1, 1, tzinfo=timezone.utc)

    window = AuthorizationWindow(
        issued_at=issued,
        expires_at=issued + timedelta(minutes=10),
        action_id="action-1",
    )

    environment = SimulatedEnvironment()

    environment.add_resource(
        "ticket:1001",
        {"priority": "critical"},
    )

    authorized = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"priority": "critical"},
        actor="agent-1",
    )

    observed = observe_execution(
        authorized,
        environment,
    )

    result = verify_unified_policy(
        authorized=authorized,
        authorization_window=window,
        action_id="action-1",
        observed=observed,
        expected_effect={
            "result": {
                "priority": "critical",
            }
        },
        parameter_constraints=[
            ParameterConstraint(
                key="priority",
                allowed_values=frozenset({"normal", "low"}),
            )
        ],
        now=issued + timedelta(minutes=5),
    )

    assert result.allowed is False
    assert result.reason == "PARAMETER_NOT_ALLOWED:priority"
