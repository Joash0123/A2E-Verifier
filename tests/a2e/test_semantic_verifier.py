from a2e_verifier.action import Action
from a2e_verifier.semantic_verifier import verify_semantic_equivalence


def test_semantically_equivalent_operations_match():
    source = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        actor="agent-1",
    )

    target = Action(
        tool="ticket_api",
        operation=" UPDATE ",
        resource="ticket:1001",
        actor="agent-1",
    )

    result = verify_semantic_equivalence(source, target)

    assert result.equivalent is True
    assert result.reason == "SEMANTICALLY_EQUIVALENT"


def test_resource_change_is_not_equivalent():
    source = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
    )

    target = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1002",
        actor="agent-1",
    )

    result = verify_semantic_equivalence(source, target)

    assert result.equivalent is False
    assert result.reason == "RESOURCE_CHANGED"


def test_parameter_change_is_not_equivalent():
    source = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"priority": "normal"},
        actor="agent-1",
    )

    target = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"priority": "critical"},
        actor="agent-1",
    )

    result = verify_semantic_equivalence(source, target)

    assert result.equivalent is False
    assert result.reason == "PARAMETERS_CHANGED"
