from a2e_verifier.action import Action
from a2e_verifier.transformation_verifier import (
    NORMALIZATION_RULE,
    RESOURCE_CANONICALIZATION_RULE,
    verify_transformation,
)
from a2e_verifier.verifier import Verdict


def test_normalization_transformation_can_match():
    source = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        parameters={"status": "open"},
        actor="agent-1",
    )

    target = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        parameters={"status": "open"},
        actor="agent-1",
    )

    result = verify_transformation(
        source,
        target,
        NORMALIZATION_RULE,
    )

    assert result.verdict == Verdict.MATCH
    assert result.allowed is True


def test_resource_canonicalization_can_match():
    source = Action(
        tool="ticket_api",
        operation="read",
        resource=" TICKET:1001 ",
        actor="agent-1",
    )

    target = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1001",
        actor="agent-1",
    )

    result = verify_transformation(
        source,
        target,
        RESOURCE_CANONICALIZATION_RULE,
    )

    assert result.verdict == Verdict.MATCH


def test_resource_canonicalization_rejects_real_substitution():
    source = Action(
        tool="ticket_api",
        operation="read",
        resource=" TICKET:1001 ",
        actor="agent-1",
    )

    target = Action(
        tool="ticket_api",
        operation="read",
        resource="ticket:1002",
        actor="agent-1",
    )

    result = verify_transformation(
        source,
        target,
        RESOURCE_CANONICALIZATION_RULE,
    )

    assert result.verdict == Verdict.RESOURCE_MISMATCH
    assert result.allowed is False
