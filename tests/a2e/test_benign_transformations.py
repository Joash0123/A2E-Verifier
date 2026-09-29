from a2e_verifier.action import Action
from a2e_verifier.benign_transformations import (
    normalize_operation,
    reorder_parameters,
)


def test_reorder_parameters_preserves_action():
    action = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"priority": "high", "status": "open"},
        actor="agent-1",
    )

    transformed = reorder_parameters(action)

    assert transformed.parameters == {
        "priority": "high",
        "status": "open",
    }


def test_normalize_operation_preserves_semantics():
    action = Action(
        tool="ticket_api",
        operation=" UPDATE ",
        resource="ticket:1001",
        actor="agent-1",
    )

    transformed = normalize_operation(action)

    assert transformed.operation == "update"
