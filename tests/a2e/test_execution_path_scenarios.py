from a2e_verifier.execution_path_scenarios import run_execution_path_scenarios
from a2e_verifier.verifier import verify


def test_execution_path_scenarios():
    scenarios = run_execution_path_scenarios()

    assert len(scenarios) == 2

    for scenario in scenarios:
        result = verify(
            scenario.authorized,
            scenario.executed,
        )

        assert result.verdict.value == scenario.expected_reason
