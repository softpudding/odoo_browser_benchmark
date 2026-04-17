"""Seed data for hr.assign_manager_set_work_location."""

MANAGER_NAME = "Nadia Reyes"
EMPLOYEE_NAME = "Maya Ortiz"
INITIAL_MANAGER = "Elliot Harper"


def setup(env):
    env["hr.employee"].search([("name", "in", [MANAGER_NAME, INITIAL_MANAGER, EMPLOYEE_NAME])]).unlink()

    dept = env["hr.department"].search([("name", "=", "Operations")], limit=1)
    if not dept:
        dept = env["hr.department"].create({"name": "Operations"})

    manager_job = env["hr.job"].search([("name", "=", "Operations Director")], limit=1)
    if not manager_job:
        manager_job = env["hr.job"].create({
            "name": "Operations Director",
            "department_id": dept.id,
        })

    employee_job = env["hr.job"].search([("name", "=", "Operations Coordinator")], limit=1)
    if not employee_job:
        employee_job = env["hr.job"].create({
            "name": "Operations Coordinator",
            "department_id": dept.id,
        })

    location = env["hr.work.location"].search([("name", "=", "HQ Annex")], limit=1)
    if not location:
        address = env["res.partner"].search([("name", "=", "HQ Annex")], limit=1)
        if not address:
            address = env["res.partner"].create({
                "name": "HQ Annex",
                "is_company": True,
            })
        location = env["hr.work.location"].create({
            "name": "HQ Annex",
            "address_id": address.id,
        })

    manager = env["hr.employee"].create({
        "name": MANAGER_NAME,
        "job_id": manager_job.id,
        "department_id": dept.id,
        "work_phone": "+1 555 0410",
    })

    initial_manager = env["hr.employee"].create({
        "name": INITIAL_MANAGER,
        "job_id": manager_job.id,
        "department_id": dept.id,
        "work_phone": "+1 555 0420",
    })

    env["hr.employee"].create({
        "name": EMPLOYEE_NAME,
        "job_id": employee_job.id,
        "department_id": dept.id,
        "work_phone": "+1 555 0440",
        "parent_id": initial_manager.id,
    })
