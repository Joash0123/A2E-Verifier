from a2e_verifier.provenance import ProvenanceTrace
from a2e_verifier.provenance_verifier import verify_provenance


def test_valid_provenance():
    trace = ProvenanceTrace()

    trace.record(
        stage="authorization",
        actor="agent-1",
        action_id="action-001",
    )

    trace.record(
        stage="execution",
        actor="agent-1",
        action_id="action-001",
    )

    result = verify_provenance(trace)

    assert result.valid is True
    assert result.reason == "PROVENANCE_VALID"


def test_detects_action_id_drift():
    trace = ProvenanceTrace()

    trace.record(
        stage="authorization",
        actor="agent-1",
        action_id="action-001",
    )

    trace.record(
        stage="execution",
        actor="agent-1",
        action_id="action-002",
    )

    result = verify_provenance(trace)

    assert result.valid is False
    assert result.reason == "ACTION_ID_DRIFT"


def test_detects_empty_provenance():
    trace = ProvenanceTrace()

    result = verify_provenance(trace)

    assert result.valid is False
    assert result.reason == "EMPTY_PROVENANCE"
