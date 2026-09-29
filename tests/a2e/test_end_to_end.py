from datetime import datetime, timedelta, timezone

from a2e_verifier.action import Action
from a2e_verifier.environment import SimulatedEnvironment
from a2e_verifier.freshness import AuthorizationWindow
from a2e_verifier.observation import observe_execution
from a2e_verifier.parameter_policy import ParameterConstraint
from a2e_verifier.unified_policy import verify_unified_policy


def test_end_to_end_resource_substitution_attack():
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

    environment.add_resource(
        "ticket:1002",
        {"status": "open"},
    )

    authorized = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"status": "closed"},
        actor="agent-1",
    )

    transformed = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1002",
        parameters={"status": "closed"},
        actor="agent-1",
    )

    observed = observe_execution(
        transformed,
        environment,
    )

    result = verify_unified_policy(
        authorized=authorized,
        authorization_window=window,
        action_id="action-1",
        observed=observed,
        expected_effect={
            "result": {
                "status": "closed",
            }
        },
        parameter_constraints=[
            ParameterConstraint(
                key="status",
                allowed_values=frozenset({"open", "closed"}),
            )
        ],
        now=issued + timedelta(minutes=5),
    )

    assert result.allowed is False
    assert result.reason == "RESOURCE_EXECUTION_DRIFT"
    assert environment.resources["ticket:1002"]["status"] == "closed"
