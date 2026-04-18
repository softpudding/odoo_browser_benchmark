"""Seed data for hr.create_department_assign_manager_three_employees.

Category: deep_ui_interaction (MEDIUM).

Bulk-reassignment task: agent must create one department, set its
manager, then re-open three separate employee records to update their
department field. Hard pattern is the multi-record loop -- agents
frequently complete 1 or 2 of the 3 reassignments and forget the rest.

Starting state:
- No 'Bench Engineering' department exists.
- Mike Manager exists in 'Operations' department, no manager.
- Eng One / Eng Two / Eng Three exist in 'Operations' department.
"""

MANAGER_NAME = "Mike Manager"
ENGINEER_NAMES = ["Eng One", "Eng Two", "Eng Three"]
NEW_DEPT_NAME = "Bench Engineering"
SEED_DEPT_NAME = "Operations"


def setup(env):
    Emp = env["hr.employee"].with_context(active_test=False)

    # --- Cleanup prior runs (employees first to release manager_id refs) ---
    Emp.search([("name", "in", [MANAGER_NAME] + ENGINEER_NAMES)]).unlink()
    env["hr.department"].with_context(active_test=False).search(
        [("name", "=", NEW_DEPT_NAME)]
    ).unlink()

    # --- Ensure base department exists ---
    seed_dept = env["hr.department"].search(
        [("name", "=", SEED_DEPT_NAME)], limit=1
    )
    if not seed_dept:
        seed_dept = env["hr.department"].create({"name": SEED_DEPT_NAME})

    # --- Ensure a job for the manager and engineers ---
    eng_job = env["hr.job"].search(
        [("name", "=", "Software Engineer")], limit=1
    )
    if not eng_job:
        eng_job = env["hr.job"].create({
            "name": "Software Engineer",
            "department_id": seed_dept.id,
        })

    mgr_job = env["hr.job"].search(
        [("name", "=", "Engineering Manager")], limit=1
    )
    if not mgr_job:
        mgr_job = env["hr.job"].create({
            "name": "Engineering Manager",
            "department_id": seed_dept.id,
        })

    # --- Create the manager ---
    env["hr.employee"].create({
        "name": MANAGER_NAME,
        "job_id": mgr_job.id,
        "department_id": seed_dept.id,
        "work_email": "mike.manager@example.com",
        "work_phone": "+1 555 0700",
    })

    # --- Create the three engineers ---
    for idx, name in enumerate(ENGINEER_NAMES, start=1):
        env["hr.employee"].create({
            "name": name,
            "job_id": eng_job.id,
            "department_id": seed_dept.id,
            "work_email": f"eng{idx}@example.com",
            "work_phone": f"+1 555 070{idx}",
        })
