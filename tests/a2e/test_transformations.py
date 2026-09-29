from a2e_verifier.action import Action
from a2e_verifier.transformations import (
    canonicalize_resource,
    normalize_parameters,
)


def test_normalize_parameters_preserves_action():
    action = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"status": "closed"},
        actor="agent-1",
    )

    result = normalize_parameters(action)

    assert result == action


def test_canonicalize_resource_normalizes_format():
    action = Action(
        tool="ticket_api",
        operation="read",
        resource=" TICKET:1001 ",
        actor="agent-1",
    )

    result = canonicalize_resource(action)

    assert result.resource == "ticket:1001"
    assert result.operation == "read"
    assert result.actor == "agent-1"
