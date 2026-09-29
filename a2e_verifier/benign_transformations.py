from a2e_verifier.action import Action


def reorder_parameters(action: Action) -> Action:
    return Action(
        tool=action.tool,
        operation=action.operation,
        resource=action.resource,
        parameters=dict(sorted(action.parameters.items())),
        context=dict(action.context),
        actor=action.actor,
    )


def normalize_operation(action: Action) -> Action:
    return Action(
        tool=action.tool,
        operation=action.operation.strip().lower(),
        resource=action.resource,
        parameters=dict(action.parameters),
        context=dict(action.context),
        actor=action.actor,
    )
