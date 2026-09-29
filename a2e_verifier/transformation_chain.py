from dataclasses import dataclass

from a2e_verifier.action import Action
from a2e_verifier.chain import ActionChain
from a2e_verifier.semantic_verifier import verify_semantic_equivalence


@dataclass(frozen=True)
class TransformationAwareResult:
    allowed: bool
    reason: str
    steps_checked: int
    failed_step: int | None = None


def verify_transformation_chain(
    chain: ActionChain,
) -> TransformationAwareResult:
    if len(chain.steps) < 2:
        raise ValueError("A chain must contain at least two steps")

    for index in range(1, len(chain.steps)):
        previous: Action = chain.steps[index - 1].action
        current: Action = chain.steps[index].action

        result = verify_semantic_equivalence(
            previous,
            current,
        )

        if not result.equivalent:
            return TransformationAwareResult(
                allowed=False,
                reason=result.reason,
                steps_checked=index + 1,
                failed_step=index,
            )

    return TransformationAwareResult(
        allowed=True,
        reason="CHAIN_SEMANTICALLY_VALID",
        steps_checked=len(chain.steps),
        failed_step=None,
    )
