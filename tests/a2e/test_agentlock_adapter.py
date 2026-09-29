from agentlock import AgentLockPermissions

from a2e_verifier.agentlock_adapter import AgentLockAdapter


def test_agentlock_adapter_registers_and_authorizes_tool():
    adapter = AgentLockAdapter()

    adapter.register_tool(
        "ticket_api",
        AgentLockPermissions(
            allowed_roles=["agent"],
        ),
    )

    result = adapter.authorize(
        "ticket_api",
        user_id="user-1",
        role="agent",
        parameters={"ticket_id": "1001"},
    )

    assert result.allowed is True
    assert result.token is not None


def test_agentlock_adapter_denies_unauthorized_role():
    adapter = AgentLockAdapter()

    adapter.register_tool(
        "ticket_api",
        AgentLockPermissions(
            allowed_roles=["agent"],
        ),
    )

    result = adapter.authorize(
        "ticket_api",
        user_id="user-1",
        role="guest",
        parameters={"ticket_id": "1001"},
    )

    assert result.allowed is False
    assert result.token is None
