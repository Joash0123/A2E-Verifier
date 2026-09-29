from a2e_verifier.action import Action
from a2e_verifier.policy import AuthorizationPolicy
from a2e_verifier.provenance import ProvenanceTrace
from a2e_verifier.report import build_report


def test_build_report_for_valid_execution():
    action = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
    )

    policy = AuthorizationPolicy(
        allowed_tools={"ticket_api"},
        allowed_operations={"read"},
        allowed_resources={"ticket:1001"},
        allowed_actors={"agent-1"},
    )

    provenance = ProvenanceTrace()
    provenance.record(
        stage="authorization",
        actor="agent-1",
        action_id="action-001",
    )
    provenance.record(
        stage="execution",
        actor="agent-1",
        action_id="action-001",
    )

    report = build_report(
        action,
        action,
        policy,
        provenance,
    )

    assert report.allowed is True
    assert report.verdict == "MATCH"
    assert report.reasons == []
    assert report.provenance_valid is True
    assert report.authorized_digest == report.executed_digest


def test_build_report_detects_multiple_failures():
    authorized = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
    )

    executed = Action(
        tool="ticket_api",
        operation="delete",
        resource="ticket:1002",
        actor="agent-2",
    )

    policy = AuthorizationPolicy(
        allowed_tools={"ticket_api"},
        allowed_operations={"read"},
        allowed_resources={"ticket:1001"},
        allowed_actors={"agent-1"},
    )

    provenance = ProvenanceTrace()
    provenance.record(
        stage="authorization",
        actor="agent-1",
        action_id="action-001",
    )
    provenance.record(
        stage="execution",
        actor="agent-2",
        action_id="action-002",
    )

    report = build_report(
        authorized,
        executed,
        policy,
        provenance,
    )

    assert report.allowed is False
    assert "OPERATION_MISMATCH" in report.reasons
    assert "POLICY_DENIED" in report.reasons
    assert "ACTION_ID_DRIFT" in report.reasons
    assert report.authorized_digest != report.executed_digest
