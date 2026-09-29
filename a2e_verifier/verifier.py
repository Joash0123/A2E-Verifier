from dataclasses import dataclass
from enum import Enum

from a2e_verifier.action import Action


class Verdict(str, Enum):
    MATCH = "MATCH"
    TOOL_MISMATCH = "TOOL_MISMATCH"
    OPERATION_MISMATCH = "OPERATION_MISMATCH"
    RESOURCE_MISMATCH = "RESOURCE_MISMATCH"
    PARAMETER_MISMATCH = "PARAMETER_MISMATCH"
    CONTEXT_MISMATCH = "CONTEXT_MISMATCH"
    ACTOR_MISMATCH = "ACTOR_MISMATCH"


@dataclass(frozen=True)
class VerificationResult:
    verdict: Verdict
    authorized: Action
    executed: Action

    @property
    def allowed(self) -> bool:
        return self.verdict == Verdict.MATCH


def verify(authorized: Action, executed: Action) -> VerificationResult:
    if authorized.tool != executed.tool:
        verdict = Verdict.TOOL_MISMATCH
    elif authorized.operation != executed.operation:
        verdict = Verdict.OPERATION_MISMATCH
    elif authorized.resource != executed.resource:
        verdict = Verdict.RESOURCE_MISMATCH
    elif authorized.parameters != executed.parameters:
        verdict = Verdict.PARAMETER_MISMATCH
    elif authorized.context != executed.context:
        verdict = Verdict.CONTEXT_MISMATCH
    elif authorized.actor != executed.actor:
        verdict = Verdict.ACTOR_MISMATCH
    else:
        verdict = Verdict.MATCH

    return VerificationResult(
        verdict=verdict,
        authorized=authorized,
        executed=executed,
    )
