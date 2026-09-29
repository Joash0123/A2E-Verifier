from a2e_verifier.benchmark_scenario import evaluate_scenario
from a2e_verifier.security_benchmark_cases import security_benchmark_cases


def test_security_benchmark_cases():
    cases = security_benchmark_cases()

    assert len(cases) == 2

    results = [
        evaluate_scenario(case)
        for case in cases
    ]

    assert all(result.detected for result in results)
    assert all(result.allowed is False for result in results)
