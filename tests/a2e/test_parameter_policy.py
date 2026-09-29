from a2e_verifier.action import Action
from a2e_verifier.parameter_policy import (
    ParameterConstraint,
    verify_parameters,
)


def test_allowed_parameter_value():
    action = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"priority": "normal"},
        actor="agent-1",
    )

    result = verify_parameters(
        action,
        [
            ParameterConstraint(
                key="priority",
                allowed_values=frozenset({"normal", "low"}),
            )
        ],
    )

    assert result.allowed is True
    assert result.reason == "PARAMETERS_ALLOWED"


def test_disallowed_parameter_value_is_rejected():
    action = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"priority": "critical"},
        actor="agent-1",
    )

    result = verify_parameters(
        action,
        [
            ParameterConstraint(
                key="priority",
                allowed_values=frozenset({"normal", "low"}),
            )
        ],
    )

    assert result.allowed is False
    assert result.reason == "PARAMETER_NOT_ALLOWED:priority"
