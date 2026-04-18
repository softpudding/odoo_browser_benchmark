"""Seed for project_todo.create_three_personal_with_specific_priorities.

Category: deep_ui_interaction (EASY).

The agent must create three brand-new personal to-do notes and only set
the priority star on one of them. The seed only ensures a clean slate —
it does NOT create the three target todos. It also tracks any pre-existing
admin todos so that cleanup / check.py can ignore them.
"""


TARGET_NAMES = ["Plan Sprint", "Write Docs", "Refactor CSS"]


def setup(env):
    # Cleanup any leftover target todos from prior runs.
    env["project.task"].with_context(active_test=False).search([
        ("name", "in", TARGET_NAMES),
    ]).unlink()

    admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    if not admin:
        raise RuntimeError("admin user not found")
