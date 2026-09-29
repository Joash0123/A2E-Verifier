from a2e_verifier.scenarios import (
    actor_substitution,
    operation_escalation,
    parameter_escalation,
    resource_substitution,
)


def test_resource_substitution_scenario():
    scenario = resource_substitution()

    assert scenario.expected_allowed is False
    assert scenario.category == "RESOURCE_DRIFT"
    assert scenario.authorized.resource != scenario.executed.resource


def test_operation_escalation_scenario():
    scenario = operation_escalation()

    assert scenario.expected_allowed is False
    assert scenario.category == "OPERATION_DRIFT"
    assert scenario.authorized.operation != scenario.executed.operation


def test_actor_substitution_scenario():
    scenario = actor_substitution()

    assert scenario.expected_allowed is False
    assert scenario.category == "ACTOR_DRIFT"
    assert scenario.authorized.actor != scenario.executed.actor


def test_parameter_escalation_scenario():
    scenario = parameter_escalation()

    assert scenario.expected_allowed is False
    assert scenario.category == "PARAMETER_DRIFT"
    assert scenario.authorized.parameters != scenario.executed.parameters
