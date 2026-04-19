"""Cleanup artifacts from prior runs."""

PROJECT_NAME = "Bench SMS Project"
TASK_A_NAME = "Urgent Review Request — Reviewer A"
TASK_B_NAME = "Urgent Review Request — Reviewer B"
REVIEWER_A_PHONE = "+16175551200"
REVIEWER_B_PHONE = "+16175551201"


def cleanup(env):
    project = env["project.project"].with_context(active_test=False).search(
        [("name", "=", PROJECT_NAME)], limit=1,
    )

    # Delete sms.sms with our phones first (captures orphans too)
    if "sms.sms" in env.registry:
        env["sms.sms"].sudo().search([
            ("number", "in", [REVIEWER_A_PHONE, REVIEWER_B_PHONE]),
        ]).unlink()

    tasks = env["project.task"].with_context(active_test=False).search([
        "|",
        ("name", "in", [TASK_A_NAME, TASK_B_NAME]),
        ("project_id", "=", project.id if project else False),
    ])
    for task in tasks:
        msgs = env["mail.message"].search([
            ("model", "=", "project.task"),
            ("res_id", "=", task.id),
        ])
        if "sms.sms" in env.registry:
            env["sms.sms"].sudo().search([
                ("mail_message_id", "in", msgs.ids),
            ]).unlink()
        msgs.sudo().unlink()
    tasks.unlink()

    if project:
        stages = env["project.task.type"].search([
            ("project_ids", "in", [project.id]),
        ])
        stages.unlink()
        project.unlink()
