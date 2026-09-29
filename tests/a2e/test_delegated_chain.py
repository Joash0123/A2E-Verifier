from a2e_verifier.action import Action
from a2e_verifier.chain import ActionChain, ActionStep
from a2e_verifier.delegation import Delegation
from a2e_verifier.delegated_chain import verify_delegated_chain


def test_valid_delegated_chain():
    original = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-2",
        context={"delegated_by": "agent-1"},
    )

    transformed = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-2",
        context={"delegated_by": "agent-1"},
    )

    chain = ActionChain(
        steps=[
            ActionStep("authorization", original),
            ActionStep("normalization", transformed),
        ]
    )

    delegation = Delegation(
        delegator="agent-1",
        delegate="agent-2",
        resources=frozenset({"ticket:1001"}),
        operations=frozenset({"read"}),
    )

    result = verify_delegated_chain(
        chain,
        delegation,
    )

    assert result.allowed is True
    assert result.reason == "DELEGATED_CHAIN_VALID"
    assert result.transformation_steps == 2


def test_delegated_chain_detects_resource_drift():
    original = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-2",
        context={"delegated_by": "agent-1"},
    )

    transformed = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1002",
        actor="agent-2",
        context={"delegated_by": "agent-1"},
    )

    chain = ActionChain(
        steps=[
            ActionStep("authorization", original),
            ActionStep("execution", transformed),
        ]
    )

    delegation = Delegation(
        delegator="agent-1",
        delegate="agent-2",
        resources=frozenset({"ticket:1001"}),
        operations=frozenset({"read"}),
    )

    result = verify_delegated_chain(
        chain,
        delegation,
    )

    assert result.allowed is False
    assert result.reason == "RESOURCE_CHANGED"
