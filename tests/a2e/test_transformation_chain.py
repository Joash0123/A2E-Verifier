from a2e_verifier.action import Action
from a2e_verifier.chain import ActionChain, ActionStep
from a2e_verifier.transformation_chain import verify_transformation_chain


def test_valid_transformation_chain_is_allowed():
    first = Action(
        tool="ticket_api",
        operation=" UPDATE ",
        resource="ticket:1001",
        actor="agent-1",
    )

    second = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        actor="agent-1",
    )

    chain = ActionChain(
        steps=[
            ActionStep("authorization", first),
            ActionStep("normalization", second),
        ]
    )

    result = verify_transformation_chain(chain)

    assert result.allowed is True
    assert result.reason == "CHAIN_SEMANTICALLY_VALID"
    assert result.failed_step is None


def test_transformation_chain_detects_resource_drift():
    first = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
    )

    second = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1002",
        actor="agent-1",
    )

    chain = ActionChain(
        steps=[
            ActionStep("authorization", first),
            ActionStep("execution", second),
        ]
    )

    result = verify_transformation_chain(chain)

    assert result.allowed is False
    assert result.reason == "RESOURCE_CHANGED"
    assert result.failed_step == 1
