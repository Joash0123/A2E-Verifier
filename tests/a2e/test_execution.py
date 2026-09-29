from a2e_verifier.action import Action
from a2e_verifier.environment import SimulatedEnvironment
from a2e_verifier.execution import verify_execution
from a2e_verifier.verifier import Verdict


def test_authorized_action_can_execute_and_produce_effect():
    env = SimulatedEnvironment()

    env.add_resource(
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

    result = verify_execution(action, action, env)

    assert result.authorization.verdict == Verdict.MATCH
    assert result.executed is True
    assert result.effect["status"] == "executed"
    assert env.resources["ticket:1001"]["status"] == "closed"


def test_unauthorized_resource_never_executes():
    env = SimulatedEnvironment()

    env.add_resource(
        "ticket:1001",
        {"status": "open"},
    )
    env.add_resource(
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

    executed = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1002",
        parameters={"status": "closed"},
        actor="agent-1",
    )

    result = verify_execution(authorized, executed, env)

    assert result.authorization.verdict == Verdict.RESOURCE_MISMATCH
    assert result.executed is False
    assert result.effect is None
    assert env.resources["ticket:1002"]["status"] == "open"
