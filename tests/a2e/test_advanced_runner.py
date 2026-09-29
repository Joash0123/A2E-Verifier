from a2e_verifier.advanced_runner import run_advanced_scenarios


def test_advanced_scenarios_are_detected():
    results = run_advanced_scenarios()

    assert len(results) == 3
    assert all(result.detected for result in results)


def test_advanced_scenario_verdicts_are_correct():
    results = run_advanced_scenarios()

    verdicts = {
        result.name: result.verdict
        for result in results
    }

    assert verdicts["context_privilege_escalation"] == "CONTEXT_MISMATCH"
    assert verdicts["reconstructed_resource_substitution"] == "RESOURCE_MISMATCH"
    assert verdicts["delegated_actor_escalation"] == "ACTOR_MISMATCH"
