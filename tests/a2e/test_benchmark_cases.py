from a2e_verifier.benchmark_cases import basic_benchmark_cases
from a2e_verifier.benchmark_scenario import evaluate_scenario


def test_basic_benchmark_cases():
    cases = basic_benchmark_cases()

    assert len(cases) == 4

    results = [
        evaluate_scenario(case)
        for case in cases
    ]

    assert all(result.detected for result in results)
    assert all(result.allowed is False for result in results)
