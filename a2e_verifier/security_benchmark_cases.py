from datetime import datetime, timedelta, timezone

from a2e_verifier.action import Action
from a2e_verifier.benchmark_scenario import BenchmarkScenario
from a2e_verifier.freshness import AuthorizationWindow


def replay_case() -> BenchmarkScenario:
    authorized = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
        context={"action_id": "action-1"},
    )

    executed = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
        context={"action_id": "action-2"},
    )

    return BenchmarkScenario(
        name="authorization_replay",
        category="REPLAY",
        authorized=authorized,
        executed=executed,
        expected_allowed=False,
    )


def stale_authorization_case() -> BenchmarkScenario:
    authorized = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
        context={
            "issued_at": "2026-01-01T00:00:00Z",
            "expires_at": "2026-01-01T00:10:00Z",
        },
    )

    executed = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
        context={
            "issued_at": "2026-01-01T00:00:00Z",
            "expires_at": "2026-01-01T00:10:00Z",
            "authorization_status": "expired",
        },
    )

    return BenchmarkScenario(
        name="stale_authorization",
        category="FRESHNESS",
        authorized=authorized,
        executed=executed,
        expected_allowed=False,
    )


def security_benchmark_cases() -> list[BenchmarkScenario]:
    return [
        replay_case(),
        stale_authorization_case(),
    ]
