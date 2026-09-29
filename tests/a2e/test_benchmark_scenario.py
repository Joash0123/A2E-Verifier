from a2e_verifier.action import Action
from a2e_verifier.benchmark_scenario import (
    BenchmarkScenario,
    evaluate_scenario,
)


def test_benchmark_scenario():
    scenario = BenchmarkScenario(
        name="resource_substitution",
        category="RESOURCE_DRIFT",
        authorized=Action(
            tool="ticket_api",
            operation="read",
            resource="ticket:1001",
            actor="agent-1",
        ),
        executed=Action(
            tool="ticket_api",
            operation="read",
            resource="ticket:1002",
            actor="agent-1",
        ),
        expected_allowed=False,
    )

    result = evaluate_scenario(scenario)

    assert result.name == "resource_substitution"
    assert result.category == "RESOURCE_DRIFT"
    assert result.detected is True
    assert result.allowed is False
    assert result.verdict == "RESOURCE_MISMATCH"
