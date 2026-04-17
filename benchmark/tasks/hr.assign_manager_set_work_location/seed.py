"""Seed data for hr.assign_manager_set_work_location."""

MANAGER_NAME = "Nadia Reyes"
INITIAL_MANAGER_NAME = "Owen Blake"
EMPLOYEE_NAME = "Maya Ortiz"


def _ensure_location(env, name, location_type, street):
    address = env["res.partner"].search([("name", "=", f"{name} Address")], limit=1)
    if not address:
        address = env["res.partner"].create({
            "name": f"{name} Address",
            "street": street,
            "city": "San Francisco",
            "country_id": env.ref("base.us").id,
        })

    location = env["hr.work.location"].search([("name", "=", name)], limit=1)
    if location:
        location.write({
            "location_type": location_type,
            "address_id": address.id,
        })
        return location

    return env["hr.work.location"].create({
        "name": name,
        "location_type": location_type,
        "address_id": address.id,
    })


def setup(env):
    env["hr.employee"].search([
        ("name", "in", [MANAGER_NAME, INITIAL_MANAGER_NAME, EMPLOYEE_NAME])
    ]).unlink()

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

    _ensure_location(env, "HQ Annex", "office", "220 Howard Street")
    alt_location = _ensure_location(env, "HQ West", "office", "80 Mission Street")

    env["hr.employee"].create({
        "name": MANAGER_NAME,
        "job_id": manager_job.id,
        "department_id": dept.id,
        "work_phone": "+1 555 0410",
    })
    initial_manager = env["hr.employee"].create({
        "name": INITIAL_MANAGER_NAME,
        "job_id": manager_job.id,
        "department_id": dept.id,
        "work_phone": "+1 555 0411",
    })

    env["hr.employee"].create({
        "name": EMPLOYEE_NAME,
        "job_id": employee_job.id,
        "department_id": dept.id,
        "work_phone": "+1 555 0440",
        "parent_id": initial_manager.id,
        "work_location_id": alt_location.id,
    })
