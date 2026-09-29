from dataclasses import dataclass

from a2e_verifier.action import Action
from a2e_verifier.benign_transformations import (
    normalize_operation,
    reorder_parameters,
)
from a2e_verifier.semantic_verifier import verify_semantic_equivalence


@dataclass(frozen=True)
class BenignScenarioResult:
    name: str
    accepted: bool
    reason: str


def parameter_reordering() -> BenignScenarioResult:
    action = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={
            "status": "closed",
            "priority": "normal",
        },
        actor="agent-1",
    )

    transformed = reorder_parameters(action)

    result = verify_semantic_equivalence(
        action,
        transformed,
    )

    return BenignScenarioResult(
        name="parameter_reordering",
        accepted=result.equivalent,
        reason=result.reason,
    )


def operation_normalization() -> BenignScenarioResult:
    action = Action(
        tool="ticket_api",
        operation=" READ ",
        resource="ticket:1001",
        actor="agent-1",
    )

    transformed = normalize_operation(action)

    result = verify_semantic_equivalence(
        action,
        transformed,
    )

    return BenignScenarioResult(
        name="operation_normalization",
        accepted=result.equivalent,
        reason=result.reason,
    )


def run_benign_scenarios() -> list[BenignScenarioResult]:
    return [
        parameter_reordering(),
        operation_normalization(),
    ]
