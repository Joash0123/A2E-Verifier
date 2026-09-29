from a2e_verifier.action import Action
from a2e_verifier.chain import ActionChain, ActionStep
from a2e_verifier.chain_verifier import verify_chain


def test_multi_stage_resource_drift_is_detected():
    chain = ActionChain(
        steps=[
            ActionStep(
                name="authorization",
                action=Action(
                    tool="ticket_api",
                    operation="read",
                    resource="ticket:1001",
                    actor="agent-1",
                ),
            ),
            ActionStep(
                name="transformation",
                action=Action(
                    tool="ticket_api",
                    operation="read",
                    resource="ticket:1001",
                    actor="agent-1",
                ),
            ),
            ActionStep(
                name="execution",
                action=Action(
                    tool="ticket_api",
                    operation="read",
                    resource="ticket:1002",
                    actor="agent-1",
                ),
            ),
        ]
    )

    result = verify_chain(chain)

    assert result.result.allowed is False
    assert result.result.verdict.value == "RESOURCE_MISMATCH"
    assert result.steps_checked == 3
