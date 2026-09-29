from a2e_verifier.registry_benchmark import run_registry_benchmark


def test_registry_benchmark():
    result = run_registry_benchmark()

    assert result.total_cases == 15
    assert result.attack_cases == 12
    assert result.benign_cases == 3
    assert result.attacks_detected == 12
    assert result.benign_accepted == 3
    assert result.false_positives == 0
    assert result.detection_rate == 1.0
    assert result.false_positive_rate == 0.0
    assert len(result.categories) >= 6
