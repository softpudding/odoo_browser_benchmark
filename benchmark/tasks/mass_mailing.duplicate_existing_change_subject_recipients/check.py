"""Postcondition checks for mass_mailing.duplicate_existing_change_subject_recipients.

Validates:
1. Original mailing 'Q1 Bulletin Template' still exists, untouched
   (mailing_model_name = 'mailing.list', state = 'draft', no sent_date).
2. A new mailing 'Q2 Bulletin Update' exists with mailing_model_name =
   'res.partner', state = 'draft', and a domain referencing Country = Germany.
3. Exactly two mailings exist across the {source, dup} subject set.
"""

from ast import literal_eval


SOURCE_SUBJECT = "Q1 Bulletin Template"
DUP_SUBJECT = "Q2 Bulletin Update"


def _domain_targets_germany(domain_str, env):
    """Return True if the domain references country in any common way that
    resolves to Germany."""
    if not domain_str:
        return False
    lowered = domain_str.lower()
    if "country" not in lowered:
        return False

    # Try to evaluate and resolve any country id/name to Germany.
    try:
        domain = literal_eval(domain_str)
    except Exception:
        # Fallback: textual heuristic.
        return "germany" in lowered or "'de'" in lowered or '"de"' in lowered

    germany = env["res.country"].search([("code", "=", "DE")], limit=1)
    germany_id = germany.id if germany else None
    germany_name = germany.name if germany else "Germany"

    def _leaf_matches(leaf):
        if not isinstance(leaf, (list, tuple)) or len(leaf) != 3:
            return False
        field, op, value = leaf
        if not isinstance(field, str) or "country" not in field.lower():
            return False
        # Accept '=', 'in', 'ilike', '=like', '=ilike'
        if isinstance(value, (list, tuple)):
            values = list(value)
        else:
            values = [value]
        for v in values:
            if isinstance(v, int) and germany_id is not None and v == germany_id:
                return True
            if isinstance(v, str) and (
                v.lower() == germany_name.lower()
                or v.lower() == "germany"
                or v.lower() == "de"
            ):
                return True
        return False

    for leaf in domain:
        if _leaf_matches(leaf):
            return True
    return False


def check(env):
    failures = []

    # --- Original must still exist and be untouched ---
    original = env["mailing.mailing"].search(
        [("subject", "=", SOURCE_SUBJECT)], limit=1
    )
    if not original:
        failures.append(f"Original mailing {SOURCE_SUBJECT!r} is missing")
    else:
        if original.state != "draft":
            failures.append(
                f"Original state is {original.state!r}, expected 'draft'"
            )
        if original.mailing_model_name != "mailing.list":
            failures.append(
                "Original mailing_model_name is "
                f"{original.mailing_model_name!r}, expected 'mailing.list' "
                "(original must remain unchanged)"
            )
        if original.sent_date:
            failures.append(
                f"Original mailing was sent at {original.sent_date}"
            )

    # --- Duplicate must exist ---
    dup = env["mailing.mailing"].search(
        [("subject", "=", DUP_SUBJECT)], limit=1
    )
    if not dup:
        return failures + [
            f"Duplicate mailing with subject {DUP_SUBJECT!r} not found"
        ]

    if dup.state != "draft":
        failures.append(
            f"Duplicate state is {dup.state!r}, expected 'draft'"
        )
    if dup.mailing_model_name != "res.partner":
        failures.append(
            "Duplicate mailing_model_name is "
            f"{dup.mailing_model_name!r}, expected 'res.partner' (Contact)"
        )
    if dup.sent_date:
        failures.append(
            f"Duplicate mailing was sent at {dup.sent_date}"
        )

    # --- Country=Germany domain on the duplicate ---
    if not _domain_targets_germany(dup.mailing_domain or "", env):
        failures.append(
            "Duplicate mailing_domain "
            f"{(dup.mailing_domain or '')!r} does not target Country = Germany"
        )

    # --- No extra mailings using either subject ---
    extras = env["mailing.mailing"].search([
        ("subject", "in", [SOURCE_SUBJECT, DUP_SUBJECT]),
    ])
    if len(extras) != 2:
        failures.append(
            "Expected exactly 2 mailings across "
            f"{{{SOURCE_SUBJECT!r}, {DUP_SUBJECT!r}}}, found {len(extras)}"
        )

    return failures
