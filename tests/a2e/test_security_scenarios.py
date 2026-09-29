from a2e_verifier.security_scenarios import run_security_scenarios


def test_security_scenarios_detected():
    results = run_security_scenarios()

    assert len(results) == 4
    assert all(result.detected for result in results)
