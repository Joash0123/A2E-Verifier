from a2e_verifier.benchmark_registry import all_benchmark_cases
from a2e_verifier.benchmark_scenario import evaluate_scenario


def test_benchmark_registry():
    cases = all_benchmark_cases()

    assert len(cases) == 15

    results = [
        evaluate_scenario(case)
        for case in cases
    ]

    assert all(result.detected for result in results)
