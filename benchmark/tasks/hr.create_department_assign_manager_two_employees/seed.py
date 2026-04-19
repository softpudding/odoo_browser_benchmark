"""Seed data for hr.create_department_assign_manager_two_employees.

Category: deep_ui_interaction (MEDIUM).

Two-worker bulk-reassignment task: agent must create one department, set
its manager, then re-open two separate employee records to update their
department field. Hard pattern is the multi-step nav across separate
employee form edits -- agents frequently complete the department but
forget (or mis-apply) one of the worker reassignments.

Distinct from row 321 (three_employees): uses 2 workers with new names
('Bench Dept Manager', 'Bench Dept Worker 1', 'Bench Dept Worker 2')
to avoid collisions with the 3-employee variant.

Starting state:
- No 'Bench Ops' department exists.
- 'Bench Dept Manager' exists with no department (department_id=False).
- 'Bench Dept Worker 1' and 'Bench Dept Worker 2' exist with no
  department (department_id=False).
"""

MANAGER_NAME = "Bench Dept Manager"
WORKER_NAMES = ["Bench Dept Worker 1", "Bench Dept Worker 2"]
NEW_DEPT_NAME = "Bench Ops"


def setup(env):
    Emp = env["hr.employee"].with_context(active_test=False)

    # --- Cleanup prior runs (employees first to release manager_id refs) ---
    Emp.search([("name", "in", [MANAGER_NAME] + WORKER_NAMES)]).unlink()
    env["hr.department"].with_context(active_test=False).search(
        [("name", "=", NEW_DEPT_NAME)]
    ).unlink()

    # --- Create the manager (no department) ---
    env["hr.employee"].create({
        "name": MANAGER_NAME,
        "department_id": False,
        "work_email": "bench.dept.manager@example.com",
        "work_phone": "+1 555 0800",
    })

    # --- Create the two workers (no department) ---
    for idx, name in enumerate(WORKER_NAMES, start=1):
        env["hr.employee"].create({
            "name": name,
            "department_id": False,
            "work_email": f"bench.worker{idx}@example.com",
            "work_phone": f"+1 555 080{idx}",
        })
