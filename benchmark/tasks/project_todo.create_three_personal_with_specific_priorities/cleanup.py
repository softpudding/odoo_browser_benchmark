"""Cleanup for project_todo.create_three_personal_with_specific_priorities."""


TARGET_NAMES = ["Plan Sprint", "Write Docs", "Refactor CSS"]


def cleanup(env):
    env["project.task"].with_context(active_test=False).search([
        ("name", "in", TARGET_NAMES),
    ]).unlink()
