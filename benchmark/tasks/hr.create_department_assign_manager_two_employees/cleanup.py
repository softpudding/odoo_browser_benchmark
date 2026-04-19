"""Cleanup for hr.create_department_assign_manager_two_employees."""

MANAGER_NAME = "Bench Dept Manager"
WORKER_NAMES = ["Bench Dept Worker 1", "Bench Dept Worker 2"]
NEW_DEPT_NAME = "Bench Ops"


def cleanup(env):
    env["hr.employee"].with_context(active_test=False).search(
        [("name", "in", [MANAGER_NAME] + WORKER_NAMES)]
    ).unlink()
    env["hr.department"].with_context(active_test=False).search(
        [("name", "=", NEW_DEPT_NAME)]
    ).unlink()
