from a2e_verifier.action import Action


def test_action_canonical_representation():
    action = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"status": "closed"},
        context={"environment": "staging"},
        actor="agent-1",
    )

    assert action.canonical() == {
        "tool": "ticket_api",
        "operation": "update",
        "resource": "ticket:1001",
        "parameters": {"status": "closed"},
        "context": {"environment": "staging"},
        "actor": "agent-1",
    }
