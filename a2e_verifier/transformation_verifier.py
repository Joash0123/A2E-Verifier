from dataclasses import dataclass

from a2e_verifier.action import Action
from a2e_verifier.verifier import VerificationResult, Verdict


@dataclass(frozen=True)
class TransformationRule:
    name: str


NORMALIZATION_RULE = TransformationRule("normalization")
RESOURCE_CANONICALIZATION_RULE = TransformationRule("resource_canonicalization")


def verify_transformation(
    source: Action,
    target: Action,
    rule: TransformationRule,
) -> VerificationResult:
    if rule.name == "normalization":
        if (
            source.tool == target.tool
            and source.operation == target.operation
            and source.resource == target.resource
            and source.parameters == target.parameters
            and source.context == target.context
            and source.actor == target.actor
        ):
            verdict = Verdict.MATCH
        else:
            verdict = Verdict.PARAMETER_MISMATCH

    elif rule.name == "resource_canonicalization":
        source_resource = (
            source.resource.strip().lower()
            if source.resource is not None
            else None
        )

        if (
            source.tool == target.tool
            and source.operation == target.operation
            and source_resource == target.resource
            and source.parameters == target.parameters
            and source.context == target.context
            and source.actor == target.actor
        ):
            verdict = Verdict.MATCH
        else:
            verdict = Verdict.RESOURCE_MISMATCH

    else:
        raise ValueError(f"Unknown transformation rule: {rule.name}")

    return VerificationResult(
        verdict=verdict,
        authorized=source,
        executed=target,
    )
