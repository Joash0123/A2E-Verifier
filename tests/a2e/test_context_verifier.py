from a2e_verifier.action import Action
from a2e_verifier.context_verifier import verify_context


def test_unchanged_context_is_valid():
    action = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        context={"session": "s1", "purpose": "support"},
        actor="agent-1",
    )

    result = verify_context(action, action)

    assert result.allowed is True
    assert result.reason == "CONTEXT_VALID"


def test_detects_context_drift():
    authorized = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        context={"session": "s1", "purpose": "support"},
        actor="agent-1",
    )

    executed = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        context={"session": "s2", "purpose": "support"},
        actor="agent-1",
    )

    result = verify_context(authorized, executed)

    assert result.allowed is False
    assert result.reason == "CONTEXT_DRIFT:session"


def test_detects_added_context():
    authorized = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        context={"session": "s1"},
        actor="agent-1",
    )

    executed = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        context={"session": "s1", "privileged": True},
        actor="agent-1",
    )

    result = verify_context(authorized, executed)

    assert result.allowed is False
    assert result.reason == "CONTEXT_DRIFT:privileged"
