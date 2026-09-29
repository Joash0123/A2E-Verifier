from a2e_verifier.action import Action


def normalize_parameters(action: Action) -> Action:
    normalized = dict(action.parameters)

    return Action(
        tool=action.tool,
        operation=action.operation,
        resource=action.resource,
        parameters=normalized,
        context=dict(action.context),
        actor=action.actor,
    )


def canonicalize_resource(action: Action) -> Action:
    resource = action.resource

    if resource is not None:
        resource = resource.strip().lower()

    return Action(
        tool=action.tool,
        operation=action.operation,
        resource=resource,
        parameters=dict(action.parameters),
        context=dict(action.context),
        actor=action.actor,
    )
