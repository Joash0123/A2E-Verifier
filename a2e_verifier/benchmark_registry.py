from a2e_verifier.advanced_benchmark_cases import advanced_benchmark_cases
from a2e_verifier.benign_benchmark_cases import benign_benchmark_cases
from a2e_verifier.benchmark_cases import basic_benchmark_cases
from a2e_verifier.effect_benchmark_cases import effect_benchmark_cases
from a2e_verifier.security_benchmark_cases import security_benchmark_cases
from a2e_verifier.benchmark_scenario import BenchmarkScenario


def all_benchmark_cases() -> list[BenchmarkScenario]:
    return (
        basic_benchmark_cases()
        + advanced_benchmark_cases()
        + security_benchmark_cases()
        + benign_benchmark_cases()
        + effect_benchmark_cases()
    )
