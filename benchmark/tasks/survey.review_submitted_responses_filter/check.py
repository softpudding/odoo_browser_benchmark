"""Postcondition checks for survey.review_submitted_responses_filter.

Validates that:
1. The survey "Customer Pulse March" still exists with 4 user_input records.
2. The participation with email reviewer-target@example.com received a
   chatter message that mentions "Reviewed".
3. None of the other three participations received a chatter message.
"""

import re

SURVEY_TITLE = "Customer Pulse March"
TARGET_EMAIL = "reviewer-target@example.com"
EXPECTED_FRAGMENT = "Reviewed"


def _strip_html(html):
    if not html:
        return ""
    plain = re.sub(r"<[^>]+>", " ", html)
    return " ".join(plain.split())


def check(env):
    failures = []

    survey = env["survey.survey"].with_context(active_test=False).search([
        ("title", "=", SURVEY_TITLE),
    ], limit=1)
    if not survey:
        return [f"Survey '{SURVEY_TITLE}' not found"]

    inputs = env["survey.user_input"].with_context(active_test=False).search([
        ("survey_id", "=", survey.id),
    ])
    if len(inputs) != 4:
        failures.append(
            f"Expected 4 participations, found {len(inputs)} (none must be deleted)"
        )

    target = inputs.filtered(lambda u: (u.email or "").lower() == TARGET_EMAIL)
    if len(target) != 1:
        return failures + [
            f"Could not find a unique participation with email {TARGET_EMAIL}"
        ]
    target = target[0]

    note_subtype = env.ref("mail.mt_note", raise_if_not_found=False)
    target_messages = env["mail.message"].search([
        ("model", "=", "survey.user_input"),
        ("res_id", "=", target.id),
        ("message_type", "=", "comment"),
    ])

    found = False
    used_internal_only = bool(target_messages)
    for msg in target_messages:
        plain = _strip_html(msg.body or "")
        if EXPECTED_FRAGMENT not in plain:
            continue
        is_internal = (
            msg.subtype_id == note_subtype if note_subtype else msg.is_internal
        )
        if not is_internal:
            found = True
            used_internal_only = False
            break
        # Internal note that matches the text — record but keep searching for
        # a regular Send message variant.

    if not found:
        if used_internal_only:
            failures.append(
                "The chatter message on the target participation was posted as "
                "an internal Log note. Please use 'Send message' instead."
            )
        else:
            failures.append(
                f"No chatter message containing '{EXPECTED_FRAGMENT}' was posted "
                f"on the participation for {TARGET_EMAIL}."
            )

    # Make sure the agent did not post on the wrong participations.
    other_inputs = inputs - target
    for ui in other_inputs:
        other_msgs = env["mail.message"].search([
            ("model", "=", "survey.user_input"),
            ("res_id", "=", ui.id),
            ("message_type", "=", "comment"),
        ])
        for msg in other_msgs:
            plain = _strip_html(msg.body or "")
            if EXPECTED_FRAGMENT in plain:
                failures.append(
                    f"Distractor participation ({ui.email}) was incorrectly "
                    f"updated with the review message."
                )
                break

    return failures
