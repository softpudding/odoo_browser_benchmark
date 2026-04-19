"""Postcondition checks for mail.create_alias_route_to_record."""

import ast


TEAM_NAME = "Bench Alias Team"
TARGET_ALIAS_NAME = "benchalias"
TARGET_MODEL = "crm.lead"
TARGET_ALIAS_CONTACT = "everyone"


def _parse_alias_defaults(raw):
    """alias_defaults is stored as a Text field holding a Python dict
    literal. Empty / falsy values are common for fresh records."""
    if not raw:
        return {}
    if isinstance(raw, dict):
        return raw
    try:
        value = ast.literal_eval(raw)
    except (ValueError, SyntaxError):
        return None
    return value if isinstance(value, dict) else None


def check(env):
    failures = []

    # --- Team still exists and is untouched ---
    team = env["crm.team"].with_context(active_test=False).search([
        ("name", "=", TEAM_NAME),
    ], limit=1)
    if not team:
        return [f"Sales Team '{TEAM_NAME}' is missing — it was renamed, archived, or deleted."]
    if not team.active:
        failures.append(f"Sales Team '{TEAM_NAME}' is archived; it must remain active.")

    # --- Exactly one alias with the target alias_name ---
    aliases = env["mail.alias"].with_context(active_test=False).search([
        ("alias_name", "=", TARGET_ALIAS_NAME),
    ])
    if len(aliases) == 0:
        failures.append(
            f"No mail.alias with alias_name='{TARGET_ALIAS_NAME}' was created."
        )
        return failures
    if len(aliases) > 1:
        failures.append(
            f"Expected exactly 1 mail.alias with alias_name='{TARGET_ALIAS_NAME}', "
            f"found {len(aliases)}."
        )

    alias = aliases[0]

    # --- alias_model_id must be crm.lead ---
    if not alias.alias_model_id:
        failures.append(
            f"Alias '{TARGET_ALIAS_NAME}' has no alias_model_id set; expected "
            f"the model '{TARGET_MODEL}' (Lead/Opportunity)."
        )
    elif alias.alias_model_id.model != TARGET_MODEL:
        failures.append(
            f"Alias '{TARGET_ALIAS_NAME}' alias_model_id is "
            f"'{alias.alias_model_id.model}', expected '{TARGET_MODEL}'."
        )

    # --- alias_contact must be 'everyone' ---
    if alias.alias_contact != TARGET_ALIAS_CONTACT:
        failures.append(
            f"Alias '{TARGET_ALIAS_NAME}' alias_contact is "
            f"'{alias.alias_contact}', expected '{TARGET_ALIAS_CONTACT}'."
        )

    # --- alias_defaults must parse as a dict containing team_id == <team.id> ---
    defaults = _parse_alias_defaults(alias.alias_defaults)
    if defaults is None:
        failures.append(
            f"Alias '{TARGET_ALIAS_NAME}' alias_defaults "
            f"({alias.alias_defaults!r}) is not a valid Python dict literal."
        )
    elif "team_id" not in defaults:
        failures.append(
            f"Alias '{TARGET_ALIAS_NAME}' alias_defaults does not contain a "
            f"'team_id' key; got keys={sorted(defaults.keys())}."
        )
    elif defaults["team_id"] != team.id:
        failures.append(
            f"Alias '{TARGET_ALIAS_NAME}' alias_defaults['team_id'] is "
            f"{defaults['team_id']!r}, expected {team.id} (id of '{TEAM_NAME}')."
        )

    return failures
