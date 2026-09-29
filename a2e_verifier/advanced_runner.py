from dataclasses import dataclass

from a2e_verifier.advanced_scenarios import (
    AdvancedScenario,
    context_privilege_escalation,
    delegated_actor_escalation,
    reconstructed_resource_substitution,
)
from a2e_verifier.verifier import verify


@dataclass(frozen=True)
class AdvancedScenarioResult:
    name: str
    detected: bool
    verdict: str
    expected_reason: str


def run_advanced_scenario(
    scenario: AdvancedScenario,
) -> AdvancedScenarioResult:
    result = verify(
        scenario.authorized,
        scenario.executed,
    )

    detected = result.verdict.value == scenario.expected_reason

    return AdvancedScenarioResult(
        name=scenario.name,
        detected=detected,
        verdict=result.verdict.value,
        expected_reason=scenario.expected_reason,
    )


def run_advanced_scenarios() -> list[AdvancedScenarioResult]:
    scenarios = [
        context_privilege_escalation(),
        reconstructed_resource_substitution(),
        delegated_actor_escalation(),
    ]

    return [
        run_advanced_scenario(scenario)
        for scenario in scenarios
    ]
