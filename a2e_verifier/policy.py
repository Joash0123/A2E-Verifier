from dataclasses import dataclass, field

from a2e_verifier.action import Action


@dataclass(frozen=True)
class AuthorizationPolicy:
    allowed_tools: set[str] = field(default_factory=set)
    allowed_operations: set[str] = field(default_factory=set)
    allowed_resources: set[str] = field(default_factory=set)
    allowed_actors: set[str] = field(default_factory=set)

    def allows(self, action: Action) -> bool:
        if self.allowed_tools and action.tool not in self.allowed_tools:
            return False

        if self.allowed_operations and action.operation not in self.allowed_operations:
            return False

        if self.allowed_resources and action.resource not in self.allowed_resources:
            return False

        if self.allowed_actors and action.actor not in self.allowed_actors:
            return False

        return True
