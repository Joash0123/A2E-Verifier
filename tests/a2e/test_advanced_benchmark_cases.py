from a2e_verifier.advanced_benchmark_cases import advanced_benchmark_cases
from a2e_verifier.benchmark_scenario import evaluate_scenario


def test_advanced_benchmark_cases():
    cases = advanced_benchmark_cases()

    assert len(cases) == 4

    results = [
        evaluate_scenario(case)
        for case in cases
    ]

    assert all(result.detected for result in results)
    assert all(result.allowed is False for result in results)
