from a2e_verifier.action import Action
from a2e_verifier.policy import AuthorizationPolicy


def test_policy_allows_authorized_action():
    policy = AuthorizationPolicy(
        allowed_tools={"ticket_api"},
        allowed_operations={"read", "update"},
        allowed_resources={"ticket:1001"},
        allowed_actors={"agent-1"},
    )

    action = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        actor="agent-1",
    )

    assert policy.allows(action) is True


def test_policy_rejects_unauthorized_resource():
    policy = AuthorizationPolicy(
        allowed_tools={"ticket_api"},
        allowed_operations={"update"},
        allowed_resources={"ticket:1001"},
        allowed_actors={"agent-1"},
    )

    action = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1002",
        actor="agent-1",
    )

    assert policy.allows(action) is False


def test_policy_rejects_unauthorized_actor():
    policy = AuthorizationPolicy(
        allowed_tools={"ticket_api"},
        allowed_operations={"read"},
        allowed_resources={"ticket:1001"},
        allowed_actors={"agent-1"},
    )

    action = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-2",
    )

    assert policy.allows(action) is False
