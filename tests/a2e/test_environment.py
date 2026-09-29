from a2e_verifier.action import Action
from a2e_verifier.environment import SimulatedEnvironment


def test_simulated_update_execution():
    env = SimulatedEnvironment()

    env.add_resource(
        "ticket:1001",
        {"status": "open", "owner": "alice"},
    )

    action = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"status": "closed"},
        actor="agent-1",
    )

    result = env.execute(action)

    assert result["status"] == "executed"
    assert result["resource"] == "ticket:1001"
    assert env.resources["ticket:1001"]["status"] == "closed"


def test_simulated_read_execution():
    env = SimulatedEnvironment()

    env.add_resource(
        "ticket:1001",
        {"status": "open"},
    )

    action = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
    )

    result = env.execute(action)

    assert result["status"] == "executed"
    assert result["result"]["status"] == "open"
