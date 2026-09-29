from dataclasses import dataclass

from a2e_verifier.action import Action


@dataclass(frozen=True)
class ActionStep:
    name: str
    action: Action


@dataclass
class ActionChain:
    steps: list[ActionStep]

    def add(self, name: str, action: Action) -> None:
        self.steps.append(ActionStep(name=name, action=action))

    @property
    def original(self) -> Action:
        return self.steps[0].action

    @property
    def final(self) -> Action:
        return self.steps[-1].action
