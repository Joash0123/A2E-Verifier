from a2e_verifier.action import Action
from a2e_verifier.chain import ActionChain


def test_action_chain_tracks_transformation():
    original = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"status": "closed"},
        context={"environment": "staging"},
        actor="agent-1",
    )

    transformed = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1002",
        parameters={"status": "closed"},
        context={"environment": "staging"},
        actor="agent-1",
    )

    chain = ActionChain(steps=[])
    chain.add("authorization", original)
    chain.add("reconstruction", transformed)

    assert chain.original == original
    assert chain.final == transformed
    assert len(chain.steps) == 2
