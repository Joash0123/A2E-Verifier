from dataclasses import dataclass

from a2e_verifier.provenance import ProvenanceTrace


@dataclass(frozen=True)
class ProvenanceVerificationResult:
    valid: bool
    reason: str


def verify_provenance(trace: ProvenanceTrace) -> ProvenanceVerificationResult:
    if not trace.events:
        return ProvenanceVerificationResult(
            valid=False,
            reason="EMPTY_PROVENANCE",
        )

    for index, event in enumerate(trace.events):
        if not event.actor:
            return ProvenanceVerificationResult(
                valid=False,
                reason=f"MISSING_ACTOR:{index}",
            )

        if not event.action_id:
            return ProvenanceVerificationResult(
                valid=False,
                reason=f"MISSING_ACTION_ID:{index}",
            )

    for previous, current in zip(
        trace.events,
        trace.events[1:],
    ):
        if previous.action_id != current.action_id:
            return ProvenanceVerificationResult(
                valid=False,
                reason="ACTION_ID_DRIFT",
            )

    return ProvenanceVerificationResult(
        valid=True,
        reason="PROVENANCE_VALID",
    )
