from a2e_verifier.action import Action
from a2e_verifier.benchmark_scenario import BenchmarkScenario


def parameter_reordering_case() -> BenchmarkScenario:
    return BenchmarkScenario(
        name="parameter_reordering",
        category="BENIGN_TRANSFORMATION",
        authorized=Action(
            tool="ticket_api",
            operation="update",
            resource="ticket:1001",
            parameters={
                "status": "closed",
                "priority": "normal",
            },
            actor="agent-1",
        ),
        executed=Action(
            tool="ticket_api",
            operation="update",
            resource="ticket:1001",
            parameters={
                "priority": "normal",
                "status": "closed",
            },
            actor="agent-1",
        ),
        expected_allowed=True,
    )


def operation_normalization_case() -> BenchmarkScenario:
    return BenchmarkScenario(
        name="operation_normalization",
        category="BENIGN_TRANSFORMATION",
        authorized=Action(
            tool="ticket_api",
            operation="READ",
            resource="ticket:1001",
            actor="agent-1",
        ),
        executed=Action(
            tool="ticket_api",
            operation="read",
            resource="ticket:1001",
            actor="agent-1",
        ),
        expected_allowed=True,
    )


def resource_canonicalization_case() -> BenchmarkScenario:
    return BenchmarkScenario(
        name="resource_canonicalization",
        category="BENIGN_TRANSFORMATION",
        authorized=Action(
            tool="ticket_api",
            operation="read",
            resource=" TICKET:1001 ",
            actor="agent-1",
        ),
        executed=Action(
            tool="ticket_api",
            operation="read",
            resource="ticket:1001",
            actor="agent-1",
        ),
        expected_allowed=True,
    )


def benign_benchmark_cases() -> list[BenchmarkScenario]:
    return [
        parameter_reordering_case(),
        operation_normalization_case(),
        resource_canonicalization_case(),
    ]
