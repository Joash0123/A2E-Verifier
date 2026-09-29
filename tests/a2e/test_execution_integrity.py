from a2e_verifier.action import Action
from a2e_verifier.environment import SimulatedEnvironment
from a2e_verifier.execution_integrity import verify_execution_integrity
from a2e_verifier.observation import observe_execution


def test_execution_integrity_accepts_matching_execution():
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

    result = verify_execution_integrity(
        action,
        observed,
    )

    assert result.intact is True
    assert result.reason == "EXECUTION_INTEGRITY_VALID"


def test_execution_integrity_detects_resource_drift():
    environment = SimulatedEnvironment()

    environment.add_resource(
        "ticket:1002",
        {"status": "open"},
    )

    expected = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"status": "closed"},
        actor="agent-1",
    )

    actual = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1002",
        parameters={"status": "closed"},
        actor="agent-1",
    )

    observed = observe_execution(
        actual,
        environment,
    )

    result = verify_execution_integrity(
        expected,
        observed,
    )

    assert result.intact is False
    assert result.reason == "RESOURCE_EXECUTION_DRIFT"
