from dataclasses import dataclass

from a2e_verifier.scenarios import (
    AttackScenario,
    actor_substitution,
    operation_escalation,
    parameter_escalation,
    resource_substitution,
)
from a2e_verifier.verifier import verify


@dataclass(frozen=True)
class ScenarioResult:
    name: str
    category: str
    detected: bool
    verdict: str


def run_scenario(scenario: AttackScenario) -> ScenarioResult:
    result = verify(
        scenario.authorized,
        scenario.executed,
    )

    detected = result.allowed == scenario.expected_allowed

    return ScenarioResult(
        name=scenario.name,
        category=scenario.category,
        detected=detected,
        verdict=result.verdict.value,
    )


def run_all_scenarios() -> list[ScenarioResult]:
    scenarios = [
        resource_substitution(),
        operation_escalation(),
        actor_substitution(),
        parameter_escalation(),
    ]

    return [
        run_scenario(scenario)
        for scenario in scenarios
    ]
