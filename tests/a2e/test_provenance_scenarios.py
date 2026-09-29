from a2e_verifier.provenance_scenarios import run_provenance_scenarios


def test_provenance_scenarios():
    results = run_provenance_scenarios()

    assert len(results) == 2
    assert results[0].detected is True
    assert results[1].detected is True
