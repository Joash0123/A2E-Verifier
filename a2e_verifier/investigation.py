from dataclasses import dataclass

from a2e_verifier.action import Action
from a2e_verifier.verifier import VerificationResult


@dataclass(frozen=True)
class InvestigationResult:
    summary: str
    category: str
    evidence: list[str]
    remediation: list[str]


def investigate(
    authorized: Action,
    executed: Action,
    verification: VerificationResult,
) -> InvestigationResult:
    if verification.allowed:
        return InvestigationResult(
            summary="The executed action matches the authorized action.",
            category="NO_DRIFT",
            evidence=[
                "Tool matches.",
                "Operation matches.",
                "Resource matches.",
                "Parameters match.",
                "Context matches.",
                "Actor matches.",
            ],
            remediation=[
                "No authorization-drift remediation is required.",
            ],
        )

    evidence: list[str] = []

    if authorized.tool != executed.tool:
        category = "TOOL_DRIFT"
        evidence.append(
            f"Authorized tool '{authorized.tool}' changed to '{executed.tool}'."
        )
    elif authorized.operation != executed.operation:
        category = "OPERATION_DRIFT"
        evidence.append(
            f"Authorized operation '{authorized.operation}' changed to "
            f"'{executed.operation}'."
        )
    elif authorized.resource != executed.resource:
        category = "RESOURCE_DRIFT"
        evidence.append(
            f"Authorized resource '{authorized.resource}' changed to "
            f"'{executed.resource}'."
        )
    elif authorized.parameters != executed.parameters:
        category = "PARAMETER_DRIFT"
        evidence.append("Execution parameters differ from the authorization.")
    elif authorized.context != executed.context:
        category = "CONTEXT_DRIFT"
        evidence.append("Execution context differs from the authorization.")
    elif authorized.actor != executed.actor:
        category = "ACTOR_DRIFT"
        evidence.append(
            f"Authorized actor '{authorized.actor}' changed to "
            f"'{executed.actor}'."
        )
    else:
        category = "AUTHORIZATION_DRIFT"
        evidence.append(
            f"Verifier returned verdict '{verification.verdict.value}'."
        )

    return InvestigationResult(
        summary=(
            "The executed action was blocked because it does not preserve "
            "the original authorization."
        ),
        category=category,
        evidence=evidence,
        remediation=[
            "Preserve the original authorization across transformations.",
            "Re-validate the action immediately before execution.",
            "Record provenance for each transformation and execution stage.",
        ],
    )
