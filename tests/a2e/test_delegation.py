from a2e_verifier.action import Action
from a2e_verifier.delegation import Delegation, apply_delegation


def test_valid_delegation_allows_delegate():
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
    )

    assert delegation.allows(action) is True


def test_delegation_rejects_wrong_resource():
    delegation = Delegation(
        delegator="agent-1",
        delegate="agent-2",
        resources=frozenset({"ticket:1001"}),
        operations=frozenset({"read"}),
    )

    action = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1002",
        actor="agent-2",
    )

    assert delegation.allows(action) is False


def test_delegation_rejects_wrong_operation():
    delegation = Delegation(
        delegator="agent-1",
        delegate="agent-2",
        resources=frozenset({"ticket:1001"}),
        operations=frozenset({"read"}),
    )

    action = Action(
        tool="ticket_api",
        operation="delete",
        resource="ticket:1001",
        actor="agent-2",
    )

    assert delegation.allows(action) is False


def test_apply_delegation_changes_actor_and_records_origin():
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
        actor="agent-1",
    )

    delegated = apply_delegation(action, delegation)

    assert delegated.actor == "agent-2"
    assert delegated.context["delegated_by"] == "agent-1"
