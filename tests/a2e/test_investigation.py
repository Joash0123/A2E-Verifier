from a2e_verifier.action import Action
from a2e_verifier.investigation import investigate
from a2e_verifier.verifier import verify


def make_action(resource="ticket:1001", operation="read"):
    return Action(
        tool="ticket_api",
        operation=operation,
        resource=resource,
        actor="agent-1",
    )


def test_investigation_accepts_matching_action():
    action = make_action()

    result = investigate(
        action,
        action,
        verify(action, action),
    )

    assert result.category == "NO_DRIFT"
    assert "matches" in result.summary


def test_investigation_detects_resource_drift():
    authorized = make_action(resource="ticket:1001")
    executed = make_action(resource="ticket:2002")

    result = investigate(
        authorized,
        executed,
        verify(authorized, executed),
    )

    assert result.category == "RESOURCE_DRIFT"
    assert result.evidence
    assert result.remediation


def test_investigation_detects_operation_drift():
    authorized = make_action(operation="read")
    executed = make_action(operation="delete")

    result = investigate(
        authorized,
        executed,
        verify(authorized, executed),
    )

    assert result.category == "OPERATION_DRIFT"
