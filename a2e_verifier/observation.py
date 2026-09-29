from dataclasses import dataclass
from typing import Any

from a2e_verifier.action import Action
from a2e_verifier.environment import SimulatedEnvironment


@dataclass(frozen=True)
class ObservedExecution:
    action: Action
    effect: dict[str, Any]
    executed: bool


def observe_execution(
    action: Action,
    environment: SimulatedEnvironment,
) -> ObservedExecution:
    effect = environment.execute(action)

    return ObservedExecution(
        action=action,
        effect=effect,
        executed=True,
    )
