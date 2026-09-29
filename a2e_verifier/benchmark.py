from dataclasses import dataclass

from a2e_verifier.scenario_runner import run_all_scenarios


@dataclass(frozen=True)
class BenchmarkResult:
    total: int
    detected: int
    missed: int
    detection_rate: float


def run_benchmark() -> BenchmarkResult:
    results = run_all_scenarios()

    total = len(results)
    detected = sum(result.detected for result in results)
    missed = total - detected

    detection_rate = (
        detected / total
        if total
        else 0.0
    )

    return BenchmarkResult(
        total=total,
        detected=detected,
        missed=missed,
        detection_rate=detection_rate,
    )
