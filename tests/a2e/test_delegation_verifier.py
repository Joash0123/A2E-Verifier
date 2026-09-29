from a2e_verifier.action import Action
from a2e_verifier.delegation import Delegation, apply_delegation
from a2e_verifier.delegation_verifier import verify_delegated_action


def test_valid_delegated_action():
    delegation = Delegation(
        delegator="agent-1",
        delegate="agent-2",
        resources=frozenset({"ticket:1001"}),
        operations=frozenset({"read"}),
    )

    original = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
    )

    delegated = apply_delegation(original, delegation)

    result = verify_delegated_action(
        delegated,
        delegation,
    )

    assert result.allowed is True
    assert result.reason == "DELEGATION_VALID"


def test_detects_delegate_drift():
    delegation = Delegation(
        delegator="agent-1",
        delegate="agent-2",
        resources=frozenset({"ticket:1001"}),
        operations=frozenset({"read"}),
    )

    action = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-3",
        context={"delegated_by": "agent-1"},
    )

    result = verify_delegated_action(
        action,
        delegation,
    )

    assert result.allowed is False
    assert result.reason == "DELEGATE_MISMATCH"


def test_detects_delegation_origin_drift():
    delegation = Delegation(
        delegator="agent-1",
        delegate="agent-2",
        resources=frozenset({"ticket:1001"}),
        operations=frozenset({"read"}),
    )

    action = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-2",
        context={"delegated_by": "agent-3"},
    )

    result = verify_delegated_action(
        action,
        delegation,
    )

    assert result.allowed is False
    assert result.reason == "DELEGATION_ORIGIN_MISMATCH"
