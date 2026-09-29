from a2e_verifier.canonical_benchmark import run_canonical_benchmark
from a2e_verifier.performance_benchmark import run_performance_benchmark


def main() -> None:
    result = run_canonical_benchmark()
    performance = run_performance_benchmark()

    print("A2E Verifier Security Benchmark")
    print("=" * 36)
    print(f"Attack cases:             {result.attack_cases}")
    print(f"Attacks detected:         {result.attacks_detected}")
    print(f"Detection rate:           {result.detection_rate:.0%}")
    print()
    print(f"Benign cases:             {result.benign_cases}")
    print(f"Benign accepted:          {result.benign_accepted}")
    print(f"False positives:          {result.false_positives}")
    print(f"False-positive rate:      {result.false_positive_rate:.0%}")
    print()
    print(f"Provenance cases:         {result.provenance_cases}")
    print(f"Provenance violations:   {result.provenance_violations_detected}")
    print()
    print(f"Execution-path cases:     {result.execution_path_cases}")
    print(f"Execution-path detected:  {result.execution_path_detected}")
    print()
    print(f"Total benchmark cases:    {performance.total_cases}")
    print(f"Benchmark latency:        {performance.elapsed_ms:.3f} ms")
    print(f"Average per case:         {performance.average_case_ms:.3f} ms")


if __name__ == "__main__":
    main()
