from dataclasses import dataclass

from a2e_verifier.action import Action


@dataclass(frozen=True)
class ContextVerificationResult:
    allowed: bool
    reason: str


def verify_context(
    authorized: Action,
    executed: Action,
) -> ContextVerificationResult:
    if authorized.context == executed.context:
        return ContextVerificationResult(
            allowed=True,
            reason="CONTEXT_VALID",
        )

    changed = set(authorized.context) | set(executed.context)

    for key in changed:
        if authorized.context.get(key) != executed.context.get(key):
            return ContextVerificationResult(
                allowed=False,
                reason=f"CONTEXT_DRIFT:{key}",
            )

    return ContextVerificationResult(
        allowed=True,
        reason="CONTEXT_VALID",
    )
