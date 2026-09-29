from a2e_verifier.canonical_benchmark import run_canonical_benchmark


def test_canonical_benchmark():
    result = run_canonical_benchmark()

    assert result.attack_cases == 14
    assert result.attacks_detected == 14
    assert result.benign_cases == 2
    assert result.benign_accepted == 2
    assert result.false_positives == 0
    assert result.detection_rate == 1.0
    assert result.false_positive_rate == 0.0
    assert result.provenance_cases == 2
    assert result.provenance_violations_detected == 1
    assert result.execution_path_cases == 2
    assert result.execution_path_detected == 2
