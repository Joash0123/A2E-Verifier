from a2e_verifier.advanced_scenarios import (
    context_privilege_escalation,
    delegated_actor_escalation,
    reconstructed_resource_substitution,
)


def test_context_privilege_escalation():
    scenario = context_privilege_escalation()

    assert scenario.expected_reason == "CONTEXT_MISMATCH"
    assert scenario.authorized.context["role"] == "support"
    assert scenario.executed.context["role"] == "administrator"


def test_reconstructed_resource_substitution():
    scenario = reconstructed_resource_substitution()

    assert scenario.expected_reason == "RESOURCE_MISMATCH"
    assert scenario.authorized.resource == "ticket:1001"
    assert scenario.executed.resource == "ticket:9999"


def test_delegated_actor_escalation():
    scenario = delegated_actor_escalation()

    assert scenario.expected_reason == "ACTOR_MISMATCH"
    assert scenario.authorized.actor == "agent-1"
    assert scenario.executed.actor == "administrator-agent"
