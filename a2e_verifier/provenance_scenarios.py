from dataclasses import dataclass

from a2e_verifier.provenance import ProvenanceTrace
from a2e_verifier.provenance_verifier import verify_provenance


@dataclass(frozen=True)
class ProvenanceScenarioResult:
    name: str
    detected: bool
    reason: str


def valid_provenance() -> ProvenanceScenarioResult:
    trace = ProvenanceTrace()

    trace.record(
        stage="authorized",
        actor="agent-1",
        action_id="action-1",
    )

    trace.record(
        stage="transformed",
        actor="agent-1",
        action_id="action-1",
    )

    trace.record(
        stage="executed",
        actor="agent-1",
        action_id="action-1",
    )

    result = verify_provenance(trace)

    return ProvenanceScenarioResult(
        name="valid_provenance",
        detected=result.valid,
        reason=result.reason,
    )


def action_id_drift() -> ProvenanceScenarioResult:
    trace = ProvenanceTrace()

    trace.record(
        stage="authorized",
        actor="agent-1",
        action_id="action-1",
    )

    trace.record(
        stage="transformed",
        actor="agent-1",
        action_id="action-2",
    )

    result = verify_provenance(trace)

    return ProvenanceScenarioResult(
        name="action_id_drift",
        detected=not result.valid,
        reason=result.reason,
    )


def run_provenance_scenarios() -> list[ProvenanceScenarioResult]:
    return [
        valid_provenance(),
        action_id_drift(),
    ]
