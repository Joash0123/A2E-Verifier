from dataclasses import dataclass, field
from typing import Any

from a2e_verifier.action import Action


@dataclass(frozen=True)
class ParameterConstraint:
    key: str
    allowed_values: frozenset[Any] = field(default_factory=frozenset)


@dataclass(frozen=True)
class ParameterPolicyResult:
    allowed: bool
    reason: str


def verify_parameters(
    action: Action,
    constraints: list[ParameterConstraint],
) -> ParameterPolicyResult:
    for constraint in constraints:
        value = action.parameters.get(constraint.key)

        if value not in constraint.allowed_values:
            return ParameterPolicyResult(
                allowed=False,
                reason=f"PARAMETER_NOT_ALLOWED:{constraint.key}",
            )

    return ParameterPolicyResult(
        allowed=True,
        reason="PARAMETERS_ALLOWED",
    )
