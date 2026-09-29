from a2e_verifier.scenario_runner import (
    run_all_scenarios,
    run_scenario,
)
from a2e_verifier.scenarios import resource_substitution


def test_single_scenario_is_detected():
    result = run_scenario(resource_substitution())

    assert result.detected is True
    assert result.category == "RESOURCE_DRIFT"
    assert result.verdict == "RESOURCE_MISMATCH"


def test_all_scenarios_are_detected():
    results = run_all_scenarios()

    assert len(results) == 4
    assert all(result.detected for result in results)
