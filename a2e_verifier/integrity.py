import hashlib
import json

from a2e_verifier.action import Action


def action_digest(action: Action) -> str:
    payload = json.dumps(
        action.canonical(),
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()
