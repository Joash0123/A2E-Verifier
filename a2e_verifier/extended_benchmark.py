from dataclasses import dataclass

from a2e_verifier.advanced_runner import run_advanced_scenarios
from a2e_verifier.scenario_runner import run_all_scenarios


@dataclass(frozen=True)
class ExtendedBenchmarkResult:
    total: int
    detected: int
    missed: int
    detection_rate: float


def run_extended_benchmark() -> ExtendedBenchmarkResult:
    basic = run_all_scenarios()
    advanced = run_advanced_scenarios()

    detected = sum(result.detected for result in basic)
    detected += sum(result.detected for result in advanced)

    total = len(basic) + len(advanced)
    missed = total - detected

    detection_rate = (
        detected / total
        if total
        else 0.0
    )

    return ExtendedBenchmarkResult(
        total=total,
        detected=detected,
        missed=missed,
        detection_rate=detection_rate,
    )
