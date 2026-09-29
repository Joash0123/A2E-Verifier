from a2e_verifier.full_benchmark import run_full_benchmark


def test_full_benchmark():
    result = run_full_benchmark()

    assert result.total == 11
    assert result.detected == 11
    assert result.missed == 0
    assert result.detection_rate == 1.0
    assert len(result.categories) == 7
