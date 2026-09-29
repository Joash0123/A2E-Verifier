from a2e_verifier.action import Action
from a2e_verifier.environment import SimulatedEnvironment
from a2e_verifier.pipeline import verify_pipeline
from a2e_verifier.policy import AuthorizationPolicy
from a2e_verifier.provenance import ProvenanceTrace


def test_pipeline_accepts_valid_execution():
    environment = SimulatedEnvironment()
    environment.add_resource(
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

    provenance = ProvenanceTrace()
    provenance.record(
        stage="authorization",
        actor="agent-1",
        action_id="action-1",
    )

    result = verify_pipeline(
        authorized=action,
        executed=action,
        expected_effect={
            "result": {
                "status": "closed",
            }
        },
        policy=policy,
        provenance=provenance,
        environment=environment,
    )

    assert result.report.allowed is True
    assert result.effect_matched is True
    assert result.effect_reason == "EFFECT_MATCH"


def test_pipeline_blocks_resource_substitution():
    environment = SimulatedEnvironment()
    environment.add_resource(
        "ticket:1001",
        {"status": "open"},
    )
    environment.add_resource(
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

    provenance = ProvenanceTrace()
    provenance.record(
        stage="authorization",
        actor="agent-1",
        action_id="action-1",
    )

    result = verify_pipeline(
        authorized=authorized,
        executed=executed,
        expected_effect={
            "result": {
                "status": "closed",
            }
        },
        policy=policy,
        provenance=provenance,
        environment=environment,
    )

    assert result.report.allowed is False
    assert result.effect_matched is False
    assert result.effect_reason == "AUTHORIZATION_VERIFICATION_FAILED"
