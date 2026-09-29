from dataclasses import dataclass
from time import perf_counter

from a2e_verifier.canonical_benchmark import run_canonical_benchmark


@dataclass(frozen=True)
class PerformanceBenchmark:
    total_cases: int
    elapsed_ms: float
    average_case_ms: float


def run_performance_benchmark() -> PerformanceBenchmark:
    benchmark = run_canonical_benchmark()

    total_cases = (
        benchmark.attack_cases
        + benchmark.benign_cases
        + benchmark.provenance_cases
        + benchmark.execution_path_cases
    )

    start = perf_counter()

    run_canonical_benchmark()

    elapsed_ms = (perf_counter() - start) * 1000

    return PerformanceBenchmark(
        total_cases=total_cases,
        elapsed_ms=elapsed_ms,
        average_case_ms=(
            elapsed_ms / total_cases
            if total_cases
            else 0.0
        ),
    )
