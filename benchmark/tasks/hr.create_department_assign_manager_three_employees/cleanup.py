"""Cleanup for hr.create_department_assign_manager_three_employees."""

MANAGER_NAME = "Mike Manager"
ENGINEER_NAMES = ["Eng One", "Eng Two", "Eng Three"]
NEW_DEPT_NAME = "Bench Engineering"


def cleanup(env):
    env["hr.employee"].with_context(active_test=False).search(
        [("name", "in", [MANAGER_NAME] + ENGINEER_NAMES)]
    ).unlink()
    env["hr.department"].with_context(active_test=False).search(
        [("name", "=", NEW_DEPT_NAME)]
    ).unlink()
