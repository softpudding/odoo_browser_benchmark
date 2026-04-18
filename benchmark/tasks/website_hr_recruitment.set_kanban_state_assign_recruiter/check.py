"""Postcondition checks for website_hr_recruitment.set_kanban_state_assign_recruiter.

Validates:
1. Diana Recruit applicant exists and is still active.
2. kanban_state == 'done' (Ready for Next Stage).
3. user_id == Recruiter Bob (login 'recruiter.bob').
4. Stage / job / contact details unchanged (no accidental edit).
5. Exactly one internal log note with body containing 'Phone screen done.'
   posted to the applicant chatter — NOT a public 'Send message' comment.
"""

import re

APPLICANT_NAME = "Diana Recruit"
JOB_NAME = "Senior QA Engineer"
RECRUITER_LOGIN = "recruiter.bob"
EXPECTED_NOTE = "Phone screen done."


def _strip_html(html: str) -> str:
    if not html:
        return ""
    text = re.sub(r"<[^>]+>", "", html)
    return " ".join(text.split())


def check(env):
    failures = []

    # ------------------------------------------------------------------
    # 0. Prerequisites
    # ------------------------------------------------------------------
    bob = env["res.users"].search([("login", "=", RECRUITER_LOGIN)], limit=1)
    if not bob:
        return [f"Seed prerequisite missing: user '{RECRUITER_LOGIN}' not found"]

    # ------------------------------------------------------------------
    # 1. Find the applicant
    # ------------------------------------------------------------------
    apps = env["hr.applicant"].with_context(active_test=False).search([
        ("partner_name", "=", APPLICANT_NAME),
    ])
    if len(apps) == 0:
        return [f"Applicant '{APPLICANT_NAME}' not found"]
    if len(apps) > 1:
        return [
            f"Multiple applicants named '{APPLICANT_NAME}' "
            f"({len(apps)}), expected exactly 1"
        ]
    app = apps

    if not app.active:
        failures.append("Applicant was archived/refused — should still be active")

    # ------------------------------------------------------------------
    # 2. Kanban state
    # ------------------------------------------------------------------
    if app.kanban_state != "done":
        failures.append(
            f"kanban_state is '{app.kanban_state}', expected 'done' "
            "(Ready for Next Stage)"
        )

    # ------------------------------------------------------------------
    # 3. Recruiter user_id
    # ------------------------------------------------------------------
    if app.user_id.id != bob.id:
        failures.append(
            f"Recruiter is '{app.user_id.name or 'not set'}', "
            f"expected 'Recruiter Bob'"
        )

    # ------------------------------------------------------------------
    # 4. Unchanged fields
    # ------------------------------------------------------------------
    if app.email_from != "diana.recruit@example.com":
        failures.append(
            f"Email changed to '{app.email_from}', expected "
            f"'diana.recruit@example.com'"
        )

    if app.partner_phone:
        phone_norm = app.partner_phone.replace(" ", "").replace("-", "")
        if phone_norm != "+15550177":
            failures.append(
                f"Phone changed to '{app.partner_phone}', "
                f"expected '+1 555-0177'"
            )

    if app.job_id.name != JOB_NAME:
        failures.append(
            f"Job changed to '{app.job_id.name}', expected '{JOB_NAME}'"
        )

    # Stage should still be the seeded one ('Initial Qualification')
    if app.stage_id.name != "Initial Qualification":
        failures.append(
            f"Stage is '{app.stage_id.name}', expected 'Initial Qualification' "
            "(the agent should not have changed the stage)"
        )

    # ------------------------------------------------------------------
    # 5. Internal log note in chatter
    # ------------------------------------------------------------------
    note_subtype = env.ref("mail.mt_note", raise_if_not_found=False)
    messages = env["mail.message"].search([
        ("model", "=", "hr.applicant"),
        ("res_id", "=", app.id),
        ("message_type", "=", "comment"),
    ])

    matching_internal = []
    matching_public = []
    for msg in messages:
        plain = _strip_html(msg.body or "")
        if EXPECTED_NOTE.lower() not in plain.lower():
            continue
        is_internal = (
            (note_subtype and msg.subtype_id == note_subtype)
            or msg.is_internal
        )
        if is_internal:
            matching_internal.append(msg)
        else:
            matching_public.append(msg)

    if not matching_internal:
        if matching_public:
            failures.append(
                "Note text was posted as a public 'Send message' comment "
                "instead of an internal 'Log note'"
            )
        else:
            failures.append(
                f"No internal log note found containing '{EXPECTED_NOTE}'"
            )
    elif len(matching_internal) > 1:
        failures.append(
            f"Found {len(matching_internal)} internal log notes containing "
            f"'{EXPECTED_NOTE}', expected exactly 1"
        )

    return failures
