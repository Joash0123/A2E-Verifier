from dataclasses import dataclass

from a2e_verifier.action import Action
from a2e_verifier.chain import ActionChain


@dataclass(frozen=True)
class Transformation:
    name: str
    source: Action
    target: Action


def transform(chain: ActionChain, name: str, target: Action) -> Transformation:
    source = chain.final
    chain.add(name, target)

    return Transformation(
        name=name,
        source=source,
        target=target,
    )
