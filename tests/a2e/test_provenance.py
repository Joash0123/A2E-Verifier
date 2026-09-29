from a2e_verifier.provenance import ProvenanceTrace


def test_provenance_records_events():
    trace = ProvenanceTrace()

    trace.record(
        stage="authorization",
        actor="agent-1",
        action_id="action-001",
    )

    trace.record(
        stage="delegation",
        actor="agent-2",
        action_id="action-001",
        details={"delegated_by": "agent-1"},
    )

    assert len(trace.events) == 2
    assert trace.actors == ["agent-1", "agent-2"]
    assert trace.stages == ["authorization", "delegation"]
    assert trace.events[1].details["delegated_by"] == "agent-1"
