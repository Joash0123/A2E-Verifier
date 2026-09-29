from dataclasses import dataclass

from a2e_verifier.chain import ActionChain
from a2e_verifier.verifier import VerificationResult, verify


@dataclass(frozen=True)
class ChainVerificationResult:
    result: VerificationResult
    steps_checked: int
    failed_step: int | None = None


def verify_chain(chain: ActionChain) -> ChainVerificationResult:
    if len(chain.steps) < 2:
        raise ValueError("A chain must contain at least two steps")

    for index in range(1, len(chain.steps)):
        previous = chain.steps[index - 1].action
        current = chain.steps[index].action

        result = verify(previous, current)

        if not result.allowed:
            return ChainVerificationResult(
                result=result,
                steps_checked=index + 1,
                failed_step=index,
            )

    result = verify(
        chain.original,
        chain.final,
    )

    return ChainVerificationResult(
        result=result,
        steps_checked=len(chain.steps),
        failed_step=None,
    )
