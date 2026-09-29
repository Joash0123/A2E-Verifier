from a2e_verifier.action import Action
from a2e_verifier.integrity import action_digest


def test_same_action_has_same_digest():
    action = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"status": "closed"},
        actor="agent-1",
    )

    assert action_digest(action) == action_digest(action)


def test_different_resource_changes_digest():
    first = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
    )

    second = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1002",
        actor="agent-1",
    )

    assert action_digest(first) != action_digest(second)


def test_parameter_change_changes_digest():
    first = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"status": "open"},
        actor="agent-1",
    )

    second = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"status": "closed"},
        actor="agent-1",
    )

    assert action_digest(first) != action_digest(second)
