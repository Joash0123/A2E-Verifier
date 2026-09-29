from dataclasses import dataclass

from a2e_verifier.action import Action


@dataclass(frozen=True)
class ExecutionPathScenario:
    name: str
    authorized: Action
    executed: Action
    expected_reason: str


def tool_path_substitution() -> ExecutionPathScenario:
    authorized = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
        context={"path": "approved"},
    )

    executed = Action(
        tool="admin_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
        context={"path": "alternate"},
    )

    return ExecutionPathScenario(
        name="tool_path_substitution",
        authorized=authorized,
        executed=executed,
        expected_reason="TOOL_MISMATCH",
    )


def execution_context_substitution() -> ExecutionPathScenario:
    authorized = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"status": "closed"},
        actor="agent-1",
        context={"execution_path": "ticket-service"},
    )

    executed = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={"status": "closed"},
        actor="agent-1",
        context={"execution_path": "admin-service"},
    )

    return ExecutionPathScenario(
        name="execution_context_substitution",
        authorized=authorized,
        executed=executed,
        expected_reason="CONTEXT_MISMATCH",
    )


def run_execution_path_scenarios() -> list[ExecutionPathScenario]:
    return [
        tool_path_substitution(),
        execution_context_substitution(),
    ]
