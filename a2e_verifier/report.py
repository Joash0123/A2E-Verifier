from dataclasses import dataclass, field
from typing import Any

from a2e_verifier.action import Action
from a2e_verifier.integrity import action_digest
from a2e_verifier.policy import AuthorizationPolicy
from a2e_verifier.provenance import ProvenanceTrace
from a2e_verifier.provenance_verifier import verify_provenance
from a2e_verifier.verifier import verify


@dataclass(frozen=True)
class VerificationReport:
    allowed: bool
    verdict: str
    reasons: list[str] = field(default_factory=list)
    authorized_digest: str = ""
    executed_digest: str = ""
    provenance_valid: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


def build_report(
    authorized: Action,
    executed: Action,
    policy: AuthorizationPolicy,
    provenance: ProvenanceTrace,
) -> VerificationReport:
    result = verify(authorized, executed)
    provenance_result = verify_provenance(provenance)
    policy_allowed = policy.allows(executed)

    reasons: list[str] = []

    if not result.allowed:
        reasons.append(result.verdict.value)

    if not policy_allowed:
        reasons.append("POLICY_DENIED")

    if not provenance_result.valid:
        reasons.append(provenance_result.reason)

    allowed = (
        result.allowed
        and policy_allowed
        and provenance_result.valid
    )

    return VerificationReport(
        allowed=allowed,
        verdict=result.verdict.value,
        reasons=reasons,
        authorized_digest=action_digest(authorized),
        executed_digest=action_digest(executed),
        provenance_valid=provenance_result.valid,
        metadata={
            "policy_allowed": policy_allowed,
            "provenance_events": len(provenance.events),
        },
    )
