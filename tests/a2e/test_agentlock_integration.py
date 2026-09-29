from agentlock import AgentLockPermissions

from a2e_verifier.action import Action
from a2e_verifier.agentlock_adapter import AgentLockAdapter
from a2e_verifier.agentlock_integration import authorize_and_verify


def make_adapter() -> AgentLockAdapter:
    adapter = AgentLockAdapter()

    adapter.register_tool(
        "ticket_api",
        AgentLockPermissions(
            allowed_roles=["agent"],
        ),
    )

    return adapter


def test_authorized_action_that_matches_is_allowed():
    adapter = make_adapter()

    authorized = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
    )

    executed = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
    )

    result = authorize_and_verify(
        adapter,
        authorized,
        executed,
        user_id="user-1",
        role="agent",
    )

    assert result.agentlock_allowed is True
    assert result.blocked is False
    assert result.verification is not None
    assert result.verification.allowed is True


def test_authorized_agent_with_drifted_resource_is_blocked():
    adapter = make_adapter()

    authorized = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
    )

    executed = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1002",
        actor="agent-1",
    )

    result = authorize_and_verify(
        adapter,
        authorized,
        executed,
        user_id="user-1",
        role="agent",
    )

    assert result.agentlock_allowed is True
    assert result.blocked is True
    assert result.verification is not None
    assert result.verification.verdict.value == "RESOURCE_MISMATCH"


def test_agentlock_denial_blocks_before_a2e_verification():
    adapter = make_adapter()

    authorized = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
    )

    executed = authorized

    result = authorize_and_verify(
        adapter,
        authorized,
        executed,
        user_id="user-1",
        role="guest",
    )

    assert result.agentlock_allowed is False
    assert result.blocked is True
    assert result.verification is None
