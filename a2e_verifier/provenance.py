from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProvenanceEvent:
    stage: str
    actor: str
    action_id: str
    details: dict[str, str] = field(default_factory=dict)


@dataclass
class ProvenanceTrace:
    events: list[ProvenanceEvent] = field(default_factory=list)

    def record(
        self,
        stage: str,
        actor: str,
        action_id: str,
        details: dict[str, str] | None = None,
    ) -> None:
        self.events.append(
            ProvenanceEvent(
                stage=stage,
                actor=actor,
                action_id=action_id,
                details=details or {},
            )
        )

    @property
    def actors(self) -> list[str]:
        return [event.actor for event in self.events]

    @property
    def stages(self) -> list[str]:
        return [event.stage for event in self.events]
