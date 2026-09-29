from dataclasses import dataclass

from a2e_verifier.advanced_runner import run_advanced_scenarios
from a2e_verifier.benign_benchmark import run_benign_scenarios
from a2e_verifier.execution_path_scenarios import run_execution_path_scenarios
from a2e_verifier.provenance_scenarios import run_provenance_scenarios
from a2e_verifier.scenario_runner import run_all_scenarios
from a2e_verifier.security_scenarios import run_security_scenarios
from a2e_verifier.verifier import verify


@dataclass(frozen=True)
class CanonicalBenchmark:
    attack_cases: int
    attacks_detected: int
    benign_cases: int
    benign_accepted: int
    false_positives: int
    detection_rate: float
    false_positive_rate: float
    provenance_cases: int
    provenance_violations_detected: int
    execution_path_cases: int
    execution_path_detected: int


def run_canonical_benchmark() -> CanonicalBenchmark:
    basic = run_all_scenarios()
    advanced = run_advanced_scenarios()
    security = run_security_scenarios()
    provenance = run_provenance_scenarios()
    execution_paths = run_execution_path_scenarios()
    benign = run_benign_scenarios()

    attack_results = []

    attack_results.extend(result.detected for result in basic)
    attack_results.extend(result.detected for result in advanced)
    attack_results.extend(result.detected for result in security)

    provenance_attack_results = [
        result.detected
        for result in provenance
        if result.name != "valid_provenance"
    ]

    execution_path_results = []

    for scenario in execution_paths:
        result = verify(
            scenario.authorized,
            scenario.executed,
        )
        execution_path_results.append(
            result.verdict.value == scenario.expected_reason
        )

    attack_results.extend(provenance_attack_results)
    attack_results.extend(execution_path_results)

    benign_accepted = sum(
        result.accepted
        for result in benign
    )

    attack_cases = len(attack_results)
    attacks_detected = sum(attack_results)

    false_positives = len(benign) - benign_accepted

    return CanonicalBenchmark(
        attack_cases=attack_cases,
        attacks_detected=attacks_detected,
        benign_cases=len(benign),
        benign_accepted=benign_accepted,
        false_positives=false_positives,
        detection_rate=(
            attacks_detected / attack_cases
            if attack_cases
            else 0.0
        ),
        false_positive_rate=(
            false_positives / len(benign)
            if benign
            else 0.0
        ),
        provenance_cases=len(provenance),
        provenance_violations_detected=sum(
            provenance_attack_results
        ),
        execution_path_cases=len(execution_paths),
        execution_path_detected=sum(
            execution_path_results
        ),
    )
