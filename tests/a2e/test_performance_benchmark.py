from a2e_verifier.performance_benchmark import run_performance_benchmark


def test_performance_benchmark():
    result = run_performance_benchmark()

    assert result.total_cases == 20
    assert result.elapsed_ms >= 0
    assert result.average_case_ms >= 0
