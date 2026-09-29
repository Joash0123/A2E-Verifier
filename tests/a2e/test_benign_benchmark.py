from a2e_verifier.benign_benchmark import run_benign_scenarios


def test_benign_scenarios_are_accepted():
    results = run_benign_scenarios()

    assert len(results) == 2
    assert all(result.accepted for result in results)
