from a2e_verifier.action import Action
from a2e_verifier.effect_integrity import verify_effect_integrity
from a2e_verifier.environment import SimulatedEnvironment
from a2e_verifier.observation import observe_execution


def test_effect_integrity_accepts_expected_state_change():
    environment = SimulatedEnvironment()

    environment.add_resource(
        "ticket:1001",
        {"status": "open"},
    )

    action = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"status": "closed"},
        actor="agent-1",
    )

    observed = observe_execution(
        action,
        environment,
    )

    expected_effect = {
        "result": {
            "status": "closed",
        }
    }

    result = verify_effect_integrity(
        action,
        expected_effect,
        observed,
    )

    assert result.intact is True
    assert result.reason == "EFFECT_INTEGRITY_VALID"


def test_effect_integrity_detects_state_drift():
    environment = SimulatedEnvironment()

    environment.add_resource(
        "ticket:1001",
        {"status": "open"},
    )

    action = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"status": "closed"},
        actor="agent-1",
    )

    observed = observe_execution(
        action,
        environment,
    )

    expected_effect = {
        "result": {
            "status": "open",
        }
    }

    result = verify_effect_integrity(
        action,
        expected_effect,
        observed,
    )

    assert result.intact is False
    assert result.reason == "STATE_EFFECT_DRIFT"
