from a2e_verifier.action import Action
from a2e_verifier.environment import SimulatedEnvironment
from a2e_verifier.policy import AuthorizationPolicy
from a2e_verifier.policy_execution import verify_with_policy
from a2e_verifier.verifier import Verdict


def test_policy_allows_matching_execution():
    env = SimulatedEnvironment()

    env.add_resource(
        "ticket:1001",
        {"status": "open"},
    )

    action = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"status": "closed"},
        actor="agent-1",
    )

    policy = AuthorizationPolicy(
        allowed_tools={"ticket_api"},
        allowed_operations={"update"},
        allowed_resources={"ticket:1001"},
        allowed_actors={"agent-1"},
    )

    result = verify_with_policy(
        action,
        action,
        policy,
        env,
    )

    assert result.authorization.verdict == Verdict.MATCH
    assert result.policy_allowed is True
    assert result.executed is True
    assert env.resources["ticket:1001"]["status"] == "closed"


def test_policy_blocks_execution_to_unauthorized_resource():
    env = SimulatedEnvironment()

    env.add_resource(
        "ticket:1001",
        {"status": "open"},
    )
    env.add_resource(
        "ticket:1002",
        {"status": "open"},
    )

    authorized = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"status": "closed"},
        actor="agent-1",
    )

    executed = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1002",
        parameters={"status": "closed"},
        actor="agent-1",
    )

    policy = AuthorizationPolicy(
        allowed_tools={"ticket_api"},
        allowed_operations={"update"},
        allowed_resources={"ticket:1001"},
        allowed_actors={"agent-1"},
    )

    result = verify_with_policy(
        authorized,
        executed,
        policy,
        env,
    )

    assert result.policy_allowed is False
    assert result.executed is False
    assert result.effect is None
    assert env.resources["ticket:1002"]["status"] == "open"
