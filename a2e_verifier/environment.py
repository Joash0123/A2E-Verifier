from dataclasses import dataclass, field
from typing import Any

from a2e_verifier.action import Action


@dataclass
class SimulatedEnvironment:
    resources: dict[str, dict[str, Any]] = field(default_factory=dict)

    def add_resource(self, resource_id: str, data: dict[str, Any]) -> None:
        self.resources[resource_id] = dict(data)

    def execute(self, action: Action) -> dict[str, Any]:
        if action.resource not in self.resources:
            raise KeyError(f"Unknown resource: {action.resource}")

        resource = self.resources[action.resource]

        if action.operation == "update":
            resource.update(action.parameters)
            return {
                "status": "executed",
                "resource": action.resource,
                "operation": action.operation,
                "result": dict(resource),
            }

        if action.operation == "read":
            return {
                "status": "executed",
                "resource": action.resource,
                "operation": action.operation,
                "result": dict(resource),
            }

        if action.operation == "delete":
            del self.resources[action.resource]
            return {
                "status": "executed",
                "resource": action.resource,
                "operation": action.operation,
            }

        raise ValueError(f"Unsupported operation: {action.operation}")
