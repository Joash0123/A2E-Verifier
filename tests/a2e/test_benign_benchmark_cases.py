from a2e_verifier.benign_benchmark_cases import benign_benchmark_cases
from a2e_verifier.benchmark_scenario import evaluate_scenario


def test_benign_benchmark_cases():
    cases = benign_benchmark_cases()

    assert len(cases) == 3

    results = [
        evaluate_scenario(case)
        for case in cases
    ]

    assert all(result.detected for result in results)
    assert all(result.allowed is True for result in results)
