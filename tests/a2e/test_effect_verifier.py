from a2e_verifier.action import Action
from a2e_verifier.effect_verifier import verify_effect
from a2e_verifier.environment import SimulatedEnvironment


def test_matching_effect_is_verified():
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

    expected = {
        "result": {
            "status": "closed",
        }
    }

    result = verify_effect(
        action,
        action,
        expected,
        environment,
    )

    assert result.matched is True
    assert result.reason == "EFFECT_MATCH"


def test_resource_effect_drift_is_detected():
    environment = SimulatedEnvironment()
    environment.add_resource(
        "ticket:1001",
        {"status": "open"},
    )
    environment.add_resource(
        "ticket:1002",
        {"status": "open"},
    )

    intended = Action(
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

    result = verify_effect(
        intended,
        actual,
        {"result": {"status": "closed"}},
        environment,
    )

    assert result.matched is False
    assert result.reason == "RESOURCE_EFFECT_DRIFT"
