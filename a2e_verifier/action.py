from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Action:
    tool: str
    operation: str
    resource: str | None = None
    parameters: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)
    actor: str | None = None

    def canonical(self) -> dict[str, Any]:
        return {
            "tool": self.tool,
            "operation": self.operation,
            "resource": self.resource,
            "parameters": self.parameters,
            "context": self.context,
            "actor": self.actor,
        }
