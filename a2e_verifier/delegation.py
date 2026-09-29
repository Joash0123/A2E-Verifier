from dataclasses import dataclass

from a2e_verifier.action import Action


@dataclass(frozen=True)
class Delegation:
    delegator: str
    delegate: str
    resources: frozenset[str]
    operations: frozenset[str]

    def allows(self, action: Action) -> bool:
        if action.actor != self.delegate:
            return False

        if action.resource not in self.resources:
            return False

        if action.operation not in self.operations:
            return False

        return True


def apply_delegation(action: Action, delegation: Delegation) -> Action:
    return Action(
        tool=action.tool,
        operation=action.operation,
        resource=action.resource,
        parameters=dict(action.parameters),
        context={
            **action.context,
            "delegated_by": delegation.delegator,
        },
        actor=delegation.delegate,
    )
