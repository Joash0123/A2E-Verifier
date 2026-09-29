from dataclasses import dataclass

from a2e_verifier.benchmark_registry import all_benchmark_cases
from a2e_verifier.benchmark_scenario import evaluate_scenario


@dataclass(frozen=True)
class RegistryBenchmarkResult:
    total_cases: int
    attack_cases: int
    attacks_detected: int
    benign_cases: int
    benign_accepted: int
    false_positives: int
    detection_rate: float
    false_positive_rate: float
    categories: dict[str, int]


def run_registry_benchmark() -> RegistryBenchmarkResult:
    cases = all_benchmark_cases()

    results = [
        evaluate_scenario(case)
        for case in cases
    ]

    attack_cases = [
        case
        for case in cases
        if case.expected_allowed is False
    ]

    benign_cases = [
        case
        for case in cases
        if case.expected_allowed is True
    ]

    attacks_detected = sum(
        result.detected
        for case, result in zip(cases, results)
        if case.expected_allowed is False
    )

    benign_accepted = sum(
        result.detected
        for case, result in zip(cases, results)
        if case.expected_allowed is True
    )

    false_positives = len(benign_cases) - benign_accepted

    categories: dict[str, int] = {}

    for case in cases:
        categories[case.category] = (
            categories.get(case.category, 0) + 1
        )

    return RegistryBenchmarkResult(
        total_cases=len(cases),
        attack_cases=len(attack_cases),
        attacks_detected=attacks_detected,
        benign_cases=len(benign_cases),
        benign_accepted=benign_accepted,
        false_positives=false_positives,
        detection_rate=(
            attacks_detected / len(attack_cases)
            if attack_cases
            else 0.0
        ),
        false_positive_rate=(
            false_positives / len(benign_cases)
            if benign_cases
            else 0.0
        ),
        categories=categories,
    )
