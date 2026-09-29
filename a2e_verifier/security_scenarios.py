from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from a2e_verifier.action import Action
from a2e_verifier.freshness import AuthorizationWindow
from a2e_verifier.freshness_verifier import verify_authorization_freshness
from a2e_verifier.parameter_policy import ParameterConstraint, verify_parameters
from a2e_verifier.verifier import verify


@dataclass(frozen=True)
class SecurityScenarioResult:
    name: str
    detected: bool
    reason: str


def replay_attack() -> SecurityScenarioResult:
    issued = datetime(2026, 1, 1, tzinfo=timezone.utc)

    window = AuthorizationWindow(
        issued_at=issued,
        expires_at=issued + timedelta(minutes=10),
        action_id="action-1",
    )

    result = verify_authorization_freshness(
        window,
        "action-2",
        issued + timedelta(minutes=5),
    )

    return SecurityScenarioResult(
        name="authorization_replay",
        detected=not result.allowed,
        reason=result.reason,
    )


def stale_authorization() -> SecurityScenarioResult:
    issued = datetime(2026, 1, 1, tzinfo=timezone.utc)

    window = AuthorizationWindow(
        issued_at=issued,
        expires_at=issued + timedelta(minutes=10),
        action_id="action-1",
    )

    result = verify_authorization_freshness(
        window,
        "action-1",
        issued + timedelta(minutes=20),
    )

    return SecurityScenarioResult(
        name="stale_authorization",
        detected=not result.allowed,
        reason=result.reason,
    )


def context_drift() -> SecurityScenarioResult:
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
        resource="ticket:1001",
        actor="agent-1",
        context={"purpose": "billing"},
    )

    result = verify(authorized, executed)

    return SecurityScenarioResult(
        name="context_drift",
        detected=not result.allowed,
        reason=result.verdict.value,
    )


def parameter_escalation() -> SecurityScenarioResult:
    action = Action(
        tool="ticket_api",
        operation="update",
        resource="ticket:1001",
        parameters={
            "status": "closed",
            "priority": "critical",
        },
        actor="agent-1",
    )

    constraints = [
        ParameterConstraint(
            key="status",
            allowed_values=frozenset({"open", "closed"}),
        ),
        ParameterConstraint(
            key="priority",
            allowed_values=frozenset({"low", "normal"}),
        ),
    ]

    result = verify_parameters(
        action,
        constraints,
    )

    return SecurityScenarioResult(
        name="parameter_escalation",
        detected=not result.allowed,
        reason=result.reason,
    )


def run_security_scenarios() -> list[SecurityScenarioResult]:
    return [
        replay_attack(),
        stale_authorization(),
        context_drift(),
        parameter_escalation(),
    ]
