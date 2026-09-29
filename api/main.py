from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from a2e_verifier.action import Action
from a2e_verifier.benchmark_registry import all_benchmark_cases
from a2e_verifier.investigation import investigate
from a2e_verifier.registry_benchmark import run_registry_benchmark
from a2e_verifier.scenarios import (
    actor_substitution,
    operation_escalation,
    parameter_escalation,
    resource_substitution,
)
from a2e_verifier.verifier import verify

BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = BASE_DIR / "web"

app = FastAPI(
    title="A2E Verifier",
    description="Authorization-to-Execution Integrity Verification API",
    version="0.1.0",
)

app.mount(
    "/static",
    StaticFiles(directory=WEB_DIR / "static"),
    name="static",
)


class ActionRequest(BaseModel):
    tool: str
    operation: str
    resource: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)
    context: dict[str, Any] = Field(default_factory=dict)
    actor: str | None = None


class VerificationResponse(BaseModel):
    allowed: bool
    verdict: str
    authorized: dict[str, Any]
    executed: dict[str, Any]
    investigation: dict[str, Any]


@app.get("/")
def index() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/verify", response_model=VerificationResponse)
def verify_action(
    authorized: ActionRequest,
    executed: ActionRequest,
) -> VerificationResponse:
    authorized_action = Action(**authorized.model_dump())
    executed_action = Action(**executed.model_dump())

    result = verify(
        authorized_action,
        executed_action,
    )

    investigation = investigate(
        authorized_action,
        executed_action,
        result,
    )

    return VerificationResponse(
        allowed=result.allowed,
        verdict=result.verdict.value,
        authorized=authorized_action.canonical(),
        executed=executed_action.canonical(),
        investigation={
            "summary": investigation.summary,
            "category": investigation.category,
            "evidence": investigation.evidence,
            "remediation": investigation.remediation,
        },
    )


@app.get("/scenarios")
def scenarios() -> list[dict[str, Any]]:
    scenario_factories = [
        resource_substitution,
        operation_escalation,
        actor_substitution,
        parameter_escalation,
    ]

    return [
        {
            "name": scenario.name,
            "category": scenario.category,
            "expected_allowed": scenario.expected_allowed,
            "authorized": scenario.authorized.canonical(),
            "executed": scenario.executed.canonical(),
        }
        for factory in scenario_factories
        for scenario in [factory()]
    ]


@app.get("/benchmark")
def benchmark() -> dict[str, Any]:
    result = run_registry_benchmark()

    return {
        "total_cases": result.total_cases,
        "attack_cases": result.attack_cases,
        "attacks_detected": result.attacks_detected,
        "benign_cases": result.benign_cases,
        "benign_accepted": result.benign_accepted,
        "false_positives": result.false_positives,
        "detection_rate": result.detection_rate,
        "false_positive_rate": result.false_positive_rate,
        "categories": result.categories,
    }

