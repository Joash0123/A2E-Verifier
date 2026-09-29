from dataclasses import dataclass

from a2e_verifier.action import Action


@dataclass(frozen=True)
class AttackScenario:
    name: str
    authorized: Action
    executed: Action
    expected_allowed: bool
    category: str


def resource_substitution() -> AttackScenario:
    authorized = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
    )

    executed = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1002",
        actor="agent-1",
    )

    return AttackScenario(
        name="resource_substitution",
        authorized=authorized,
        executed=executed,
        expected_allowed=False,
        category="RESOURCE_DRIFT",
    )


def operation_escalation() -> AttackScenario:
    authorized = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
    )

    executed = Action(
        tool="ticket_api",
        operation="delete",
        resource="ticket:1001",
        actor="agent-1",
    )

    return AttackScenario(
        name="operation_escalation",
        authorized=authorized,
        executed=executed,
        expected_allowed=False,
        category="OPERATION_DRIFT",
    )


def actor_substitution() -> AttackScenario:
    authorized = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
    )

    executed = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-2",
    )

    return AttackScenario(
        name="actor_substitution",
        authorized=authorized,
        executed=executed,
        expected_allowed=False,
        category="ACTOR_DRIFT",
    )


def parameter_escalation() -> AttackScenario:
    authorized = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"priority": "normal"},
        actor="agent-1",
    )

    executed = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"priority": "critical", "admin": True},
        actor="agent-1",
    )

    return AttackScenario(
        name="parameter_escalation",
        authorized=authorized,
        executed=executed,
        expected_allowed=False,
        category="PARAMETER_DRIFT",
    )
