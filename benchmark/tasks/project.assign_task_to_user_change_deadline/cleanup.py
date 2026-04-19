"""Cleanup for project.assign_task_to_user_change_deadline."""


PROJECT_NAME = "Bench Assign Project"
TASK_NAME = "Bench Assign Task"
DEV_LOGIN = "bench_dev"
DEV_NAME = "Bench Dev"


def cleanup(env):
    # Drop the task (by canonical name).
    env["project.task"].with_context(active_test=False).search([
        ("name", "=", TASK_NAME),
    ]).unlink()

    # Drop the project (any residual tasks first).
    project = env["project.project"].with_context(active_test=False).search([
        ("name", "=", PROJECT_NAME),
    ])
    for p in project:
        env["project.task"].with_context(active_test=False).search([
            ("project_id", "=", p.id),
        ]).unlink()
    project.unlink()

    # Drop the benchmark-owned user (and any duplicate quick-created users
    # matching the canonical name).
    dev = env["res.users"].with_context(active_test=False).search([
        ("login", "=", DEV_LOGIN),
    ])
    dupes = env["res.users"].with_context(active_test=False).search([
        ("name", "=", DEV_NAME),
    ])
    all_users = dev | dupes
    if all_users:
        partners = all_users.mapped("partner_id")
        all_users.unlink()
        for partner in partners:
            if partner.name == DEV_NAME:
                try:
                    partner.unlink()
                except Exception:
                    pass
