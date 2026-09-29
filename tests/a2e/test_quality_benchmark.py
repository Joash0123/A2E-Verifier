from a2e_verifier.quality_benchmark import run_quality_benchmark


def test_quality_benchmark():
    result = run_quality_benchmark()

    assert result.attack_cases == 11
    assert result.attacks_detected == 11
    assert result.benign_cases == 2
    assert result.benign_accepted == 2
    assert result.false_positives == 0
    assert result.detection_rate == 1.0
    assert result.false_positive_rate == 0.0
