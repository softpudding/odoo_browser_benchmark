"""Postconditions for project_sms.send_reminder_sms_to_task_followers.

Validates:
1. Project `Bench SMS Project` still exists with both tasks intact.
2. At least 2 sms.sms records exist whose body contains 'reminder'
   (case-insensitive) AND whose `number` matches one of the seeded
   reviewer phones (+16175551200 / +16175551201).
3. The two matching sms.sms records cover both distinct numbers (i.e. the
   agent did not accidentally send both SMS to the same reviewer).
4. Each matching sms.sms is linked via mail_message_id to a mail.message
   on model=project.task with message_type='sms' (mass mode uses
   message_log, which also sets message_type='sms').
"""

PROJECT_NAME = "Bench SMS Project"
REVIEWER_A_PHONE = "+16175551200"
REVIEWER_B_PHONE = "+16175551201"
TASK_A_NAME = "Urgent Review Request — Reviewer A"
TASK_B_NAME = "Urgent Review Request — Reviewer B"
BODY_FRAGMENT = "reminder"


def check(env):
    failures = []

    project = env["project.project"].search(
        [("name", "=", PROJECT_NAME)], limit=1,
    )
    if not project:
        return [f"Project {PROJECT_NAME!r} not found"]

    task_a = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", TASK_A_NAME),
    ], limit=1)
    task_b = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", TASK_B_NAME),
    ], limit=1)
    if not task_a:
        failures.append(f"Task {TASK_A_NAME!r} not found on project")
    if not task_b:
        failures.append(f"Task {TASK_B_NAME!r} not found on project")

    if "sms.sms" not in env.registry:
        return failures + ["sms.sms model not registered — sms module missing"]

    sms_recs = env["sms.sms"].sudo().search([
        ("number", "in", [REVIEWER_A_PHONE, REVIEWER_B_PHONE]),
    ])
    if not sms_recs:
        return failures + [
            f"No sms.sms record found with number in "
            f"{[REVIEWER_A_PHONE, REVIEWER_B_PHONE]!r} — Send SMS was "
            f"not invoked on the seeded tasks."
        ]

    matching = sms_recs.filtered(
        lambda s: BODY_FRAGMENT in (s.body or "").lower()
    )
    if len(matching) < 2:
        bodies = [f"id={s.id}: number={s.number!r} body={s.body!r}" for s in sms_recs]
        return failures + [
            f"Expected ≥2 sms.sms with body containing {BODY_FRAGMENT!r} "
            f"(case-insensitive) and number in seeded phones; got "
            f"{len(matching)}. Existing matching numbers: " + "; ".join(bodies)
        ]

    covered_numbers = set(matching.mapped("number"))
    missing_numbers = set([REVIEWER_A_PHONE, REVIEWER_B_PHONE]) - covered_numbers
    if missing_numbers:
        failures.append(
            f"No matching sms.sms for number(s): {sorted(missing_numbers)!r} — "
            f"agent may have selected only one task or sent to the same "
            f"recipient twice."
        )

    # Linkage check: each matching sms should link to a mail.message on
    # project.task with message_type='sms'.
    task_ids = {task_a.id, task_b.id}
    if task_a and task_b:
        for sms in matching:
            if not sms.mail_message_id:
                failures.append(
                    f"sms.sms id={sms.id} number={sms.number!r} has no "
                    f"mail_message_id — not posted on any document."
                )
                continue
            msg = sms.mail_message_id
            if msg.model != "project.task":
                failures.append(
                    f"sms.sms id={sms.id} linked to mail.message.model="
                    f"{msg.model!r}, expected 'project.task'"
                )
            elif msg.res_id not in task_ids:
                failures.append(
                    f"sms.sms id={sms.id} linked to mail.message.res_id="
                    f"{msg.res_id}, expected one of {sorted(task_ids)}"
                )
            if msg.message_type != "sms":
                failures.append(
                    f"sms.sms id={sms.id} mail.message.message_type="
                    f"{msg.message_type!r}, expected 'sms'"
                )

    return failures
