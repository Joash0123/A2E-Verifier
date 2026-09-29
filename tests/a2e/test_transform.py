from a2e_verifier.action import Action
from a2e_verifier.chain import ActionChain
from a2e_verifier.transform import transform


def test_transformation_records_source_and_target():
    original = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"status": "closed"},
        actor="agent-1",
    )

    transformed = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1002",
        parameters={"status": "closed"},
        actor="agent-1",
    )

    chain = ActionChain(steps=[])
    chain.add("authorization", original)

    transformation = transform(
        chain,
        "parameter_reconstruction",
        transformed,
    )

    assert transformation.name == "parameter_reconstruction"
    assert transformation.source == original
    assert transformation.target == transformed
    assert chain.final == transformed
