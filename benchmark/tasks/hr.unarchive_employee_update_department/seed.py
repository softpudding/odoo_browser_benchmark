"""Seed an archived employee for the unarchive-update-department task.

Category 2 (MEDIUM): The agent must reveal archived records via filter,
unarchive the correct employee, then set their department. Capability
tested: archived filter + unarchive action + relational field edit.
"""


def setup(env):
    # --- Ensure department ---
    dept = env["hr.department"].search(
        [("name", "=", "Engineering")], limit=1
    )
    if not dept:
        dept = env["hr.department"].create({"name": "Engineering"})

    Emp = env["hr.employee"].with_context(active_test=False)

    # --- Cleanup prior runs ---
    stale = Emp.search([
        ("name", "in", ["Avery Collins", "Priya Patel"]),
    ])
    stale.unlink()

    # --- Create archived target employee ---
    env["hr.employee"].create({
        "name": "Avery Collins",
        "work_email": "avery.collins@example.com",
        "active": False,
    })

    # --- Distractor: an active, never-archived employee ---
    env["hr.employee"].create({
        "name": "Priya Patel",
        "work_email": "priya.patel@example.com",
        "department_id": dept.id,
        "active": True,
    })
