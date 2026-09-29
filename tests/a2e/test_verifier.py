from a2e_verifier.action import Action
from a2e_verifier.verifier import Verdict, verify


def make_action(**overrides):
    values = {
        "tool": "ticket_api",
        "operation": "update",
        "resource": "ticket:1001",
        "parameters": {"status": "closed"},
        "context": {"environment": "staging"},
        "actor": "agent-1",
    }
    values.update(overrides)
    return Action(**values)


def test_identical_actions_match():
    result = verify(make_action(), make_action())

    assert result.verdict == Verdict.MATCH
    assert result.allowed is True


def test_resource_substitution_is_detected():
    result = verify(
        make_action(),
        make_action(resource="ticket:1002"),
    )

    assert result.verdict == Verdict.RESOURCE_MISMATCH
    assert result.allowed is False


def test_parameter_drift_is_detected():
    result = verify(
        make_action(),
        make_action(parameters={"status": "deleted"}),
    )

    assert result.verdict == Verdict.PARAMETER_MISMATCH
    assert result.allowed is False


def test_operation_change_is_detected():
    result = verify(
        make_action(),
        make_action(operation="delete"),
    )

    assert result.verdict == Verdict.OPERATION_MISMATCH
    assert result.allowed is False


def test_context_drift_is_detected():
    result = verify(
        make_action(),
        make_action(context={"environment": "production"}),
    )

    assert result.verdict == Verdict.CONTEXT_MISMATCH
    assert result.allowed is False
