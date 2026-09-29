from a2e_verifier.benchmark import run_benchmark


def test_benchmark_detects_all_current_scenarios():
    result = run_benchmark()

    assert result.total == 4
    assert result.detected == 4
    assert result.missed == 0
    assert result.detection_rate == 1.0
