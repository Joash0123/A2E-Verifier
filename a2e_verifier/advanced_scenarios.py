from dataclasses import dataclass

from a2e_verifier.action import Action


@dataclass(frozen=True)
class AdvancedScenario:
    name: str
    authorized: Action
    executed: Action
    expected_reason: str


def context_privilege_escalation() -> AdvancedScenario:
    authorized = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
        context={"role": "support"},
    )

    executed = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
        context={"role": "administrator"},
    )

    return AdvancedScenario(
        name="context_privilege_escalation",
        authorized=authorized,
        executed=executed,
        expected_reason="CONTEXT_MISMATCH",
    )


def reconstructed_resource_substitution() -> AdvancedScenario:
    authorized = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
        context={"purpose": "support"},
    )

    executed = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:9999",
        actor="agent-1",
        context={"purpose": "support"},
    )

    return AdvancedScenario(
        name="reconstructed_resource_substitution",
        authorized=authorized,
        executed=executed,
        expected_reason="RESOURCE_MISMATCH",
    )


def delegated_actor_escalation() -> AdvancedScenario:
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
        actor="administrator-agent",
    )

    return AdvancedScenario(
        name="delegated_actor_escalation",
        authorized=authorized,
        executed=executed,
        expected_reason="ACTOR_MISMATCH",
    )
