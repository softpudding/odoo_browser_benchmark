"""Cleanup for project.create_task_with_deadline_tags_assignees."""


PROJECT_NAME = "Bench Tag Proj"
TAG_NAMES = ["urgent", "backend"]
DEV2_LOGIN = "bench_dev_2"
DEV2_NAME = "Bench Dev 2"
NEW_TASK_NAME = "Fix login bug"


def cleanup(env):
    # Drop the created task.
    env["project.task"].with_context(active_test=False).search([
        ("name", "=", NEW_TASK_NAME),
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

    # Drop the benchmark-owned tags.
    env["project.tags"].with_context(active_test=False).search([
        ("name", "in", TAG_NAMES),
    ]).unlink()

    # Drop the dev user.
    dev = env["res.users"].with_context(active_test=False).search([
        ("login", "=", DEV2_LOGIN),
    ])
    if dev:
        partners = dev.mapped("partner_id")
        dev.unlink()
        for partner in partners:
            if partner.name == DEV2_NAME:
                try:
                    partner.unlink()
                except Exception:
                    pass
