from dataclasses import dataclass

from a2e_verifier.action import Action


@dataclass(frozen=True)
class SemanticVerificationResult:
    equivalent: bool
    reason: str


def verify_semantic_equivalence(
    source: Action,
    target: Action,
) -> SemanticVerificationResult:
    if source.tool != target.tool:
        return SemanticVerificationResult(
            equivalent=False,
            reason="TOOL_CHANGED",
        )

    source_resource = (
        source.resource.strip().lower()
        if source.resource is not None
        else None
    )

    target_resource = (
        target.resource.strip().lower()
        if target.resource is not None
        else None
    )

    if source_resource != target_resource:
        return SemanticVerificationResult(
            equivalent=False,
            reason="RESOURCE_CHANGED",
        )

    if source.actor != target.actor:
        return SemanticVerificationResult(
            equivalent=False,
            reason="ACTOR_CHANGED",
        )

    if source.context != target.context:
        return SemanticVerificationResult(
            equivalent=False,
            reason="CONTEXT_CHANGED",
        )

    if source.operation.strip().lower() != target.operation.strip().lower():
        return SemanticVerificationResult(
            equivalent=False,
            reason="OPERATION_CHANGED",
        )

    if source.parameters != target.parameters:
        return SemanticVerificationResult(
            equivalent=False,
            reason="PARAMETERS_CHANGED",
        )

    return SemanticVerificationResult(
        equivalent=True,
        reason="SEMANTICALLY_EQUIVALENT",
    )
