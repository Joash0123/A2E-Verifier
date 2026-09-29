from dataclasses import dataclass

from a2e_verifier.action import Action
from a2e_verifier.semantic_verifier import verify_semantic_equivalence
from a2e_verifier.verifier import verify


@dataclass(frozen=True)
class BenchmarkScenario:
    name: str
    category: str
    authorized: Action
    executed: Action
    expected_allowed: bool


@dataclass(frozen=True)
class BenchmarkScenarioResult:
    name: str
    category: str
    detected: bool
    allowed: bool
    verdict: str


def evaluate_scenario(
    scenario: BenchmarkScenario,
) -> BenchmarkScenarioResult:
    if scenario.category == "BENIGN_TRANSFORMATION":
        result = verify_semantic_equivalence(
            scenario.authorized,
            scenario.executed,
        )

        allowed = result.equivalent
        verdict = result.reason
    else:
        result = verify(
            scenario.authorized,
            scenario.executed,
        )

        allowed = result.allowed
        verdict = result.verdict.value

    detected = allowed == scenario.expected_allowed

    return BenchmarkScenarioResult(
        name=scenario.name,
        category=scenario.category,
        detected=detected,
        allowed=allowed,
        verdict=verdict,
    )
