from a2e_verifier.action import Action
from a2e_verifier.environment import SimulatedEnvironment
from a2e_verifier.observation import observe_execution


def test_observation_records_actual_execution_effect():
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

    assert observed.executed is True
    assert observed.action == action
    assert observed.effect["result"]["status"] == "closed"
