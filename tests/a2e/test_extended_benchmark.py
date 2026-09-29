from a2e_verifier.extended_benchmark import run_extended_benchmark


def test_extended_benchmark_detects_all_current_scenarios():
    result = run_extended_benchmark()

    assert result.total == 7
    assert result.detected == 7
    assert result.missed == 0
    assert result.detection_rate == 1.0
