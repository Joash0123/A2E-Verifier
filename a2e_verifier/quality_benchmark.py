from dataclasses import dataclass

from a2e_verifier.benign_benchmark import run_benign_scenarios
from a2e_verifier.full_benchmark import run_full_benchmark


@dataclass(frozen=True)
class QualityBenchmark:
    attack_cases: int
    attacks_detected: int
    benign_cases: int
    benign_accepted: int
    false_positives: int
    detection_rate: float
    false_positive_rate: float


def run_quality_benchmark() -> QualityBenchmark:
    attacks = run_full_benchmark()
    benign = run_benign_scenarios()

    benign_accepted = sum(
        result.accepted
        for result in benign
    )

    false_positives = len(benign) - benign_accepted

    return QualityBenchmark(
        attack_cases=attacks.total,
        attacks_detected=attacks.detected,
        benign_cases=len(benign),
        benign_accepted=benign_accepted,
        false_positives=false_positives,
        detection_rate=attacks.detection_rate,
        false_positive_rate=(
            false_positives / len(benign)
            if benign
            else 0.0
        ),
    )
