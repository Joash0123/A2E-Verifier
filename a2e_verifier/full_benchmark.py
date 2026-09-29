from dataclasses import dataclass

from a2e_verifier.advanced_runner import run_advanced_scenarios
from a2e_verifier.scenario_runner import run_all_scenarios
from a2e_verifier.security_scenarios import run_security_scenarios


@dataclass(frozen=True)
class BenchmarkSummary:
    total: int
    detected: int
    missed: int
    detection_rate: float
    categories: dict[str, int]


def _category(name: str) -> str:
    mapping = {
        "context_privilege_escalation": "CONTEXT_DRIFT",
        "reconstructed_resource_substitution": "RESOURCE_DRIFT",
        "delegated_actor_escalation": "ACTOR_DRIFT",
        "authorization_replay": "REPLAY",
        "stale_authorization": "FRESHNESS",
        "context_drift": "CONTEXT_DRIFT",
        "parameter_escalation": "PARAMETER_DRIFT",
    }

    return mapping.get(name, name)


def run_full_benchmark() -> BenchmarkSummary:
    basic = run_all_scenarios()
    advanced = run_advanced_scenarios()
    security = run_security_scenarios()

    detected = sum(result.detected for result in basic)
    detected += sum(result.detected for result in advanced)
    detected += sum(result.detected for result in security)

    total = len(basic) + len(advanced) + len(security)
    missed = total - detected

    categories: dict[str, int] = {}

    for result in basic:
        category = result.category
        categories[category] = categories.get(category, 0) + 1

    for result in advanced:
        category = _category(result.name)
        categories[category] = categories.get(category, 0) + 1

    for result in security:
        category = _category(result.name)
        categories[category] = categories.get(category, 0) + 1

    return BenchmarkSummary(
        total=total,
        detected=detected,
        missed=missed,
        detection_rate=detected / total if total else 0.0,
        categories=categories,
    )
