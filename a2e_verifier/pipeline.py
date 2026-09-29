from dataclasses import dataclass
from typing import Any

from a2e_verifier.action import Action
from a2e_verifier.effect_verifier import verify_effect
from a2e_verifier.environment import SimulatedEnvironment
from a2e_verifier.policy import AuthorizationPolicy
from a2e_verifier.provenance import ProvenanceTrace
from a2e_verifier.report import VerificationReport, build_report


@dataclass(frozen=True)
class PipelineResult:
    report: VerificationReport
    effect_matched: bool
    effect_reason: str
    effect: dict[str, Any] | None


def verify_pipeline(
    authorized: Action,
    executed: Action,
    expected_effect: dict[str, Any],
    policy: AuthorizationPolicy,
    provenance: ProvenanceTrace,
    environment: SimulatedEnvironment,
) -> PipelineResult:
    report = build_report(
        authorized,
        executed,
        policy,
        provenance,
    )

    if not report.allowed:
        return PipelineResult(
            report=report,
            effect_matched=False,
            effect_reason="AUTHORIZATION_VERIFICATION_FAILED",
            effect=None,
        )

    effect_result = verify_effect(
        authorized,
        executed,
        expected_effect,
        environment,
    )

    return PipelineResult(
        report=report,
        effect_matched=effect_result.matched,
        effect_reason=effect_result.reason,
        effect=effect_result.actual,
    )
